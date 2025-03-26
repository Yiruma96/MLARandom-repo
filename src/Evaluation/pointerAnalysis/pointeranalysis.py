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
import traceback


"""
对于pie-large来说：
1. 缺失jpt： 因为模式不一样所以jpt都没有识别出来 & rand中误收集了一些非jpt的指针数组

2. data节非jpt： 目前没有发现 & 绝对指针
3. text节非jpt的指针： mov num,reg导致缺失的 & rip，call，jmp，绝对指针
"""

def show(elf, retu):
    print(">>> " + elf)

    # [C2C, C2D, dict(C_insJMP), dict(C_insJMP_reloc), dict(C_insMEM), dict(C_insMEM_reloc), dict(C_insNOMEM), dict(C_insNOMEM_reloc)]
    print("===========CODE=============")
    print("C2C: %d C2D: %d" % (retu[0][0], retu[0][1]))

    print("-----control transfer------")
    control_num = 0
    for opcode in retu[0][2]:
        control_num += retu[0][2][opcode]
        print("%s: %d" % (arm64opcodeStr(opcode), retu[0][2][opcode]))
    print("all control num: %d" % (control_num))
    for reloc in retu[0][3]:
        print("%s: %d" % (reloc, retu[0][3][reloc]))

    print("-----MEM instruction------")
    mem_num = 0
    for opcode in retu[0][4]:
        mem_num += retu[0][4][opcode]
        print("%s: %d" % (arm64opcodeStr(opcode), retu[0][4][opcode]))
    print("all mem num: %d" % (mem_num))
    for reloc in retu[0][5]:
        print("%s: %d" % (reloc, retu[0][5][reloc]))

    print("-----NO MEM instruction------")
    no_mem_num = 0
    for opcode in retu[0][6]:
        no_mem_num += retu[0][6][opcode]
        print("%s: %d" % (arm64opcodeStr(opcode), retu[0][6][opcode]))
    print("all no mem num: %d" % (no_mem_num))
    for reloc in retu[0][7]:
        print("%s: %d" % (reloc, retu[0][7][reloc]))


    # [D2C, D2D, DIC, D_JPT_num, dict(D_JPT_reloc), D_AbsPtr_num, dict(D_AbsPtr_reloc), D_OtherData_num, dict(D_Other_reloc), dict(D_padding)]
    print("\n===========DATA=============")
    print("D2C: %d D2D: %d DIC: %d\n" % (
        retu[1][0], retu[1][1], retu[1][2]))

    print("-----JPT Data Pointer--{}----".format(retu[1][3]))
    for reloc in retu[1][4]:
        print("%s: %d" % (reloc, retu[1][4][reloc]))

    print("-----Abs Data Pointer--{}----".format(retu[1][5]))
    for reloc in retu[1][6]:
        print("%s: %d" % (reloc, retu[1][6][reloc]))

    print("-----Other Data Pointer--{}----".format(retu[1][7]))
    for reloc in retu[1][8]:
        print("%s: %d" % (reloc, retu[1][8][reloc]))

    print("---------padding---------")
    for padding in retu[1][9]:
        print("%s: %d" % (padding, retu[1][9][padding]))


    # print("--------addressmode------")
    # for addressmode in retu[1][3]:
    #     print("%s: %d" % (base_type_str(addressmode), retu[1][3][addressmode]))





def pointer_state_finish():
    """
    [C2C, C2D, dict(C_insJMP), dict(C_insJMP_reloc), dict(C_insMEM), dict(C_insMEM_reloc), dict(C_insNOMEM), dict(C_insNOMEM_reloc)]
    [D2C, D2D, DIC, D_JPT_num, dict(D_JPT_reloc), D_AbsPtr_num, dict(D_AbsPtr_reloc), D_OtherData_num, dict(D_Other_reloc), dict(D_padding)]
    """

    def dict_add(input_dict, output_dict):
        for input in input_dict:
            if input not in output_dict:
                output_dict[input] = input_dict[input]
            else:
                output_dict[input] += input_dict[input]
        return output_dict

    pointer_state_all = [[0,0,{},{},{},{},{},{}], [0,0,0,0,{},0,{},0,{},{}]]
    for elf in pointer_state:
        retu = pointer_state[elf]
        text_retu = retu[0]
        data_retu = retu[1]

        pointer_state_all[0][0] += text_retu[0]
        pointer_state_all[0][1] += text_retu[1]
        dict_add(text_retu[2], pointer_state_all[0][2])
        dict_add(text_retu[3], pointer_state_all[0][3])
        dict_add(text_retu[4], pointer_state_all[0][4])
        dict_add(text_retu[5], pointer_state_all[0][5])
        dict_add(text_retu[6], pointer_state_all[0][6])
        dict_add(text_retu[7], pointer_state_all[0][7])

        pointer_state_all[1][0] += data_retu[0]
        pointer_state_all[1][1] += data_retu[1]
        pointer_state_all[1][2] += data_retu[2]
        pointer_state_all[1][3] += data_retu[3]
        dict_add(data_retu[4], pointer_state_all[1][4])
        pointer_state_all[1][5] += data_retu[5]
        dict_add(data_retu[6], pointer_state_all[1][6])
        pointer_state_all[1][7] += data_retu[7]
        dict_add(data_retu[8], pointer_state_all[1][8])
        dict_add(data_retu[9], pointer_state_all[1][9])

    show("All", pointer_state_all)

    print("================")


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

    def getInstFromCodePtr(VA):
        idx = inRange(VA, codeRange)
        if idx == None:
            return None

        codeSecStartVA, codeSecEndVA, codeSecRegion = codeRange[idx]
        ins_bytes = codeSecRegion[VA-codeSecStartVA : VA-codeSecStartVA+4]

        md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
        md.detail = True
        ins = None
        for i in md.disasm(ins_bytes, VA):
            ins = i
            continue
        if ins == None:
            # 应该是遇到了Data Pointer
            return None
        else:
            return ins

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

    def readFun(funsProto):
        funs = set()
        for fun in funsProto:
            funVA = textAddr + fun.offset
            funs.add(funVA)
        return funs

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
        print("[%d] Start %s" % (dataIndex, elf_path))

    # Step 1. 解析元数据
    C.relocDict = C.aarch64_reloc_dict
    status, fixedMetadata = unit.FixedMetadata.fixedMetadataFactory(elf_path, fast=True)
    _elfParser = fixedMetadata.elfParser

    # Step 2. 划定处理的范围，建立MultiRandom指针放弃表以及DDisasm指针放弃表
    textStartVA, textEndVA = _elfParser.section_ranges['.text']
    textAddr, textSize, textRegion = readSectionContent(".text")
    codeRange = [[textStartVA, textEndVA, textRegion]]

    dataStartVA, dataEndVA = _elfParser.section_ranges['.data']
    dataAddr, dataSize, dataRegion = readSectionContent(".data")
    rodataStartVA, rodataEndVA = _elfParser.section_ranges['.rodata']
    rodataAddr, rodataSize, rodataRegion = readSectionContent(".rodata")
    dataRange = [[dataStartVA, dataEndVA, dataRegion],
                 [rodataStartVA, rodataEndVA, rodataRegion]]

    # Step 3. 读取元数据
    gtFixups = dict() # 读取待分析的fixup
    randFixupRange = list()
    randFixupSection = set()
    readFixup(fixedMetadata.fixups)
    readFixup(fixedMetadata.otherfixups)
    # gtFuns = readFun(fixedMetadata.funs)

    mroutRangePtr = []
    raoutRangePtr = []

    # Step 4. 准备对比所需的信息其他信息
    # ins_dict = get_ins_objdump(elf_path) # 我们直接用objdump的结果
    relas = get_relas(elf_path) # 存储动态重定位节中指针，在出现FP的时候比对判断
    execRange = _elfParser.getExecSectionRange()

    # Step 5. 开始比对(仅统计)
    C2C = 0
    C2D = 0
    DIC = 0
    C_insJMP = defaultdict(int) # control transfer instruction : num
    C_insJMP_reloc = defaultdict(int)
    C_insMEM = defaultdict(int) # no cti & memory instruction_opcode : num
    C_insMEM_reloc = defaultdict(int)
    C_insNOMEM = defaultdict(int) # no cti & no memory instruction_opcode : num
    C_insNOMEM_reloc = defaultdict(int)
    D2C = 0
    D2D = 0
    D_padding = defaultdict(int) # padding : num
    D_reloc = defaultdict(int)
    D_JPT_num = 0
    D_JPT_reloc = defaultdict(int)
    D_AbsPtr_num = 0
    D_AbsPtr_reloc = defaultdict(int)
    D_OtherData_num = 0
    D_Other_reloc = defaultdict(int)

    for VA in gtFixups:
        base_addr, target_addr, reloc_type_num, reloc_type, fixup_str = gtFixups[VA]
        detailPtrInfo = C.aarch64_reloc_dict[reloc_type_num]

        codeIdx = inRange(VA, codeRange) # Source采用粗分类，以过滤掉一些指针. 同时我们过滤掉R_AARCH64_ABS64
        # Step 5.1 处理Data in Code
        isDIC = False
        if codeIdx != None and reloc_type_num == 257:
            DIC += 1
            isDIC = True

        # Step 5.1 处理Code Pointer
        if codeIdx != None and isDIC == False:
            # C_addressmode[detailPtrInfo[5].value] += 1
            # C_reloc[detailPtrInfo[0]] += 1
            if inRange(target_addr, execRange):
                C2C += 1
            else:
                C2D += 1
            
            # Step 5.1.1 进一步分类Code Pointer的来源
            capInst = getInstFromCodePtr(VA)
            if capInst == None:
                print("[ERROR] Code Pointer无法在正确反汇编 {}".format(hex(VA)))
                exit(0x233)

            # Case 1. 控制流转移指令
            if unit.RecursiveDisass.Tools.isControlFlowInst(capInst):
                C_insJMP_reloc[detailPtrInfo[0]] += 1
                C_insJMP[capInst.id] += 1
                continue

            # Case 2. 特定的内存访问指令
            findMem = False
            for op in capInst.operands:
                if op.type == ARM64_OP_MEM:
                    findMem = True
            if findMem:
                C_insMEM_reloc[detailPtrInfo[0]] += 1
                C_insMEM[capInst.id] += 1
                continue

            # Case 3. 非特定内存访问指令
            C_insNOMEM_reloc[detailPtrInfo[0]] += 1
            C_insNOMEM[capInst.id] += 1
            continue

        # Step 5.2 处理Data Pointer
        dataIdx = inRange(VA, dataRange)
        if dataIdx != None or isDIC:
            # D_addressmode[detailPtrInfo[5].value] += 1
            # D_reloc[detailPtrInfo[0]] += 1
            if inRange(target_addr, execRange): # 这都是过滤后留下来的经典指针，后续要处理了所以Target采用细分类
                D2C += 1
            else:
                D2D += 1

            # Step 5.2.1 进一步分类Data Pointer的Padding
            if VA % 8 == 0:
                D_padding[8] += 1
            elif VA % 4 == 0:
                D_padding[4] += 1
            elif VA % 2 == 0:
                D_padding[2] += 1
            else:
                D_padding[1] += 1

            # Step 5.2.2 进一步分类Data Pointer的来源
            # Case 1. JPT Pointer
            if base_addr != None:
                D_JPT_reloc[detailPtrInfo[0]] += 1
                D_JPT_num += 1
            # Case 2. Abs Data Pointer (func ptr or var ptr)
            elif reloc_type_num == 257:
                # if dataIndex == -1:
                #     print(fixup_str)
                D_AbsPtr_reloc[detailPtrInfo[0]] += 1
                D_AbsPtr_num += 1
            # Case 3. Other Data Pointer
            else:
                # if dataIndex == -1:
                #     print(fixup_str)
                D_Other_reloc[detailPtrInfo[0]] += 1
                D_OtherData_num += 1
            continue

        # Step 5.3 没有归类的纳入mroutRangePtr
        mroutRangePtr.append([VA, _elfParser.getSectionByVA(VA)])

    retu =[[C2C, C2D, dict(C_insJMP), dict(C_insJMP_reloc), dict(C_insMEM), dict(C_insMEM_reloc), dict(C_insNOMEM), dict(C_insNOMEM_reloc)],
            [D2C, D2D, DIC, D_JPT_num, dict(D_JPT_reloc), D_AbsPtr_num, dict(D_AbsPtr_reloc), D_OtherData_num, dict(D_Other_reloc), dict(D_padding)]]
    pointer_state[elf_path] = retu

    if dataIndex == -1:
        show(elf_path, retu)
        print(len(mroutRangePtr))
    else:
        savedStdout = sys.stdout
        sys.stdout = fw
        show(elf_path, retu)
        sys.stdout = savedStdout


if __name__ == '__main__':


    # directories = ["/ccr/x86-sok/dataset/x86_dataset/linux",
    #                "/ccr/x86-sok/dataset/armmips_dataset/arm32_executables",
    #                "/ccr/x86-sok/dataset/armmips_dataset/aarch64_executables"]
    # directories = ["/ccr/x86-sok/dataset/x86_dataset/linux"]
    # directories = ["/E/binaryset/binaries-popular/O0"]
    # directories = ["/E/binaryset/binaries-spec"]
    # directories = ["/E/binaryset/binaries-spec-arm64/O0",
    #                "/E/binaryset/binaries-spec-arm64/O1",
    #                "/E/binaryset/binaries-spec-arm64/O2",
    #                "/E/binaryset/binaries-spec-arm64/O3",
    #                "/E/binaryset/binaries-spec-arm64/Of",
    #                "/E/binaryset/binaries-spec-arm64/Os"]

    directories = ["/E/binaryset/binaries-spec-arm64/O0-pie",
                   "/E/binaryset/binaries-spec-arm64/O1-pie",
                   "/E/binaryset/binaries-spec-arm64/O2-pie",
                   "/E/binaryset/binaries-spec-arm64/O3-pie",
                   "/E/binaryset/binaries-spec-arm64/Of-pie",
                   "/E/binaryset/binaries-spec-arm64/Os-pie"
                   ]

    # directories = ["/E/binaryset/temp"]

    elfList = []
    for directory in directories:
        for path, dir_list, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(path, file)
                retu = subprocess.getstatusoutput("file " + file_path)[1]
                if "executable" in retu or "shared object" in retu:
                    elfList.append(os.path.join(path, file))

    fw = open("Result-pie.txt", "w")
    thread = myThread.myThread(elfList, pointer_state_analysis, poolNum=64, onFinish=pointer_state_finish) # , onFinish=pointer_state_finish
    thread.start()

    # pointer_state_analysis("/E/binaryset/binaries-spec-arm64/O0-pie/511-povray_r-povray_r")
    # pointer_state_analysis("/E/binaryset/binaries-spec-arm64/O0-pie/554-roms_r-roms_r")