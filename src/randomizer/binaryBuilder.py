# coding=utf-8
import os
import logging
import struct
import time

import unit
import util
import constants as C
from constants import Formats
from constants import PK
from reorderInfo import *
from unit import *
from bitarray import bitarray


# from capstone.x86_const import *

class BinaryBuilder():
    """
    该类按照随机化结果重写出变体程序
    """

    def __init__(self, EI, RE, oldBin, newBin, options):
        """
        初始化BinaryBuilder的一些成员变量
        """

        self.RE = RE
        self.EI = EI
        self.layout = EI.layout
        self.fixups = EI.fixups
        self.oldBin = oldBin
        self.newBin = newBin
        self.options = options
        self.dwarfParser = self.EI.dwarfParser
        self.elfParser = self.EI.elfParser

        # 二进制文件相关
        self.origBin = self.elfParser.bin  # Original Binary Dump
        self.instBin = 0            # Instrumented Binary
        self.sections = list()
        self.totalSec = 0
        self.secFixups = dict()

    def getOrderedSections(self):
        """
        确定origBin中的节顺序 (存放在self.updatedSections中)
        """
        ELF = self.elfParser.elf
        elfInfo = ELF._parse_elf_header()

        self.sections = []
        self.totalSec = ELF.num_sections()

        # 遍历所有的节， 创建unit.section对象，主要是获得name(.interp)、size(0x1c)、VA(0x400238)、start(0x238)、end(0x238+0x1c)
        for i in range(1, self.totalSec):
            sec = ELF.get_section(i)
            s = unit.Section()
            s.idx = i
            s.name = sec.name
            if sec.header["sh_flags"] & 4 == 4:
                s.isCodeSection = True
            else:
                s.isCodeSection = False

            # 这几个节分配size但在elf中不具有实体，
            if sec.header['sh_type'] == "SHT_NOBITS":
                continue
            if s.name == ".rand":  # gold更改rand节写入方案后，.rand节位于整个文件的最后而不在节数组中，因此将其排除
                continue

            s.sz = sec['sh_size']
            s.va = sec['sh_addr']
            s.sectionStart = sec['sh_offset']
            s.sectionEnd = s.sectionStart + s.sz

            if s.name in [C.SEC_TEXT]: # .text
                s.type = C.SecType.TEXT
            elif s.name in [C.SEC_REL_DYN, C.SEC_REL_PLT]: # .rela.dyn .rela.plt
                s.type = C.SecType.RELOC
            elif s.name in [C.SEC_DYNSYM, C.SEC_SYMTAB]: # .symtab .dynsym
                s.type = C.SecType.SYMBOL
            elif s.name in [C.SEC_EH_FRAME]: # .eh_frame
                s.type = C.SecType.EHFRAME
            elif s.name in [C.SEC_EH_FR_HDR]: # .eh_frame_hdr
                s.type = C.SecType.EHFRAMEHDR
            else:
                s.type = C.SecType.NORMAL

            self.sections.append(s)

        # section header table并不一定是按照地址顺序排列的，这里需要按照start重新排序，python的sorted是稳定排序，因此是tbss前 datal.rel.ro.local后
        self.sections = sorted(self.sections, key=lambda s: s.sectionStart)

        # Section.fileOffsetEnd其实指的是节包括填充的那一部分的末尾。
        # fileOffsetEnd = 下一个节的开头，因为sectionEnd并不一定包括填充的部分。 最后一个节的fileOffsetEnd是section header table的开头。
        self.sections[-1].fileOffsetEnd = elfInfo['e_shoff']
        for i in range(len(self.sections)-1):
            self.sections[i].next = self.sections[i+1]
            if self.sections[i].sectionEnd < self.sections[i+1].sectionStart:
                self.sections[i].fileOffsetEnd = self.sections[i+1].sectionStart
            elif self.sections[i].sectionEnd == self.sections[i+1].sectionStart:
                self.sections[i].fileOffsetEnd = self.sections[i].sectionEnd
            else:
                logging.warning("{}的offset+size={},其大于下一个节{}的开头{}\n".format(
                    self.sections[i].name, hex(self.sections[i].sectionEnd),
                    self.sections[i+1].name, hex(self.sections[i+1].sectionStart)))
                exit(1)

        # 剥离总Fixup到每个节中
        for sec in self.sections:
            self.secFixups[sec.idx] = list()
        for FI in self.fixups.FixupsLayout:
            self.secFixups[FI.sec].append(FI)
        # 记得给所有的fixups列表排序，我们收集的时候是不注意顺序的，但写binary的时候是以fixup切分code来写的。
        for sec in self.sections:
            self.secFixups[sec.idx] = sorted(self.secFixups[sec.idx], key=lambda FI: FI.offset)
        self.fixups.FixupsLayoutPrev = sorted(self.fixups.FixupsLayoutPrev, key=lambda FI: FI.offset)
        self.fixups.FixupsLayoutLast = sorted(self.fixups.FixupsLayoutLast, key=lambda FI: FI.offset)

    def getNewValue(self, oldVA):
        """
        位于随机化区域外部的，返回原地址
        位于随机化区域内部的，基于所在的FUN计算newValue
        """
        if not self.layout.isInReorderRange(oldVA):
            return oldVA

        Fun = self.layout.binarySearchFun(oldVA)
        return (oldVA - Fun.VA) + Fun.newVA

    def writeFile(self, temp):
        self.instBin += len(temp)
        self.fw.write(temp)

    def writePointer(self, FI=None, sectionData=None, pos=None, value=None, size=None, tag=None):
        """
        根据架构、指针类型选择合适的指针写入函数
        """

        # 处理非FI的情况，直接小端字节序转换value后写入即可
        if value!=None and size!=None:
            try:
                if tag: # 有符号数值
                    bytes = struct.pack(C.getSignedFormat(size/8), value)
                else: # 无符号数值
                    bytes = struct.pack(C.getUnsignedFormat(size/8), value)
                self.writeFile(bytes)
            except:
                exit("发生溢出")
            return int(size/8)

        # 处理FI的情况
        if self.options.arch == C.ARM64:
            if FI.isCodePointer:
                return self.writeARMCodePointer(FI, sectionData, pos)
            else:
                return self.writeDataPointer(FI)
        else:
            return self.writeDataPointer(FI)

    def writeARMCodePointer(self, FI, sectionData, pos):
        """
        专门为ARMCodePointer这种小端字节序+小端比特序设计的指针写入函数
        """

        # Step 1. 根据最大的dooffset，在节中预取超过该长度的字节序列。
        byteSeqInst = sectionData[pos: pos + 4]
        bitSeqInst = bitarray(endian='little')
        bitSeqInst.frombytes(byteSeqInst)

        # Step 2. 取bitSeqIMM，在不变时时直接用当时所取的，在变化时从newValue中根据mask取出来
        if not FI.baseInRand and not FI.targetInRand:
            bitIMM = FI.bitIMM
        else:
            if FI.isRela:
                byteSeqX = struct.pack("<q", FI.newValue)
            else:
                byteSeqX = struct.pack("<Q", FI.newValue)
            bitX = bitarray(endian='little')
            bitX.frombytes(byteSeqX)
            bitIMM = bitX[FI.mask[0] : FI.mask[1]]

        # Step 3. 处理mask的和doffset的不一致情况，需要低位扩展0
        # 比如'R_AARCH64_LD64_GOT_LO12_NC或R_AARCH64_LDST64_ABS_LO12_NC这种，mask为[3, 12],因此imm为9位，但doffset为12位
        # 从AArch64 ELF文档中可以看到，LDST8_ABS_LO12的mask是[2,12]，LDST16_ABS_LO12的mask是[1,12]，LDST32_ABS_LO12的mask是[2,12]，
        # LDST64_ABS_LO12的mask是[3,12]，LDST128_ABS_LO12的mask是[4,12]，所以猜测是要对bitIMM低位补0。之前应该是写错了
        # 此时将多余的预留空间置0吧，好像都是无符号数直接用0扩展就行
        lengthOffset = 0
        for offset in FI.doffsets:
            lengthOffset += offset[1]-offset[0]
        lengthIMM = len(bitIMM)
        for i in range(lengthOffset-lengthIMM):
            bitIMM.insert(0, False)

        # Step 4. 按照doffset填充bitSeqIMM到指令中去，
        indexIMM = 0
        # print(FI.idx)
        for doffset in FI.doffsets:
            for indexInst in range(doffset[0], doffset[1]):
                # print("{} {}".format(indexInst, indexIMM))

                bitSeqInst[indexInst] = bitIMM[indexIMM]
                indexIMM += 1

        # Step 5. 将四字节指令写入到二进制文件中
        self.writeFile(bitSeqInst.tobytes())
        return 4

    def writeDataPointer(self, FI):
        """
        为小端字节序+大端bit序列设计的写入函数，适用于ARM的数据段指针以及x64的所有指针
        """

        # 在指针不变时时直接用当时所取的原封填入
        if not FI.baseInRand and not FI.targetInRand:
            bitIMM = FI.bitIMM
            self.writeFile(bitIMM.tobytes())

        # 在指针变化时从newValue计算出对应的bytes。因为data下的指针都是byte粒度的，因此直接从newValue转到bytes即可
        else:
            if FI.isRela:
                bytes = struct.pack(C.getSignedFormat(FI.derefSz/8), FI.newValue)
            else:
                bytes = struct.pack(C.getUnsignedFormat(FI.derefSz/8), FI.newValue)
            self.writeFile(bytes)

        return int(FI.derefSz/8)

    def patchTextSection(self, sectionChunk):

        # 1. 随机化前的部分 因为main函数也作为一个Fixup收录了，所以不需要分三段，也不需要根据前一个字节来猜是相对地址还是绝对地址了
        pos = 0
        # logging.info("instBin={}".format(hex(self.instBin-0x2740+self.EI.layout.textVA)))
        for FI in self.fixups.FixupsLayoutPrev:
            self.writeFile(sectionChunk[pos:FI.offset])
            pos = FI.offset
            pos += self.writePointer(FI, sectionChunk, pos)

        self.writeFile(sectionChunk[pos:self.layout.randomOffset])
        pos = self.layout.randomOffset

        # 2. 随机化的代码部分，开始的pos为reorderObjStartFromText，按照随机化后FUN的顺序来填充
        # logging.info("instBin={}".format(hex(self.instBin-0x2740+self.EI.layout.textVA)))
        textBar = util.ProgressBar(len(self.RE.randomizedFunContainer))
        for F in self.RE.randomizedFunContainer:
            FUNcode = sectionChunk[F.offset:F.offset + F.size]
            fixupsLayout = sorted(F.fixups, key=lambda F: F.offset)

            pos = 0
            for FI in fixupsLayout:
                # 填充一段非fixup的 0-10
                self.writeFile(FUNcode[pos : FI.offset - F.offset]) # Fixup在FUN内的偏移，使用以前的offset计算就可以
                # print("{} {}".format(hex(F.VA+pos), util.bytes2Str(FUNcode[pos : FI.offset - F.offset])))
                # time.sleep(0.1)
                pos = FI.offset - F.offset
                # 再填充上fixup 10-18    refVal是newRefVal
                pos += self.writePointer(FI, FUNcode, pos)

            self.writeFile(FUNcode[pos:])
            pos += len(FUNcode[pos:])

            textBar += 1
        textBar.finish()

        # 3. 随机化后的部分，可能仍存在Fixup，不知道cfi是不是也在这一部分。
        '''
        Only when for -cfi-icall option has been enabled (implementation-specific)
        Other CFI options for LLVM do not contain any orphan point observed yet.
            1) cfi_icall:          CFI for indirect calls
            2) cfi_vcall:          CFI for virtual function calls
            3) cfi_nvcall:         CFI for calling non-virtual member functions
            4) cfi_unrelated_cast: CFI for the casts between objects of unrelated types
            5) cfi_derived_cast:   CFI for the casts between a base and a derived class
            6) cfi_cast_strict:    specific instance where 5) would not catch an illegal cast
        '''
        # logging.info("instBin={} randomEndVA={}".format(hex(self.instBin-0x2740+self.EI.layout.textVA), hex(self.layout.randomEndVA)))
        pos = self.layout.randomEndVA - self.layout.textVA
        for FI in self.fixups.FixupsLayoutLast:
            self.writeFile(sectionChunk[pos:FI.offset])
            pos = FI.offset
            pos += self.writePointer(FI, sectionChunk, pos)
        self.writeFile(sectionChunk[pos:])

    def patchNormalSection(self, sectionChunk, fixups, isCodeSection):
        pos = 0
        if fixups:
            dataBar = util.ProgressBar(len(fixups))
            fixups = sorted(fixups, key=lambda F: F.offset)

            for FI in fixups:
                self.writeFile(sectionChunk[pos:FI.offset])
                pos = FI.offset
                if isCodeSection:
                    pos += self.writePointer(FI, sectionChunk, pos)
                else:
                    pos += self.writePointer(FI)
                dataBar += 1
            dataBar.finish()

        self.writeFile(sectionChunk[pos:])


    def patchRelocationSection(self, secName, sectionChunk):
        """
        r_offset  8  需要重定位的指针在该节的偏移
        r_info    8
            - 前4字节 符号表中的index
            - 后4字节 重定位的类型
        r_addend  8  加数

        程序的动态重定位表同样需要修正
            - Offset   如果该指针位于随机化区域中的话，指针位置可能发生改变
            - Sym      保持不变
            - Addend   考虑以下几种情况：
                - Case1. 表示数组内偏移.           保持不变
                - Case2. 表示节到符号的偏移.       重新指向正确的IFUN
                - Case3. RELATIVE下直接指向IFUN.  重新指向正确的IFUN

        Case1.
        这是最常见的，比如plt节就使用该重定位在运行时确定自己想要的函数的VA
        此时，我们只要保证dyn.sym的符号是修复的就行

        重定位节 '.rela.plt' at offset 0x598 contains 6 entries:
            偏移量                类型                  符号名称 + 加数
        0000000000020000 R_AARCH64_JUMP_SLOT    __libc_start_main@GLIBC_2.17 + 0
        0000000000020008 R_AARCH64_JUMP_SLOT    abort@GLIBC_2.17 + 0

        Case2.
        这在ASLR的程序中很常见。在开启ASLR时，代码段会改用相对地址，而数据段仍然使用绝对地址，
        此时这些地址就会在运行时机制确定后，加上这个偏移
        此时，我们只要保证这些RVA指向了正确的位置就行

        重定位节 '.rela.dyn' at offset 0x490 contains 11 entries:
            偏移量                类型           符号名称 + 加数
        000000000001fd90   R_AARCH64_RELATIVE        7c8
        000000000001fd98   R_AARCH64_RELATIVE        780

        Case3.
        这在使用了ifunc的程序中可以见到。ifunc本质是一个选择函数，动态链接器会调用该函数
        来确定一个指针到底应该填哪个值。注意该特性只在glibc中被部分使用过。
        此时，我们只要确保这个ifunc函数指向了正确的RVA就行

        Relocation section '.rela.plt' at offset 0x1d8 contains 21 entries:
          Offset         Type              Sym. Name + Addend
        00000069c018  R_X86_64_IRELATIV        416060

        0000000000416060 <strcpy_ifunc>:
          416060:       f6 05 05 8d 28 00 10    testb  $0x10,0x288d05(%rip)        # 69ed6c <_dl_x86_cpu_features+0x4c>
          416067:       75 27                   jne    416090 <strcpy_ifunc+0x30>
          416069:       f6 05 c1 8c 28 00 02    testb  $0x2,0x288cc1(%rip)
        """

        def _get_reloc_entries(r):
            return r['r_offset'], r['r_addend'], r['r_info_type'], r['r_info_sym']

        reloc = self.elfParser.elf.get_section_by_name(secName)
        assert (len(sectionChunk) % reloc.num_relocations() == 0)

        bars = util.ProgressBar(reloc.data_size / reloc.entry_size)
        pos = 0
        for rel in reloc.iter_relocations():
            bars += 1
            offset, addend, type, sym = _get_reloc_entries(rel)

            # 更新offset
            newOffset = self.getNewValue(offset)
            self.writePointer(value=newOffset, size=64, tag=0)

            # 写入type和sym下标
            self.writeFile(PK(Formats.UINT, type))
            self.writeFile(PK(Formats.UINT, sym))

            # 更新加数
            if (self.options.arch == C.ARM64 and type in [1027, 1032]) or (self.options.arch == C.X64 and type in [8, 37, 38]):
                addend = self.getNewValue(addend)
            self.writePointer(value=addend, size=64, tag=1)

            # 更新pos
            pos += 24
        bars.finish()

        # 看到cangjie应该是对plt节有填充的，所以重定位节并不一定严格是24的倍数
        self.writeFile(sectionChunk[pos:])


    def patchSymbolTable(self, secName, sectionChunk):
        """ Patches all symbol values after randomization for '.dynsym' and '.symtab' section
        Num:    Value          Size   Type     Bind   Vis      Ndx    Name
        0: 0000000000000000     0   NOTYPE   LOCAL  DEFAULT  UND
        1: 0000000000000000     0   FILE     LOCAL  DEFAULT  ABS   crtstuff.c
        2: 0000000000402da8     0   OBJECT   LOCAL  DEFAULT   18   __JCR_LIST__
        3: 0000000000403060     0   OBJECT   LOCAL  DEFAULT   25   __TMC_LIST__
        4: 0000000000400970     0   FUNC     LOCAL  DEFAULT   12   deregister_tm_clones
        5: 00000000004009b0     0   FUNC     LOCAL  DEFAULT   12   register_tm_clones
        6: 00000000004009f0     0   FUNC     LOCAL  DEFAULT   12   __do_global_dtors_aux

        typedef struct {
            Elf32_Word st_name;
            Elf32_Addr st_value;
            Elf32_Word st_size;
            unsigned char st_info;
            unsigned char st_other;
            Elf32_Half st_shndx;
        } Elf32_Sym;

        sym_name   4  符号的名字。在.strtab中的第几个字节(不是第几个符号)
        sym_info   1
            - symbol_bind(前4bit) LOCAL-0 GLOBAL-1 WEAK-2 ...
            - symbol_type(后4bit) OBJECT-1 FUNC-2 SECTION-3 FILE-4
        sym_other  1  该属性目前未使用，一律为0
        sym_shndx  2  对于节名符号来说，就是节号
        sym_value  8  符号的地址。节名符号的地址、函数符号的地址等等
        sym_size   8  对于函数符号来说，就是函数的大小
        """

        symbolTable = self.elfParser.elf.get_section_by_name(secName)
        assert(len(sectionChunk) % symbolTable.num_symbols() == 0)
        symbolBar = util.ProgressBar(symbolTable.num_symbols())

        patchCtr = 0
        symOffset = 0

        for symbol in symbolTable.iter_symbols():
            """
            前8个字节代表name, info, orther, shndx四个属性，是不变的。
            symbol['st_info']['type'], symbol['st_info']['bind'], symbol['st_other']['visibility'], symbol['st_shndx']
            """
            symProperty = sectionChunk[symOffset:symOffset + 8]
            self.writeFile(symProperty)

            """
            后16个字节为 8字节的value + 8字节的size
            """
            # 遍历符号表的Value，如果符号地址位于随机化范围内，则更新value
            symVal, symSz = symbol['st_value'], symbol['st_size']
            if self.layout.isInReorderRange(symVal):
                try:
                    newSymVal = self.getNewValue(symVal)
                    self.writePointer(value=newSymVal, size=64, tag=0)
                    self.writeFile(PK(Formats.LONG, symSz))
                    patchCtr += 1
                except AttributeError:
                    self.writeFile(PK(Formats.LONG, symVal))
                    logging.warning(" [%s] Failed to update the symbol: 0x%x " % (secName, symVal))
            else:
                # 如果符号的Value没有处在随机化范围中，不需要改变的话，将value、size两个8字节数据原封不动的填入。
                self.writeFile(PK(Formats.LONG, symVal))
                self.writeFile(PK(Formats.LONG, symSz))

            # Each entry for a symbol is 24B in size; Move on the next entry
            symOffset += 24
            symbolBar += 1

        symbolBar.finish()


    def patchEhframe(self, secName, sectionChunk):
        """
        除了按照基本编码格式提取出以下结构体中的字段，但除了lsda外没有做更进一步的解析,包括以下字段：
        - CIE.augmentation_string指导解释CIE.augmentation_data和FDE.augmentation_data字段，比如personality和lsda指针
          _parse_cie_augmentation()  _parse_lsda_pointer()
        - CIE.initial_instructions和FDE.instructions  在_parse_instructions()中解析

        Common Information Entry (CIE)
        - length(unit32 4B 0:4)
        - Extended Length(unit64 8B) optional
        - CIE_id(unit32 4B 4:8): 常数0。该字段用于区分CIE和FDE，在FDE中该字段非0，为CIE_pointer
        - version(unit8 1B 8): 常数1
        - augmentation_string(string):
            描述CIE/FDE参数列表的字串。
            P字符表示personality routine指针；
            L字符表示FDE的augmentation data存储了language-specific data area (LSDA)
        - address_size: 一般为4或8
        - segment_selector_size: for x86
        - code_alignment_factor: 假设指令长度都是2或4的倍数(用于RISC)，影响DW_CFA_advance_loc等的参数的乘数
        - data_alignment_factor: 影响DW_CFA_offset DW_CFA_val_offset等的参数的乘数
        - return_address_register
        - augmentation_data_length
        - augmentation_data:  如果CIE的augmentation_string包含P字符，则这里记录personality routine的指针，会在c++ exception的两轮Phase中用到
        - initial_instructions context保存相关的的指令
        - padding

        Frame Description Entry (FDE)
        - length(unit32 4B 0:4): FDE自身长度。
        - Extended Length(unit64) optional
        - CIE_pointer(uint32 4B 4:8): 父类CIE的地址。计算公式：eh_frame.VA+pos+8(该位置VA) + (-1227) = 0x400600
        - initial_location(uint32 4B 8:12): 该FDE对应的地址 计算公式：eh_frame.VA+pos+8(该位置VA) + (-1227) = 0x400600
        - address_range(uint32 4B 12:16): 该FDE的size，因此initial_location和address_range共同描述了一个地址区间
        - instructions: context保存相关的的指令
        - augmentation_data_length
        - augmentation_data:    如果CIE的augmentation_string包含L字符，这里会记录language-specific data area，会在.gcc_exception_table中用到
        - padding
        """
        entryPos = 0
        for entry in self.dwarfParser.entryList:
            if isinstance(entry, CIE):
                # CIE无需修改，直接写入即可
                self.writeFile(entry.bytes)
                entryPos += len(entry.bytes)
                #print("origLength=%s newLength=%s entryPos=%s" % (hex(len(entry.bytes)), hex(len(entry.bytes)), hex(entryPos)))
            else:
                # FDE需要修改initial_location后写入
                if self.layout.isInReorderRange(entry.initial_location): # 如果指向的函数位于随机化区域的话，定位到该BBL，并获得新地址
                    newInitial_location = self.getNewValue(entry.initial_location)

                    value, valueLength = self.dwarfParser.encode_value(
                        entry.FDEFormat, entry.FDEMode, newInitial_location, self.dwarfParser.eh_frameVA+entryPos+entry.initial_location_range[0], 0
                    )
                    self.writeFile(entry.bytes[:entry.initial_location_range[0]])
                    self.writeFile(value)
                    self.writeFile(entry.bytes[entry.initial_location_range[0]+valueLength:])
                    entryPos += len(entry.bytes) + (valueLength - (entry.initial_location_range[1]-entry.initial_location_range[0]))
                    # print("origLength=%s newLength=%s entryPos=%s" % (hex(len(entry.bytes)),
                    #                                       hex(len(entry.bytes) + (valueLength - (entry.initial_location_range[1]-entry.initial_location_range[0]))),
                    #                                       hex(entryPos)))
                else:
                    self.writeFile(entry.bytes)
                    entryPos += len(entry.bytes)
                    #print("origLength=%s newLength=%s entryPos=%s" % (hex(len(entry.bytes)), hex(len(entry.bytes)), hex(entryPos)))

        # 尾部会有空FDE作为ZERO Terminal，一般为4个字节
        self.writeFile(sectionChunk[entryPos:])


    # 注意：eh_frame_hdr要求随机化是以Frame为单位的，不然随机化后的对象无法再用Frame来表示。
    # 一般情况下这是满足的，因为frame对应单个函数。
    # 同时要注意，eh_frame机制和完全随机的BBL序列是不兼容的，因为完全的BBL随机时Frame也被拆分为了多个不连续的部分，目前的frame机制无法表示，
    # 也就是完全随机化后的代码因为找不到正确的FDE而进行了错误的unwind
    def patchEhframeHdr(self, secName, sectionChunk):
        """
        .eh_frame_hdr
            Contains a table of pairs(initial location, ptr to the FDE in .eh_frame)
        Attributes in order
            Encoding	    Field
            unsigned byte	version
            unsigned byte	eh_frame_ptr_enc
            unsigned byte	fde_count_enc
            unsigned byte	table_enc
            encoded	        eh_frame_ptr
            encoded	        fde_count
                            binary search table
                            <initialLoc(targetFun), targetFDE>

        References
            https://refspecs.linuxfoundation.org/LSB_1.3.0/gLSB/gLSB/ehframehdr.html
        """

        # Step1: 先解析.eh_frame_hdr节
        ver = self.dwarfParser.ULInt8_decode(sectionChunk, 0)
        eh_frame_ptrFormat, eh_frame_ptrMode = self.dwarfParser.format_enc(sectionChunk[1])
        fde_countFormat, fde_countMode = self.dwarfParser.format_enc(sectionChunk[2])
        tableFormat, tableMode = self.dwarfParser.format_enc(sectionChunk[3])
        # fde_count_enc字段为0xff表示不存在二进制搜索表，此时就无需patch该节了
        if fde_countFormat == self.dwarfParser.DW_EH_PE_omit:
            self.writeFile(sectionChunk)
            return

        eh_frame_ptr, index = self.dwarfParser.decode_value(eh_frame_ptrFormat, eh_frame_ptrMode, sectionChunk, 4, self.dwarfParser.eh_frame_hdrVA+4, 0)
        fde_count, index = self.dwarfParser.decode_value(fde_countFormat, fde_countMode, sectionChunk, index, self.dwarfParser.eh_frame_hdrVA+index, 0)
        binarySearchTablePos = index

        binarySearchTable = []
        for _ in range(fde_count):
            initialLoc, index = self.dwarfParser.decode_value(tableFormat, tableMode, sectionChunk, index, self.dwarfParser.eh_frame_hdrVA+index, 0)
            targetFDE, index = self.dwarfParser.decode_value(tableFormat, tableMode, sectionChunk, index, self.dwarfParser.eh_frame_hdrVA+index, 0)

            if self.layout.isInReorderRange(initialLoc):
                if initialLoc not in self.layout.lookupByVA:
                    logging.error("FDE initialLoc位于随机化范围内，但其不属于任何函数")
                    exit(3)
                newinitialLoc = self.getNewValue(initialLoc)
                binarySearchTable.append((newinitialLoc, targetFDE))
            else:
                binarySearchTable.append((initialLoc, targetFDE))

        # Step2: 重写该节，注意binary search table要求按照frame边界的顺序来写入，以便于进行二分法搜索
        self.writeFile(sectionChunk[:binarySearchTablePos])
        binarySearchTable = sorted(binarySearchTable, key=lambda x: x[0])
        for initialLoc, targetFDE in binarySearchTable:
            initialLocBytes, len = self.dwarfParser.encode_value(tableFormat, tableMode, initialLoc, binarySearchTablePos, 0)
            binarySearchTablePos += len
            targetFDEBytes, len = self.dwarfParser.encode_value(tableFormat, tableMode, targetFDE, binarySearchTablePos, 0)
            binarySearchTablePos += len
            self.writeFile(initialLocBytes)
            self.writeFile(targetFDEBytes)

        self.writeFile(sectionChunk[binarySearchTablePos:]) # binary search table后面应该没有数据了


    def handleBin(self):
        """
        这些额外的操作包括:
        长度校验  替换text节  修改可执行权限  删除rand节  调试模式下写_rand _layout _disam _shuffled_disam _rand这几个文件
        """

        assert (len(self.origBin) == self.instBin), \
            "Mismatch the instrumented binary in size!\n Orig: 0x%04x, Inst: 0x%04x" \
            % (len(self.origBin), self.instBin)

        # 修改可执行权限
        os.chmod(self.newBin, 0o755)

        # 删除objcopy提取出的rand样本
        if self.options.arch == C.ARM64:
            OBJCOPY = 'aarch64-linux-gnu-objcopy'
        else:
            OBJCOPY = 'objcopy'
        removeSecCmd = '%s --remove-section .rand %s' % (OBJCOPY, self.newBin)
        os.system(removeSecCmd)

        # 调试模式下写一些文件
        if self.options.debug:
            # 写bbl的map文件，用于调试时找到对应的代码
            logging.info("写layout文件")
            fw = open(self.newBin + ".layout", "w")
            for F in self.RE.randomizedFunContainer:
                fw.write(F.getWrittenFun()+ '\n')
            fw.flush()
            fw.close()

            # 将反汇编结果写到文件中
            logging.info("写原程序的反汇编文件")
            disasm_path = self.oldBin + ".disasm"
            fw = open(disasm_path, "w")
            if self.options.arch == C.ARM64:
                fw.write(os.popen("aarch64-linux-gnu-objdump -d {} > {}".format(self.oldBin, disasm_path)).read())
            elif self.options.arch == C.X64:
                fw.write(os.popen("objdump -d {} > {}".format(self.oldBin, disasm_path)).read())
            fw.flush()
            fw.close()

            logging.info("写变体程序的反汇编文件")
            disasm_path = self.newBin + ".disasm"
            fw = open(disasm_path, "w")
            if self.options.arch == C.ARM64:
                fw.write(os.popen("aarch64-linux-gnu-objdump -d {} > {}".format(self.newBin, disasm_path)).read())
            elif self.options.arch == C.X64:
                fw.write(os.popen("objdump -d {} > {}".format(self.newBin, disasm_path)).read())
            fw.flush()
            fw.close()

            # 将rand写到文件中
            rand_path = self.oldBin + ".rand"
            os.system("reader-np.sh %s > %s" % (self.oldBin, rand_path))

    def instrumentBin(self):
        """
        重构变体程序：写elf头，写实体节，写elf尾
        """

        self.fw = open(self.newBin, 'wb')
        elfInfo = self.elfParser.elf._parse_elf_header()

        # 为所有节初始化unit.Section，包括完成以下几项重要的工作
        # 1. 确定sec的边界，其中节头取自sh_addr，节尾取自下一个节
        # 2. 确定sec.type，以方便后面根据type确定节的修复方式
        # 3. 剥离出属于该节的fixup
        # 4. 节可能并非顺序的，因此按照sec.sectionStart来重排序self.sections
        self.getOrderedSections()

        # 开启alltext时候需要修改entry_point
        if self.options.alltext:
            _startVA = struct.unpack("<Q", self.origBin[24:32])[0]
            _startNewVA = self.getNewValue(_startVA)
            self.origBin = self.origBin[:24] + struct.pack("<Q", _startNewVA) + self.origBin[32:]

        # 写elf文件头，段表，以及部分无需修改的节
        self.writeFile(self.origBin[:self.sections[0].sectionStart])

        for sec in self.sections:
            """
            原方案采用sectionStart, fileOffsetEnd来确定一个section的边界，但考虑到可能存在bss段有size但并不占实际体积，
            总之就是size不一定能反应该section在文件中占用的大小。
            因此现在使用两个节的Off差来做为节的大小
                  Name              Type            Address          Off    Size   ES Flg Lk Inf Al
            [18] .tbss             NOBITS          0000000001c35cc0 1834cc0 000024 00 WAT  0   0  8
            [19] .jcr              PROGBITS        0000000001c35cc0 1834cc0 000008 00  WA  0   0  8

            [27] .bss              NOBITS          0000000001c41c60 1840c50 156450 00  WA  0   0 32
            [28] .comment          PROGBITS        0000000000000000 1840c50 000063 01  MS  0   0  1
            """
            secName = sec.name
            start = sec.sectionStart
            end = sec.fileOffsetEnd
            sectionChunk = self.origBin[start:end]
            fixups = self.secFixups[sec.idx]

            logging.info("\tProcessing section [%s]" % (secName))
            # 根据sectionType选择相应的Patch方式
            if sec.type == C.SecType.NORMAL:
                self.patchNormalSection(sectionChunk, fixups, sec.isCodeSection)
            elif sec.type == C.SecType.SYMBOL:
                self.patchSymbolTable(secName, sectionChunk)
            elif sec.type == C.SecType.EHFRAME:
                self.patchEhframe(secName, sectionChunk)
            elif sec.type == C.SecType.EHFRAMEHDR:
                self.patchEhframeHdr(secName, sectionChunk)
            elif sec.type == C.SecType.RELOC:
                self.patchRelocationSection(secName, sectionChunk)
            elif sec.type == C.SecType.TEXT:
                self.patchTextSection(sectionChunk)
            else:
                logging.error("sec.type不合法 "+str(sec.type))
                exit(3)

            logging.debug("[0x%04x:0x%04x] Sz:%5dB InstBinSz:%5dB (%s)" % \
                          (sec.sectionStart, sec.fileOffsetEnd, sec.fileOffsetEnd - sec.sectionStart, self.instBin, secName))

            assert (end == self.instBin), \
                "Size Mismatch (%s): end=0x%04x instBin: 0x%04x" % \
                (secName, end, self.instBin)

        # Step3. 写入节表
        pos = elfInfo['e_shoff']
        shSz = elfInfo['e_shentsize']
        textIdx = self.elfParser.getSectionIdx(".text")
        textStartVA = self.elfParser.getSectionVA(".text")
        nextStartVA = self.elfParser.getNextSectionRange(".text")[0]
        for i in range(elfInfo['e_shnum']):
            sh = self.origBin[pos : pos+shSz]
            # 在随机化整个text节时，需要将text与fini间的padding作为text节长度，不然objcopy会将这几个字节置为0
            if i == textIdx and self.options.alltext:
                self.writeFile(sh[:32])
                self.writeFile(struct.pack("<Q", nextStartVA-textStartVA))
                self.writeFile(sh[40:])
            else:
                self.writeFile(sh)
            pos += shSz

        # Step4. 写入程序尾部的rand节
        self.writeFile(self.origBin[pos:])

        self.fw.close()

        # Step. 现在文件已经写完了，对变体程序作一些额外的处理
        self.handleBin()

