# coding=utf-8

from distutils import spawn
from enum import Enum
import struct
import logging
import leb128
from elftools.elf.elffile import ELFFile


def enum(*seq, **named):
    enums = dict(zip(seq, range(len(seq))), **named)
    return type('Enum', (), enums)


Formats = enum('CHAR', 'UCHAR', 'SHORT', 'USHORT',
               'INT', 'UINT', 'LONG', 'ULONG',
               'INVALID')
Sizes = {
    Formats.CHAR: 1,
    Formats.UCHAR: 1,
    Formats.SHORT: 2,
    Formats.USHORT: 2,
    Formats.INT: 4,
    Formats.UINT: 4,
    Formats.LONG: 8,
    Formats.ULONG: 8,
    Formats.INVALID: 0
}

# 通过类型指定
fmt = {Formats.CHAR: "<b", Formats.UCHAR: "<B",
       Formats.SHORT: "<h", Formats.USHORT: "H",
       Formats.INT: "<i", Formats.UINT: "<I",
       Formats.LONG: "<q", Formats.ULONG: "<Q"}

PK = lambda f, val: struct.pack(fmt[f], val)
UPK = lambda f, val: struct.unpack(fmt[f], val)[0]



# 通过长度指定
def getSignedFormat(sz):
    if sz == 1: return "<b"
    if sz == 2: return "<h"
    if sz == 4: return "<i"
    if sz == 8: return "<q"

def getUnsignedFormat(sz):
    if sz == 1: return "<B"
    if sz == 2: return "<H"
    if sz == 4: return "<I"
    if sz == 8: return "<Q"

signedRangeDict = {
    1: [-128, 127],
    2: [-0x8000, 0x7fff],
    4: [-0x80000000, 0x7fffffff],
    8: [-0x8000000000000000, 0x7fffffffffffffff]
}

unSignedRangeDict = {
    1: [0, 0xff],
    2: [0, 0xffff],
    4: [0, 0xffffffff],
    8: [0, 0xffffffffffffffff]
}

ANGR = 1
IDA = 2
GHIDRA = 3
RW = 4
DD = 5
BASE_ADDR_MAP = {ANGR: 0x400000, GHIDRA: 0x100000, IDA: 0x0, RW: 0x0, DD: 0x0}

VERSION = '0.83'
METADATA_PATH = './metadata.tmp.gz'
NEWBIN_POSTFIX = '_shuffled'
METADATA_POSTFIX = '.shuffle.bin'
METADESC_POSTFIX = '.meta.txt'
LOG_POSTFIX = '.log'
RAND_SECTION = '.rand'

ARM64 = 1
X64 = 2

X64_PrefixByte = [b'\x66', # 调整操作数宽度的指令前缀
                  b'\x67', # 调整地址宽度的指令前缀
                  b'\x2e',b'\x36',b'\x3e',b'\x26',b'\x64',b'\x65', # 段前缀指令
                  b'\xf0',b'\xf2',b'\xf3', # LOCK和PEPEAT前缀指令
                  ]

X64_PADDINGS = [
    b'\x90',
    b'\x66',
    b'\x00',
    b'\x40',
    b'\x84',
    b'\x44',
    b'\x80',
    b'\x0f\x1f',
    b'\x2e\x0f\x1f',
]

ARM64_PADDINGS = [b'\x1f\x20\x03\xd5']

# 下面这几个节里的指针被直接记录在fixup元数据中
SEC_TEXT = '.text'
SEC_RODATA = '.rodata'
SEC_DATA = '.data'
SEC_DATA_REL = '.data.rel.ro'
SEC_DATA_REL_LOCAL = '.data.rel.ro.local'
SEC_INIT_ARR = '.init_array'
SEC_FINI_ARR = '.fini_array'
SEC_PERINIT_ARR = '.preinit_array'
SEC_GOT = '.got'
SEC_INIT = '.init'
SEC_FINI = '.fini'
# 下面这几个节的结构中可能含有指针，通过结构解析即可得到无需记录在fixup中
SEC_TM_CLONE = '.tm_clone_table'
SEC_BSS = '.bss'
SEC_TBSS = '.tbss'
SEC_REL_DYN = '.rela.dyn'
SEC_REL_PLT = '.rela.plt'
SEC_DYNSYM = '.dynsym'
SEC_EH_FRAME = '.eh_frame'
SEC_EH_FR_HDR = '.eh_frame_hdr'
SEC_GCC_EXECPT_TABLE = '.gcc_except_table'
SEC_SYMTAB = '.symtab'
SEC_DEBUG_INFO = '.debug_info'

class SecType(Enum):
    NORMAL = 1
    TEXT = 2
    RELOC = 3
    SYMBOL = 4
    EHFRAME = 5
    EHFRAMEHDR = 6

# Type definitions
BBL_TYPE = {0: "BBL", 1: "FUN", 2: "OBJ", 3: "OBJ_TEMP"}
FIXUP_TYPE = {0: "C2C", 1: "C2D", 2: "D2C", 3: "D2D", 4: "NewSectionStart", 5: 'Special', 6: "None"}
SRC_TYPE = {0: "C/C++", 1: "Inline Assembly", 2: "Standalone Assembly"}

SRC_TYPE_C, SRC_TYPE_INLINE, SRC_TYPE_ASSEMBLY = 0, 1, 2
# xie: FT_NewSectionStart类型不存在，链接阶段会计算其type   FT_Special类型的我都一起纳入到FixupLayout中去了
FT_C2C, FT_C2D, FT_D2C, FT_D2D, FT_NewSectionStart, FT_Special, FT_None = 0, 1, 2, 3, 4, 5, 6
FT_NewSec = 4  # Fixup Type that new section begins
FT_Special = 5  # {".text.unlikely", ".text.exit", ".text.startup", ".text.hot"} section

DS_FIXUP_TEXT = ['fixup_offset', 'fixup_deref_size',
                 'fixup_is_rela', 'fixup_type',
                 'fixup_num_jt_entries', 'fixup_jt_entry_sz']
DS_FIXUP_RODATA = ['fixup_offset_ro', 'fixup_deref_size_ro',
                   'fixup_is_rela_ro', 'fixup_type_ro']
DS_FIXUP_DATA = ['fixup_offset_data', 'fixup_deref_size_data',
                 'fixup_is_rela_data', 'fixup_type_data']
DS_FIXUP_DATAREL = ['fixup_offset_datarel', 'fixup_deref_size_datarel',
                    'fixup_is_rela_datarel', 'fixup_type_datarel']
DS_FIXUP_INIT_ARR = ['fixup_offset_initarray', 'fixup_deref_size_initarray',
                     'fixup_is_rela_initarray', 'fixup_type_initarray']

FUN_ALIGNMENT = 0x10  # 函数的地址，也就是函数入口基本块的对齐粒度，注意这会改变text节的大小，但应该不会太多



class TargetType(Enum):
    NORMAL = 1  # S+A
    PAGE_NORMAL = 2  # 目标对象为Symbol地址取Page            PAGE(S+A)
    GOT_ENTRY = 3  # 目标对象为GOT Entry                  G(GDAT(S+A))
    PAGE_GOT_ENTRY = 4  # 目标对象为GOT Entry的地址取Page       Page(G(GDAT(S+A)))
    TLS_ENTRY = 5  # 目标对象为Thread Local Variable      TPREL(S+A)
    PAGE_TLS_ENTRY = 6  # 目标对象为TLS或TLS offset后再取Page   Page(G(GTPREL(S+A)))
    UNKNOWN = 7  # 一些暂时不太清楚的



class BaseType(Enum):
    SYM = 1  # sym
    PC = 2  # P
    PAGE_PC = 3  # Page(P)
    GOT = 4
    PAGE_GOT = 5  # Page(GOT) 以GOT_OFFSET_TABLE地址所在页作为基址，因为Target为GOT_ENTRY，其高地址更加临近GOT附近
    TLS = 6
    TP = 7  # TPREL(S+A) target为TLS，基址为TP
    UNKNOWN = 8
    NONE = 9  # 绝对寻址
    JPTSYM = 10 # SYM中为跳转表的


"""
### 两种多指针联合重定位，导致提取出的指针只是一部分，并影响指针更新过程
1. 先传高位(用Page(target)或Page(target)-Page(base))，再传低12位low(S+A)。
2. group relocation

联合重定位主要会对指针更新式子产生影响。
指针更新方案中，指针newValue=mask(F+△)，这需要完整的F和△和mask才能得到，需要注意它≠mask(F)+mask(△)。
一般来说，F是能够直接提取的，而组合重定位下F是部分值的时候，则需要考虑怎么把F还原出来
1. Page(Base) + Fixup = Page(S+A)
对于这种情况，F的低位一定是0，所以容易还原
2. P + F = S + A
这种情况下就很难办了，要还原出来完整的F可以考虑以下两种方案
a. movw这种group relocation，他们好像是连续的，所以F还是可以拿到的
b. low(12) low(15)的这种情况，可以看到他们并非连续的，而且就算是顺序相连，由于存在高位相对低位绝对的情况，两者的bit也没法直接链接。
  4172a0:	d0ffffe5 	adrp	x5, 415000 <predict_16x16_p+0x90>
  4172a4:	d0ffffe6 	adrp	x6, 415000 <predict_16x16_p+0x90>
  4172a8:	911900a5 	add	x5, x5, #0x640
  4172ac:	9116e0c6 	add	x6, x6, #0x5b8
  这种情况下我们再分别考虑：
  1. 如果它是绝对寻址，则mask(F+△)中△不会导致lowF需要高位借位，因此mask(F+△)=mask(lowF+△)
  2. 如果他是相对寻址，则mask(F+△)中存在△需要lowF向高位借位的情况，因此导致F需要高位借位，因此mask(F+△)=mask(lowF+△)
  
补充考虑：对于二进制分析来说，遇到了2.b的情况时，他面临着有base，有部分fixup，构建不出来完整式子的问题，这时候需要运行必要的数据流分析来找到高位fixup才行


### 溢出检查：checkHigh 和 checkLow的判断规则
联合重定位中的HI，在省略部分高位时如[12, 33]，关注高位溢出
联合重定位中的LO，在省略部分低位时如[2, 12]，关注低位溢出
联合重定位中的group relocation，因为使用完整的64位表示所以无需关注溢出
其他类型的，还是看是否省略了高位和低位，来看是否要关注溢出，要注意其中一些加了LO，但其实并非是联合重定位，如273、274


### 理解一些常见的重定位
ABS             绝对寻址类型
PREL            相对寻址类型
GOTREL GOTOFF   got-relative
TPREL           tls-relative

GOTOFF_G0 TLSGD GOT_LD_PREL19  目标地址为GOT ENTRY
TLSLE TLSLD TLSGD    目标地址为TLS ENTRY

LDST8|16|3|64|128|256 ldr和str指令，取目标地址处的nbit
ADD add指令所属，一般用来传低位
ADR adrp指令所属，一般用来传高位

LO 联合重定位中的低位
HI 联合重定位中的高位
MOVW_G0|1|2|3  联合重定位中的16bit


### TLS相关的四类重定位
if (executable) { // -fno-pic or -fpie
  if (preemptible)
    initial-exec;
  else
    local-exec;
} else { // -fpic
  if (preemptible || local-dynamic is not profitable)
    general-dynamic;
  else
    local-dynamic;
}

- Local Exec thread-local storage model       如R_AARCH64_TLSLE_MOVW_TPREL_G2
这是最有效的TLS模型。它适用于在可执行文件中定义TLS符号的情况。
```
thread_local int b=0;
400c0c:	d53bd040 	mrs	x0, tpidr_el0            # x0存放TLS基址
400c10:	91400000 	add	x0, x0, #0x0, lsl #12    # 基址累加上tls-offset,即高位的0和低12bit的0x14
400c14:	91005000 	add	x0, x0, #0x14            # 最后拿到tls-var地址
```

- Initial Exec thread-local storage model     如R_AARCH64_TLSIE_MOVW_GOTTPREL_G1
这种模式比Local Exec的效率要低。它将TLS-offset存放到GOT Entry中，使用的时候会在GOT中取。
```
extern thread_local int ref;
400c1c:	94000098 	bl	400e7c <_ZTW1c>  # 取得TLS地址
400c20:	b9400001 	ldr	w1, [x0]
0000000000400e7c <_ZTW1c>:
    400e9c:	d53bd041 	mrs	x1, tpidr_el0     # tls基址
    400ea0:	f00000e0 	adrp	x0, 41f000 <__FRAME_END__+0x1de40>  # 从GOT表中取得tls-offset
    400ea4:	f947f000 	ldr	x0, [x0, #4064]
    400ea8:	8b000020 	add	x0, x1, x0        # 基址x1累加tls-offset(x0),拿到tls-var的地址
```

- Local Dynamic TLS relocations               如R_AARCH64_TLSLD_ADR_PREL21
- General Dynamic thread-local storage model  如R_AARCH64_TLSGD_ADR_PREL21
这两种模式是在TLS符号定义在shared lib中使用的
```
// main函数中创建一个key，该key是全局共用的
pthread_key_t tls_key;
int err = pthread_key_create(&tls_key, cleanup); 
// 线程中使用
pthread_setspecific(tls_key, p);  // 线程为该TLS存储设置值
p = pthread_getspecific(tls_key); // 线程为读取该TLS值
目前还没有观察这两类对应的汇编指令
```

然后，LD,GD,IE,LE是一个效率逐渐优化的过程，所以aarch64.cc里有个optimize_tls_reloc函数负责做TLS的降级，包括
TLSOPT_NONE,  不做转换
TLSOPT_TO_LD, 转换GD -> LD
TLSOPT_TO_LE, 转换GD或LD -> LE
TLSOPT_TO_IE  转换GD或LD或LE -> IE
TLS相关指令的优化需要考虑以下两点：
1. 是否影响layout元数据？ 由于xx2xx的转换是一个复杂到简单的过程，不再需要的指令会被替换为nop做填充，因此TLS相关指令的优化不会影响layout布局
2. 是否影响fixup元数据？ 会影响。LD GD IE LE使用不同的重定位类型，比如从LE转IE的话，就会从GOTTPREL变为TPREL，
    前者表示rip到GOTEntry的offset，在随机化时发生改变，而后者表示tls-offset，在随机化时不发生改变。


### 注意以下情况
1.  .L490:
2.      ldr	x1, [x19, 16]
3 .    mov	x2, x19
4 .    ...
5 . .L494
6 .    adr	x2, .Lrtx491
7 .    add	x1, x2, w1, sxtb #2
8 .    br	x1
9 . .Lrtx491:
10.     .bbInfo_BE 0
11.     .section	.rodata
12. .L491:
13.     .byte	(.L490 - .Lrtx491) / 4
14.     .byte	(.L490 - .Lrtx491) / 4
15. .bbInfo_FUNE
16. .bbInfo_FUNB
17. stp	x29, x30, [sp, -112]!
line6 line13 line14里的指针，都使用到了.Lrtx491这个符号，该符号其实是表示一个基本块的尾部
由于我们记录符号的地址并找到其所指向的BBL，因此.Lrtx491被认为表示的是后一个基本块也就是line17所在的基本块
这相当于我们的随机化更换了跳转表的基址，本来是处于上一个基本块尾部也就是line8的位置，但是现在基址变到了下一个基本块开头也就是line17的位置。
其实如果只是改到函数内还没什么，但如果基址改到下一个函数，函数间的位置改变就会导致基址和目标地址间的距离过大而溢出
要解决的话需要将符号所属的BBL给切换回上一个去，但这需要定制处理，目前不做修复，只是将此类短指针加入到低约束中


### binutils中和重定位相关的结构
1. gas中使用自己定义的bfd_reloc，该enum定义在 bfd/bfd-in2.h中. 这样每个bfd_reloc就有了一个编号
enum bfd_reloc_code_real {
    /* Basic absolute relocations of N bits.  */
    BFD_RELOC_64,
    BFD_RELOC_32,
    BFD_RELOC_8,
    
    /* x86-64/elf relocations  */
    BFD_RELOC_X86_64_GOT32,
    BFD_RELOC_X86_64_PLT32,
    
    /* aarch64/elf relocations */
    BFD_RELOC_AARCH64_64,
    BFD_RELOC_AARCH64_32,
    BFD_RELOC_AARCH64_16,
}

2. gas在写重定位的时候，需要将bfd_reloc转化为elf-reloc(即reloc_howto_type,里面包括elf_reloc的名字，以及mash，shift，doffset等信息)
从实现机制上来看，都是要从howto_table中拿到reloc_howto_type，
- 但是aarch64的howto_type是以bfd_reloc作为下标组织的
- 而x64的howto_table是以elf_reloc作为下标组织的，因此在查询前就需要先做一个转换。尤其x86_64_reloc_map还不是hash_map,采用顺序搜索的方法
#### x64采用如下机制：
static reloc_howto_type* elf_x86_64_reloc_type_lookup (bfd *abfd, bfd_reloc_code_real_type code) {
    for (i = 0; i < sizeof (x86_64_reloc_map) / sizeof (struct elf_reloc_map); i++){
        // 1. 首先通过reloc_map找到对应的bfd_reloc
        if (x86_64_reloc_map[i].bfd_reloc_val == code)
            // 2. 然后根据elf_reloc在howto_table中拿到reloc_howto_type
            return elf_x86_64_rtype_to_howto (abfd, x86_64_reloc_map[i].elf_reloc_val);
    }
}
static const struct elf_reloc_map x86_64_reloc_map[] =
{
  { BFD_RELOC_NONE,		R_X86_64_NONE, },
  { BFD_RELOC_64,		R_X86_64_64,   },
  { BFD_RELOC_32_PCREL,		R_X86_64_PC32, },
  ...
}
static reloc_howto_type x86_64_elf_howto_table[] =
{
    HOWTO(R_X86_64_NONE, 0, 3, 0, FALSE, 0, complain_overflow_dont,
        bfd_elf_generic_reloc, "R_X86_64_NONE",	FALSE, 0x00000000, 0x00000000, FALSE),
    HOWTO(R_X86_64_64, 0, 4, 64, FALSE, 0, complain_overflow_bitfield,
        bfd_elf_generic_reloc, "R_X86_64_64", FALSE, MINUS_ONE, MINUS_ONE, FALSE),
    ...
}

#### aarch64采用如下机制：
static reloc_howto_type* elfNN_aarch64_howto_from_bfd_reloc (bfd_reloc_code_real_type code){
    // 1. 通用的bfd_reloc转换为aarch64特定的bfd_reloc
    // static const struct elf_aarch64_reloc_map elf_aarch64_reloc_map[] = {
    //     {BFD_RELOC_CTOR, BFD_RELOC_AARCH64_NN},
    //     {BFD_RELOC_64, BFD_RELOC_AARCH64_64},
    //     {BFD_RELOC_32, BFD_RELOC_AARCH64_32},
    //     {BFD_RELOC_16, BFD_RELOC_AARCH64_16},
    //      ...
    // }
    if (elf_aarch64_reloc_map[i].from == code){
        code = elf_aarch64_reloc_map[i].to;
    }
    
    // 2. 该howto_table的下标是bfd_reloc, 因此通过bfd_reloc即可在map中对应到elf_reloc
    reloc_howto_type elf_reloc =  elfNN_aarch64_howto_table[code - BFD_RELOC_AARCH64_RELOC_START];
}
static reloc_howto_type elfNN_aarch64_howto_table[] = {
    HOWTO64 (R_AARCH64_NULL,	/* type */
        0,			/* rightshift */
        3,			/* size (0 = byte, 1 = short, 2 = long) */
        0,			/* bitsize */
        FALSE,			/* pc_relative */
        0,			/* bitpos */
        complain_overflow_dont,	/* complain_on_overflow */
        bfd_elf_generic_reloc,	/* special_function */
        "R_AARCH64_NULL",	/* name */
        FALSE,			/* partial_inplace */
        0,			/* src_mask */
        0,			/* dst_mask */
        FALSE),		/* pcrel_offset */
    ...
}


#### 汇编语言的信息同样不完整？
该汇编指令以绝对地址指向GOT位置，表示从GOT结尾向前的偏移
movabsq	$PL_sv_undef@GOT, %rdx


   18a1c:	48 ba 80 d9 ff ff ff 	movabs $0xffffffffffffd980,%rdx
   18a23:	ff ff ff 

"""


# relocName, addressMode, targetDesc, targetType, baseDesc, baseType, mask, dooffset, size, nextNum, checkHigh, checkLow, neesShow, isCodePointer
# NOTE: 每一项的解释
# mask. value要首先进行mask，得到更简略的bit序列
# dooffset. mask后的bit序列如何写入到指令中
# nextNum. 用来判断是否可以从下一条指令中继续收集指针的其余部分信息
# isCodePointer. ARM下text节中可能存在data pointer，而且data pointer和code pointer是两种转换方法，所以我们要区分指针类型以采用不同的修复方法。
#                前者是小端byte序+大端bit序，后者是小端byte序+小端bit序。
# NOTE: 基址和目标地址仍存在三种不准确的情况，注意讨论
#  Case1. SYM基址包含在PC中
#  Case2. need_update重新收集导致第一等式变为第二等式 (不影响PC因此不影响SYM类型的识别)
#  Case2. [reloc]无法收集到第一等式 (非rand的直接排除即可)
aarch64_reloc_dict = {
    0: ['R_AARCH64_NONE', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 64, 0, 0, 0, 1, 1],
    256: ['R_AARCH64_withdrawn', 'Treat as R_AARCH64_NONE', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 64, 0, 0, 0, 1, 1],
    257: ['R_AARCH64_ABS64', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 64], [[0, 64]], 64, 0, 0, 0, 0, 0],
    258: ['R_AARCH64_ABS32', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 32], [[0, 32]], 32, 0, 1, 0, 0, 0],
    259: ['R_AARCH64_ABS16', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 16], [[0, 16]], 16, 0, 1, 0, 0, 0],
    260: ['R_AARCH64_PREL64', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [0, 64], [[0, 64]], 64, 0, 0, 0, 0, 0],
    261: ['R_AARCH64_PREL32', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 1, 0, 0, 0],
    262: ['R_AARCH64_PREL16', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [0, 16], [[0, 16]], 16, 0, 1, 0, 0, 0],
    263: ['R_AARCH64_MOVW_UABS_G0', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 16], [[5, 21]], 16, 0, 0, 0, 0, 1],
    264: ['R_AARCH64_MOVW_UABS_G0_NC', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 16], [[5, 21]], 16, 0, 0, 0, 0, 1],
    265: ['R_AARCH64_MOVW_UABS_G1', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [16, 32], [[5, 21]], 16, 1, 0, 0, 0, 1],
    266: ['R_AARCH64_MOVW_UABS_G1_NC', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [16, 32], [[5, 21]], 16, 1, 0, 0, 0, 1],
    267: ['R_AARCH64_MOVW_UABS_G2', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [32, 48], [[5, 21]], 16, 2, 0, 0, 0, 1],
    268: ['R_AARCH64_MOVW_UABS_G2_NC', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [32, 48], [[5, 21]], 16, 2, 0, 0, 0, 1],
    269: ['R_AARCH64_MOVW_UABS_G3', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [48, 64], [[5, 21]], 16, 3, 0, 0, 0, 1],
    270: ['R_AARCH64_MOVW_SABS_G0', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 16], [[5, 21]], 16, 0, 0, 0, 1, 1],
    271: ['R_AARCH64_MOVW_SABS_G1', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [16, 32], [[5, 21]], 16, 1, 0, 0, 1, 1],
    272: ['R_AARCH64_MOVW_SABS_G2', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [32, 48], [[5, 21]], 16, 2, 0, 0, 1, 1],
    273: ['R_AARCH64_LD_PREL_LO19', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [2, 21], [[5, 24]], 19, -1, 1, 1, 1, 1],  # doffset存疑，目前用的LD结构，而非LDST的存储结构
    274: ['R_AARCH64_ADR_PREL_LO21', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [0, 21], [[29, 31], [5, 24]], 21, -1, 1, 0, 0, 1], # 虽然是LO，但不再有高位输入，因此要关注高位溢出
    275: ['R_AARCH64_ADR_PREL_PG_HI21', 'Page(S+A) - Page(P)', 'Page(S+A)', TargetType.PAGE_NORMAL, 'Page(P)', BaseType.PAGE_PC, [12, 33], [[29, 31], [5, 24]], 21, 0, 1, 0, 0, 1],
    276: ['R_AARCH64_ADR_PREL_PG_HI21_NC', 'Page(S+A) - Page(P)', 'Page(S+A)', TargetType.PAGE_NORMAL, 'Page(P)', BaseType.PAGE_PC, [12, 33], [[29, 31], [5, 24]], 21, 0, 1, 0, 0, 1],
    277: ['R_AARCH64_ADD_ABS_LO12_NC', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 12], [[10, 22]], 12, -1, 0, 0, 0, 1],
    278: ['R_AARCH64_LDST8_ABS_LO12_NC', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 12], [[10, 22]], 12, -1, 0, 0, 0, 1],
    279: ['R_AARCH64_TSTBR14', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [2, 16], [[5, 19]], 14, 0, 1, 1, 0, 1],
    280: ['R_AARCH64_CONDBR19', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [2, 21], [[5, 24]], 19, 0, 1, 1, 0, 1],
    282: ['R_AARCH64_JUMP26', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [2, 28], [[0, 26]], 26, 0, 1, 1, 0, 1],
    283: ['R_AARCH64_CALL26', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [2, 28], [[0, 26]], 26, 0, 1, 1, 0, 1],
    284: ['R_AARCH64_LDST16_ABS_LO12_NC', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [1, 12], [[10, 22]], 12, -1, 0, 1, 0, 1],
    285: ['R_AARCH64_LDST32_ABS_LO12_NC', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [2, 12], [[10, 22]], 12, -1, 0, 1, 0, 1],
    286: ['R_AARCH64_LDST64_ABS_LO12_NC', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [3, 12], [[10, 22]], 12, -1, 0, 1, 0, 1],
    287: ['R_AARCH64_MOVW_PREL_G0', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, None, None, 16, 0, 0, 0, 1, 1],
    288: ['R_AARCH64_MOVW_PREL_G0_NC', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, None, None, 16, 0, 0, 0, 1, 1],
    289: ['R_AARCH64_MOVW_PREL_G1', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, None, None, 16, 1, 0, 0, 1, 1],
    290: ['R_AARCH64_MOVW_PREL_G1_NC', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, None, None, 16, 1, 0, 0, 1, 1],
    291: ['R_AARCH64_MOVW_PREL_G2', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, None, None, 16, 2, 0, 0, 1, 1],
    292: ['R_AARCH64_MOVW_PREL_G2_NC', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, None, None, 16, 2, 0, 0, 1, 1],
    293: ['R_AARCH64_MOVW_PREL_G3', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, None, None, 16, 3, 0, 0, 1, 1],
    299: ['R_AARCH64_LDST128_ABS_LO12_NC', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [4, 12], [[10, 22]], 12, -1, 0, 1, 0, 1],
    300: ['R_AARCH64_MOVW_GOTOFF_G0', 'G(GDAT(S+A))-GOT', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 0, 0, 0, 1, 1],
    301: ['R_AARCH64_MOVW_GOTOFF_G0_NC', 'G(GDAT(S+A))-GOT', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 0, 0, 0, 1, 1],
    302: ['R_AARCH64_MOVW_GOTOFF_G1', 'G(GDAT(S+A))-GOT', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 1, 0, 0, 1, 1],
    303: ['R_AARCH64_MOVW_GOTOFF_G1_NC', 'G(GDAT(S+A))-GOT', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 1, 0, 0, 1, 1],
    304: ['R_AARCH64_MOVW_GOTOFF_G2', 'G(GDAT(S+A))-GOT', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 2, 0, 0, 1, 1],
    305: ['R_AARCH64_MOVW_GOTOFF_G2_NC', 'G(GDAT(S+A))-GOT', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 2, 0, 0, 1, 1],
    306: ['R_AARCH64_MOVW_GOTOFF_G3', 'G(GDAT(S+A))-GOT', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 3, 0, 0, 1, 1],
    307: ['R_AARCH64_GOTREL64', 'S + A - GOT', 'S', TargetType.NORMAL, 'GOT', BaseType.GOT, None, None, 64, 0, 0, 0, 1, 0],
    308: ['R_AARCH64_GOTREL32', 'S + A - GOT', 'S', TargetType.NORMAL, 'GOT', BaseType.GOT, None, None, 32, 0, 1, 0, 1, 0],
    309: ['R_AARCH64_GOT_LD_PREL19', 'G(GDAT(S+A))-P', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'P', BaseType.PC, None, None, 19, 0, 0, 0, 1, 1],
    310: ['R_AARCH64_LD64_GOTOFF_LO15', 'G(GDAT(S+A))-GOT', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 15, -1, 0, 0, 1, 1],
    311: ['R_AARCH64_ADR_GOT_PAGE', 'Page(G(GDAT(S+A)))-Page(P)', 'Page(G(GDAT(S+A)))', TargetType.PAGE_GOT_ENTRY, 'Page(P)', BaseType.PAGE_PC, [12, 33], [[29, 31], [5, 24]], 21, 0, 1, 0, 0, 1],
    312: ['R_AARCH64_LD64_GOT_LO12_NC', 'G(GDAT(S+A))', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, '', BaseType.NONE, [3, 12], [[10, 22]], 12, -1, 0, 1, 0, 1],
    313: ['R_AARCH64_LD64_GOTPAGE_LO15', 'G(GDAT(S+A))-Page(GOT)', 'G(GDAT(S+A))', TargetType.GOT_ENTRY, 'Page(GOT)', BaseType.PAGE_GOT, [3, 15], [[10, 22]], 15, -1, 0, 1, 1, 1],
    314: ['R_AARCH64_PLT32', 'S + A - P', 'S', TargetType.NORMAL, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 1, 0, 0, 0],
    512: ['R_AARCH64_TLSGD_ADR_PREL21', 'G(GTLSIDX(S,A)) - P', 'G(GTLSIDX(S,A))', TargetType.GOT_ENTRY, 'P', BaseType.PC, None, None, 21, 0, 0, 0, 1, 1],
    513: ['R_AARCH64_TLSGD_ADR_PAGE21', 'Page(G(GTLSIDX(S,A)))-Page(P)', 'Page(G(GTLSIDX(S,A)))', TargetType.PAGE_GOT_ENTRY, 'Page(P)', BaseType.PAGE_PC, [12, 33], [[29, 31], [5, 24]], 21, 0, 0, 0, 1, 1],
    514: ['R_AARCH64_TLSGD_ADD_LO12_NC', 'G(GTLSIDX(S,A))', 'G(GTLSICX(S,A))', TargetType.GOT_ENTRY, '', BaseType.NONE, [0, 12], [[10, 22]], 12, -1, 0, 0, 1, 1],
    515: ['R_AARCH64_TLSGD_MOVW_G1', 'G(GTLSIDX(S,A)) - GOT', 'G(GTLSIDX(S,A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 1, 0, 0, 1, 1],
    516: ['R_AARCH64_TLSGD_MOVW_G0_NC', 'G(GTLSIDX(S,A)) - GOT', 'G(GTLSIDX(S,A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 0, 0, 0, 1, 1],
    517: ['R_AARCH64_TLSLD_ADR_PREL21', 'G(GLDM(S)) - P', 'G(GLDM(S))', TargetType.GOT_ENTRY, 'P', BaseType.PC, None, None, 21, 0, 0, 0, 1, 1],
    518: ['R_AARCH64_TLSLD_ADR_PAGE21', 'Page(G(GLDM(S))) - Page(P)', 'Page(G(GLDM(S)))', TargetType.PAGE_GOT_ENTRY, 'Page(P)', BaseType.PAGE_PC, [12, 33], [[29, 31], [5, 24]], 21, 0, 1, 0, 1, 1],
    519: ['R_AARCH64_TLSLD_ADD_LO12_NC', 'G(GLDM(S))', 'G(GLDM(S))', TargetType.GOT_ENTRY, '', BaseType.NONE, [0, 12], [[10, 22]], 12, -1, 0, 0, 1, 1],
    520: ['R_AARCH64_TLSLD_MOVW_G1', 'G(GLDM(S)) - GOT', 'G(GLDM(S))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 1, 1, 0, 1, 1],
    521: ['R_AARCH64_TLSLD_MOVW_G0_NC', 'G(GLDM(S)) - GOT', 'G(GLDM(S))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 0, 1, 0, 1, 1],
    522: ['R_AARCH64_TLSLD_LD_PREL19', 'G(GLDM(S)) - P', 'G(GLDM(S))', TargetType.GOT_ENTRY, 'P', BaseType.PC, None, None, 19, 0, 0, 0, 1, 1],
    523: ['R_AARCH64_TLSLD_MOVW_DTPREL_G2', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 16, 2, 0, 0, 1, 1],
    524: ['R_AARCH64_TLSLD_MOVW_DTPREL_G1', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, [16, 32], [[29, 31], [5, 24]], 16, 1, 0, 0, 1, 1],
    525: ['R_AARCH64_TLSLD_MOVW_DTPREL_G1_NC', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 16, 1, 0, 0, 1, 1],
    526: ['R_AARCH64_TLSLD_MOVW_DTPREL_G0', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 16, 0, 0, 0, 1, 1],
    527: ['R_AARCH64_TLSLD_MOVW_DTPREL_G0_NC', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, [0, 16], [[5, 21]], 16, 0, 0, 0, 1, 1],
    528: ['R_AARCH64_TLSLD_ADD_DTPREL_HI12', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, [12, 24], [[10, 22]], 12, -1, 1, 0, 1, 1],
    529: ['R_AARCH64_TLSLD_ADD_DTPREL_LO12', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    530: ['R_AARCH64_TLSLD_ADD_DTPREL_LO12_NC', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, [0, 12], [[10, 22]], 12, -1, 0, 0, 1, 1],
    531: ['R_AARCH64_TLSLD_LDST8_DTPREL_LO12', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    532: ['R_AARCH64_TLSLD_LDST8_DTPREL_LO12_NC', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    533: ['R_AARCH64_TLSLD_LDST16_DTPREL_LO12', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    534: ['R_AARCH64_TLSLD_LDST16_DTPREL_LO12_NC', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    535: ['R_AARCH64_TLSLD_LDST32_DTPREL_LO12', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    536: ['R_AARCH64_TLSLD_LDST32_DTPREL_LO12_NC', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    537: ['R_AARCH64_TLSLD_LDST64_DTPREL_LO12', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    538: ['R_AARCH64_TLSLD_LDST64_DTPREL_LO12_NC', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    539: ['R_AARCH64_TLSIE_MOVW_GOTTPREL_G1', 'G(GTPREL(S+A)) - GOT', 'G(GTPREL(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, [16, 32], [[5, 21]], 16, 1, 0, 0, 1, 1],
    540: ['R_AARCH64_TLSIE_MOVW_GOTTPREL_G0_NC', 'G(GTPREL(S+A)) - GOT', 'G(GTPREL(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, [0, 16], [[5, 21]], 16, 0, 0, 0, 1, 1],
    541: ['R_AARCH64_TLSIE_ADR_GOTTPREL_PAGE21', 'Page(G(GTPREL(S+A)))-Page(P)', 'Page(G(GTPREL(S+A)))', TargetType.PAGE_GOT_ENTRY, 'Page(P)', BaseType.PAGE_PC, [12, 33], [[29, 31], [5, 24]], 21, 0, 1, 0, 1, 1],
    542: ['R_AARCH64_TLSIE_LD64_GOTTPREL_LO12_NC', 'G(GTPREL(S+A))', 'G(GTPREL(S+A))', TargetType.GOT_ENTRY, '', BaseType.NONE, [3, 12], [[10, 22]], 12, -1, 0, 1, 1, 1],
    543: ['R_AARCH64_TLSIE_LD_GOTTPREL_PREL19', 'G(GTPREL(S+A)) - P', 'G(GTPREL(S+A))', TargetType.GOT_ENTRY, 'P', BaseType.PC, [2, 21], [[5, 24]], 19, 0, 0, 1, 1, 1],
    544: ['R_AARCH64_TLSLE_MOVW_TPREL_G2', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, [32, 48], [[5, 21]], 16, 2, 0, 0, 1, 1],
    545: ['R_AARCH64_TLSLE_MOVW_TPREL_G1', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, [16, 32], [[5, 21]], 16, 1, 0, 0, 1, 1],
    546: ['R_AARCH64_TLSLE_MOVW_TPREL_G1_NC', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, [16, 32], [[5, 21]], 16, 1, 0, 0, 1, 1],
    547: ['R_AARCH64_TLSLE_MOVW_TPREL_G0', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, [0, 16], [[5, 21]], 16, 0, 0, 0, 1, 1],
    548: ['R_AARCH64_TLSLE_MOVW_TPREL_G0_NC', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, [0, 16], [[5, 21]], 16, 0, 0, 0, 1, 1],
    549: ['R_AARCH64_TLSLE_ADD_TPREL_HI12', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, [12, 24], [[10, 22]], 12, -1, 1, 0, 1, 1],
    550: ['R_AARCH64_TLSLE_ADD_TPREL_LO12', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, [0, 12], [[10, 22]], 12, -1, 0, 0, 1, 1],
    551: ['R_AARCH64_TLSLE_ADD_TPREL_LO12_NC', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, [0, 12], [[10, 22]], 12, -1, 0, 0, 1, 1],
    552: ['R_AARCH64_TLSLE_LDST8_TPREL_LO12', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12, -1, 0, 0, 1, 1],
    553: ['R_AARCH64_TLSLE_LDST8_TPREL_LO12_NC', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12, -1, 0, 0, 1, 1],
    554: ['R_AARCH64_TLSLE_LDST16_TPREL_LO12', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12, -1, 0, 0, 1, 1],
    555: ['R_AARCH64_TLSLE_LSDT16_TPREL_LO12_NC', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12, -1, 0, 0, 1, 1],
    556: ['R_AARCH64_TLSLE_LDST32_TPREL_LO12', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12, -1, 0, 0, 1, 1],
    557: ['R_AARCH64_TLSLE_LDST32_TPREL_LO12_NC', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12,-1, 0, 0, 1, 1],
    558: ['R_AARCH64_TLSLE_LDST64_TPREL_LO12', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12, -1, 0, 0, 1, 1],
    559: ['R_AARCH64_TLSLE_LDST64_TPREL_LO12_NC', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12, -1, 0, 0, 1, 1],
    560: ['R_AARCH64_TLSDESC_LD_PREL19', 'G(GTLSDESC(S+A)) - P', 'G(GTLSDESC(S+A))', TargetType.GOT_ENTRY, 'P', BaseType.PC, None, None, 19, 0, 0, 0, 1, 1],
    561: ['R_AARCH64_TLSDESC_ADR_PREL21', 'G(GTLSDESC(S+A)) - P', 'G(GTLSDESC(S+A))', TargetType.GOT_ENTRY, 'P', BaseType.PC, None, None, 21, 0, 0, 0, 1, 1],
    562: ['R_AARCH64_TLSDESC_ADR_PAGE21', 'Page(G(GTLSDESC(S+A)))-Page(P)', 'Page(G(GTLSDESC(S+A)))', TargetType.PAGE_GOT_ENTRY, 'Page(P)', BaseType.PAGE_PC, [12, 33], [[29, 31], [5, 24]], 21, 0, 1, 0, 1, 1],
    563: ['R_AARCH64_TLSDESC_LD64_LO12', 'G(GTLSDESC(S+A))', 'G(GTLSDESC(S+A))', TargetType.GOT_ENTRY, '', BaseType.NONE, [3, 12], [[10, 22]], 12, -1, 0, 1, 1, 1],
    564: ['R_AARCH64_TLSDESC_ADD_LO12', 'G(GTLSDESC(S+A))', 'G(GTLSDESC(S+A))', TargetType.GOT_ENTRY, '', BaseType.NONE, [0, 12], [[10, 22]], 12, -1, 0, 0, 1, 1],
    565: ['R_AARCH64_TLSDESC_OFF_G1', 'G(GTLSDESC(S+A)) - GOT', 'G(GTLSDESC(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 0, 0, 0, 1, 1],
    566: ['R_AARCH64_TLSDESC_OFF_G0_NC', 'G(GTLSDESC(S+A)) - GOT', 'G(GTLSDESC(S+A))', TargetType.GOT_ENTRY, 'GOT', BaseType.GOT, None, None, 16, 0, 0, 0, 1, 1],
    567: ['R_AARCH64_TLSDESC_LDR', 'None', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, None, 0, 0, 0, 1, 1],
    568: ['R_AARCH64_TLSDESC_ADD', 'None', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, None, 0, 0, 0, 1, 1],
    569: ['R_AARCH64_TLSDESC_CALL', 'None', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, None, 0, 0, 0, 1, 1],
    570: ['R_AARCH64_TLSLE_LDST128_TPREL_LO12', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12, -1, 0, 0, 1, 1],
    571: ['R_AARCH64_TLSLE_LDST128_TPREL_LO12_NC', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TP, None, None, 12, -1, 0, 0, 1, 1],
    572: ['R_AARCH64_TLSLD_LDST128_DTPREL_LO12', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    573: ['R_AARCH64_TLSLD_LDST128_DTPREL_LO12_NC', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.TLS_ENTRY, '', BaseType.TLS, None, None, 12, -1, 0, 0, 1, 1],
    # 这里开始是动态重定位，随机化时不会遇到
    1024: ['R_AARCH64_COPY', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, None, 0, 0, 0, 1, 1],
    1025: ['R_AARCH64_GLOB_DAT', 'S + A', 'S', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, None, 0, 0, 0, 1, 1],
    1026: ['R_AARCH64_JUMP_SLOT', 'S + A', 'S', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, None, 0, 0, 0, 1, 1],
    1027: ['R_AARCH64_RELATIVE', 'Delta(S) + A', 'Delta(S)', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, None, 0, 0, 0, 1, 0],
    1028: ['R_AARCH64_TLS_DTPMOD64', 'LDM(S)', 'LDM(S)', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 64, 0, 0, 0, 1, 1],
    1029: ['R_AARCH64_TLS_DTPREL64', 'DTPREL(S+A)', 'DTPREL(S+A)', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 64, 0, 0, 0, 1, 1],
    1030: ['R_AARCH64_TLS_TPREL64', 'TPREL(S+A)', 'TPREL(S+A)', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 64, 0, 0, 0, 1, 1],
    1031: ['R_AARCH64_TLSDESC', 'TLSDESC(S+A)', 'TLSDESC(S+A)', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, None, 0, 0, 0, 1, 1],
    1032: ['R_AARCH64_IRELATIVE', 'Indirect(Delta(S) + A)', 'Indirect(Delta(S) + A)', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, None, 0, 0, 0, 1, 0],

    # 这里开始是自己补充的。
    # 由于一些指针在编译时解决因此不会分配给其elf_reloc_type. 所以bfd_reloc_type和elf_reloc_type是不对应的，这里要补充上
    2000: ['R_AARCH64_ABS8', 'S + A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 8], [[0, 8]], 8, 0, 1, 0, 0, 0]
}

# relocName, addressMode, targetDesc, targetType, baseDesc, baseType, mask, dooffset, size, nextNum, checkHigh, checkLow, neesShow
# mask就是[0, len]取数值而已， doffset就是[[0, len]], size，其他的都不要
# NOTE: 重定位中记录的BaseType并不完全准确，因为只包含3种基址，SYM基址蕴含在PC中，通过检查base_bbl_sym是否存在可以得知
x64_reloc_dict = {
    # 经典重定位(8,16,32,64的绝对寻址以及pc-relative寻址)
    1:  ['R_X86_64_64', 'S+A', 'S+A', TargetType.NORMAL, '', BaseType.NONE, [0, 64], [[0, 64]], 64, 0, 0, 0, 0, None], # Direct 64 bit
    10: ['R_X86_64_32', 'S+A', 'S+A', TargetType.NORMAL, '', BaseType.NONE, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # Direct 32 bit zero extended
    11: ['R_X86_64_32S', 'S+A', 'S+A', TargetType.NORMAL, '', BaseType.NONE, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # Direct 32 bit sign extended
    12: ['R_X86_64_16', 'S+A', 'S+A', TargetType.NORMAL, '', BaseType.NONE, [0, 16], [[0, 16]], 16, 0, 0, 0, 0, None], # Direct 16 bit zero extended
    14: ['R_X86_64_8', 'S+A', 'S', TargetType.NORMAL, '', BaseType.NONE, [0, 8], [[0, 8]], 8, 0, 0, 0, 0, None], # Direct 8 bit sign extended

    24: ['R_X86_64_PC64', 'S+A-P',  'S+A', TargetType.NORMAL, 'P', BaseType.PC, [0, 64], [[0, 64]], 64, 0, 0, 0, 0, None], # 64-bit PC relative
    2:  ['R_X86_64_PC32', 'S+A-P', 'S+A', TargetType.NORMAL, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # PC relative 32 bit signed
    39: ['R_X86_64_PC32_BND', 'S+A-P', 'S+A', TargetType.NORMAL, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # (Deprecated) PC relative 32 bit signed with BND prefix
    13: ['R_X86_64_PC16', 'S+A-P', 'S+A', TargetType.NORMAL, 'P', BaseType.PC, [0, 16], [[0, 16]], 16, 0, 0, 0, 0, None],# 16 bit sign extended pc relative
    15: ['R_X86_64_PC8', 'S+A-P', 'S+A', TargetType.NORMAL, 'P', BaseType.PC, [0, 8], [[0, 8]], 8, 0, 0, 0, 0, None], # 8 bit sign extended pc relative

    # 围绕GOT的有很多种用法：
    # 1. R_X86_64_GOTOFF64   sym@GOTOFF    base为_GOT_OFFSET_TABLE_，target为任意符号。    常见于pielarge编译选项下访问data或code的memory object
    # 2. R_X86_64_GOTPCREL   sym@GOTPCREL  base为PC，target为GOT Entry                   常见于普通编译选项希望用GOT的情况
    # 3. R_X86_64_GOT64      sym@GOT       base为_GOT_OFFSET_TABLE_，target为GOT Entry   常见于large编译选项下希望用GOT的情况
    # 4. R_X86_64_GOTPC64    base为PC，target为_GOT_OFFSET_TABLE_   非PIELarge下这样获取_GOT_OFFSET_TABLE_

    # 其他target为normal的
    25: ['R_X86_64_GOTOFF64', 'S+A-GOT', 'S+A', TargetType.NORMAL, 'GOT', BaseType.GOT, [0, 64], [[0, 64]], 64, 0, 0, 0, 0, None], # 基址为_GOT_OFFSET_TABLE_,target为非GOTEntry和非PLTEntry外的任意符号
    4:  ['R_X86_64_PLT32', 'L+A-P', 'L+A', TargetType.NORMAL, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # 32 bit .plt address 521.wrf_r中发现该重定位类型的指针仍指向已有函数而非重新定位到.plt节的跳板
    40: ['R_X86_64_PLT32_BND', 'L+A-P', 'L+A', TargetType.NORMAL, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # (Deprecated) 32 bit PLT address with BND prefix
    31: ['R_X86_64_PLTOFF64', 'L+A-GOT', 'L+A', TargetType.NORMAL, 'GOT', BaseType.GOT, [0, 64], [[0, 64]], 64, 0, 0, 0, 0, None], # 基址为_GOT_OFFSET_TABLE_,target为PLTEntry

    # target为got entry, 其基址有不同类型：sym@GOTPCREL这种以PC为基址，@GOT这种以_GOT_OFFSET_TABLE_为基址
    9:  ['R_X86_64_GOTPCREL', 'G+GOT+A-P', 'G+GOT+A', TargetType.GOT_ENTRY, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # foo@GOTPCREL(%rip) 32 bit signed PC relative offset to GOT
    41: ['R_X86_64_GOTPCRELX', 'G+GOT+A-P', 'G+GOT+A', TargetType.GOT_ENTRY, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # foo@GOTPCREL(%rip) 32 bit signed PC relative offset to GOT without REX prefix
    42: ['R_X86_64_REX_GOTPCRELX', 'G+GOT+A-P', 'G+GOT+A', TargetType.GOT_ENTRY, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # 32 bit signed PC relative offset to GOT with REX prefix
    28: ['R_X86_64_GOTPCREL64', 'G+GOT+A-P', 'G+GOT+A', TargetType.GOT_ENTRY, 'P', BaseType.PC, [0, 64], [[0, 64]], 64, 0, 0, 0, 0, None],  # foo@GOTPCREL(%rip) 64-bit PC relative offset to GOT entry
    3:  ['R_X86_64_GOT32', 'G+A', 'G+A', TargetType.GOT_ENTRY, '', BaseType.GOT, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # 32 bit GOT entry
    27: ['R_X86_64_GOT64', 'G+A-.got.plt', 'G+A', TargetType.GOT_ENTRY, '.got.plt', BaseType.GOT, [0, 64], [[0, 64]], 64, 0, 0, 0, 0, None], # foo@GOTPCREL(%rip) 基址为_GOT_OFFSET_TABLE_,target为GOTEntry
    30: ['R_X86_64_GOTPLT64', 'G+A', 'G+A', TargetType.GOT_ENTRY, '', BaseType.NONE, [0, 64], [[0, 64]], 64, 0, 0, 0, 0, None], # (Deprecated) Like GOT64
    26: ['R_X86_64_GOTPC32', 'GOT+A-P', 'GOT+A', TargetType.GOT_ENTRY, 'P', BaseType.PC,  [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # 32-bit PC relative offset to GOT
    29: ['R_X86_64_GOTPC64', 'GOT+A-P', 'GOT+A', TargetType.GOT_ENTRY, 'P', BaseType.PC,  [0, 64], [[0, 64]], 64, 0, 0, 0, 0, None], # 64-bit PC relative offset to GOT


    # target为tls var
    19: ['R_X86_64_TLSGD', 'GOT+G+A-P', 'GOT+G+A', TargetType.GOT_ENTRY, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None],  # 32 bit signed PC relative offset to two
    20: ['R_X86_64_TLSLD', 'GOT+G+A-P', 'GOT+G+A', TargetType.GOT_ENTRY, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None],  # 32 bit signed PC relative offset to two
    34: ['R_X86_64_GOTPC32_TLSDESC', 'GOT+G+A-P', 'GOT+G+A', TargetType.GOT_ENTRY, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # 32-bit PC relative to TLS descriptor in GOT
    35: ['R_X86_64_TLSDESC_CALL', 'GOT+G+A-P', 'GOT+G+A', TargetType.GOT_ENTRY, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # Relaxable call through TLS descriptor
    17: ['R_X86_64_DTPOFF64', '', '', TargetType.TLS_ENTRY, '', BaseType.TLS, [0, 64], [[0, 64]], 32, 0, 0, 0, 0, None],  # Offset in module TLS block
    21: ['R_X86_64_DTPOFF32', '', '', TargetType.TLS_ENTRY, '', BaseType.TLS, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None],  # Initial-exec. 将偏移记录在Got Entry中，以在运行时进行动态修复
    22: ['R_X86_64_GOTTPOFF', 'GOT+G+A-P', 'GOT+G+A', TargetType.GOT_ENTRY, 'P', BaseType.PC, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # 32 bit signed PC relative offset to GOT
    23: ['R_X86_64_TPOFF32', '', '', TargetType.TLS_ENTRY, '', BaseType.TLS, [0, 32], [[0, 32]], 32, 0, 0, 0, 0, None], # Local-exec 偏移可以确定，因此直接记录在指令中

    # 动态重定位中的RELATIVE和IRELATIVE
    37: ['R_X86_64_IRELATIVE', '', '', TargetType.NORMAL, '', BaseType.NONE, None, None, None, 0, 0, 0, 0, None], # Adjust indirectly by program base
    38: ['R_X86_64_RELATIVE64', '', '', TargetType.NORMAL, '', BaseType.NONE, None, None, None, 0, 0, 0, 0, None], # 64-bit adjust by program base
    8:  ['R_X86_64_RELATIVE', '', '', TargetType.NORMAL, '', BaseType.NONE, None, None, None, 0, 0, 0, 0, None], # Adjust by program base

    # 其他动态重定位。我们不修复动态重定位的指针，因为这些指针会在运行时候会被动态链接器重新覆盖。针对动态重定位的三种resolve方式，我们修改动态符号表和IRELATIVE/RELATIVE的add来处理此类问题
    5:  ['R_X86_64_COPY', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None], # Copy symbol at runtime
    6:  ['R_X86_64_GLOB_DAT', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None],  # Create GOT entry
    7:  ['R_X86_64_JUMP_SLOT', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None],  # Create PLT entry
    18: ['R_X86_64_TPOFF64', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None], # Offset in initial TLS block
    16: ['R_X86_64_DTPMOD64', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None], # ID of module containing symbol
    36: ['R_X86_64_TLSDESC', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None], # 2 by 64-bit TLS descriptor

    # gold2.36.1不支持的
    32: ['R_X86_64_SIZE32', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None], #
    33: ['R_X86_64_SIZE64', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None], #

    # gold2.36.1中不做处理，无实际意义的
    0:  ['R_X86_64_NONE', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None],  # No reloc
    250: ['R_X86_64_GNU_VTINHERIT', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None],  #
    251: ['R_X86_64_GNU_VTENTRY', '', '', TargetType.UNKNOWN, '', BaseType.UNKNOWN, None, None, 0, 0, 0, 0, 0, None],  #
}

relocDict = aarch64_reloc_dict



