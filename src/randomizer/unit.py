# coding=utf-8
import logging

import constants as C
import shuffleInfo_pb2 as NP
from capstone import *
from capstone.x86_const import *
from capstone.arm_const import *
from capstone.arm64_const import *
import os
import elfParser
from elftools.dwarf.structs import DWARFStructs
from elftools.construct import Struct, Switch
from elftools.common.py3compat import iterbytes
from elftools.common.py3compat import BytesIO
from elftools.dwarf.callframe import CallFrameInfo
import leb128
from bitarray import bitarray
import struct
import util
import re
from pointerAnalysis.capStr import *

class FixedMetadata():
    class DIC:
        def __init__(self, pendingBytes, start, end):
            self.pendingBytes = pendingBytes
            self.start = start
            self.end = end

    class CMC:
        def __init__(self, pendingBytes, start, end, disassStr):
            self.pendingBytes = pendingBytes
            self.start = start
            self.end = end
            self.disassStr = disassStr

    class FixedFun:
        def __init__(self, info, insts, offset, section, isTemp):
            self.info = info
            self.insts = insts
            self.offset = offset
            self.section = section
            self.isTemp = isTemp

    def __init__(self, metadata, _elfParser, arch, fast=False):
        self.metadata = metadata
        self.elfParser = _elfParser
        self.arch = arch
        self.fast = fast
        self.funs = list()
        self.tempFuns = list()
        self.fixups = list()
        self.otherfixups = list()
        self.goldinfo = metadata.goldinfo

        self.n_funs = len(metadata.funs)
        if self.n_funs == 0:
            logging.error("该元数据中没有fun，请排查该问题")
            exit(1)

        self.n_fixups = len(metadata.fixups)
        for fixup in metadata.fixups:
            self.fixups.append(fixup)
        self.n_othefixups = len(metadata.otherfixups)
        for fixup in metadata.otherfixups:
            self.otherfixups.append(fixup)

        self.n_allfixups = self.n_fixups + self.n_othefixups
        self.allfixups = list()
        for fixup in self.metadata.fixups:
            self.allfixups.append(fixup)
        for fixup in self.metadata.otherfixups:
            self.allfixups.append(fixup)

        if self.arch == C.X64:
            self.md = Cs(CS_ARCH_X86, CS_MODE_64)
            self.md.detail = True
        else:
            self.md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
            self.md.detail = True

        # 解析.eh_frame和.gcc_except_table节
        logging.info("      解析eh_frame节和gcc_except_table节...")
        self.dwarfParser = DWarfParser(self.elfParser.fn, self.elfParser.elf)
        self.dwarfParser.parse_eh_frame()
        self.dwarfParser.parseLSDA()

        self.textIdx = self.elfParser.section_index[".text"]
        self.textVA, self.textEnd = self.elfParser.section_ranges[".text"]
        self.textContent = self.elfParser.elf.get_section_by_name(C.SEC_TEXT).data()

        self.DatainCode = list()
        self.codeMisCollection = list()

        # 初始化RecursiveDisass
        self.recursiveDisass = None

        logging.info("      校验中...")
        if self.fast:
            self.fastCheck()
        else:
            self.recursiveDisass = RecursiveDisass(fixedMetadata=self, show=False)
            self.slowCheck()


    @classmethod
    def fixedMetadataFactory(self, elfPath, fast=False):
        if not os.path.exists(elfPath):
            return 1, "  要解析的ELF({})不存在".format(elfPath)
        _elfParser = elfParser.ELFParser(elfPath)

        # 判断架构类型
        arch_retu = os.popen("readelf -hW {}".format(elfPath)).read()
        if "AArch64" in arch_retu:
            arch = C.ARM64
        elif "X86-64" in arch_retu:
            arch = C.X64
        else:
            return 1, "  ELF({})架构类型未知".format(elfPath)

        # 提取元数据
        if ".rand" not in _elfParser.section_ranges:
            return 1, "  ELF({})中不存在rand节".format(elfPath)
        randStart = _elfParser.section_offset['.rand'][0]
        randSize = _elfParser.section_offset['.rand'][1]
        fr = open(elfPath, "rb")
        fr.seek(randStart, 0)
        randBytes = fr.read(randSize)
        fr.close()

        # 反序列化元数据
        metadata = NP.Metadata()
        metadata.ParseFromString(randBytes)

        # 检查并修复元数据
        fixedMetadata = FixedMetadata(metadata, _elfParser, arch, fast)
        return 0, fixedMetadata

    def fastCheck(self):
        """
        Layout校验
            - 是否所有函数都位于.text节
        """

        for fun_idx, fun in enumerate(self.metadata.funs):
            self.funs.append(fun)

            # Check 1. 检查layout中的所有fun是否都位于.text节
            if fun.section != self.textIdx:
                print("Fun ({}) 的section并非.text，而是{}{}，请排查该问题".format(fun.info, str(fun.section), self.elfParser.section_name[fun.section]))
                exit(0x1)

    def slowCheck(self):
        """
        Summary: 该函数在ps-vs-np比对、随机化、二进制分析工具比对这三部分中都应该被调用
            Layout校验
                - 是否所有函数都位于.text节
                - 是否存在至少一个函数，以及每个函数中至少存在一条指令
                - 记录存在的data in code，
                - 记录存在的code mis-collection，并将其弥补到fun.insts中去(这使我们不得不用list替换掉原有的funProto.insts)
            Fixup校验
                - pass
        """

        lastInstVA = None
        lastInstSZ = None
        lastFun = None
        for fun_idx, fun in enumerate(self.metadata.funs):
            # print(fun.info)

            # Check 1. 检查layout中的所有fun是否都位于.text节
            if fun.section != self.textIdx:
                print("Fun ({}) 的section并非.text，而是{}{}，请排查该问题".format(fun.info, str(fun.section), self.elfParser.section_name[fun.section]))
                exit(0x1)

            funVA = self.textVA + fun.offset

            # Check 2. 向上检查上一轮次函数尾部是否存在pendingBytes (首函数和np-temp都无需进行此次检查)
            if lastInstVA != None and lastInstVA+lastInstSZ != funVA:
                lastInstBytes = self.textContent[lastInstVA - self.textVA: lastInstVA + lastInstSZ - self.textVA]
                pendingBytes = self.textContent[lastInstVA + lastInstSZ - self.textVA: funVA - self.textVA]
                self.handlePendingBytes(lastFun.insts, None, pendingBytes, lastInstVA+lastInstSZ, funVA, lastInstBytes, lastInstVA)

            # if lastFun != None:
            #     print("Last Fun: {}".format(lastFun.info))
            #     for inst in lastFun.insts:
            #         print("    "+hex(inst.offset+self.textVA))

            # Check 3. np-temp函数无需检查函数内的pendingBytes，同时，我们归零last_fun以禁止下一轮函数向上检查np-temp中的bytes
            if fun.info.startswith("np-temp"):
                lastFun = None
                lastInstVA = None
                lastInstSZ = None
                fixedFun = self.FixedFun(fun.info, [], fun.offset, fun.section, True)
            # Check 3. 非np-temp函数需要继续遍历inst以检查函数内的pendingBytes
            else:
                lastInstVA = funVA
                lastInstSZ = 0x0
                tempInsts = list()
                for inst in fun.insts:
                    instVA = self.textVA + inst.offset

                    # PendingBytes分类————padding? code mis-collection? data in code?
                    if lastInstVA != None and lastInstVA + lastInstSZ != instVA:
                        lastInstBytes = self.textContent[lastInstVA - self.textVA: lastInstVA + lastInstSZ - self.textVA]
                        pendingBytes = self.textContent[lastInstVA + lastInstSZ - self.textVA: instVA - self.textVA]
                        self.handlePendingBytes(tempInsts, inst, pendingBytes, lastInstVA+lastInstSZ, instVA, lastInstBytes, lastInstVA)

                    tempInsts.append(inst)

                    lastInstVA = inst.offset + self.textVA # 不能直接用instVA,因为handlePendingBytes里可能修改inst的offset和size
                    lastInstSZ = inst.size

                # Check 4. fun里至少应该有一条指令的，后面的代码都是基于这个假设写的！ 所以如果遇到空函数在两个fun的offset一致时删除上一个函数，
                # 注意：这里我们在下一个函数中检查上一个函数的指令情况，考虑到有些函数NP没有收集到任何指令，需要在下一个函数中才能检查到这些PendingBytes
                if lastFun != None and not lastFun.isTemp:
                    if len(lastFun.insts) == 0:
                        if lastFun.offset != fun.offset:
                            logging.error("Fun {} 里面没有指令，但其具有体积，这说明有code被识别为data或者padding，请排查该问题  (Fun {} VA={} -- > Fun {} VA={})".format(
                                lastFun.info, lastFun.info, hex(lastFun.offset+self.textVA), fun.info, hex(fun.offset+self.textVA)))
                            exit(1)
                        else:
                            del self.funs[-1]

                fixedFun = self.FixedFun(fun.info, tempInsts, fun.offset, fun.section, False)

            self.funs.append(fixedFun)
            lastFun = fixedFun

    def handlePendingBytes(self, tempInsts, inst, pendingBytes, pendingBytesStartVA, pendingBytesEndVA, lastInstBytes, lastInstVA):
        """
        根据self.identifyPendingBytesType()识别的三种结果采取对应操作：
        - Padding. 无需修改元数据，不记录
        - Code Mis-collection by NoCompiler. 反汇编这些指令并添加到所属的fun中去，然后特别记录下来
        - Data in Code. 无需修改元数据，但特别记录下来
        - Inst Prefix. 将其加到
        """

        def bytes2Str(bytes):
            length = 40

            def formatLength(singleByte):
                return '0' * (2 - len(singleByte)) + singleByte

            temp = ""
            for i in bytes:
                temp += formatLength(str(hex(i))[2:]) + " "
            return temp + ' ' * (length - len(temp))

        # print("Handle PendingBytes [{}-{}]".format(hex(pendingBytesStartVA), hex(pendingBytesEndVA)))
        pendingTypeList = self.identifyPendingBytesType(pendingBytes, pendingBytesStartVA, lastInstBytes, lastInstVA)
        # print(pendingTypeList)

        for subPending in pendingTypeList:
            subPendingVA = subPending[0]
            subPendingSize = subPending[1]
            subPendingType = subPending[2]
            subPendingInsts = None
            if subPendingType == 2:
                subPendingInsts = subPending[3]

            subPendingBytes = pendingBytes[subPendingVA-pendingBytesStartVA : subPendingVA+subPendingSize-pendingBytesStartVA]

            # Case 1. code mis-collected by NoCompiler. 反汇编这些指令并添加到所属的fun中去
            if subPendingType == 2:
                disass_str = ""
                for i in subPendingInsts:
                    disass_str += "{}:\t{}\t{}\t{}\n".format(str(hex(i.address)),
                                                                bytes2Str(i.bytes), i.mnemonic,
                                                                i.op_str)
                    if "nop" not in i.mnemonic:
                        newInst = NP.Metadata.InstInfo()
                        newInst.offset = i.address-self.textVA
                        newInst.size = i.size
                        tempInsts.append(newInst)
                cmc = self.CMC(subPendingBytes, subPendingVA, subPendingVA+subPendingSize, disass_str)
                self.codeMisCollection.append(cmc)

            # Case 2. data in code. 无需修改元数据，但特别记录下来
            elif subPendingType == 3:
                dic = self.DIC(subPendingBytes, subPendingVA, subPendingVA+subPendingSize)
                self.DatainCode.append(dic)

            # Case 3. Inst Prefix. 基于它调整该inst即可
            elif subPendingType == 4:
                if subPendingVA + len(subPendingBytes) == pendingBytesEndVA:
                    inst.offset = inst.offset - len(pendingBytes)
                    inst.size = inst.size + len(pendingBytes)
                else:
                    print("反汇编分割出的区域{}被识别为Prefix，但它并非位于PendingBytes的尾部".format(hex(subPendingVA)))
                    exit(1)

    def identifyPendingBytesType(self, pendingBytes, pendingBytesVA, lastInstBytes, lastInstBytesVA):
        """
        Input:
            pendingBytes: 可疑的Bytes
            pendingBytesLast: 可疑的Bytes的上一条指令

        Output:
            return 4: not padding, it is prefix bytes of curInst
            return 3: not padding, it is still a pending bytes, may be a data in code
            return 2: not padding, it is a code which is mis-collected by NoCompiler
            return 1: is padding

        首先判断两种最常见的逻辑：
        1. 判断是否为短字节长度的指令前缀
        2. 判断是否为两种padding，固定格式以及全\x00
        3. 都不是的话，通过递归式反汇编区分data和code，具体见recursiveDisass函数的描述
        """

        if self.arch not in [C.X64, C.ARM64]:
            print("判断padding时没有指定正确的arch")
            exit(1)

        # Check 1. 是否为Padding或者Prefix
        type = self.recursiveDisass.Tools.isPaddingorPrefix(pendingBytes, self.arch)
        if type != 3:
            return [[pendingBytesVA, len(pendingBytes), type]]

        # Check 2. 不确定的话就进行递归式反汇编来分割区域，再分别判断区域类型
        pendingTypeList = list()

        # Step 1. 首先判断上一条指令是否存在Fall-Through，以增加新的CodePointer
        ins = None # 注意到如果pendingBytes位于函数开头的话，是没有lastInstBytes的，此时ins保持为None
        for _ins in self.md.disasm(lastInstBytes, lastInstBytesVA):
            ins = _ins
            break
        if ins != None and self.recursiveDisass.Tools.isFallThroughInst(ins, self.arch):
            self.recursiveDisass.preciseCodePointers.add(pendingBytesVA)

        # Step 2. 开始递归式反汇编
        codeBlocksOrderedList = self.recursiveDisass.recursiveDisass(pendingBytes, pendingBytesVA) #, show=True if pendingBytesVA==0x24b56 else None)

        # Step 3. 分析反汇编结果，分流CodeBlock和中间的PendingBytes. 注意我们要校验出递归反汇编中的一种错误————其可能由指令前缀引起
        lastCodeBlockEnd = pendingBytesVA
        # 增加一个尾节点，以处理尾部是pendingByte的情况，该尾节点size为默认的None，因此在下面不会被处理
        codeBlocksOrderedList.append(RecursiveDisass.CodeBlock(pendingBytesVA+len(pendingBytes)))
        for codeBlock in codeBlocksOrderedList:
            # CodeBlock合法性校验，以及处理和上一个CodeBlock的间距————DataBlock
            if codeBlock.VA > lastCodeBlockEnd:
                subPendingBytes = pendingBytes[lastCodeBlockEnd-pendingBytesVA : codeBlock.VA-pendingBytesVA]
                type = self.recursiveDisass.Tools.isPaddingorPrefix(subPendingBytes, self.arch)
                pendingTypeList.append([lastCodeBlockEnd, codeBlock.VA-lastCodeBlockEnd, type])
            elif codeBlock.VA < lastCodeBlockEnd:
                print("解析反汇编结果时长度错误，上一个codeblock+size={}，而下一个codeblock.VA={}".format(
                    hex(lastCodeBlockEnd), hex(codeBlock.VA)))
                exit(1)

            # 处理当前CodeBlock
            if codeBlock.size != None:
                if codeBlock.isPaddingorPrefix != None: # 该CodeBlock是指令前缀或者Padding，并非普通指令块
                    pendingTypeList.append([codeBlock.VA, codeBlock.size, codeBlock.isPaddingorPrefix])
                else:
                    pendingTypeList.append([codeBlock.VA, codeBlock.size, 2, codeBlock.capsInsts])
                lastCodeBlockEnd = codeBlock.VA + codeBlock.size

        return pendingTypeList


# xie. 该类主要被FixedMetadata用于识别PendingByte，因为当时对于openssl这种里面有大段的硬编码的pending bytes，我们要通过这种递归式的反汇编来得到code block和真正的data block.
class RecursiveDisass():

    class Tools():
        unconditionalControlFlowX64 = [X86_INS_JMP,
                                       X86_INS_RET, X86_INS_RETF, X86_INS_RETFQ]
        unconditionalControlFLOWJUMPARM64 = [ARM64_INS_B, ARM64_INS_BR]
        unconditionalControlFlowRETURNARM64 = [ARM64_INS_RET]

        # https://bbs.kanxue.com/thread-224583.htm
        cdeclX86 = []
        stdcallX86 = []
        fastcallX86 = [X86_REG_RDI, X86_REG_EDI, X86_REG_RSI, X86_REG_ESI, X86_REG_RDX, X86_REG_EDX,
                       X86_REG_RCX, X86_REG_ECX, X86_REG_R8, X86_REG_R8D, X86_REG_R9, X86_REG_R9D]
        ATPCSARM = [ARM_REG_R0, ARM_REG_R1, ARM_REG_R2, ARM_REG_R3]
        ATPCSARM64 = [ARM64_REG_X0, ARM64_REG_X1, ARM64_REG_X2, ARM64_REG_X3, ARM64_REG_X4, ARM64_REG_X5, ARM64_REG_X6, ARM64_REG_X7,
                      ARM64_REG_W0, ARM64_REG_W1, ARM64_REG_W2, ARM64_REG_W3, ARM64_REG_W4, ARM64_REG_W5, ARM64_REG_W6, ARM64_REG_W7]

        rxxReg = re.compile("X86_REG_R\d{1,2}")

        @classmethod
        def isFallThroughInst(self, capsInst, arch):
            # NOTE. 目前我们粗略的认为除了以下几类外的控制流转移指令，都是有Fall-Through的
            #  - 非条件跳转指令
            #  - 返回指令
            #  NOTE. 其实Call指令(X86_INS_CALL,ARM64_INS_BL)是否为Fall-Through要由返回指令才能判断，从之前分析IDA可以看到这是一个Common Challenge，
            #        会受到terminal函数、尾调用优化的影响，所以我们目前统一假设Call指令都是会返回，有Fall-Through的。


            if arch == C.X64:
                # X64的判断规则从指令id出发来设计就可以
                if capsInst.id not in RecursiveDisass.Tools.unconditionalControlFlowX64:
                    return True
            else:
                # ARM64的条件跳转是b|br指令+cc的形式，如b.eq，所以除了RET是无条件跳转外，对于JMP指令要进一步判断其cc属性
                if capsInst.id not in RecursiveDisass.Tools.unconditionalControlFlowRETURNARM64 and not (
                        capsInst.id in RecursiveDisass.Tools.unconditionalControlFLOWJUMPARM64 and capsInst.cc == 0):
                    return True

            return False

        @classmethod
        def isControlFlowInst(self, capsInst):
            if capsInst.group(CS_GRP_JUMP) or capsInst.group(CS_GRP_CALL) \
                    or capsInst.group(CS_GRP_RET) or capsInst.group(CS_GRP_IRET)\
                    or capsInst.group(CS_GRP_PRIVILEGE):
                return True
            return False

        @classmethod
        def isJMPInst(self, capsInst):
            if capsInst.group(CS_GRP_JUMP):
                return True
            return False

        @classmethod
        def isMovInst(self, capsInst, arch):
            if arch == C.X64:
                if capsInst.mnemonic.startswith("mov"):
                    return True
                return False
            return None

        @classmethod
        def isPushInst(self, capsInst, arch):
            if arch == C.X64:
                if capsInst.mnemonic.startswith("push"):
                    return True
                return False
            return None

        @classmethod
        def isCallInst(self, capsInst, arch):
            if arch == C.X64:
                if capsInst.mnemonic.startswith("call"):
                    return True
                return False
            return None

        @classmethod
        def isSameReg(self, reg1, reg2, arch):
            if arch == C.X64:
                reg1Str = x86regStr(reg1)
                reg2Str = x86regStr(reg2)
                if reg1Str == None or reg2Str == None:
                    return False

                # 匹配rdi, edi, di类型
                if reg1Str[-2:] == reg2Str[-2:]:
                    return True
                # 匹配r10, r10d, r10w类型
                strReg1 = RecursiveDisass.Tools.rxxReg.findall(reg1Str)
                strReg2 = RecursiveDisass.Tools.rxxReg.findall(reg2Str)
                if len(strReg1) != 0 and len(strReg2) != 0:
                    if strReg1[0] == strReg2[0]:
                        return True
                # 匹配XMM10，YMM10类型
                elif "MM" in reg1Str:
                    if reg1Str[9:] == reg2Str[9:]:
                        return True
                return False
            return None

        @classmethod
        def isPaddingorPrefix(self, pendingBytes, arch):
            bytesLength = len(pendingBytes)

            # Case 1. 检查是否是当前指令的前缀 (注意这个判断要放在padding判断前，因为纯\x66字节序列应该优先是指令前缀，其次才是padding)
            if arch == C.X64:
                if len(pendingBytes) <= 3:
                    for prefixByte in C.X64_PrefixByte:
                        if len(pendingBytes) * prefixByte == pendingBytes:
                            return 4
            else:
                pass  # aarch64因为是定长指令应该不存在指令前缀

            # Case 2. 全\x00时候一定是padding
            if b'\x00' * bytesLength == pendingBytes:
                return 1

            # Case 3. 检查是否为第二种padding，即由padding碎片拼接而成
            isPadding = True
            candicatePadding = C.X64_PADDINGS if arch == C.X64 else C.ARM64_PADDINGS
            idx = 0
            while idx < bytesLength:
                find_padding_ele = False
                for padding in candicatePadding:
                    padding_length = len(padding)
                    if idx + padding_length <= bytesLength and pendingBytes[idx:idx + padding_length] == padding:
                        idx += padding_length
                        find_padding_ele = True
                        break
                if not find_padding_ele:
                    isPadding = False
                    break
            if isPadding:
                return 1

            # Case 4. 检查是否为第三种，即由jmp指令和nop构成
            if bytesLength >= 16 and pendingBytes[:1] == b'\xe9' and pendingBytes[5:] == b'\x90' * (bytesLength - 5):
                return 1

            return 3

    def __init__(self, file=None, fixedMetadata=None, show=False):

        self.file = file
        self.fixedMetadata = fixedMetadata
        self.show = show

        if self.file != None and fixedMetadata == None:
            self.elfPath = file
            self.elfParser = elfParser.ELFParser(file)
            self.textContent = self.elfParser.elf.get_section_by_name(".text").data()
            self.textVA = self.elfParser.getSectionVA(".text")
            self.textIdx = self.elfParser.getSectionIdx(".text")
            self.getDetailInfo()
            self.getMetadata()
        elif fixedMetadata != None and file == None:
            self.elfPath = self.fixedMetadata.elfParser.fn
            self.elfParser = self.fixedMetadata.elfParser
            self.textContent = self.fixedMetadata.textContent
            self.textVA = self.fixedMetadata.textVA
            self.textIdx = self.fixedMetadata.textIdx
            self.arch = self.fixedMetadata.arch
            self.md = self.fixedMetadata.md
            self.dwarfParser = self.fixedMetadata.dwarfParser
            self.metadata = self.fixedMetadata.metadata
            if self.arch == C.ARM64:
                C.relocDict = C.aarch64_reloc_dict
            elif self.arch == C.X64:
                C.relocDict = C.x64_reloc_dict
        self.allfixups = list()
        for fixup in self.metadata.fixups:
            self.allfixups.append(fixup)
        for fixup in self.metadata.otherfixups:
            self.allfixups.append(fixup)

        self.getPreciseCodePointers()

    def getDetailInfo(self):
        """
        self.arch
        self.md
        self.relocDict
        self.dwarfParser
        """

        self.arch = None
        arch_retu = os.popen("readelf -hW {}".format(self.elfPath)).read()
        if "AArch64" in arch_retu:
            self.arch = C.ARM64
        elif "X86-64" in arch_retu:
            self.arch = C.X64
        else:
            return 1, "  ELF({})架构类型未知".format(self.elfPath)

        if self.arch == C.X64:
            self.md = Cs(CS_ARCH_X86, CS_MODE_64)
            self.md.detail = True
        else:
            self.md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
            self.md.detail = True

        if self.arch == C.ARM64:
            C.relocDict = C.aarch64_reloc_dict
        elif self.arch == C.X64:
            C.relocDict = C.x64_reloc_dict

        self.dwarfParser = DWarfParser(self.elfParser.fn, self.elfParser.elf)
        self.dwarfParser.parse_eh_frame()
        self.dwarfParser.parseLSDA()


    def getMetadata(self):
        if ".rand" not in self.elfParser.section_ranges:
            return 1, "  ELF({})中不存在rand节".format(self.elfPath)
        randStart = self.elfParser.section_offset['.rand'][0]
        randSize = self.elfParser.section_offset['.rand'][1]
        fr = open(self.elfPath, "rb")
        fr.seek(randStart, 0)
        randBytes = fr.read(randSize)
        fr.close()

        # 反序列化元数据
        self.metadata = NP.Metadata()
        self.metadata.ParseFromString(randBytes)


    def getPreciseCodePointers(self):
        """
        我们尽可能多的提取Code Pointers，用来支持后面对PendingBytes做递归式反汇编。这些Code Pointers来自
        Case 1. 控制流指令中的指针
        Case 2. 函数头
        Case 3. gcc_except_table中的call site
        """

        self.preciseCodePointers = set()

        # 得到指令列表，这对于x64架构是必须的，因为我们需要确定fixup位于哪条指令中。而ARM64则不用，因为其指令地址即为指针地址。
        instDict = dict()
        if self.arch == C.X64:
            for fun in self.metadata.funs:
                for inst in fun.insts:
                    instDict[inst.offset] = inst.size

        # Case 1. 来自于控制流指令的Code Pointers
        for fixup in self.allfixups:
            if fixup.section != self.textIdx:
                continue

            # if self.show:
            #     print("Handle Fixup: {} {}".format(hex(fixup.offset+self.textVA), C.relocDict[(fixup.type >> 16) & 0xffff][0]))

            # 提取指针所在的指令字节
            instBytes = None
            instVA = 0
            if self.arch == C.X64:
                instHead = 0  # 向前定位指令头
                while instHead <= 0x10:
                    if fixup.offset - instHead in instDict:
                        break
                    instHead += 1
                if instHead != 0x11:  # 没有找到该指令
                    instOffst = fixup.offset - instHead
                    instBytes = self.textContent[instOffst : instOffst+instDict[instOffst]]
                    instVA = fixup.offset - instHead + self.textVA
            else:
                instBytes = self.textContent[fixup.offset: fixup.offset + 4]
                instVA = fixup.offset + self.textVA

            # 反汇编指令，如果为控制流相关指令则记录该fixup的地址为code pointer
            if instBytes == None:
                continue
            if self.arch == C.X64:
                firstCapsInst = None
                for capsInst in self.md.disasm(instBytes, instVA):
                    firstCapsInst = capsInst
                    break
                # 对于x64来说首先要确认fixup在该指令中，因为我们不确定instHead和instTail是否正确
                if firstCapsInst and firstCapsInst.address <= fixup.offset + self.textVA < firstCapsInst.address + firstCapsInst.size:
                    # 然后再确认操作码是否为控制流转移指令
                    if firstCapsInst.group(CS_GRP_JUMP) or firstCapsInst.group(CS_GRP_CALL):
                        self.preciseCodePointers.add(fixup.target_bbl_sym)  # 回顾了gold的指针合并策略，target_bbl_sym一定是value，并且是VA
            else:
                firstCapsInst = None
                for capsInst in self.md.disasm(instBytes, instVA):
                    firstCapsInst = capsInst
                    break
                if firstCapsInst:
                    # 确认操作码是否为控制流转移指令
                    if firstCapsInst.group(CS_GRP_JUMP) or firstCapsInst.group(CS_GRP_CALL):
                        self.preciseCodePointers.add(fixup.target_bbl_sym)
                        if self.show: print("[*] Add Control Flow Fixup {}".format(hex(fixup.target_bbl_sym)))

        # Case 2. 加入所有函数头
        for fun in self.metadata.funs:
            self.preciseCodePointers.add(self.textVA + fun.offset)
            if self.show: print("[*] Add Funtion Head {}".format(hex(self.textVA + fun.offset)))

        # Case 3. 如果有gcc_except_table的话，加入call site
        for lsda in self.dwarfParser.lsdas:
            for callsite in lsda.CallSites:
                if callsite.myLandingPadPositionVA != 0:
                    self.preciseCodePointers.add(callsite.myLandingPadPositionVA)
                    if self.show: print("[*] Add Call Site {}".format(hex(callsite.myLandingPadPositionVA)))


    class CodeBlock:
        def __init__(self, VA, bytes=None, size=None, isPaddingorPrefix=None):
            """
            VA. code block的VA
            size. 如果是None的话说明还没有对该block做反汇编
            """
            self.VA = VA
            self.bytes = bytes
            self.size = size
            self.isPaddingorPrefix = isPaddingorPrefix
            self.capsInsts = list()


    def recursiveDisass(self, pendingBytes, pendingVA, show=None):
        """
        传入一段指定VA的字节序列，对其进行递归式反汇编，返回范围划分数组以及代码块的capsInsts序列
        1. 在将precisionCodePointers加上fall-through的隐式控制流和函数头部后，我们根据指针对其进行切分并标记为代码块和数据块
        2. 遍历所有代码块直到控制流转移指令，然后得到新的两个指针*代码块
        3. 新指针指向新的代码块，来进一步分割出可能的code
        """
        if show != None:
            origShowFlag = self.show
            self.show = show

        blocksDict = dict()
        blocksOrderedList = list()
        newCodePointers = list(self.preciseCodePointers)
        addressReg = re.compile("0x[\da-f]{1,16}")
        pendingEndVA = pendingVA + len(pendingBytes)

        # NOTE. 一直到本轮次没有发现新的code pointers为止
        disassRound = 1
        while len(newCodePointers) != 0:
            if self.show: print("\n[*] =====Round {}=====".format(disassRound))

            # Step 1. 根据newCodePointers切割出新的Code Blocks，其VA确定但Size=None，等待后面的反汇编
            for newCodePointer in newCodePointers:
                if newCodePointer not in blocksDict and pendingVA <= newCodePointer < pendingEndVA:
                    newCodeBlock = self.CodeBlock(newCodePointer, size=None)

                    # 将newCodeBlock插入blocksDict和blocksOrderedList中
                    blocksDict[newCodePointer] = newCodeBlock
                    if len(blocksOrderedList) == 0 or newCodePointer >= blocksOrderedList[-1].VA:
                        blocksOrderedList.append(newCodeBlock)
                    else:
                        for blockIdx in range(len(blocksOrderedList)):
                            if newCodePointer < blocksOrderedList[blockIdx].VA:
                                blocksOrderedList.insert(blockIdx, newCodeBlock)
                                break

            # Step 2. 对这些新的Code Blocks进行反汇编，直到遇到控制流跳转指令停止。以确定Code Block的长度，并得到新的指针，可以继续下一轮的切割
            newCodePointers.clear()
            codeBlocksNum = len(blocksOrderedList)
            codeBlocksNeedRemove = list() # 当反汇编引擎是由fixedMetadata调用的话，我们允许CodeBlock中不含有任何指令，并随后将该block删除
            for blockIdx in range(codeBlocksNum):
                curCodeBlock = blocksOrderedList[blockIdx]
                if curCodeBlock.size != None:
                    continue

                # Step 2.1. 确定该block要反汇编的bytes
                if blockIdx == codeBlocksNum-1:
                    curBlockLength = pendingEndVA - curCodeBlock.VA
                else:
                    curBlockLength = blocksOrderedList[blockIdx+1].VA - curCodeBlock.VA
                codeBlockBytes = pendingBytes[curCodeBlock.VA-pendingVA : curCodeBlock.VA+curBlockLength-pendingVA]
                curCodeBlock.bytes = codeBlockBytes

                # Step 2.2. 反汇编直到遇到控制流转移指令时终止，同时尝试从中提取Code Pointer，确定长度
                if self.show: print("[*] Start Disass CodeBlock {}-{}".format(hex(curCodeBlock.VA), hex(curCodeBlock.VA+curBlockLength)))
                isFirstInst = True
                for capsInst in self.md.disasm(codeBlockBytes, curCodeBlock.VA):
                    # 对于CodeBlock我们要求可反汇编的指令一定是从开头Bytes开始的，不然说明该CodeBlock并不准确，我们会在本Round后删除它
                    # 注意capstone会反汇编\x00\x00指令，但我们并不将其看做指令而是padding
                    if isFirstInst:
                        if capsInst.address != curCodeBlock.VA:
                            print("反汇编出的第一条指令为{}, 其并非位于CodeBlock的头部{}，准备删除该CodeBlock".format(
                                hex(capsInst.address), hex(curCodeBlock.VA)))
                            break
                        if capsInst.bytes == b'\x00'*capsInst.size:
                            break
                        isFirstInst = False

                    # 累增每一条反汇编的指令
                    curCodeBlock.capsInsts.append(capsInst)

                    # 遇到控制流转移指令时终止
                    if RecursiveDisass.Tools.isControlFlowInst(capsInst):
                        # 确定该Code Block的长度
                        curCodeBlock.size = capsInst.address + capsInst.size - curCodeBlock.VA

                        # 收集新的CodePointer，首先从指令中提取
                        # 我们对能提取指针的指令要求比较多，首先他是控制流转移指令，其次它得有操作数，且操作数中不能有MEM，得有IMM (为了应付cbz	x20, 400940)
                        canExtractPointer = False
                        if len(capsInst.operands) > 0:
                            for op in capsInst.operands:
                                if op.type == CS_OP_IMM:
                                    canExtractPointer = True
                                    break
                            for op in capsInst.operands:
                                if op.type == CS_OP_MEM:
                                    canExtractPointer = False
                                    break
                        if canExtractPointer:
                            reRetu = addressReg.findall(capsInst.op_str)
                            if len(reRetu) == 1:
                                newCodePointer = int(reRetu[0], 16)
                                if newCodePointer not in self.preciseCodePointers:
                                    newCodePointers.append(newCodePointer)
                                    self.preciseCodePointers.add(newCodePointer)
                                    if self.show: print("Add Tail Control Flow Pointer {} from Inst {}".format(
                                        hex(newCodePointer), hex(capsInst.address)))
                            else:
                                print("请排查该控制流转移指令，其op_type=IMM，但我们并未匹配出有效的地址\n{}:\t{}\t{}\t{}".format(
                                    hex(capsInst.address), util.bytes2Str(capsInst.bytes), capsInst.mnemonic, capsInst.op_str
                                ))
                                exit(1)

                        # 收集新的CodePointer, 判断Fall-Through：
                        if RecursiveDisass.Tools.isFallThroughInst(capsInst, self.arch):
                            if capsInst.address + capsInst.size not in self.preciseCodePointers:
                                newCodePointers.append(capsInst.address + capsInst.size)
                                self.preciseCodePointers.add(capsInst.address + capsInst.size)
                                if self.show: print("[*] Add Fall-Through Pointer {}".format(hex(capsInst.address + capsInst.size)))

                        # 终止该Block的反汇编
                        break

                # Step 2.3 处理一些特殊的CodeBlock
                #  - Case 1. 如果没有遇到控制流转移指令作为结尾的话，取反汇编的最后一条指令作为CodeBlock的size
                #  - Case 2. 如果CodeBlock中没有指令的话，考虑删除该CodeBlock.
                #  - Case 3. 如果该CodeBlock的第一条指令并非从第一个Byte开始的话(在前面会直接break导致同样没有指令),考虑删除该CodeBlock
                #  - 所有的特殊操作都由CodeBlock.size==None触发，但后两个情况涉及到删除CodeBlock，我们要额外检查是否为fixedMetadata传入指令前缀bytes的情况
                if curCodeBlock.size == None:
                    if len(curCodeBlock.capsInsts) != 0:
                        lastInst = curCodeBlock.capsInsts[-1]
                        curCodeBlock.size = lastInst.address + lastInst.size - curCodeBlock.VA
                    else:
                        curCodeBlock.isPaddingorPrefix = self.Tools.isPaddingorPrefix(curCodeBlock.bytes, self.arch)
                        if self.fixedMetadata != None and curCodeBlock.isPaddingorPrefix:
                            curCodeBlock.size = len(curCodeBlock.bytes)
                        else:
                            codeBlocksNeedRemove.append(blockIdx)
                        # print("分割出的Code Block {}一条指令都没有反汇编出来，请排查该问题".format(hex(curCodeBlock.VA)))
                        # exit(1)

                # Step 2.4 处理newCodePointer指向CodeBlock内部的情况
                for newCodePointer in newCodePointers:
                    for codeBlock in blocksOrderedList:
                        if codeBlock.size == None: # 在Step3准备删除的CodeBlock
                            continue
                        if codeBlock.VA < newCodePointer < codeBlock.VA + codeBlock.size: # 不考虑头部重合的情况
                            codeBlock.size = newCodePointer - codeBlock.VA

            # Step 3. 在本轮结束后，删除一些特殊情况的CodeBlock
            for codeBlockNeedRemoveIdx in codeBlocksNeedRemove:
                codeBlock = blocksOrderedList[codeBlockNeedRemoveIdx]
                del blocksDict[codeBlock.VA]
                blocksOrderedList.remove(codeBlock)
                del codeBlock
            codeBlocksNeedRemove.clear()

            if self.show:
                print("[*] Round {} End".format(disassRound))
                for codeBlockIdx, codeBlock in enumerate(blocksOrderedList):
                    print ("      CodeBlock#{} {}->{}".format(codeBlockIdx, hex(codeBlock.VA), hex(codeBlock.VA + codeBlock.size)))
                newCodePointersStr = ""
                for newCodePointer in newCodePointers:
                    newCodePointersStr += hex(newCodePointer)+" "
                print("    newCodePointer: [{}]".format(newCodePointersStr))

            disassRound += 1

        if show != None:
            self.show = origShowFlag
        return blocksOrderedList



    def disassText(self):
        codeBlocksOrderedList = self.recursiveDisass(self.textContent, self.textVA)

        for codeBlock in codeBlocksOrderedList:
            print("BLOCK #{}: {} INST".format(hex(codeBlock.VA), len(codeBlock.capsInsts)))
            for capsInst in codeBlock.capsInsts:
                print("  {}:\t{}\t{}\t{}".format(hex(capsInst.address),
                                           util.bytes2Str(capsInst.bytes), capsInst.mnemonic, capsInst.op_str))

class Inst():
    def __init__(self, capsInst, node, fixups):
        self.capsInst = capsInst
        self.node = node
        self.fixups = fixups
        self.next = None
        self.last = None

    def __str__(self):
        return "{}:\t{}\t{}\t{}".format(hex(self.capsInst.address), util.bytes2Str(self.capsInst.bytes),
                                          self.capsInst.mnemonic, self.capsInst.op_str)

class Node():
    def __init__(self, addr, firstInstIdx):
        self.insts = list()

        self.addr2instIdx = dict()
        self.addr = addr
        self.endAddr = None
        self.firstInstIdx = firstInstIdx

        self.inNodes = set()
        self.outNodes = set()
        self.inSubNodes = set()
        self.outSubNodes = list()
        self.outStatus = None

    def addInst(self, inst):
        self.addr2instIdx[inst.capsInst.address] = len(self.insts)
        self.insts.append(inst)

    def instInNode(self, inst):
        if inst.capsInst.address in self.addr2instIdx:
            return True
        else:
            return False


# xie. 提供一系列静态程序分析功能
class CFG():
    def __init__(self, nodes, arch):
        self.arch = arch
        self.nodes = nodes
        self.addr2node = dict()
        for node in self.nodes:
            self.addr2node[node.addr] = node

    @classmethod
    def dotBytes2Str(self, bytes):
        length = 40
        def formatLength(singleByte):
            return '0' * (2 - len(singleByte)) + singleByte
        temp = ""
        for i in bytes:
            temp += '\\\\x' + formatLength(str(hex(i))[2:])
        return temp + ' ' * (length - len(bytes)*4)

    @classmethod
    def generatorDotGraph(self, nodes, outFile):
        if not outFile.endswith(".svg"):
            print("unit.CFG.generatorDotGraph 请输出svg后缀的dot文件路径")
            return False
        dot_fd = open(outFile+".dot", "w")

        dot_fd.write("digraph Fun%s {\n" % (hex(nodes[0].addr)))

        # xie. 打印节点
        for node in nodes:
            dot_fd.write("  Node%s [shape=box, fontname=\"DejaVu Sans Mono\", label=\"" % (hex(node.addr)))
            for inst in node.insts:
                inst_str = "{}:\t{}\t{}\t{}".format(str(hex(inst.capsInst.address)),
                                                         CFG.dotBytes2Str(inst.capsInst.bytes), inst.capsInst.mnemonic,
                                                         inst.capsInst.op_str)
                dot_fd.write("{}\\l".format(inst_str))
            dot_fd.write("\"]\n")

        # xie. 打印边
        dot_fd.write("\n")
        for node in nodes:
            for outNode in node.outNodes:
                dot_fd.write("  Node%s -> Node%s\n" % (hex(node.addr), hex(outNode.addr)))

        dot_fd.write("}\n")

        print("/usr/bin/dot -T svg -o %s %s.dot" % (outFile, outFile))
        # retu = os.system("/usr/bin/dot -T svg -o %s %s.dot" % (outFile, outFile))

    @classmethod
    def generatorSubDotGraph(self, nodes, addr2node, outFile, subNodeAddrs):
        if not outFile.endswith(".svg"):
            print("unit.CFG.generatorDotGraph 请输出svg后缀的dot文件路径")
            return False
        dot_fd = open(outFile+".dot", "w")

        dot_fd.write("digraph Fun%s {\n" % (hex(nodes[0].addr)))

        # xie. 打印节点
        for subNodeAddr in subNodeAddrs:
            subNode = addr2node[subNodeAddr]
            dot_fd.write("  Node%s [shape=box, fontname=\"DejaVu Sans Mono\", label=\"" % (hex(subNode.addr)))
            for inst in subNode.insts:
                inst_str = "{}:\t{}\t{}\t{}".format(str(hex(inst.capsInst.address)),
                                                         CFG.dotBytes2Str(inst.capsInst.bytes), inst.capsInst.mnemonic,
                                                         inst.capsInst.op_str)
                dot_fd.write("{}\\l".format(inst_str))
            dot_fd.write("\"]\n")

        # xie. 打印边
        dot_fd.write("\n")
        for subNodeAddr in subNodeAddrs:
            subNode = addr2node[subNodeAddr]
            for outSubNode in subNode.outSubNodes:
                dot_fd.write("  Node%s -> Node%s\n" % (hex(subNode.addr), hex(outSubNode.addr)))

        dot_fd.write("}\n")

        print("/usr/bin/dot -T svg -o %s %s.dot" % (outFile, outFile))
        # retu = os.system("/usr/bin/dot -T svg -o %s %s.dot" % (outFile, outFile))

    @classmethod
    def getForwardTraverseOrder(self, nodes, addr2node, instAddr, generateSubDotGraph=False):
        if len(nodes) == 0:
            return list()

        # 从instAddr确定Node
        # print("确定Node")
        findNode = None
        for node in nodes:
            if node.addr <= instAddr < node.endAddr:
                findNode = node
                break
        if findNode == None:
            return list()

        # 首先裁剪该CFG
        # print("裁剪该CFG")
        subNodes = set()
        nodeNeedHandled = [findNode]
        while len(nodeNeedHandled) != 0:
            tempNode = nodeNeedHandled[0]
            nodeNeedHandled = nodeNeedHandled[1:]
            subNodes.add(tempNode.addr)
            for outNode in tempNode.outNodes:
                if outNode.addr not in subNodes:
                    nodeNeedHandled.append(outNode)

        # 根据裁剪后的subNodes生成inSubNodes, outSubNodes
        # print("生成inSubNodes")
        for node in nodes:
            node.inSubNodes = set()
            node.outSubNodes = list()
        for node in nodes:
            if node.addr in subNodes:
                for inNode in node.inNodes:
                    if inNode.addr in subNodes:
                        node.inSubNodes.add(inNode.addr)
        for node in nodes:
            if node.addr in subNodes:
                for outNode in node.outNodes:
                    if outNode.addr in subNodes:
                        node.outSubNodes.append(outNode)
        if generateSubDotGraph:
            CFG.generatorSubDotGraph(nodes, addr2node, "/tmp/subout.svg", subNodes)

        # NOTE. 采用基于边界节点思想的宽度优先遍历，遵循原则：
        #  1. 向上走的边界节点，仅允许走一次，以代表我们执行循环操作且仅执行一次的目标
        # print("开始遍历")
        orderedNode = list()
        boundaryNodes = [findNode]
        upEdgesOneTime = set()
        nodeSet = set()
        while len(boundaryNodes) != 0:
            tempBoundaryNodesAddr = set()

            # xie. 从边界节点boundaryNodes生成下一层的边界节点tempBoundaryNodes
            for node in boundaryNodes:
                # 加入边界节点到orderedNodes
                orderedNode.append(node)
                nodeSet.add(node.addr)
                # 注意，如果该临接节点向上走的且已经执行过一次，则可以忽略该临接节点
                for outNode in node.outSubNodes:
                    # NOTE. 向上执行的循环边仅允许走一次
                    if outNode.addr <= node.addr:
                        if outNode.addr + node.addr in upEdgesOneTime:
                            continue
                        else:
                            upEdgesOneTime.add(outNode.addr + node.addr)
                    if outNode.addr not in tempBoundaryNodesAddr:
                        tempBoundaryNodesAddr.add(outNode.addr)

            boundaryNodes.clear()
            for tempBoundaryNodeAddr in tempBoundaryNodesAddr:
                boundaryNodes.append(addr2node[tempBoundaryNodeAddr])

            # print("{} / {} / {}".format(len(nodeSet), len(subNodes), len(orderedNode)))
            # for node in boundaryNodes:
            #     print(hex(node.addr), end=" ")
            # print()
            # time.sleep(0.5)

        print("    FunNodes:{} / SubNodes:{} / PathNodes:{}".format(len(nodeSet), len(subNodes), len(orderedNode)))
        return orderedNode

    @classmethod
    # xie. 从startNode开始，传入的func负责接受中间状态并根据当前指令更新中间状态，而forwardAnalysis函数分支的跳转以及合并
    def forwardAnalysis(self, nodes, addr2node, arch, traverseOrder, analysisFunc, mergeFunc, args, show=False):
        """
        return:
            - status. 数据流分析的状态，-1表示因异常而终止传播，1表示因有发现而终止传播，0表示完整传播结束
            - nodes.  数据流分析终止时，分析了多少块。该信息用于统计指针和内存访问的临近程度
            - args.   由analysisFunc自定义，可能表示数据流分析结束时的args，或者数据流分析异常时的提示语，或是数据流分析成功时的所在inst
        """

        # 清空所有node.status
        for node in nodes:
            node.outStatus = None

        for idx, node in enumerate(traverseOrder):
            if node.addr not in addr2node:
                return -1, idx, "traverseOrder异常，节点{}不存在于CFG中".format(hex(node.addr))

            # xie. 首个节点使用args，后续节点则使用入度节点的状态
            if idx != 0:
                args = None
                for inNode in node.inNodes:
                    if inNode.outStatus != None:
                        args = mergeFunc(args, inNode.outStatus)
                if args == None:
                    print("Node#{}的status合并异常，没有发现任何有效的入度状态")
                    exit(0x233)

            # xie. 生成的args用于该node的传播
            if show: print("Node {} args={}".format(hex(node.addr), str(args)))
            for inst in node.insts:
                # status == -1 因analysisFunc异常而终止传播，args为错误说明字符串
                # status == 0  完整传播结束，args为传播结束时的状态
                # status == 1  因analysisFunc有发现而终止传播，args中记录结果
                status, args = analysisFunc(inst, args, arch)
                if status == -1 or status == 1: # 允许analysisFunc择机停止
                    return status, idx, args

            # xie. 传播完的args作为node的输出状态记录下来
            node.outStatus = args
        return 0, len(traverseOrder), args

    @classmethod
    def listMerged(self, argsOld, argsNew):
        # 格式化args为[instAddr, [regs], <regs, [pc, inst]]格式
        if argsOld and type(argsOld) == int:
            argsOld = [argsOld, set(), dict()]
        if argsNew and type(argsNew) == int:
            argsNew = [argsNew, set(), dict()]

        # 由于入度状态可能是None，这里需要做状态检查
        if argsOld == None and argsNew == None:
            return None
        elif argsOld == None and argsNew != None:
            return argsNew
        elif argsOld != None and argsNew == None:
            return argsOld

        # 合并寄存器的污点传播状态
        for reg in argsNew[1]:
            if reg not in argsOld[1]:
                argsOld[1].add(reg)

        # 合并栈状态，有相同寄存器入栈的话，取计数器最大的
        for stackReg in argsNew[2]:
            # 如果都存在则取计数器最大的
            if stackReg in argsOld[2] and argsNew[2][stackReg][0] > argsOld[2][stackReg][0]:
                argsOld[2][stackReg] = argsNew[2][stackReg]
            # 如果不存在则直接装入即可
            else:
                argsOld[2][stackReg] = argsNew[2][stackReg]

        return argsOld

    @classmethod
    def constantPropagation(self, inst, args, arch):
        """
        给定指令地址作为source(从指针到寄存器的第一次传播)，跟踪指令中常量在寄存器中的传播情况，并在进行内存访问时候返回
        - inst 当前指令
        - args [[source的地址], {传播的regs}, {传播的regs}, <栈情况>, ...others]
        - retu status, args | retu_content
        """
        # print("     Handle Inst#{} args={}".format(hex(inst.capsInst.address), str(args)))

        def regInStatus(reg, statusRegs, arch):
            for statusReg in statusRegs:
                if RecursiveDisass.Tools.isSameReg(reg, statusReg, arch):
                    return True
            return False
        def removeRegInStatus(reg, statusRegs, arch):
            newArgs = set()
            for statusReg in statusRegs:
                if not RecursiveDisass.Tools.isSameReg(reg, statusRegs, arch):
                    newArgs.add(statusReg)
            return newArgs

        # 格式化args为[instAddr, [regs], <regs, [pc, inst]]格式
        if type(args) == int:
            args = [args, set(), dict()] # [[source的地址], {传播的regs}, <栈情况>, ...others]

        # xie. Find Source
        if inst.capsInst.address == args[0]:
            dstReg = None
            # 粗略判断
            for opearand in inst.capsInst.operands:
                if opearand.type == CS_OP_REG:
                    dstReg = opearand.reg
            # 按照指令类型的精细化判断
            # if RecursiveDisass.Tools.isMovInst(inst.capsInst, C.X64) and len(inst.capsInst.operands) == 2:
            #     if inst.capsInst.operands[0].type == CS_OP_REG and inst.capsInst.operands[1].type == CS_OP_IMM:
            #         dstReg = inst.capsInst.operands[0].reg
            if dstReg != None:
                args[1].add(dstReg)
                return 0, args
            else:
                return -1, "Source并非mov reg, imm形式，无法找到常量传播到的寄存器"

        # xie. Find Sink
        # Case 1. 函数调用传出该值
        if RecursiveDisass.Tools.isCallInst(inst.capsInst, C.X64):
            # FIXME. 目前考虑寄存器传参，以及push r3d的压栈传参。根据调用约定还有其他传参方法，可以后面再加上。
            if arch == C.X64:
                for argReg in RecursiveDisass.Tools.fastcallX86:
                    if argReg in args[1]:
                        return 1, [inst, argReg]
                if len(args[2]) != 0:
                    return 1, [inst, str(args[2])]
            elif arch == C.ARM64:
                for argReg in RecursiveDisass.Tools.ATPCSARM64:
                    if argReg in args[1]:
                        return 1, [inst, argReg]
        # Case 2. 函数结束传出该值
        pass # 这个要等到函数传播结束后再进行判断
        # Case 3. 正常内存访问使用该值
        for op in inst.capsInst.operands:
            if op.type == CS_OP_MEM:
                if op.mem.index != 0 and regInStatus(op.mem.index, args[1], C.X64): # [0x400500(disp) + rax(index)*4(scale)]
                    return 1, [inst, op.mem.index]
                elif op.mem.base != 0 and regInStatus(op.mem.base, args[1], C.X64): # [rax(base)]  [rbx(base)-0x28(disp)]
                    return 1, [inst, op.mem.base]
        # Case 4. 控制流转移指令使用到它
        if RecursiveDisass.Tools.isControlFlowInst(inst.capsInst):
            for operand in inst.capsInst.operands:
                if operand.type == CS_OP_REG:
                    if regInStatus(operand.reg, args[1], C.X64):
                        return 1, [inst, operand.reg]

        # xie. Propogation
        if RecursiveDisass.Tools.isMovInst(inst.capsInst, C.X64) and len(inst.capsInst.operands) == 2:
            dst = inst.capsInst.operands[0]
            src = inst.capsInst.operands[1]
            if dst.type == CS_OP_REG and not regInStatus(dst.reg, args[1], C.X64): # Case 1. 污点寄存器的传播
                if src.type == CS_OP_REG and regInStatus(src.reg, args[1], C.X64):
                    args[1].add(dst.reg)
            elif dst.type == CS_OP_REG and regInStatus(dst.reg, args[1], C.X64):   # Case 2. 污点寄存器洗白
                if not (src.type == CS_OP_REG and regInStatus(src.reg, args[1], C.X64)):
                    args[1] = removeRegInStatus(dst.reg, args[1], C.X64)
        elif RecursiveDisass.Tools.isPushInst(inst.capsInst, C.X64) and len(inst.capsInst.operands) == 1:
            src = inst.capsInst.operands[0]
            if src.type == CS_OP_REG and regInStatus(src.reg, args[1], C.X64):
                args[2][src.reg] = [30, inst.capsInst] # xie. list[2]代表指令计数器，每一次遍历我们会将计数器-1，以此来做简易的函数调用前的栈状态维护
        # 每一条指令会将栈状态的计数器-1, 为0时则清除该栈状态
        stackRegsNeedRemove = list()
        for stackReg in args[2]:
            if args[2][stackReg][0] > 0:
                args[2][stackReg][0] -= 1
            if args[2][stackReg][0] == 0:
                stackRegsNeedRemove.append(stackReg)
        for stackRegNeedRemove in stackRegsNeedRemove:
            del args[2][stackRegNeedRemove]

        return 0, args


# xie. 不进行反汇编而是直接依靠元数据进行完全理想情况下的CFG构建 (完全理想仅限于指令识别，间接控制流跳转依靠元数据也无法解析，而是需要在指针识别的基础上一步步完善才行)
# xie. PerfectCFG用于准确的CFG构建，CFG则提供了数据流分析算法。两者一起提供了一些基础的数据流分析能力，因此在当时主要是用于反汇编排错的自动化分析
"""
print("> 开始构建FixedMetadata")
startTime = time.time()
fixedMetadata = FixedMetadata.fixedMetadataFactory("/ccr/binaryset/502/cpugcc_r_gcc9O3")[1]
endTime = time.time()
print("用时{}\n".format(endTime-startTime))

print("> 开始构建PerfectCFG")
startTime = time.time()
perfectCFG = PerfectCFG(fixedMetadata, 0x7994cc, show=False)
endTime = time.time()
print("用时{}\n".format(endTime-startTime))

CFG.generatorDotGraph(perfectCFG.cfg.nodes, "/tmp/out.svg")

print("> 开始构建子图并寻找路径")
startTime = time.time()
orderedNodes = CFG.getForwardTraverseOrder(perfectCFG.cfg.nodes, perfectCFG.cfg.addr2node, 0x7994cc, generateSubDotGraph=True)
endTime = time.time()
for node in orderedNodes:
    print(hex(node.addr))
print("用时{}\n".format(endTime-startTime))

print("> 开始数据流分析")
args = 0x4bee9b
status, steps, args = CFG.forwardAnalysis(perfectCFG.cfg.nodes, perfectCFG.cfg.addr2node, perfectCFG.cfg.arch,
                                          orderedNodes, CFG.constantPropagation, CFG.listMerged, args, show=True)
if status == 1:
    print("Find Sink {} in Inst {}".format(steps, str(args[0])))
elif status == 0:
    if X86_REG_RAX in args or X86_REG_EAX in args:
        print("Find Sink {} in 函数出口".format(steps))
    else:
        print("Not Found" + str(args))
else:
    print("运行报错")
    print(status)
    print(args)
"""
class PerfectCFG():

    def __init__(self, fixedMetadata, instAddr, show=False):
        self.fixedMetadata = fixedMetadata
        self.show = show

        # Step 1. 搜索inst所在的fun，如果instAddr不在元数据收集范围内则返回False
        findFun = None
        funVA = None
        nextFunVA = None
        for funIdx in range(len(fixedMetadata.funs)):
            funVA = fixedMetadata.textVA + fixedMetadata.funs[funIdx].offset
            if funIdx != fixedMetadata.n_funs-1:
                nextFunVA = fixedMetadata.textVA + fixedMetadata.funs[funIdx+1].offset
            else:
                nextFunVA = fixedMetadata.textVA + fixedMetadata.funs[funIdx].insts[-1].offset + fixedMetadata.funs[funIdx].insts[-1].size

            if funVA <= instAddr < nextFunVA and not fixedMetadata.funs[funIdx].info.startswith("np-temp"):
                findFun = fixedMetadata.funs[funIdx]
                break

        if findFun == None:
            self.status = False
            return
        findFunStart = funVA
        findFunEnd = nextFunVA

        # Step 2. 基于元数据提供的指令边界来反汇编该函数, 同时为每一条指令搜索其指针
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        md.detail = True
        capsInsts = list()
        addr2instIdx = dict()
        addr2inst = dict()
        fixupsDict = dict()
        for inst in findFun.insts:
            # Step 2.2 反汇编该指令
            instBytes = fixedMetadata.textContent[inst.offset : inst.offset+inst.size]
            instVA = fixedMetadata.textVA + inst.offset
            firstCapsInst = None
            for capsInst in md.disasm(instBytes, instVA):
                firstCapsInst = capsInst
                break
            if firstCapsInst == None:
                continue

            # Step 2.3. 搜索该指令中的指针 (目前只搜索控制流转移指令的中的指针)
            if RecursiveDisass.Tools.isControlFlowInst(firstCapsInst):
                fixupsDict[firstCapsInst.address] = self.findFixupsInInst(firstCapsInst)
            else:
                fixupsDict[firstCapsInst.address] = list()

            addr2instIdx[firstCapsInst.address] = len(capsInsts)
            capsInsts.append(firstCapsInst)
            addr2inst[firstCapsInst.address] = firstCapsInst

        # Step 3. 构建Nodes
        instsLength = len(capsInsts)
        instIdx2node = [None] * instsLength
        addr2node = dict()
        nodes = list()
        newNodeList = list()
        # 函数头一定是一个node的开始
        firstNode = Node(capsInsts[0].address, 0)
        newNodeList.append(firstNode)
        while True:
            # xie. 检查是否有inst还没有归属于Node，这表明这是一个没有入度的block
            if len(newNodeList) == 0:
                for instsIdx, node in enumerate(instIdx2node):
                    if node == None:
                        nextNode = Node(capsInsts[instsIdx].address, instsIdx)
                        addr2node[capsInsts[instsIdx].address] = nextNode
                        newNodeList.append(nextNode)
                        if show: print("find next node {}".format(hex(nextNode.addr)))
                        break
                if len(newNodeList) == 0:
                    break

            # xie. 取出新的Node
            curNode = newNodeList[0]
            newNodeList = newNodeList[1:]
            curInstIdx = curNode.firstInstIdx

            if show: print("Handle New Node {} {}".format(hex(curNode.addr), curInstIdx))
            # xie. 该Node需要一直遍历指令到控制流跳转，或是其他的Node开头？
            while curInstIdx < instsLength:
                curCapsInst = capsInsts[curInstIdx]
                curInst = Inst(curCapsInst, curNode, fixupsDict[curCapsInst.address])

                # xie. 如果是其他Node开头的话，终止该Node，同时加入一个指向该Node的Fall-through边 (其他Node包括老node以及newNodeList还没有处理的，所以要用addr2node而非instIdx2node来判断)
                if curCapsInst.address in addr2node and curCapsInst.address != curNode.addr:
                    oldNode = addr2node[curCapsInst.address]
                    # 建立与下一个node间的关系
                    curNode.outNodes.add(oldNode)
                    oldNode.inNodes.add(curNode)
                    # 终止curNode
                    curNode.endAddr = curNode.insts[-1].capsInst.address + curNode.insts[-1].capsInst.size
                    nodes.append(curNode)
                    break

                # xie. 将该指令加入当前Node
                curNode.addInst(curInst)
                instIdx2node[curInstIdx] = curNode

                # xie. 如果是控制流转移指令的话，终止该Node，同时加入fixup以及下一个的Fall-through边
                if RecursiveDisass.Tools.isControlFlowInst(curInst.capsInst):
                    # 从fall-through和指针两方面收集跳转关系
                    nextNodes = list()
                    # 只收集jmp指令的fixup，call指令的不收集
                    if RecursiveDisass.Tools.isJMPInst(curInst.capsInst):
                        for FI in curInst.fixups:
                            if findFunStart <= FI.targetAddr < findFunEnd and FI.targetAddr in addr2inst:
                                nextNodes.append([addr2instIdx[FI.targetAddr], addr2inst[FI.targetAddr]])
                    # 还要收集fall-through的跳转关系，目前默认call指令是fall-through的
                    if RecursiveDisass.Tools.isFallThroughInst(curInst.capsInst, C.X64) and curInstIdx+1<instsLength:
                        nextNodes.append([curInstIdx+1, capsInsts[curInstIdx+1]])

                    # xie. 如果该target属于某个node的头部，那么直接建立出度入度关系，否则建立新的节点并加入newNodeList (其他Node包括老node以及newNodeList还没有处理的，所以要用addr2node而非instIdx2node来判断)
                    for nextCapsInstIdx, nextCapsInst in nextNodes:
                        createNewNode = False
                        if nextCapsInst.address in addr2node:
                            oldNode = addr2node[nextCapsInst.address]
                            oldNode.inNodes.add(curNode)
                            curNode.outNodes.add(oldNode)
                        else:
                            createNewNode = True
                            nextNode = Node(nextCapsInst.address, nextCapsInstIdx)
                            nextNode.inNodes.add(curNode)
                            curNode.outNodes.add(nextNode)
                            addr2node[nextNode.addr] = nextNode # 不能等到处理该节点时再inst2node，不然会有重复的newNodeList加入
                            newNodeList.append(nextNode)

                        if show:
                            print(" -> {} ({})".format(hex(nextCapsInst.address), "NEW" if createNewNode else ""))

                    # 终止curNode
                    curNode.endAddr = curNode.insts[-1].capsInst.address + curNode.insts[-1].capsInst.size
                    nodes.append(curNode)
                    break

                curInstIdx += 1

            # xie. 检查newNodeList是否是其他Node的一部分，并对其做裁剪 (其他Node只包括老Node)
            for newNode in newNodeList:
                oldNode = instIdx2node[newNode.firstInstIdx]
                if oldNode != None:
                    # xie. 裁剪老Node：1. 删除addr后面的指令  2. 相应的修改出度和入度
                    newHeadInstIdx = oldNode.addr2instIdx[newNode.addr]
                    oldNode.insts = oldNode.insts[:newHeadInstIdx]
                    oldNode.endAddr = oldNode.insts[-1].capsInst.address + oldNode.insts[-1].capsInst.size
                    oldNode.addr2inst = dict()
                    for instIdx, inst in enumerate(oldNode.insts):
                        oldNode.addr2inst[inst.capsInst.address] = instIdx

                    for outNode in oldNode.outNodes:
                        outNode.inNodes.remove(oldNode)
                    oldNode.outNodes = {newNode}
                    newNode.inNodes.add(oldNode)

        # xie. 为了静态数据流分析，需要破掉所有的循环线路。和操作系统中的防止死锁类似, 将资源进行排序，如果往低地址跳转则会构成环
        #  具体做法是将这个跳转边删除即可，注意考虑到自循环的block，地址判断要用<和>，而非<=和>=
        # for node in nodes:
        #     outNodes = set()
        #     for outNode in node.outNodes:
        #         if outNode.addr > node.addr:
        #             outNodes.add(outNode)
        #         else:
        #             if self.show: print("删除Node#{}->Node#{}的边".format(hex(node.addr), hex(outNode.addr)))
        #     node.outNodes = outNodes
        #
        #     inNodes = set()
        #     for inNode in node.inNodes:
        #         if inNode.addr < node.addr:
        #             inNodes.add(inNode)
        #         else:
        #             if self.show: print("删除Node#{}->Node#{}的边".format(hex(inNode.addr), hex(node.addr)))
        #     node.inNodes = inNodes

        self.cfg = CFG(nodes, C.X64)

    def findFixupsInInst(self, capsInst):
        subfixups = list()
        for fixupProto in self.fixedMetadata.allfixups:
            if fixupProto.section != self.fixedMetadata.textIdx:
                continue
            if capsInst.address <= fixupProto.offset+self.fixedMetadata.textVA < capsInst.address + capsInst.size:
                FI = Fixup()
                FI.offset = fixupProto.offset
                FI.VA = self.fixedMetadata.textVA + FI.offset

                _type = fixupProto.type
                FI.baseType = _type & 3
                FI.targetType = (_type >> 2) & 3
                FI.relocType = (_type >> 16) & 0xffff
                FI.relocName = C.relocDict[FI.relocType][0]

                FI.baseAddr = None
                if FI.baseType == 2:
                    if fixupProto.base_section:
                        FI.baseAddr = self.fixedMetadata.elfParser.section_ranges_idx[fixupProto.base_section][0] + fixupProto.base_bbl_sym
                    else:
                        FI.baseAddr = fixupProto.base_bbl_sym

                FI.targetAddr = None
                if FI.targetType == 2:
                    if fixupProto.target_section:
                        FI.targetAddr = self.fixedMetadata.elfParser.section_ranges_idx[fixupProto.target_section][0] + fixupProto.target_bbl_sym
                    else:
                        FI.targetAddr = fixupProto.target_bbl_sym
                else:
                    print("fixup {}的targetType不为2 {}".format(hex(FI.VA), FI.targetType))
                    exit(233)

                subfixups.append(FI)
        return subfixups








class Function():
    def __init__(self):
        self.idx = -1

        # 位置标识
        self.sec = None
        self.offset = 0x0
        self.VA = 0x0
        self.size = 0x0

        self.refTos = dict()  # 函数间的交叉引用
        self.refFroms = dict()  # 函数间的交叉引用

        # 调试所需的信息，函数名以及obj
        self.name = None
        self.objName = None
        self.mergedCheckFlag = False

        self.insts = None
        self.fixups = []  # Basic Blocks that consist of this function (children nodes)
        self.hasLSDA = False  # 即在gcc_except_table中指向该函数的call site, landing pad的指针，因此该函数不做随机化
        self.toMergedFunIdx = 0x0

        # Updated After randomization
        self.adjustedBytes = 0x0
        self.newOffset = 0x0
        self.newVA = 0x0

        # Simulation purpose
        self.testVA = 0x0

    def __repr__(self):
        return "Fun#{} <{}>: VA={} section_idx={}".format(
            str(self.idx),
            self.info,
            hex(self.VA),
            self.sec)

    def getWrittenFun(self):
        return str(hex(self.VA)) + ' ' + str(hex(self.newVA))


class Fixup():
    def __init__(self):
        self.idx = -1

        # 链表相关
        self.parent = None  # 此Fixup所属的FUN
        self.next = None

        # 寻址模式相关
        self.addressMode = None
        self.info = ""

        self.targetType = None
        self.target_bbl_sym = 0
        self.targetSec = None
        self.targetAddr = None
        self.targetInRand = False
        self.targetFun = None

        self.baseType = None
        self.base_bbl_sym = 0
        self.baseSec = None
        self.baseAddr = 0
        self.baseInRand = False
        self.baseFun = None

        self.add = 0
        self.step = 0

        self.value = 0
        self.newValue = 0
        self.testVA = 0
        self.bitIMM = None
        self.bitX = None
        self.isCodePointer = None

        # 编码方式相关
        self.mask = None
        self.doffsets = None
        self.derefSz = 0  # fixup所在value的大小，如果小于4则是ShortDist
        self.nextNum = 0  # 该重定位后面的重定位数量，用于还原出来
        self.hasCombined = False
        self.checkHighOverFlow = False
        self.checkLowOverFlow = False

        # 位置标识
        self.sec = None
        self.secName = None
        self.offset = 0x0  # Fixup的相对节的偏移
        self.VA = 0x0  # Fixup所处的VA
        self.testVA = 0x0  # Simulation purpose

        # 一些标志位
        self.show = 0
        self.isFromRand = False
        self.isFromReloc = False
        self.isFromGOT = False
        self.needUpdate = None

        # 杂
        self.isRela = False
        self.relocType = None
        self.relocName = None

    def __str__(self):
        base_str = ""
        if self.baseType not in [C.BaseType.NONE, C.BaseType.UNKNOWN]:
            base_str = 'Base:{num}, '.format(num=hex(self.baseAddr))
        target_str = 'Target:{num},'.format(num=hex(self.targetAddr))

        return "Fixup#%4d VA:0x%04x, Offset:0x%04x, Reloc:%s, %s%s add:0x%04x (@Sec %s)%s%s%s%d" % \
               (self.idx,
                self.VA,
                self.offset,
                self.relocType,
                base_str,
                target_str,
                self.add,
                self.sec,
                " (RAND)" if self.isFromRand else "",
                " (RELOC)" if self.isFromReloc else "",
                " (GOT)" if self.isFromGOT else "",
                self.step)


class Section():
    def __init__(self):
        self.idx = -1
        self.name = None
        self.sectionStart = 0x0
        self.sectionEnd = 0x0
        self.sz = 0x0
        self.align = 0x0
        self.va = 0x0
        self.type = C.SecType.NORMAL
        self.isCodeSection = False

        self.fileOffsetEnd = 0x0  # includes the alignment to rewrite a binary
        self.next = None

    def __str__(self):
        return '[Sec#%2d] FileOff[0x%04x:0x%04x] VA=0x%08x (%s)' \
               % (self.idx, self.sectionStart, self.fileOffsetEnd, self.va, self.name)


class LSDA():

    def __init__(self, LPStartformat, LPStartmode, LPStart,
                 TTypeformat, TTypemode, TTBase,
                 CallSiteformat, CallSitemode, CallSiteTableSize, CallSites,
                 ActionTablePosition):
        self.LPStartformat = LPStartformat
        self.LPStartmode = LPStartmode
        self.LPStart = LPStart

        self.TTypeformat = TTypeformat
        self.TTypemode = TTypemode
        self.TTBase = TTBase

        self.CallSiteformat = CallSiteformat
        self.CallSitemode = CallSitemode
        self.CallSiteTableSize = CallSiteTableSize
        self.CallSites = CallSites

        self.ActionTablePosition = ActionTablePosition


class CallSite():
    found_nothing = 0x00
    found_cleanup = 0x10
    found_handler = 0x20

    def __init__(self, CallSitePosition, CallSiteLength, LandingPadPosition, FirstAction, myLandingPadPositionVA):
        self.CallSitePosition = CallSitePosition
        self.CallSiteLength = CallSiteLength
        self.LandingPadPosition = LandingPadPosition
        self.FirstAction = FirstAction
        self.myLandingPadPositionVA = myLandingPadPositionVA

        if self.LandingPadPosition == 0:
            self.found_type = CallSite.found_nothing
        elif self.FirstAction == 0:
            self.found_type = self.found_cleanup
        else:  # 否则还要进一步通过Action来判断
            self.found_type = self.found_handler  # 不准确，在personality中会进一步区分出handler cleanup specifications


class CIE():
    def __init__(self):
        self.bytes = None
        self.length = None
        self.length_range = None
        self.CIE_id = None
        self.CIE_id_range = None
        self.version = None
        self.version_range = None
        self.augmentation_string = None
        self.augmentation_string_range = None
        self.code_alignment_factor = None
        self.code_alignment_factor_range = None
        self.data_alignment_factor = None
        self.data_alignment_factor_range = None
        self.return_address_register = None
        self.return_address_register_range = None
        self.augmentation_data = None
        self.augmentation_data_range = None
        self.initial_instructions = None
        self.initial_instructions_range = None

    def set_bytes(self, bytes):
        self.bytes = bytes

    def set_length(self, length, range):
        self.length = length
        self.length_range = range

    def set_CIE_id(self, CIE_id, range):
        self.CIE_id = CIE_id
        self.CIE_id_range = range

    def set_version(self, version, version_range):
        self.version = version
        self.version_range = version_range

    def set_augmentation_string(self, augmentation_string, range):
        self.augmentation_string = augmentation_string
        self.augmentation_string_range = range

    def set_code_alignment_factor(self, code_alignment_factor, range):
        self.code_alignment_factor = code_alignment_factor
        self.code_alignment_factor_range = range

    def set_data_alignment_factor(self, data_alignment_factor, range):
        self.data_alignment_factor = data_alignment_factor
        self.data_alignment_factor_range = range

    def set_return_address_register(self, return_address_register, range):
        self.return_address_register = return_address_register
        self.return_address_register_range = range

    def set_augmentation_data(self, augmentation_data, range):
        self.augmentation_data = augmentation_data
        self.augmentation_data_range = range

    def set_initial_instruction(self, initial_instructions, range):
        self.initial_instructions = initial_instructions
        self.initial_instructions_range = range


class FDE():
    def __init__(self):
        self.bytes = None
        self.FDEFormat = None
        self.FDEMode = None
        self.length = None
        self.length_range = None
        self.CIE_pointer = None
        self.CIE_pointer_range = None
        self.initial_location = None
        self.initial_location_range = None
        self.address_range = None
        self.address_range_range = None
        self.augmentation_data = None
        self.augmentation_data_range = None
        self.augmentation_data_length = None
        self.augmentation_data_length_range = None
        self.instructions = None
        self.instructions_range = None

    def set_bytes(self, bytes):
        self.bytes = bytes

    def set_FDEEnc(self, FDEFormat, FDEMode):
        self.FDEFormat = FDEFormat
        self.FDEMode = FDEMode

    def set_length(self, length, range):
        self.length = length
        self.length_range = range

    def set_CIE_pointer(self, CIE_pointer, range):
        self.CIE_pointer = CIE_pointer
        self.CIE_pointer_range = range

    def set_initial_location(self, initial_location, range):
        self.initial_location = initial_location
        self.initial_location_range = range

    def set_address_range(self, address_range, range):
        self.address_range = address_range
        self.address_range_range = range

    def set_augmentation_data_length(self, augmentation_data_length, range):
        self.augmentation_data_length = augmentation_data_length
        self.augmentation_data_length_range = range

    def set_augmentation_data(self, augmentation_data, range):
        self.augmentation_data = augmentation_data
        self.augmentation_data_range = range

    def set_instructions(self, instructions, range):
        self.instructions = instructions
        self.instructions_range = range

class DWarfParser():

    def __init__(self, filePath, elffile):
        self.elffile = elffile
        self.filePath = filePath
        self.dwarfConfig = self.elffile.get_dwarf_info().config

        self.textVA = \
            self.elffile.get_section_by_name(".text")['sh_addr'] if self.elffile.get_section_by_name(".text") != None else 0
        self.eh_frame_hdrVA = \
            self.elffile.get_section_by_name(".eh_frame_hdr")['sh_addr'] if self.elffile.get_section_by_name(".eh_frame_hdr") != None else 0
        self.eh_frameVA = \
            self.elffile.get_section_by_name(".eh_frame")['sh_addr'] if self.elffile.get_section_by_name(".eh_frame") != None else 0
        self.gcc_except_tableVA = \
            elffile.get_section_by_name(".gcc_except_table")['sh_addr'] if self.elffile.get_section_by_name(".gcc_except_table") != None else 0


        eh_frameSec = self.elffile.get_section_by_name(".eh_frame")
        compressed = bool(self.elffile.get_section_by_name('.zdebug_info'))
        if eh_frameSec != None:
            dwarf_eh_frameSec = self.elffile._read_dwarf_section(eh_frameSec, False)
            if compressed:
                dwarf_eh_frameSec = self.elffile._decompress_dwarf_section(dwarf_eh_frameSec)

            self.structs = DWARFStructs(
                little_endian=self.dwarfConfig.little_endian,
                dwarf_format=32,
                address_size=self.dwarfConfig.default_address_size)

            self.callFrameInfo = CallFrameInfo(
                stream=dwarf_eh_frameSec.stream,
                size=dwarf_eh_frameSec.size,
                address=dwarf_eh_frameSec.address,
                base_structs=self.structs,
                for_eh_frame=True)
        else:
            self.callFrameInfo = None

        self.lsdas = list()         # 基于lsda指针从.gcc_except_table中解析出的lsda对象，在调用parseLSDA()后生成
        self.FDEsHasLSDA = list()   # 从entry中筛选出来的，含有LSDA结构的FDE，这些FDE在随机化时需要格外注意
        self.entryList = list()     # 从eh_frame中解析出的多个entry，有CIE和FDE两种，在调用parse_eh_frame()后生成

        if self.elffile.little_endian:
            self.ptr_encode = self.LPtr_encode
            self.uint8_encode = self.ULInt8_encode
            self.uint16_encode = self.ULInt16_encode
            self.uint32_encode = self.ULInt32_encode
            self.uint64_encode = self.ULInt64_encode
            self.int8_encode = self.SLInt8_encode
            self.int16_encode = self.SLInt16_encode
            self.int32_encode = self.SLInt32_encode
            self.int64_encode = self.SLInt64_encode

            self.ptr_decode = self.LPtr_decode
            self.uint8_decode = self.ULInt8_decode
            self.uint16_decode = self.ULInt16_decode
            self.uint32_decode = self.ULInt32_decode
            self.uint64_decode = self.ULInt64_decode
            self.int8_decode = self.SLInt8_decode
            self.int16_decode = self.SLInt16_decode
            self.int32_decode = self.SLInt32_decode
            self.int64_decode = self.SLInt64_decode
        else:
            self.ptr_encode = self.BPtr_encode
            self.uint8_encode = self.UBInt8_encode
            self.uint16_encode = self.UBInt16_encode
            self.uint32_encode = self.UBInt32_encode
            self.uint64_encode = self.UBInt64_encode
            self.int8_encode = self.SBInt8_encode
            self.int16_encode = self.SBInt16_encode
            self.int32_encode = self.SBInt32_encode
            self.int64_encode = self.SBInt64_encode

            self.ptr_decode = self.BPtr_decode
            self.uint8_decode = self.ULInt8_decode
            self.uint16_decode = self.ULInt16_decode
            self.uint32_decode = self.ULInt32_decode
            self.uint64_decode = self.ULInt64_decode
            self.int8_decode = self.SLInt8_decode
            self.int16_decode = self.SLInt16_decode
            self.int32_decode = self.SLInt32_decode
            self.int64_decode = self.SLInt64_decode

        self.decode_func = {
            self.DW_EH_PE_absptr: self.ptr_decode,
            self.DW_EH_PE_uleb128: self.uleb128_decode,
            self.DW_EH_PE_udata2: self.uint16_decode,
            self.DW_EH_PE_udata4: self.uint32_decode,
            self.DW_EH_PE_udata8: self.uint64_decode,

            self.DW_EH_PE_sleb128: self.sleb128_decode,
            self.DW_EH_PE_sdata2: self.int16_decode,
            self.DW_EH_PE_sdata4: self.int32_decode,
            self.DW_EH_PE_sdata8: self.int64_decode
        }

        self.encode_func = {
            self.DW_EH_PE_absptr: self.ptr_encode,
            self.DW_EH_PE_uleb128: self.uleb128_encode,
            self.DW_EH_PE_udata2: self.uint16_encode,
            self.DW_EH_PE_udata4: self.uint32_encode,
            self.DW_EH_PE_udata8: self.uint64_encode,

            self.DW_EH_PE_sleb128: self.sleb128_decode,
            self.DW_EH_PE_sdata2: self.int16_encode,
            self.DW_EH_PE_sdata4: self.int32_encode,
            self.DW_EH_PE_sdata8: self.int64_encode
        }

    def format_enc(self, enc):
        if enc == self.DW_EH_PE_omit:
            return self.DW_EH_PE_omit, self.DW_EH_PE_omit
        else:
            format, mode = enc & 0x0F, enc & 0x70
            if format in self.val_format and mode in self.val_mode:
                return format, mode
            else:
                logging.error("Unkown encoding: %s", hex(enc))
                exit(1)

    def encode_value(self, format, mode, value, VA, fun):
        """
        输入value，输出bytes序列
        """
        base = 0
        if mode in [self.DW_EH_PE_omit, self.DW_EH_PE_absptr, self.DW_EH_PE_aligned]:
            base = 0
        elif mode == self.DW_EH_PE_pcrel:
            base = VA
        elif mode == self.DW_EH_PE_textrel:  # .text位置？？ 在gdb的patch邮件中，注意到该patch是将.text作为了base
            logging.warning("mode为DW_EH_PE_textrel")
            if self.textVA == 0:
                logging.warning("没有text节")
            base = self.textVA
        elif mode == self.DW_EH_PE_datarel:  # eh_frame_hdr的位置？？ 在binutil讨论邮件中，看到有人说这个基址指的就是eh_frame_hdr，而且CCR在解析eh_frame_hdr也是基于此
            #logging.warning("mode为DW_EH_PE_datarel")
            if self.eh_frame_hdrVA == 0:
                logging.warning("没有eh_frame_hdr节")
            base = self.eh_frame_hdrVA
        elif mode == self.DW_EH_PE_funcrel:  # 在unwind-pe.h的base_of_encoded_value中，看到funcrel是以_Unwind_GetRegionStart，也就是该frame的基址作为base
            logging.warning("mode为DW_EH_PE_funcrel")
            base = fun
        elif mode == self.DW_EH_PE_aligned:  # 在unwind-pe.h的decode_value_with_base中，看到DW_EH_PE_aligned经过了比较复杂的处理，目前先不做实现
            logging.error("mode为DW_EH_PE_aligned")  # 在
            exit(1)
        elif mode == self.DW_EH_PE_indirect:
            logging.error("mode为DW_EH_PE_indirect")
            exit(1)

        offset = value - base

        if format not in self.encode_func:
            logging.error("不匹配的format = %s", str(format))
            exit(1)
        bytes, len = self.encode_func[format](offset)

        return bytes, len


    def decode_value(self, format, mode, ea, index, VA, fun, addIndex=True, needOffset=False):
        """
        输入bytes序列，输出解析出的value

        format: 该字段的编码方式
        mode:   该字段到目标地址的计算方式
        ea:     字节序列
        index:  字节序列的下标

        VA:     当前字节序列下标的VA，在DW_EH_PE_pcrel的mode中用到
        fun:    在gcc_except_table中表示frame的基址(从gcc解析lsda的观察中得知)，DW_EH_PE_funcrel的mode中用到
                在eh_frame_hdr中，应该不存在funcrel吧
        """

        # 根据mode确定base
        base = 0
        if mode in [self.DW_EH_PE_omit, self.DW_EH_PE_absptr, self.DW_EH_PE_aligned]:
            base = 0
        elif mode == self.DW_EH_PE_pcrel:
            base = VA
        elif mode == self.DW_EH_PE_textrel:  # .text位置？？ 在gdb的patch邮件中，注意到该patch是将.text作为了base
            logging.warning("mode为DW_EH_PE_textrel")
            if self.textVA == 0:
                logging.warning("没有text节")
            base = self.textVA
        elif mode == self.DW_EH_PE_datarel:  # eh_frame_hdr的位置？？ 在binutil讨论邮件中，看到有人说这个基址指的就是eh_frame_hdr，而且CCR在解析eh_frame_hdr也是基于此
            #logging.warning("mode为DW_EH_PE_datarel")
            if self.eh_frame_hdrVA == 0:
                logging.warning("没有eh_frame节")
            base = self.eh_frame_hdrVA
        elif mode == self.DW_EH_PE_funcrel:  # 在unwind-pe.h的base_of_encoded_value中，看到funcrel是以_Unwind_GetRegionStart，也就是该frame的基址作为base
            logging.warning("mode为DW_EH_PE_funcrel")
            base = fun
        elif mode == self.DW_EH_PE_aligned:  # 在unwind-pe.h的decode_value_with_base中，看到DW_EH_PE_aligned经过了比较复杂的处理，目前先不做实现
            logging.error("mode为DW_EH_PE_aligned")  # 在
            exit(1)
        elif mode == self.DW_EH_PE_indirect:
            logging.error("mode为DW_EH_PE_indirect")
            exit(1)

        # 根据format解析出数值
        if format not in self.decode_func:
            logging.error("不匹配的format = %s", str(format))
            exit(1)
        value, add_index = self.decode_func[format](ea, index)

        return value if needOffset else base + value, index + add_index if addIndex else add_index


    def _parseLSDA(self, lsdaFDE, gccChunk, show=False):
        frame_base = lsdaFDE.initial_location
        lsdaPointer = lsdaFDE.augmentation_data["lsda_pointer"]
        index = lsdaPointer - self.gcc_except_tableVA

        LPStartformat, LPStartmode = self.format_enc(gccChunk[index])
        index += 1
        if LPStartformat != self.DW_EH_PE_omit:
            LPStart, index = self.decode_value(LPStartformat, LPStartmode, gccChunk, index, self.gcc_except_tableVA + index,
                                                frame_base)
        else:
            LPStart = frame_base
        if show:
            print("LPStart: %s : %s : %s" % (self.val_format[LPStartformat], self.val_mode[LPStartmode], hex(LPStart)))

        TTypeformat, TTypemode = self.format_enc(gccChunk[index])
        index += 1
        if TTypemode != self.DW_EH_PE_omit:
            TTBase, index = self.uleb128_decode(gccChunk, index, addIndex=True)
        else:
            TTBase = 0
        if show:
            print("TTpye: %s : %s : %s %s" % (
                self.val_format[TTypeformat],
                self.val_mode[TTypemode],
                str(TTBase),
                hex(self.gcc_except_tableVA + index + TTBase)))

        CallSiteformat, CallSitemode = self.format_enc(gccChunk[index])
        index += 1
        CallSiteTableSize, index = self.uleb128_decode(gccChunk, index, addIndex=True)
        if show:
            print("CallSite: %s : %s CallSiteTableSize: %s" % (
                self.val_format[CallSiteformat], self.val_mode[CallSitemode], hex(CallSiteTableSize)))
        ActionTablePosition = index + CallSiteTableSize

        CallSites = list()
        while index < ActionTablePosition:
            CallSitePosition, index = self.decode_value(CallSiteformat, CallSitemode, gccChunk, index,
                                                         self.gcc_except_tableVA + index, frame_base)
            CallSiteLength, index = self.decode_value(CallSiteformat, CallSitemode, gccChunk, index,
                                                       self.gcc_except_tableVA + index, frame_base)
            LandingPadPosition, index = self.decode_value(CallSiteformat, CallSitemode, gccChunk, index,
                                                           self.gcc_except_tableVA + index, frame_base)
            FirstAction, index = self.uleb128_decode(gccChunk, index, addIndex=True)
            if LandingPadPosition == 0:
                found_type = "found_nothing"
            elif FirstAction == 0:
                found_type = "found_cleanup"
            else:  # 否则还要进一步通过Action来判断
                found_type = "found_cleanup | handler"
            # 如果frame是跨函数的话，要求这几个函数仍然要是相邻的
            # 在每个函数内部，需要按照callsite来划分，然后newValue要重新排序写进去，并更新相应的landingpad。
            # 最后，因为leb128编码方式的存在，call site table的长度可能改变，所以还要改变header里的CallSiteTableSize字段
            # 因为call site中的pos都是基于frame的，所以如果frame整体不改变则call site无需改变，目前采用这种最简单的方式
            if show:
                print("CallSiteRange=(%s, %s), LandingPadPos=%s, firstAction=%s %s" % (
                    hex(frame_base + CallSitePosition),
                    hex(frame_base + CallSitePosition + CallSiteLength),
                    hex(frame_base + LandingPadPosition) if LandingPadPosition != 0 else hex(0),
                    hex(FirstAction),
                    found_type))
            CallSites.append(CallSite(CallSitePosition, CallSiteLength, LandingPadPosition, FirstAction,
                                      (frame_base + LandingPadPosition) if LandingPadPosition != 0 else 0))

        return LSDA(LPStartformat, LPStartmode, LPStart,
                    TTypeformat, TTypemode, TTBase,
                    CallSiteformat, CallSitemode, CallSiteTableSize, CallSites,
                    ActionTablePosition)


    def parseLSDA(self, show=False):
        # 判断是否有.gcc_except_table
        if not self.elffile.get_section_by_name(".gcc_except_table") or \
                not self.elffile.get_section_by_name(".eh_frame"):
            return

        # 从eh_frame中解析出gcc_except_table的地址
        gcc_except_tableSec = self.elffile.get_section_by_name(".gcc_except_table")
        fr = open(self.filePath, "rb")
        fr.seek(gcc_except_tableSec['sh_offset'], 0)
        gccBytes = fr.read(gcc_except_tableSec['sh_size'])
        fr.close()

        # 从fde中找到所有的lsda指针
        for entry in self.entryList:
            if isinstance(entry, FDE) and "lsda_pointer" in entry.augmentation_data:
                self.FDEsHasLSDA.append(entry)
                LSDA = self._parseLSDA(entry, gccBytes, show)
                self.lsdas.append(LSDA)

    def parse_eh_frame(self):

        def parseEntry(bytes, index, isShow=False):
            entryStart = index

            if isShow:
                print(hex(index), end="")

            # length(unit32 4B 0:4)
            length, index = self.uint32_decode(bytes, index, addIndex=True)

            entryEnd = index + length
            if isShow:
                print(" length: %s" % (hex(length)), end="")

            if length == 0:
                if isShow:
                    print(" ZERO terminator")
                return None, None, entryEnd

            dwarf_format = 64 if length == 0xFFFFFFFF else 32

            # CIE_id(unit32 4B 4:8): 常数0。该字段用于区分CIE和FDE，在FDE中该字段非0，为CIE_pointer
            if dwarf_format == 64:
                CIE_id, index = self.uint64_decode(bytes, index, addIndex=True)
            else:
                CIE_id, index = self.uint32_decode(bytes, index, addIndex=True)
            if isShow:
                print(" %s: %s (%s)" % ("CIE_id" if CIE_id==0 else "CIE_pointer", hex(CIE_id), "CIE" if CIE_id==0 else "FDE"))

            # CIE_id字段为0时表示该Entry为CIE
            if CIE_id == 0:
                cie = CIE()
                cie.set_bytes(bytes[entryStart : entryEnd])
                cie.set_length(length, [0, 4])
                cie.set_CIE_id(CIE_id, [4, index-entryStart])

                version, addIndex = self.uint8_decode(bytes, index, addIndex=False)
                cie.set_version(version, [index-entryStart, index+addIndex-entryStart])
                index += addIndex

                augmentation, addIndex = self.cstring_decode(bytes, index, addIndex=False)
                cie.set_augmentation_string(augmentation, [index-entryStart, index+addIndex-entryStart])
                index += addIndex
                # 默认是Dwarf v2, 以下两个字段是在v4中才引入的. pyelftools.structs._create_callframe_entry_headers中做了区分但默认使用v2
                # # address_size
                # address_size, index = self.dwarfParser.uint8_decode(bytes, index, addIndex=True)
                # # segment_size
                # segment_size, index = self.dwarfParser.uint8_decode(bytes, index, addIndex=True)

                code_alignment_factor, addIndex = self.uleb128_decode(bytes, index, addIndex=False)
                cie.set_code_alignment_factor(code_alignment_factor, [index-entryStart, index+addIndex-entryStart])
                index += addIndex

                data_alignment_factor, addIndex = self.sleb128_decode(bytes, index, addIndex=False)
                cie.set_data_alignment_factor(data_alignment_factor, [index-entryStart, index+addIndex-entryStart])
                index += addIndex

                return_address_register, addIndex = self.uleb128_decode(bytes, index, addIndex=False)
                cie.set_return_address_register(return_address_register, [index-entryStart, index+addIndex-entryStart])
                index += addIndex

                augmentation_data_stream = BytesIO()
                augmentation_data_stream.write(bytes[index:entryEnd])
                augmentation_data_stream.seek(0)
                self.aug_dict, aug_length = self.parse_cie_augmentation(augmentation, dwarf_format, augmentation_data_stream)
                cie.set_augmentation_data(self.aug_dict, [index-entryStart, index+aug_length-entryStart])
                augmentation_data = bytes[index : index+aug_length]
                index += aug_length

                initial_instructions = bytes[index:entryEnd]
                cie.set_initial_instruction(initial_instructions, [index-entryStart, entryEnd-entryStart])

                if isShow:
                    print(" Version: %s\n"
                          " Augmentation: %s\n"
                          " code_alignment_factor: %s\n"
                          " data_alignment_factor: %s\n"
                          " return_address_register: %s\n"
                          " augmentation_data: %s\n"
                          "  %s\n" % (
                        hex(version),
                        augmentation,
                        hex(code_alignment_factor),
                        hex(data_alignment_factor),
                        hex(return_address_register),
                        ' '.join('{:02x}'.format(b) for b in augmentation_data),
                        str(self.aug_dict)
                    ))

                return 0, cie, entryEnd

            # CIE_id字段非0时表示该Entry为FDE
            else:
                fde = FDE()
                fde.set_bytes(bytes[entryStart : entryEnd])
                fde.set_length(length, [0, 4])
                fde.set_CIE_pointer(CIE_id, [4, index-entryStart])

                # initial_location  由CIE.augmentation的R和CIE.augmentation_data决定，一般是1b，即4字节的pc-relative
                initFormat, initMode = self.format_enc(self.aug_dict["FDE_encoding"])
                initial_location, addIndex = self.decode_value(initFormat, initMode, bytes, index, self.eh_frameVA+index, 0, addIndex=False)
                fde.set_FDEEnc(initFormat, initMode)
                fde.set_initial_location(initial_location, [index-entryStart, index+addIndex-entryStart])
                index += addIndex

                address_range, addIndex = self.decode_value(initFormat, initMode, bytes, index, self.eh_frameVA + index, 0, addIndex=False, needOffset=True)
                fde.set_address_range(address_range, [index-entryStart, index+addIndex-entryStart])
                index += addIndex

                augmentation_data_length, addIndex = self.uleb128_decode(bytes, index, addIndex=False)
                fde.set_augmentation_data_length(augmentation_data_length, [index-entryStart, index+addIndex-entryStart])
                index += addIndex

                augmentation_data = bytes[index : index+augmentation_data_length]
                fde_aug_dict = self.parse_fde_augmentation(augmentation_data, self.eh_frameVA+index)
                fde.set_augmentation_data(fde_aug_dict, [index-entryStart, index+augmentation_data_length-entryStart])
                index += augmentation_data_length

                instructions = bytes[index:entryEnd]
                fde.set_instructions(instructions, [index-entryStart, entryEnd-entryStart])

                if isShow:
                    print(" initial_location: %s..%s\n"
                          " address_range: %s\n"
                          " augmentation_data_length: %s\n"
                          " augmentation_data: %s\n" % (
                        hex(initial_location),
                        hex(initial_location+address_range),
                        hex(address_range),
                        hex(augmentation_data_length),
                        ' '.join('{:02x}'.format(b) for b in augmentation_data)
                    ))

                return 1, fde, entryEnd

        if not self.elffile.get_section_by_name(".eh_frame"):
            return

        eh_frameSec = self.elffile.get_section_by_name(".eh_frame")
        fr = open(self.filePath, "rb")
        fr.seek(eh_frameSec['sh_offset'], 0)
        eh_frameChuck = fr.read(eh_frameSec['sh_size'])
        fr.close()

        index = 0
        self.aug_dict = None # 类函数和普通函数不同，类函数内定义的变量无法作用到内部函数中去，之前使用错误的使用global声明了aug_dict，导致多线程时出错。推荐的做法是self
        while index < len(eh_frameChuck):
            isFDE, entry, index = parseEntry(eh_frameChuck, index, isShow=False)
            if entry != None:
                self.entryList.append(entry)


    def parse_fde_augmentation(self, augmentation_data, VA):
        fde_aug_dict = dict()
        if "LSDA_encoding" in self.aug_dict:
            lsdaFormat, lsdaMode = self.format_enc(self.aug_dict["LSDA_encoding"])
            lsdaPointer, index = self.decode_value(lsdaFormat, lsdaMode, augmentation_data, 0, VA, 0)
            fde_aug_dict["lsda_pointer"] = lsdaPointer
        return fde_aug_dict


    def parse_cie_augmentation(self, augmentation, dwarf_format, augmentation_data_stream):
        """ Parse CIE augmentation data from the annotation string in `header`.

        Return a tuple that contains 1) the augmentation data as a string
        (without the length field) and 2) the augmentation data as a dict.
        """
        if not augmentation:
            return ('', {})

        entry_structs = DWARFStructs(
            little_endian=self.dwarfConfig.little_endian,
            dwarf_format=dwarf_format,
            address_size=self.dwarfConfig.default_address_size)

        # Augmentation parsing works in minimal mode here: we need the length
        # field to be able to skip unhandled augmentation fields.
        assert augmentation.startswith('z'), (
            'Unhandled augmentation string: {}'.format(repr(augmentation)))

        available_fields = {
            'z': entry_structs.Dwarf_uleb128('length'),
            'L': entry_structs.Dwarf_uint8('LSDA_encoding'),
            'R': entry_structs.Dwarf_uint8('FDE_encoding'),
            'S': True,
            'P': Struct(
                'personality',
                entry_structs.Dwarf_uint8('encoding'),
                Switch('function', lambda ctx: ctx.encoding & 0x0f, {
                    enc: fld_cons('function')
                    for enc, fld_cons
                    in self.callFrameInfo._eh_encoding_to_field(entry_structs).items()})),
        }

        # Build the Struct we will be using to parse the augmentation data.
        # Stop as soon as we are not able to match the augmentation string.
        fields = []
        aug_dict = {}

        for b in iterbytes(augmentation):
            try:
                fld = available_fields[b]
            except KeyError:
                break

            if fld is True:
                aug_dict[fld] = True
            else:
                fields.append(fld)

        # Read the augmentation twice: once with the Struct, once for the raw
        # bytes. Read the raw bytes last so we are sure we leave the stream
        # pointing right after the augmentation: the Struct may be incomplete
        # (missing trailing fields) due to an unknown char: see the KeyError
        # above.
        struct = Struct('Augmentation_Data', *fields)
        aug_dict.update(struct.parse_stream(augmentation_data_stream))
        return aug_dict, augmentation_data_stream.tell()

    # ====================Tool Funcs=========================

    val_format = {
        0x00: "DW_EH_PE_ptr",
        0x01: "DW_EH_PE_uleb128",
        0x02: "DW_EH_PE_udata2",
        0x03: "DW_EH_PE_udata4",
        0x04: "DW_EH_PE_udata8",
        0x08: "DW_EH_PE_signed",
        0x09: "DW_EH_PE_sleb128",
        0x0A: "DW_EH_PE_sdata2",
        0x0B: "DW_EH_PE_sdata4",
        0x0C: "DW_EH_PE_sdata8",
        0xFF: "DW_EH_PE_omit"
    }
    val_mode = {
        0x00: "DW_EH_PE_absptr",
        0x10: "DW_EH_PE_pcrel",
        0x20: "DW_EH_PE_textrel",
        0x30: "DW_EH_PE_datarel",
        0x40: "DW_EH_PE_funcrel",
        0x50: "DW_EH_PE_aligned",
        0xFF: "DW_EH_PE_omit"
    }

    DW_EH_PE_ptr = 0x00
    DW_EH_PE_uleb128 = 0x01
    DW_EH_PE_udata2 = 0x02
    DW_EH_PE_udata4 = 0x03
    DW_EH_PE_udata8 = 0x04
    DW_EH_PE_signed = 0x08
    DW_EH_PE_sleb128 = 0x09
    DW_EH_PE_sdata2 = 0x0A
    DW_EH_PE_sdata4 = 0x0B
    DW_EH_PE_sdata8 = 0x0C

    DW_EH_PE_absptr = 0x00
    DW_EH_PE_pcrel = 0x10
    DW_EH_PE_textrel = 0x20
    DW_EH_PE_datarel = 0x30
    DW_EH_PE_funcrel = 0x40
    DW_EH_PE_aligned = 0x50

    DW_EH_PE_indirect = 0x80
    DW_EH_PE_omit = 0xFF

    def ULInt8_encode(self, value):
        return struct.pack("<B", value), 1

    def ULInt16_encode(self, value):
        return struct.pack("<H", value), 2

    def ULInt32_encode(self, value):
        return struct.pack("<I", value), 4

    def ULInt64_encode(self, value):
        return struct.pack("<Q", value), 8

    def SLInt8_encode(self, value):
        return struct.pack("<b", value), 1

    def SLInt16_encode(self, value):
        return struct.pack("<h", value), 2

    def SLInt32_encode(self, value):
        return struct.pack("<i", value), 4

    def SLInt64_encode(self, value):
        return struct.pack("<q", value), 8

    def UBInt8_encode(self, value):
        return struct.pack(">B", value), 1

    def UBInt16_encode(self, value):
        return struct.pack(">H", value), 2

    def UBInt32_encode(self, value):
        return struct.pack(">I", value), 4

    def UBInt64_encode(self, value):
        return struct.pack(">Q", value), 8

    def SBInt8_encode(self, value):
        return struct.pack(">b", value), 1

    def SBInt16_encode(self, value):
        return struct.pack(">h", value), 2

    def SBInt32_encode(self, value):
        return struct.pack(">i", value), 4

    def SBInt64_encode(self, value):
        return struct.pack(">q", value), 8

    def ULInt8_decode(self, bytes, index, addIndex=False):
        return struct.unpack("<B", bytes[index:index+1])[0], 1+index if addIndex else 1

    def ULInt16_decode(self, bytes, index, addIndex=False):
        return struct.unpack("<H", bytes[index:index+2])[0], 2+index if addIndex else 2

    def ULInt32_decode(self, bytes, index, addIndex=False):
        return struct.unpack("<I", bytes[index:index+4])[0], 4+index if addIndex else 4

    def ULInt64_decode(self, bytes, index, addIndex=False):
        return struct.unpack("<Q", bytes[index:index+8])[0], 8+index if addIndex else 8

    def SLInt8_decode(self, bytes, index, addIndex=False):
        return struct.unpack("<b", bytes[index:index+1])[0], 1+index if addIndex else 1

    def SLInt16_decode(self, bytes, index, addIndex=False):
        return struct.unpack("<h", bytes[index:index+2])[0], 2+index if addIndex else 2

    def SLInt32_decode(self, bytes, index, addIndex=False):
        try:
            return struct.unpack("<i", bytes[index:index+4])[0], 4+index if addIndex else 4
        except:
            a = 1

    def SLInt64_decode(self, bytes, index, addIndex=False):
        return struct.unpack("<q", bytes[index:index+8])[0], 8+index if addIndex else 8

    def UBInt8_decode(self, bytes, index, addIndex=False):
        return struct.unpack(">B", bytes[index:index+1])[0], 1+index if addIndex else 1

    def UBInt16_decode(self, bytes, index, addIndex=False):
        return struct.unpack(">H", bytes[index:index+2])[0], 2+index if addIndex else 2

    def UBInt32_decode(self, bytes, index, addIndex=False):
        return struct.unpack(">I", bytes[index:index+4])[0], 4+index if addIndex else 4

    def UBInt64_decode(self, bytes, index, addIndex=False):
        return struct.unpack(">Q", bytes[index:index+8])[0], 8+index if addIndex else 8

    def SBInt8_decode(self, bytes, index, addIndex=False):
        return struct.unpack(">b", bytes[index:index+1])[0], 1+index if addIndex else 1

    def SBInt16_decode(self, bytes, index, addIndex=False):
        return struct.unpack(">h", bytes[index:index+2])[0], 2+index if addIndex else 2

    def SBInt32_decode(self, bytes, index, addIndex=False):
        return struct.unpack(">i", bytes[index:index+4])[0], 4+index if addIndex else 4

    def SBInt64_decode(self, bytes, index, addIndex=False):
        return struct.unpack(">q", bytes[index:index+8])[0], 8+index if addIndex else 8

    def LPtr_encode(self, value):
        if self.dwarfConfig.default_address_size == 8: # 64位
            format = "<Q"
            length = 8
        else:                               # 32位
            format = "<I"
            length = 4
        return struct.pack(format, value), length

    def BPtr_encode(self, value):
        if self.dwarfConfig.default_address_size == 8: # 64位
            format = "<Q"
            length = 8
        else:                               # 32位
            format = "<I"
            length = 4
        return struct.pack(format, value), length

    def LPtr_decode(self, bytes, index):
        if self.dwarfConfig.default_address_size == 8: # 64位
            format = "<Q"
            length = 8
        else:                               # 32位
            format = "<I"
            length = 4
        return struct.unpack(format, bytes[index:index+length])[0], length

    def BPtr_decode(self, bytes, index):
        if self.dwarfConfig.default_address_size == 8: # 64位
            format = "<Q"
            length = 8
        else:                               # 32位
            format = "<I"
            length = 4
        return struct.unpack(format, bytes[index:index+8])[0], length

    def cstring_decode(self, bytes, index, addIndex=False):
        retu_str = ""
        length_str = 0
        while True:
            if bytes[index+length_str] != 0:
                retu_str += chr(bytes[index+length_str])
                length_str += 1
            else:
                length_str += 1
                break
        return retu_str, length_str+index if addIndex else length_str


    def leb128_decode(self, bytes, index, signed):
        orig_index = index

        # 拼接出来
        bits = bitarray()
        while (1):
            bit7 = bitarray()
            byte = bytes[index]
            bit7.frombytes(byte.to_bytes(1, byteorder='little'))
            bits = bit7[1:] + bits

            if bit7[0] == False:
                index += 1
                break
            index += 1

        if len(bits) > 64:
            logging.error("leb编码的数据长度超过64bit")
            exit(1)

        # 根据高位是否为1，来进行高位填充
        bits_retu = bitarray()
        for i in range(64):
            bits_retu.append(True if signed and bits[0] == True else False)
        offset = 64 - len(bits)
        for i in range(len(bits)):
            bits_retu[offset + i] = bits[i]

        return struct.unpack(">q" if signed else ">Q", bits_retu.tobytes())[0], index - orig_index

    def uleb128_decode(self, bytes, index, addIndex=False):
        value, indexAdd = self.leb128_decode(bytes, index, False)
        if addIndex:
            return value, indexAdd + index
        else:
            return value, indexAdd

    def sleb128_decode(self, _bytes, index, addIndex=False):
        value, indexAdd = self.leb128_decode(_bytes, index, True)
        if addIndex:
            return value, indexAdd + index
        else:
            return value, indexAdd

    def uleb128_encode(self, value):
        bytes = leb128.u.encode(value)
        return bytes, len(bytes)

    def sleb128_encode(self, value):
        bytes = leb128.i.encode(value)
        return bytes, len(bytes)


    # def getLandingPad(self):
    #     for callSite in self.CallSites:
    #         if callSite.found_type != CallSite.found_nothing:
    #
    #
    #         if callSite.LandingPadPosition == 0:
    #             found_type = CallSite.found_nothing
    #         elif callSite.FirstAction == 0:
    #             found_type =
    #         else:  # 否则还要进一步通过Action来判断
    #             found_type = "found_cleanup | handler"
    #
    #         if found_type != "found_nothing"
    #
    #         if callSite.LandingPadPosition


if __name__ == '__main__':
    disass = RecursiveDisass("/ccr/code/x64/main2")
    disass.disassText()