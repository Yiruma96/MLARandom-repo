//
// Created by root on 2020/11/17.
//

#ifndef GAS_RAND_H
#define GAS_RAND_H

#include "config.h"
#include "shuffleInfo.pb-c.h"
#include "as.h"
#include "frags.h"
#include "listing.h"

extern bfd_boolean strict_listing;
extern const char* object_file_name;

extern ShuffleInfo__Metadata metadata;
extern ShuffleInfo__Metadata__FixupInfo** global_fixups;
extern ShuffleInfo__Metadata__FunInfo** global_funs;
extern uint64_t c_funs;

struct fixup_node_{
    ShuffleInfo__Metadata__FixupInfo* fixupTuple;
    asection* sec;
    struct fixup_node_* next;
};
typedef struct fixup_node_ fixup_node;


/// 使用add_fixup函数加入fixup链表.
/// 注意第二类fixup在收集时即加入了,而第一类Fixup在fixup_collect_after函数才通过遍历fixup加入
extern fixup_node* fixups_head;
extern fixup_node* fixups_tail;
extern uint64_t global_fixup_count;

/// 收集第二类fixup到该链表. 在确定符号表后会遍历并更新其中的bbl_sym值
extern fixup_node* jmp_fixup_head;
extern fixup_node* jmp_fixup_tail;

//extern bfd_boolean has_writen_rand_section;
extern unsigned metadata_buf_len;
extern char* metadata_buf;

extern const pseudo_typeS bbInfo_pseudo_table[];

enum bbl_type{
    BBL=0,
    FUN=1,
    OBJ=2,
    INLINE_ASSEMBLY=3
};

typedef struct list_info_struct list_info_type;
typedef struct inst_node_ inst_node;
typedef struct inst_list_ inst_list;
typedef struct label_node_ label_node;
typedef struct label_list_ label_list;

struct inst_node_{
    list_info_type* inst_list_info;
    uint64_t offset;
    uint64_t size;
    inst_node* next;
};

struct inst_list_{
    uint64_t inst_count;
    inst_node* inst_list_head;
    inst_node* inst_list_tail;
};

struct label_node_{
    asection* sec; // which section the function belongs to
    const char* name;
    elf_symbol_type* sym;

    fragS* frag; // 考虑到fun头部可能是.align指令，因此不能简单的将函数开头等同于第一条实体指令
    uint64_t frag_offset;
    uint64_t offset;

    uint64_t inst_count;
    inst_node* inst_list_head;
    inst_node* inst_list_tail;

    label_node* pre;  // link pre label
    label_node* next; // link next label
};

struct label_list_{
    uint64_t label_count;
    label_node* label_list_head;
    label_node* label_list_tail;
};


enum section_enum{
    TEXT,
    RODATA,
    DATA,
    DATAREL,
    INITARRAY,
    NONE_SEC
};

enum base_type{
    NONE_BASE = 0,
    VALUE_BASE = 2,
    INDEX_BASE = 3
};

enum target_type{
	NONE_TARGET = 0,
	VALUE_TARGET = 2,
	INDEX_TARGET = 3
};

extern htab_t sec2label_map;
extern htab_t sec2inst_map;
extern label_list* now_labelList;
extern inst_list* now_instList;
extern uint64_t global_label_count;
extern uint64_t global_label_index;



void shuffleInfo_init(void);
bfd_boolean is_special_section_for_fixup(const char* secname);
void add_fixup(const char*, ShuffleInfo__Metadata__FixupInfo*);
void add_jmp_fixup(const char*, ShuffleInfo__Metadata__FixupInfo*, asection*);
void update_fixup(void);
char *targetType2Char(enum target_type);
char *baseType2Char(enum base_type);
char *bblType2Char(enum bbl_type);
void fixupInfo_init(u_int64_t, u_int64_t, u_int64_t, u_int64_t, u_int64_t);
u_int64_t serializeShuffleInfo(void);
void handle_jmp_fixup_list(void);

void label_handler(elf_symbol_type* elfsym);
void inst_handler(list_info_type* new_list_info, const char* line);

char *int2str(unsigned int value);

void funcb_bbInfo_handler(int ignored ATTRIBUTE_UNUSED);
void funce_bbInfo_handler(int ignored ATTRIBUTE_UNUSED);
void bb_bbInfo_handler(int ignored ATTRIBUTE_UNUSED);
void be_bbInfo_handler(int ignored ATTRIBUTE_UNUSED);
void inlineb_bbInfo_handler(int ignored ATTRIBUTE_UNUSED);
void inlinee_bbInfo_handler(int ignored ATTRIBUTE_UNUSED);
void bbinfo_jmptbl_handler(int ignored ATTRIBUTE_UNUSED);


#endif //GAS_RAND_H






