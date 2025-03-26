from collections import defaultdict
from Other.benchmarkPerformanceEvaluation import myThread
from Other.pointerEvaluation.tools import *
from capstone.x86 import *
from capstone.arm64 import *
import shuffleInfo_pb2 as NP
import elfParser
import unit
import constants as C
from capStr import *
import sys


"""
对于pie-large来说：
1. 缺失jpt： 因为模式不一样所以jpt都没有识别出来 & rand中误收集了一些非jpt的指针数组

2. data节非jpt： 目前没有发现 & 绝对指针
3. text节非jpt的指针： mov num,reg导致缺失的 & rip，call，jmp，绝对指针
"""

def show(elf, retu):
    print(">>> " + elf)
    print("===========CODE=============")
    print("C2C: %d C2D: %d" % (retu[0][0], retu[0][1]))
    print("-----control transfer------")
    for opcode in retu[0][2]:
        print("%s: %d" % (x86opcodeStr(opcode), retu[0][2][opcode]))
    print("-----MEM instruction------")
    for opcode in retu[0][3]:
        print("%s: %d" % (x86opcodeStr(opcode), retu[0][3][opcode]))
    print("-----NO MEM instruction------")
    for opcode in retu[0][4]:
        print("%s: %d" % (x86opcodeStr(opcode), retu[0][4][opcode]))
    # print("---------addressmode--------------------")
    # for addressmode in retu[0][5]:
    #     print("%s: %d" % (base_type_str(addressmode), retu[0][5][addressmode]))
    print("---------reloc--------------------")
    for addressmode in retu[0][6]:
        print("%s: %d" % (addressmode, retu[0][6][addressmode]))

    print("\n===========DATA=============")
    print("D2C: %d D2D: %d" % (retu[1][0], retu[1][1]))
    print("---------padding---------")
    for padding in retu[1][2]:
        print("%s: %d" % (padding, retu[1][2][padding]))
    # print("--------addressmode------")
    # for addressmode in retu[1][3]:
    #     print("%s: %d" % (base_type_str(addressmode), retu[1][3][addressmode]))
    print("---------reloc--------------------")
    for addressmode in retu[1][4]:
        print("%s: %d" % (addressmode, retu[1][4][addressmode]))




def pointer_state_finish():
    """
    [C2C, C2D, dict(C_insJMP), dict(C_insMEM), dict(C_insNOMEM), dict(C_addressmode), dict(C_reloc)],
    [D2C, D2D, dict(D_padding), dict(D_addressmode), dict(D_reloc)]
    """
    C_insMEM = defaultdict(int)
    C_insNOMEM = defaultdict(int)

    for elf in pointer_state:
        retu = pointer_state[elf]
        for opcode in retu[0][3]:
            C_insMEM[opcode] += retu[0][3][opcode]
        for opcode in retu[0][4]:
            C_insNOMEM[opcode] += retu[0][4][opcode]

    print("-----MEM instruction------")
    for opcode in C_insMEM:
        print("%s: %d" % (x86opcodeStr(opcode), C_insMEM[opcode]))
    print("-----NO MEM instruction------")
    for opcode in C_insNOMEM:
        print("%s: %d" % (x86opcodeStr(opcode), C_insNOMEM[opcode]))

    fw.close()


pointer_state = {}
def pointer_state_analysis(elf_path, dataIndex=-1, threadNum=-1):
    def inRange(VA, range):
        idx = 0
        for startVA, endVA, region in range:
            if startVA <= VA < endVA:
                return idx
            idx += 1
        return None

    def readFixup(fixups):
        for fixup_idx, fixup in enumerate(fixups):
            fixup_va = _elfParser.section_ranges_idx[fixup.section][0] + fixup.offset

            _type = fixup.type
            baseType = _type & 3
            targetType = (_type >> 2) & 3
            isJumpTable = (_type >> 6) & 1
            isFromRand = (_type >> 7) & 1
            isFromReloc = (_type >> 8) & 1
            isFromGOT = (_type >> 9) & 1
            reloc_type_num = (_type >> 16) & 0xffff
            reloc_type = C.relocDict[reloc_type_num][0]

            if fixup.section not in randFixupSection:
                randFixupRange.append(_elfParser.getSectionRangesIdx(fixup.section))

            reloc_type = C.relocDict[reloc_type_num][0]

            base_addr = None
            if baseType == 2:
                if fixup.base_section:
                    base_addr = _elfParser.section_ranges_idx[fixup.base_section][0] + fixup.base_bbl_sym
                else:
                    base_addr = fixup.base_bbl_sym
                base_str = 'Base:({}), '.format(hex(base_addr))
            else:
                base_str = ""

            target_addr = None
            if targetType == 2:
                type = "VALUE"
                if fixup.target_section:
                    target_addr = _elfParser.section_ranges_idx[fixup.target_section][0] + fixup.target_bbl_sym
                else:
                    target_addr = fixup.target_bbl_sym
            else:
                print("fixup {}的targetType不为2 {}".format(hex(fixup_va), targetType))
                exit(233)
            target_str = 'Target:({}),'.format(hex(target_addr))

            if fixup.info:
                sec_str = fixup.info
            else:
                try:
                    sec_str = _elfParser.section_name[fixup.section]
                except:
                    sec_str = "Unknown " + str(fixup.section)

            fixup_str = "Fixup#%4d VA:0x%04x, Offset:0x%04x, Reloc:%s, %s%s add:0x%04x (@Sec %s)%s%s%s%s%d" % \
                        (fixup_idx,
                         fixup_va,
                         fixup.offset,
                         reloc_type,
                         base_str,
                         target_str,
                         fixup.add,
                         sec_str,
                         " (JMPTBL)" if isJumpTable else "",
                         " (RAND)" if isFromRand else "",
                         " (RELOC)" if isFromReloc else "",
                         " (GOT)" if isFromGOT else "",
                         fixup.step)

            gtFixups[fixup_va] = [base_addr, target_addr, reloc_type_num, reloc_type, fixup_str]

    def readSectionContent(secName):
        for sec in _elfParser.elf.iter_sections():
            if sec.name == secName:
                content = open(_elfParser.fn, 'rb').read()
                secSize = sec['sh_size']
                secAddr = sec['sh_addr']
                secOff = sec['sh_offset']
                secRegion = content[secOff: secOff + secSize]
                return secAddr, secSize, secRegion
        return 0, 0, None

    if dataIndex != -1:
        print("[%d] %s" % (dataIndex, elf_path))

    # Step 1. 读取、解析、处理元数据
    C.relocDict = C.aarch64_reloc_dict
    status, fixedMetadata = unit.FixedMetadata.fixedMetadataFactory(elf_path, fast=True)
    _elfParser = fixedMetadata.elfParser
    gtFixups = dict() # 读取待分析的fixup
    randFixupRange = list()
    randFixupSection = set()
    readFixup(fixedMetadata.fixups)
    readFixup(fixedMetadata.otherfixups)

    # Step 2. 读取Reassembly的指针结果
    pass # 非比对，仅统计

    # Step 3. 划定处理的范围，建立MultiRandom指针放弃表以及DDisasm指针放弃表
    textStartVA, textEndVA = _elfParser.section_ranges['.text']
    textAddr, textSize, textRegion = readSectionContent(".text")
    codeRange = [[textStartVA, textEndVA, textRegion]]

    dataStartVA, dataEndVA = _elfParser.section_ranges['.data']
    dataAddr, dataSize, dataRegion = readSectionContent(".data")
    rodataStartVA, rodataEndVA = _elfParser.section_ranges['.rodata']
    rodataAddr, rodataSize, rodataRegion = readSectionContent(".rodata")
    dataRange = [[dataStartVA, dataEndVA, dataRegion],
                 [rodataStartVA, rodataEndVA, rodataRegion]]

    mroutRangePtr = []
    raoutRangePtr = []

    # Step 4. 准备对比所需的信息其他信息
    relas = get_relas(elf_path) # 存储动态重定位节中指针，在出现FP的时候比对判断
    execRange = _elfParser.getExecSectionRange()
    ins_dict = get_ins_objdump(elf_path)

    # Step 5. 开始比对(仅统计)
    C2C = 0
    C2D = 0
    C_insJMP = defaultdict(int) # control transfer instruction : num
    C_insMEM = defaultdict(int) # no cti & memory instruction_opcode : num
    C_insNOMEM = defaultdict(int) # no cti & no memory instruction_opcode : num
    C_addressmode = defaultdict(int) # addressing_mode : num
    C_reloc = defaultdict(int)
    D2C = 0
    D2D = 0
    D_padding = defaultdict(int) # padding : num
    D_addressmode = defaultdict(int) # addressing_mode : num
    D_reloc = defaultdict(int)

    for VA in gtFixups:
        base_addr, target_addr, reloc_type_num, reloc_type, fixup_str = gtFixups[VA]
        detailPtrInfo = C.x64_reloc_dict[reloc_type_num]

        # Step 5.1 处理Code Pointer
        idx = inRange(VA, codeRange) # Source采用粗分类，以过滤掉一些指针
        if idx != None:
            C_addressmode[detailPtrInfo[5].value] += 1
            C_reloc[detailPtrInfo[0]] += 1
            if inRange(target_addr, execRange): # 这都是过滤后留下来的经典指针，后续要处理了所以Target采用细分类
                C2C += 1
            else:
                C2D += 1
            
            # Step 5.1.1 进一步分类Code Pointer的来源
            insVA, obj_ins = get_ins_from_pointerVA(ins_dict, VA)
            capInst = disasm_ins(obj_ins, insVA, C.X64)
            # Case 1. 控制流转移指令
            if unit.RecursiveDisass.Tools.isControlFlowInst(capInst):
                C_insJMP[capInst.id] += 1
                continue

            # Case 2. 特定的内存访问指令
            findMem = False
            for op in capInst.operands:
                if op.type == X86_OP_MEM:
                    findMem = True
            if findMem:
                C_insMEM[capInst.id] += 1
                continue

            # Case 3. 非特定内存访问指令
            C_insNOMEM[capInst.id] += 1
            print("{} {}".format(hex(VA), x86opcodeStr(capInst.id)))
            continue

        # Step 5.2 处理Data Pointer
        idx = inRange(VA, dataRange)
        if idx != None:
            D_addressmode[detailPtrInfo[5].value] += 1
            D_reloc[detailPtrInfo[0]] += 1
            if VA % 8 == 0:
                D_padding[8] += 1
            elif VA % 4 == 0:
                D_padding[4] += 1
            elif VA % 2 == 0:
                D_padding[2] += 1
            else:
                D_padding[1] += 1
            if inRange(target_addr, execRange): # 这都是过滤后留下来的经典指针，后续要处理了所以Target采用细分类
                D2C += 1
            else:
                D2D += 1
            continue

        # Step 5.3 没有归类的纳入mroutRangePtr
        mroutRangePtr.append([VA, _elfParser.getSectionByVA(VA)])

    retu =[[C2C, C2D, dict(C_insJMP), dict(C_insMEM), dict(C_insNOMEM), dict(C_addressmode), dict(C_reloc)],
            [D2C, D2D, dict(D_padding), dict(D_addressmode), dict(D_reloc)]]
    pointer_state[elf_path] = retu

    if len(C_insNOMEM) != 0:
        print("-----NO MEM instruction------")
        print(">>> %s" % (elf_path))
        for opcode in retu[0][4]:
            print("%s: %d" % (x86opcodeStr(opcode), retu[0][4][opcode]))

    if dataIndex == -1:
        show(elf_path, retu)
        print(len(mroutRangePtr))
    else:
        savedStdout = sys.stdout
        sys.stdout = fw
        show(elf_path, retu)
        sys.stdout = savedStdout


if __name__ == '__main__':

    elfList = []

    # 遍历单层目录 /E/binaryset/binaries-spec-arm64/O3/
    binDir = "/E/binaryset/binaries-spec/"
    for exe in os.listdir(binDir):
        exePath = binDir+"/"+exe

        # 要求该文件是elf可执行文件
        retu = subprocess.getstatusoutput("readelf -SW {}".format(exePath))[1]
        if "Failed" in retu or "错误" in retu:
            continue
        elfList.append(exePath)

    # 遍历双层目录 /E/binaryset/binaries-spec-arm64/
    # binDir = "/E/binaryset/binaries-spec-arm64/"
    # for path in os.listdir(binDir):
    #     if path.startswith("!"):
    #         continue
    #
    #     binBuildPath = binDir + path
    #
    #     for exe in os.listdir(binBuildPath):
    #         exePath = binBuildPath+"/"+exe
    #
    #         # 要求该文件是elf可执行文件
    #         retu = subprocess.getstatusoutput("readelf -SW {}".format(exePath))[1]
    #         if "Failed" in retu or "错误" in retu:
    #             continue
    #         elfList.append(exePath)

    # fw = open("Result.txt", "w")
    # thread = myThread.myThread(elfList, pointer_state_analysis, poolNum=8, onFinish=pointer_state_finish) # , onFinish=pointer_state_finish
    # thread.start()

    pointer_state_analysis("/E/binaryset/binaries-spec-arm64/!temp/502-gcc_r-cpugcc_r")
    # pointer_state_analysis("/E/binaryset/binaries-spec-arm64/gcc_O3pie/ffmpeg_g")