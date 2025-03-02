# coding=utf-8

import logging

import shuffleInfo_pb2
import util
import struct
import unit
import constants as C
from elfParser import ELFParser
from bitarray import bitarray
from unit import DWarfParser


class Functions():
    """
    记录二进制程序中的所有函数对象
    """

    def __init__(self, funsProto, EI):
        # 入口检查
        if len(funsProto) == 0:
            logging.error("metadata中没有fun")
            exit(1)

        self.EI = EI
        self.elfParser = self.EI.elfParser
        self.funsProto = funsProto
        self.num = len(self.funsProto)
        self.FunctionLayout = []
        self.lookupByVA = dict()

        self.textIdx = self.elfParser.section_index[C.SEC_TEXT]
        self.textVA, self.textEndVA = self.elfParser.section_ranges[C.SEC_TEXT]
        self.textContent = self.elfParser.elf.get_section_by_name(C.SEC_TEXT).data()

        # 我们把识别随机化边界的任务交给二进制重写阶段完成，同时这一次遍历也起到layout检查的作用
        # TODO: 为什么不包括np-temp?理论上来说，np_temp作为一个函数体，来一起做随机化也可以？
        maxRandomStart = 0
        maxRandomEnd = 0
        maxRandomStartIdx = 0
        maxRandomEndIdx = 0
        maxRandomSize = 0
        curRandomStart = 0
        curRandomEnd = 0
        curRandomStartIdx = 0
        curRandomEndIdx = 0
        newArea = True
        for funIdx, fun in enumerate(self.funsProto):
            # 不处理temp类型的fun
            if fun.info.startswith("np-temp"):
                continue

            # Step1. newArea标志位用于初始化curRandom的新环境
            if newArea:
                curRandomStart = self.textVA + fun.offset
                curRandomStartIdx = funIdx
                newArea = False

            # Step3. 如果后面已经没有fun或者是temp的时候，我们将当前的随机化区域size和历史最大值做比对
            if funIdx == self.num-1 or self.funsProto[funIdx+1].info.startswith("np-temp"):
                newArea = True

                # 计算当前元数据块的终点
                curRandomEndIdx = funIdx
                if funIdx == self.num-1:
                    curRandomEnd = self.textVA + fun.offset
                else:
                    curRandomEnd = self.textVA + self.funsProto[funIdx+1].offset

                # 和历史最大值作比对
                if curRandomEnd - curRandomStart > maxRandomSize:
                    maxRandomSize = curRandomEnd - curRandomStart
                    maxRandomStart = curRandomStart
                    maxRandomEnd = curRandomEnd
                    maxRandomStartIdx = curRandomStartIdx
                    maxRandomEndIdx = curRandomEndIdx

        # FIXME 1. 调整随机化尾部的padding，使其归入上个函数中，来避免随机化后它会影响后面的函数对齐。text节最后一个函数的padding是不归属于text的，所以不建议随机化text节中最后一个函数，不然要为之调整很多东西，来避免随机化后它会影响后面的函数对齐
        # check 1. 检查下随机化范围是否包括最后一个函数，如果包括的话就将随机化范围减去尾部函数
        if maxRandomEndIdx == self.num-1:
            if maxRandomStartIdx == maxRandomEndIdx:
                logging.error("可随机化范围为text节仅为最后一个函数，因此无可随机化范围")
                exit(1)
            maxRandomEnd = self.textVA + self.funsProto[maxRandomEndIdx].offset
            maxRandomEndIdx -= 1
            maxRandomSize = maxRandomEnd - maxRandomStart
        # check 2. 调整maxRandomEnd为下一个函数的offset，而非由函数的inst[-1]得来，这样会漏掉padding
        maxRandomEnd = self.textVA + self.funsProto[maxRandomEndIdx+1].offset

        # 现在可以确定随机化边界了
        logging.info("  找到最大的子元数据连续记录区域为{}: {}-{}，其占text节{}-{}的{}".format(
            hex(maxRandomSize), hex(maxRandomStart), hex(maxRandomEnd),
            hex(self.textVA), hex(self.textEndVA), str(round(maxRandomSize / (self.textEndVA - self.textVA),5))))

        self.randomOffset  = maxRandomStart - self.textVA
        self.randomStartVA = maxRandomStart
        self.randomEndVA   = maxRandomEnd
        self.num = maxRandomEndIdx - maxRandomStartIdx + 1

        # 开始建立layout
        for funIdx, funIdxProto in enumerate(range(maxRandomStartIdx, maxRandomEndIdx+1)):
            funProto = self.funsProto[funIdxProto]
            F = unit.Function()
            F.idx = funIdx
            F.insts = funProto.insts
            F.sec = funProto.section
            F.offset = funProto.offset
            F.VA = self.textVA + funProto.offset
            F.info = funProto.info
            F.size = (self.textVA + self.funsProto[funIdxProto + 1].offset) - F.VA

            self.FunctionLayout.append(F)
            self.lookupByVA[F.VA] = F


    def binarySearchFun(self, addr):

        if self.randomStartVA <= addr < self.randomEndVA:
            lower = 0
            upper = self.num - 1

            while True:
                if lower > upper or not (0<=lower<self.num) or not (0<=upper<self.num) :
                    logging.error("{}位于随机化范围内，但没有搜索到所属的Fun，大概是Fun序列存在问题，请排查".format(hex(addr)))
                    exit(1)

                middle = int((lower + upper) / 2)
                middleFun = self.FunctionLayout[middle]
                if middleFun.VA <= addr < middleFun.VA+middleFun.size:
                    return middleFun
                elif addr >= middleFun.VA+middleFun.size:
                    lower = middle + 1
                else:
                    upper = middle - 1
        else:
            return None

    def getReorderObjOff(self):
        return self.randomOffset

    def isInReorderRange(self, addr):
        return self.randomStartVA <= addr < self.randomEndVA


class Fixups():
    """
    存储Fixup元数据。每个节对应一个Fixups实例，目前考虑了五个节因此共有五个Fixups实例
    """

    def __init__(self, fixupsProto, otherfixupsProto, EI):
        """
        从FixupDataList中解析并存储每个Fixup，需要执行以下步骤：
        1. 从Fixup元数据中提取出指针的基本属性
        2. 根据FI.offset计算FI.VA, 并将位于随机化区域里的Fixup附加到所属的BBL上去
        3. 根据FI.baseType和FI.targetType，确定FI.baseAddr和FI.targetAddr，并进一步确定其FI.baseBB和FI.targetBB
        4. 读取二进制文件以提取出指针的bit
        5. 设置一些标志位，包括：该指针是否需要更新？是否包含短跳转？是否需要打印查看？

        6. 遍历FixupsLayout，从指针的bit计算出来Value
        """

        self.FixupsLayout = []     # 后面处理都是根据这个数组，所以它是最全的，不用担心随机化代码的Fixup，采用BBL的方式来获得。
        self.FixupsLayoutPrev = [] # 随机化代码前的Fixup
        self.FixupsLayoutLast = [] # 随机化代码后的Fixup
        self.num = len(fixupsProto) + len(otherfixupsProto)

        self.EI = EI
        self.elfParser = self.EI.elfParser
        self.fixupsProto = list()
        for fixup in fixupsProto:
            self.fixupsProto.append(fixup)
        for fixup in otherfixupsProto:
            self.fixupsProto.append(fixup)
        self.layout = self.EI.layout
        self.secData = dict() # 一个简单的缓存机制，避免重复读取以加速

        def getSectionData(secIdx):
            if secIdx not in self.secData:
                # self.secData[secIdx] = self.elfParser.elf.get_section_by_name(self.elfParser.section_name[secIdx]).data()
                # 原本使用的get_section_by_name，但直到我看到了同名的.init_array出现在ELF中，所以还是使用section idx作为key吧
                self.secData[secIdx] = self.elfParser.elf.get_section(secIdx).data()
            return self.secData[secIdx]

        def extractPointerBitSeq(FI, sectionData):
            # 取8字节的数据足够了，在x64下FI.offset就是指针位置,最长8字节，在ARM64下FI.offset是指令位置，对齐的4字节
            eightBytes = sectionData[FI.offset: FI.offset + 8]
            if self.EI.arch == C.ARM64:
                bitInst = bitarray(endian='little')
                bitIMM = bitarray(endian='little')
            else:
                bitInst = bitarray()
                bitIMM = bitarray()

            # 从二进制指令中基于dooffset拼接出指针
            bitInst.frombytes(eightBytes)
            for doffset in FI.doffsets:
                bitIMM += bitInst[doffset[0]:doffset[1]]

            return bitIMM

        def setBitSeq(orig, childBitSeq, childRange):
            childIndex = 0
            origIndex = childRange[0]
            while 1:
                if origIndex < childRange[1]:
                    orig[origIndex] = childBitSeq[childIndex]
                else:
                    break
                childIndex += 1
                origIndex += 1

        # 第一轮遍历，构建Fixup元素数组. 该遍历涉及到VA所属Fun的二分搜索，会比较耗时间因此用bar记录下
        bar = util.ProgressBar(self.num)
        for fixupIdx, fixup in enumerate(self.fixupsProto):

            # 初始化一个Fixup实例用于存放一个指针
            FI = unit.Fixup()

            # 1. Fixup的基础属性：提取自Fixup元数据
            """
                message FixupInfo {
                  // address
                  required uint64 offset = 1;     
                  required uint32 section = 2;    
                
                  // addressing mode
                  required uint32 type = 3; //0-1base->(Out|PC|VALUE|INDEX) 2-3target->(Out|PC|VALUE|INDEX) 4->isRela 5->is_new_section 6->isJump 7->isRAND 8->isRELOC 9->isGOT [16:31]->reloc_type
                  required uint64 base_bbl_sym = 4;
                  required uint32 base_section = 5;
                  required uint64 target_bbl_sym = 6;
                  required uint32 target_section = 7;
            	  optional int64  add = 8;
                  optional uint32 step = 9;
                
                  // other
                  optional string info = 10;
                }
            """
            FI.idx = fixupIdx
            FI.offset = fixup.offset
            if fixup.section in self.elfParser.section_name:
                FI.secName = self.elfParser.section_name[fixup.section]
                FI.sec = fixup.section
            else:
                logging.error("Fixup (VA={})的fixup.section不合法 (FISec={})".format(hex(FI.VA), fixup.section))
                exit(1)
            FI.base_bbl_sym = fixup.base_bbl_sym
            FI.target_bbl_sym = fixup.target_bbl_sym
            FI.baseSec = fixup.base_section
            FI.targetSec = fixup.target_section
            FI.add = fixup.add
            FI.step = fixup.step
            FI.type = fixup.type

            # 2. 从FI.type扩充出其他属性
            protoBaseType = FI.type & 3
            protoTargetType = (FI.type >> 2) & 3
            FI.isFromRand = (FI.type >> 7) & 1
            FI.isFromReloc = (FI.type >> 8) & 1
            FI.isFromGOT = (FI.type >> 9) & 1
            FI.relocType = (FI.type >> 16) & 0xffff
            FI.relocName, FI.addressMode, FI.targetDesc, FI.targetType, FI.baseDesc, FI.baseType, FI.mask, FI.doffsets, \
            FI.derefSz, FI.nextNum, FI.checkHighOverFlow, FI.checkLowOverFlow, FI.show, FI.isCodePointer = C.relocDict[FI.relocType]

            # 3. 扩展FI的三个位置相关属性
            FI.VA = self.elfParser.section_ranges_idx[FI.sec][0] + FI.offset
            FIfun = self.layout.binarySearchFun(FI.VA)
            if FIfun != None:
                FIfun.fixups.append(FI)
                FI.parent = FIfun

            if protoBaseType > 1: # 没有的则说明为绝对地址或者pc，pc会在后面处理，绝对地址则保持默认的baseAddr=0即可
                if protoBaseType == 2:
                    if FI.baseSec:
                        FI.baseAddr = self.elfParser.section_ranges_idx[FI.baseSec][0] + FI.base_bbl_sym
                    else:
                        FI.baseAddr = FI.base_bbl_sym
                else:
                    logging.error("Fixup (VA={})的base type=INDEX，请排查".format(hex(FI.VA)))
                    exit(1)
            if FI.baseType in [C.BaseType.PC, C.BaseType.PAGE_PC]:
                if self.EI.arch == C.ARM64:
                    FI.baseAddr = FI.VA
                elif self.EI.arch == C.X64:
                    FI.baseAddr = FI.VA # FI.VA + FI.derefSz/8 一方面加了这个size，也不一定指到下一条指令的结尾，其次如果是BBL的末尾指令还会误将下一个BBL作为自己的baseBB，综上决定就以指针所在作为Addr了
            if FI.baseAddr != 0:
                FI.isRela = True
            # 在ps中有一个处理见util.countRefToNops()函数：即fixup的符号是.Lrtx5483，但该符号和紧邻的BBL头部间隔了一条nop指令，那么该fixup
            # 的符号归属于哪一个bbl呢？其实归属于什么都没问题，还是要看其计算出的base是什么。
            # 这种情况对于函数来说应该是不存在的，因为目标符号一定是准确的函数，没有其他可能。
            FIBaseFun = self.layout.binarySearchFun(FI.baseAddr)
            if FIBaseFun != None:
                FI.baseFun = FIBaseFun
                FI.baseInRand = True

            if protoTargetType > 1:
                if protoTargetType == 2:
                    if FI.targetSec:
                        FI.targetAddr = self.elfParser.section_ranges_idx[FI.targetSec][0] + FI.target_bbl_sym
                    else:
                        FI.targetAddr = FI.target_bbl_sym
                else:
                    logging.error("Fixup (VA={})的base type=INDEX，请排查".format(hex(FI.VA)))
                    exit(1)
            FITargetFun = self.layout.binarySearchFun(FI.targetAddr)
            if FITargetFun != None:
                FI.targetFun = FITargetFun
                FI.targetInRand = True

            # 4. 根据三个位置属性，设置一些标志位
            # flagA: 该fixup是否需要更新？ 根据base和target是否位于随机化区域来设置
            FI.needUpdate = False
            if FI.isRela:
                # 对于相对寻址来说,base和target只有一个变,则fixup需要更新. base和target都变时则检查指向的FUN,如果是同一个则不变
                if FI.baseInRand and not FI.targetInRand:
                    FI.needUpdate = True
                if not FI.baseInRand and FI.targetInRand:
                    FI.needUpdate = True
                if FI.baseInRand and FI.targetInRand:
                    if FI.baseFun != FI.targetFun:
                        FI.needUpdate = True
            else:
                # 对于绝对寻址来说, target改变则必定改变
                if FI.targetInRand:
                    FI.needUpdate = True

            # flagB: 从fixup中收集随机化区域内的函数间引用关系
            # 目前我们先只考虑两个端点都位于随机化区域内部的情况，因为如果有位于外部的话，这种情况一般都预留了足够的指针空间。而且我们会有溢出测试
            if FI.baseFun and FI.targetFun and FI.baseFun != FI.targetFun:  # 两个端点位于随机化区域内但不同
                if FI.targetFun.idx not in FI.baseFun.refTos: # 为baseFun设置refTos
                    FI.baseFun.refTos[FI.targetFun.idx] = {FI.relocType}
                else:
                    FI.baseFun.refTos[FI.targetFun.idx].add(FI.relocType)

                if FI.baseFun.idx not in FI.targetFun.refFroms: # 为targetFun设置refFroms
                    FI.targetFun.refFroms[FI.baseFun.idx] = {FI.relocType}
                else:
                    FI.targetFun.refFroms[FI.baseFun.idx].add(FI.relocType)

            # 5. 提取FI的值，这里只是提取出来存储的bit序列，计算X值的工作放到后面的循环中
            # 从二进制指令中基于dooffset拼接出指针，注意在后续Fixup中补充低位以及按照符号位补充高位，在后面单独做
            FI.bitIMM = extractPointerBitSeq(FI, getSectionData(FI.sec))

            # 6. 将FI放入三个列表
            self.FixupsLayout.append(FI)
            if FI.sec == self.layout.textIdx:
                if self.layout.textVA <= FI.VA < self.layout.randomStartVA:
                    self.FixupsLayoutPrev.append(FI)
                elif self.layout.randomEndVA <= FI.VA < self.layout.textEndVA:
                    self.FixupsLayoutLast.append(FI)
                elif FI.VA < self.layout.textVA or FI.VA >= self.layout.textEndVA:
                    logging.error("该Fixup的VA异常，不属于text节范围内.\n" + str(FI))
                    exit(1)

            bar += 1
        bar.finish()

        # 第二轮遍历，我们读取FI的bytes然后计算value。注意虽然理论上value可以通过target-base+add来得到，但我们还是更愿意直接提取出来，因此分为下面三种情况
        #   Case1.为nextNum=-1的group relocation. 因为缺少顺序关系，其缺失的高位很难通过，所以我们通过Target和Based计算出Fixup再取位数
        #   Case2.为nextNum存在的group relocation，结合其前后相邻的fixup，来共同组建出该指针
        #   Case3.nextNum为0时候，低位补0，高位补齐符号位
        # 另外还需要注意，从bit序列转到byte序列转到value，byte转value的时候是要考虑正负数。这一点在X转回去的时候也要考虑
        for fixIdx, FI in enumerate(self.FixupsLayout):

            # Case1. 记录的F值只是一部分，因此只能通过Target+Addend-Based来解决
            # 但该方案需要保证baseAddr和targetAddr两个值都是准确的，因此费了很大周折去确定target符号和base符号
            if FI.nextNum == -1:
                FI.value = FI.targetAddr + FI.add - FI.baseAddr  # FI.bitSeq后面应该用不到，不用存储了
                continue

            # Case2,Case3. 通过读取还原F值，这种方式最准确
            if not FI.hasCombined:
                # 1. 先初始化一个64位的数字
                if self.EI.arch == C.ARM64:
                    tempPointerBitSeq = bitarray(endian='little')
                else:
                    tempPointerBitSeq = bitarray()
                for i in range(64):
                    tempPointerBitSeq.append(False)
                # 2. 将这一系列的Fixup按照mask写入tempPointerBitSeq
                if FI.hasCombined == False:
                    for i in range(FI.nextNum+1):
                        curFI = self.FixupsLayout[fixIdx + i]
                        setBitSeq(tempPointerBitSeq, curFI.bitIMM, curFI.mask)
                # 3. 尾部保持默认的0，开头如果是有符号数的话则按照最高bit进行符号位扩展
                if FI.isRela:  # 有符号扩充
                    if self.EI.arch == C.ARM64:
                        highestBit = FI.bitIMM[-1]
                    else:
                        highestBit = FI.bitIMM[-8]
                    for i in range(FI.mask[1], 64):
                        tempPointerBitSeq[i] = highestBit
                # 4. 将计算好的X放入该系列的Fixup中
                for i in range(FI.nextNum + 1):
                    curFI = self.FixupsLayout[fixIdx + i]
                    curFI.bitX = tempPointerBitSeq
                    curFI.hasCombined = True
                    if curFI.isRela:
                        curFI.value = struct.unpack("<q", FI.bitX.tobytes())[0]
                    else:
                        curFI.value = struct.unpack("<Q", FI.bitX.tobytes())[0]

            # print hex(FI.VA)
            # print hex(FI.value)
            # print


class EssentialInfo():
    def __init__(self, fixedMetadata, filePath, options):
        self.options = options

        # 二进制文件信息
        self.fixedMetadata = fixedMetadata
        self.arch = fixedMetadata.arch
        self.filePath = filePath
        self.elfParser = fixedMetadata.elfParser
        self.entryPoint = self.elfParser.elf.header['e_entry']  # 入口点400500
        self.base = self.elfParser.elf.get_segment(2)['p_vaddr']  # 基址400000
        self.dwarfParser = fixedMetadata.dwarfParser

        # 解析元数据
        logging.info("  Step1. 初始化Layout元数据")
        self.layout = Functions(self.fixedMetadata.funs, self)

        logging.info("  Step2. 初始化Fixup元数据")
        self.fixups = Fixups(self.fixedMetadata.fixups, self.fixedMetadata.otherfixups, self)

        logging.info("  元数据初始化结束, Fun={}, Fixup={}, 其中拥有lsda的FDE={}".format
                     (len(self.layout.FunctionLayout), self.fixups.num, len(self.dwarfParser.FDEsHasLSDA) if self.dwarfParser else 0))
