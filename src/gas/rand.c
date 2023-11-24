//
// Created by root on 2020/11/17.
//

# include "rand.h"
# include <stdlib.h>
# include "subsegs.h"

bfd_boolean strict_listing = FALSE;

const char* object_file_name = NULL;

ShuffleInfo__Metadata metadata;
ShuffleInfo__Metadata__FixupInfo** global_fixups = NULL;
ShuffleInfo__Metadata__FunInfo** global_funs = NULL;
uint64_t c_funs = 0;

/// 使用add_fixup函数加入fixup链表.
/// 注意第二类fixup在收集时即加入了,而第一类Fixup在fixup_collect_after函数才通过遍历fixup加入
fixup_node* fixups_head = NULL;
fixup_node* fixups_tail = NULL;
uint64_t global_fixup_count = 0;

/// 收集第二类fixup到该链表. 在确定符号表后会遍历并更新其中的bbl_sym值
fixup_node* jmp_fixup_head;
fixup_node* jmp_fixup_tail;

htab_t sec2label_map;
htab_t sec2inst_map;
label_list* now_labelList = NULL;
inst_list* now_instList = NULL;
uint64_t global_label_count;
uint64_t global_label_index;


unsigned metadata_buf_len = 0;
char* metadata_buf = NULL;

const pseudo_typeS bbInfo_pseudo_table[] = {
        {"bbinfo_funb",    funcb_bbInfo_handler,    0},
        {"bbinfo_fune",    funce_bbInfo_handler,    0},
        {"bbinfo_bb",      bb_bbInfo_handler,       0},
        {"bbinfo_be",      be_bbInfo_handler,       0},
        {"bbinfo_inlineb", inlineb_bbInfo_handler,  0},
        {"bbinfo_inlinee", inlinee_bbInfo_handler,  0},
        {"bbinfo_jmptbl",  bbinfo_jmptbl_handler,  0},
        {NULL, NULL,                   0}
};


void shuffleInfo_init(void){
    /// 普通变量： 使用SHUFFLE_INFO__METADATA__INIT来初始化
    /// 数组变量： 自己malloc出来一个二维的指针数组

    metadata = (ShuffleInfo__Metadata)SHUFFLE_INFO__METADATA__INIT;
    shuffle_info__metadata__init(&metadata);

    /// layout和fixup都是数组，现在应该还无法确定长度。因此我们只需要初始化sec2layout_map
    sec2label_map = str_htab_create();
    sec2inst_map = str_htab_create();
}


void handle_jmp_fixup_list(void){

    ShuffleInfo__Metadata__FixupInfo* fixupTuple;
    symbolS* target_sym;
    enum target_type targetType;

    fixup_node* p = jmp_fixup_head;
    while(p != NULL){
        fixupTuple = p->fixupTuple;
        /// 记录第二类fixup的section属性
        fixupTuple->section = elf_section_data (p->sec)->this_idx;

        /// 记录第二类fixup的target相关属性————value时的节下标，或是index的符号表下标
        target_sym = (symbolS*)fixupTuple->target_bbl_sym;
	    if (target_sym->bsym->udata.i != 0) { /// 有的话就存下标
		    targetType = INDEX_TARGET;
		    fixupTuple->target_bbl_sym = target_sym->bsym->udata.i;
	    } else{  /// 没有的话要记录value
		    targetType = VALUE_TARGET;
		    fixupTuple->target_bbl_sym = S_GET_VALUE(target_sym);
		    fixupTuple->target_section = elf_section_data (S_GET_SEGMENT(target_sym))->this_idx;
	    }

        /// 记录第二类fixup的base相关属性————value时的节下标，或是index的符号表下标
        if(targetType == VALUE_TARGET) {
            fixupTuple->type &= 0xFFFFFFF3;
            fixupTuple->type |= 0x8;
        } else if (targetType == INDEX_TARGET) {
            fixupTuple->type &= 0xFFFFFFF3;
            fixupTuple->type |= 0xc;
        }

        p = p->next;
    }
}



void update_fixup(void){
    /// 现在确定数量了，可以初始化FixupInfo指针数组了
    uint64_t all_fixup_num = global_fixup_count;
    global_fixups = malloc(sizeof(ShuffleInfo__Metadata__FixupInfo*) * all_fixup_num);
    metadata.fixups = global_fixups;
    metadata.n_fixups = all_fixup_num;

    fixup_node* fixup = fixups_head;
    uint64_t i = 0;
    while(fixup!= NULL){
        global_fixups[i] = fixup->fixupTuple;

        i++;
        fixup = fixup->next;
    }
}

bfd_boolean is_prefix_of(const char* prefix, const char* str){
    return strncmp(prefix, str, strlen(prefix)) == 0;
}

bfd_boolean is_special_section_for_fixup(const char* secname){
    static const char* const special_text_section[] =
    {
            ".debug",
            ".eh_frame",
            ".gcc_except_table",
            ".note.gnu.property"
    };

    for (size_t i = 0; i < sizeof(special_text_section) / sizeof(special_text_section[0]); i++)
        if (is_prefix_of(special_text_section[i], secname))
            return TRUE;
    return FALSE;
}

void add_fixup(const char* secName, ShuffleInfo__Metadata__FixupInfo* fixupTuple){

    if (is_special_section_for_fixup(secName))
        return;

    fixup_node* fixupNode = malloc(sizeof(fixup_node));
    fixupNode->fixupTuple = fixupTuple;
    fixupNode->next = NULL;
    if (global_fixup_count == 0){
        fixups_head = fixupNode;
        fixups_tail = fixupNode;
    }else{
        fixups_tail->next = fixupNode;
        fixups_tail = fixupNode;
    }
    global_fixup_count++;
}

void add_jmp_fixup(const char* secName, ShuffleInfo__Metadata__FixupInfo* fixupTuple, asection* sec){

    if (is_special_section_for_fixup(secName))
        return;

    fixup_node* fixupNode = malloc(sizeof(fixup_node));

    fixupNode->fixupTuple = fixupTuple;
    fixupNode->sec = sec;
    fixupNode->next = NULL;

    if (jmp_fixup_head == NULL){
        jmp_fixup_head = fixupNode;
        jmp_fixup_tail = fixupNode;
    }else{
        jmp_fixup_tail->next = fixupNode;
        jmp_fixup_tail = fixupNode;
    }
}



/* 可以看到，gcc通过检测指令来判断基本块的开头，并不一定是准确的。
 * 第二个bbInfo_BB应该是在movl指令位置，但它实际上把上一个基本块的两个align也包括了
 * 因此gas中，记录基本块的开始，应该是从实际的指令开始，因为这个是一定不会错的。
 *
 * 但同时要考虑到，有可能基本块内没有实际的指令，导致该基本块的开头为空。
 * 应对方案是：下一个基本块检测到上一个基本块存在这种情况，应该删除该basicblock,相当于把这块align附加到上一个基本块上
 *
 *.bbInfo_BB
	xorl	%eax, %eax
  .bbInfo_BE 1
  .bbInfo_BB
	.p2align 4,,10
	.p2align 3
	movl	$.LC2, %edi
  .bbInfo_BE 1
 *
 * */

void label_handler(elf_symbol_type* elfsym) {

    if (now_labelList == NULL){
        printf("该label(%s)没有对应的now_labelList，请排查subsegs.c中的环境切换函数subseg_set_rest\n", elfsym->symbol.name);
        exit(0x233);
    }

    /// 初始化一个label_node
    label_node* label = malloc(sizeof(label_node));
    memset(label, 0, sizeof(label_node));

    /// 为该label设定一些属性
    label->sec = now_seg;
    label->name = elfsym->symbol.name;
    label->sym = elfsym;
    label->frag = frag_now;
    label->frag_offset = (frchain_now->frch_obstack.next_free) - &(frag_now->fr_literal[0]);

    /// 加入当前sec的label列表中
    now_labelList->label_count++;
    if(now_labelList->label_list_head == NULL){
        now_labelList->label_list_tail = label;
        now_labelList->label_list_head = label;
    }else{
        now_labelList->label_list_tail->next = label;
        label->pre = now_labelList->label_list_tail;
        now_labelList->label_list_tail = label;
    }
}

void inst_handler(list_info_type* new_list_info, const char* line){

    if (new_list_info == NULL){
        printf("该指令(%s)没有生成对应的list_info_type，请排查该问题\n", line);
        exit(0x233);
    }
    if (now_instList == NULL){
        printf("该指令(%s)没有对应的now_instList，请排查subsegs.c中的环境切换函数subseg_set_rest\n", line);
        exit(0x233);
    }

    /// 创建一个新的inst_node
    inst_node* inst = malloc(sizeof(inst_node));
    memset(inst, 0, sizeof(inst_node));

    /// 为该inst设定一些属性
    inst->inst_list_info = new_list_info;

    /// 加入当前sec的指令列表中
    now_instList->inst_count++;
    if(now_instList->inst_list_tail == NULL){
        now_instList->inst_list_head = inst;
        now_instList->inst_list_tail = inst;
    }else{
        now_instList->inst_list_tail->next = inst;
        now_instList->inst_list_tail = inst;
    }
}

char *int2str(unsigned int value) {
    assert(value>0);
    unsigned int temp = value;
    unsigned int length = 0;

    while(temp){
        temp /= 10;
        length++;
    }

    char *cint = malloc(length+1);
    memset(cint, 0, length+1);

    temp = value;
    length--;
    while(temp){
        cint[length] = 0x30 + (temp % 10);
        temp /= 10;
        length--;
    }
    return cint;
}


char * baseType2Char(enum base_type baseType){
    switch(baseType)
    {
        case NONE_BASE : return "NONE_BASE";
        case VALUE_BASE : return "VALUE_BASE";
        case INDEX_BASE  : return "INDEX_BASE";
        default    : printf("Illegal direction value!\n");
    }
}

char * targetType2Char(enum target_type targetType){
    switch(targetType)
    {
        case NONE_TARGET : return "NONE_TARGET";
        case VALUE_TARGET  : return "VALUE_TARGET";
        case INDEX_TARGET  : return "INDEX_TARGET";
        default    : printf("Illegal direction value!\n");
    }
}

char * bblType2Char(enum bbl_type bblType){
    switch(bblType)
    {
        case BBL : return "BBL";
        case FUN  : return "FUN";
        case OBJ : return "OBJ";
        case INLINE_ASSEMBLY  : return "INLINE_ASSEMBLY";
        default    : printf("Illegal direction value!\n");
    }
}

void funcb_bbInfo_handler(int ignored ATTRIBUTE_UNUSED) {
    c_funs += 1;
};
void funce_bbInfo_handler(int ignored ATTRIBUTE_UNUSED) {};
void bb_bbInfo_handler(int ignored ATTRIBUTE_UNUSED) {
    offsetT is_fall_through = get_absolute_expression();
};
void be_bbInfo_handler(int ignored ATTRIBUTE_UNUSED) {
    offsetT is_fall_through = get_absolute_expression();
};
void inlineb_bbInfo_handler(int ignored ATTRIBUTE_UNUSED) {};
void inlinee_bbInfo_handler(int ignored ATTRIBUTE_UNUSED) {};
void bbinfo_jmptbl_handler(int ignored ATTRIBUTE_UNUSED) {};