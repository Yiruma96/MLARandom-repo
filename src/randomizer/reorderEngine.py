# coding=utf-8
import logging
import random
import copy
import struct
from bitarray import bitarray
import constants as C
import util
import time
import psutil
import json
import os
from reorderInfo import *
from unit import *


class ReorderCore():
    def __init__(self, EI, oldBin, newBin, options):

        # xie: 使用reorderInfo.py中的EssentialInfo来解析并存储这些元数据
        self.EI = EI
        self.layout = EI.layout
        self.fixups = EI.fixups
        self.oldBin = oldBin
        self.newBin = newBin
        self.options = options
        self.elfParser = self.EI.elfParser

        if self.options.arch == C.X64:
            self.md = Cs(CS_ARCH_X86, CS_MODE_64)
            self.md.detail = True
        else:
            self.md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
            self.md.detail = True

        self.mergedFunsIdx = list()  # 对应mergedFun的下标  [0, 1]
        self.randomizedFunContainer = None  # 一维所对应的FUN对象列表

        """
        我们现在只关注函数间引用的约束，采用单层重随机化的约束方法
        274 - R_AARCH64_ADR_PREL_LO21
        273 - R_AARCH64_LD_PREL_LO19
        280 - R_AARCH64_CONDBR19
        15  - R_X86_64_PC8
        """
        self.constraintFun = {274, 273, 280, 15}

    def mergeLayout(self):
        """
        代码位置置换
        Step 1: self.EI.functions.FunctionLayout[0]合并到funcLayout，并随机化
        Step 2: 遍历funcLayout里的每个mergedFunc，合并其bbl到BBLs，并随机化
        Step 3: 生成randLayout
        """

        """
        说明：关于溢出策略
        Orig：
        先考虑抽象出来的一个问题：一个list，以及一个记录两点间距离关系的lines，如何随机化list能同时保证lines中记录的两点距离不变大？
        现在我们没有找到一个合适的算法来在满足该需求的同时还使list具有高熵值，但一个可行的思路是"压缩"：
        将所有具有依赖关系的line都提出来，然后将其压缩到一起并作为一个随机化单位，这可以保证任意两点间的距离在随机化后没有变大。
        压缩虽然可行，但其实在关系复杂时使得几乎所有点都具有关系，因此最后list中的随机化单位变得很少。

        我们现在采用的方案是"压缩"，同时为了保证随机化熵值还需要尽量降低lines的数量。因此我们将所有指针构成的lines缩减为短指针的lines，
        当短指针的定义广时记为高约束，基本可以等效于所有的lines；当短指针的定义窄时记为低约束，此时可能存在溢出。

        具体的随机化方案如下，我们要随机化的list有funLayout和很多BBLs。
        - funLayout的话我们使用低约束(收集自全局的低约束短指针)，
        - BBLs的话我们使用低约束(收集自全局的低约束短指针)。
        然后随机化后检查指针，对那些溢出是由于BBLs导致的话，就重新使用高约束(收集自该BBLs内的高约束短指针，虽然不是收集自全局但应该是全的，)来随机化该BBLs
        如果溢出是funcLayout导致的话，目前没有好的解决方案来处理，因为该高约束应用在funLayout上会导致极低的熵值。一个可行的解决方案是重随机化，可能就解决了。

        New:
        因为我们不在进行函数内随机化，所以只对函数间引用进行约束就可以了，根据之前的分析，我们决定使用单层约束，且并不会增量约束而是多次重随机化
            高约束应用在funLayout上会导致极低的熵值。一个可行的解决方案是重随机化，可能就解决了。
        """
        for F in self.layout.FunctionLayout:
            self.mergedFunsIdx.append([F.idx])

        # 不做随机化的话就无需聚合
        if self.options.no_rand:
            return

        # Step 1. 根据函数间的交叉引用关系，从FunctionLayout中得到lines
        funLines = list()
        for F in self.layout.FunctionLayout:
            for targetF in F.refTos:
                for cond in self.constraintFun:
                    if cond in F.refTos[targetF]:
                        line = sorted([F.idx, targetF])
                        if line not in funLines:
                            funLines.append(line)

        # Step 2. 根据函数末尾是否有数据流转移指令，确定两个Function是否为FallThrough关系，来决定是否加入lines
        textChunk = self.elfParser.elf.get_section_by_name(".text").data()
        textVA = self.elfParser.getSectionVA(".text")
        for funIdx in range(len(self.layout.FunctionLayout)-1):
            F = self.layout.FunctionLayout[funIdx]
            findFunctionEnd = False

            # 从一个函数的最后一条指令开始逆序追溯
            instCount = 0
            firstCapsInst = None
            for inst in F.insts[::-1]:
                instBytes = textChunk[inst.offset : inst.offset+inst.size]
                # Case 1. 如果是nop则跳过
                if RecursiveDisass.Tools.isPaddingorPrefix(instBytes, self.options.arch) == 1:
                    continue
                # Case 2. 如果是控制流转移指令则判断该函数非FallThrough,置findFunctionEnd标志位为True
                for capsInst in self.md.disasm(instBytes, inst.offset):
                    firstCapsInst = capsInst
                    break
                if RecursiveDisass.Tools.isControlFlowInst(firstCapsInst) or firstCapsInst.id == 57:
                    findFunctionEnd = True
                if firstCapsInst.id == 57: # isControlFlowInst只是根据capstone的group进行判断，而brk跳转指令不属于任何group，所以要额外判断一次
                    findFunctionEnd = True
                # Case 3. 否则判断该函数为FallThrough，保持findFunctionEnd标志位为False
                break

            if findFunctionEnd == False:
                # print("[{} {}] {} -> {}".format(funIdx, funIdx+1, F.info, self.layout.FunctionLayout[funIdx+1].info))
                funLines.append([funIdx, funIdx+1])

        # Step 3. 将多条lines区分为不同块。这是和原版PointerScope最不同的地方，原版是不做区分的。
        # 两层循环进行lines分组，内层循环从funLines中按照图的宽度优先遍历(每一轮边缘节点)寻找linesGroup，
        # 外层循环删除每一轮发现的linesGroup后剩余的funLines，在图算法中是不必要的，但这里我们是为了减少funLines搜索空间，这太花费时间了
        remainFunLines = funLines
        linesGroups = list()
        while len(remainFunLines) != 0:
            oldPointers = set()
            oldPointers.add(remainFunLines[0][0])
            oldPointers.add(remainFunLines[0][1])
            edgePointers = remainFunLines[0]
            newEdgePointers = list()
            linesGroup = [remainFunLines[0]]
            # 一直循环到不能由边发现新的节点即可以停止
            while len(edgePointers) != 0:
                # 遍历edgePointers以寻找newEdgePointers
                for pointer in edgePointers:
                    for line in remainFunLines:
                        anotherPointer = None
                        if pointer == line[0]:
                            anotherPointer = line[1]
                        elif pointer == line[1]:
                            anotherPointer = line[0]
                        if anotherPointer and anotherPointer not in oldPointers:
                            newEdgePointers.append(anotherPointer)
                            linesGroup.append(line)
                            oldPointers.add(anotherPointer)
                # 将新找到的newEdgePointers替换掉已经搜索完毕的edgePointers
                edgePointers = newEdgePointers
                newEdgePointers = list()
            linesGroups.append(linesGroup)

            # 根据linesGroup对remainFunLines进行去重
            tempRemainFunLines = list()
            for temp in remainFunLines:
                if temp not in linesGroup:
                    tempRemainFunLines.append(temp)
            remainFunLines.clear()
            remainFunLines = tempRemainFunLines

        # Step 3. 根据不同的lines，合并出self.mergedFunsIdx
        for linesGroup in linesGroups:
            """
            通过lines进一步合并mergedObj
            我们的目标是，让那些两点之间的距离不要在随机化之后变的更大，所以策略如下：
            1. 将有约束关系的提取出来，然后将他们顺序的压紧实，也就是作为一整个BBL
            2. 再进行随机化
            mergedObjs  [[1,2], [3], [4,5,6], [7,8], [9]]
            lines       [[3,7], [8,9]]
            retu        Step1: [[1,2], [4,5,6], [3,7,8,9]]
                        Step2: [[3,7,8,9], [1,2], [4,5,6]]
            """
            # 拿到端点集合
            endPoints = set()
            for line in linesGroup:
                endPoints.add(line[0])
                endPoints.add(line[1])

            # 从端点集合找到要聚合的基本块
            endMergedObjs = set()
            for endPoint in endPoints:
                for i in range(len(self.mergedFunsIdx)):
                    if endPoint in self.mergedFunsIdx[i]:
                        endMergedObjs.add(i)

            # 遍历MergedObjs，将两组分开来
            needRandom = []
            noNeedRandom = []
            for i in range(0, len(self.mergedFunsIdx)):
                if i in endMergedObjs:
                    noNeedRandom += self.mergedFunsIdx[i]
                else:
                    needRandom.append(self.mergedFunsIdx[i])

            needRandom.append(noNeedRandom)
            del self.mergedFunsIdx
            self.mergedFunsIdx = needRandom

        # Step 4. 对函数体进行排序，保证每个单元内部函数相对顺序和随机化前是一致的
        # fw = open("/ccr/randomizer/NoCompiler/mergedFunsIdx", "w")
        # fw.write(str(linesGroups)+"\n\n\n")
        # fw.write(str(self.mergedFunsIdx))
        # fw.close()
        for idx in range(len(self.mergedFunsIdx)):
            self.mergedFunsIdx[idx] = sorted(self.mergedFunsIdx[idx])

        # Step 5. 校验每个fun是否都出现且仅出现一次，用于保证上面的算法是没有问题的
        for mergedFunsIdx in self.mergedFunsIdx:
            for funIdx in mergedFunsIdx:
                if self.layout.FunctionLayout[funIdx].mergedCheckFlag == True:
                    logging.error("函数布局合并后出现不一致，Fun#{}重复出现".format(funIdx))
                    exit(1)
                self.layout.FunctionLayout[funIdx].mergedCheckFlag = True
        for fun in self.layout.FunctionLayout:
            if fun.mergedCheckFlag == False:
                logging.error("函数布局合并后出现不一致，Fun#{}没有出现".format(fun.idx))

    def updateFixup(self, shuffle_round, bar):
        """
        在代码布局置换后更新Fixup
        """

        # 检查一段64位的bit序列在FI.mask的裁剪下是否发生溢出
        def checkOverFlow(FI, arch, show=False):
            overflowFlag = False

            # arm直接检查其bit序列的溢出就可以，因为其bit序列就是按照从最小到最大的顺序
            if arch == C.ARM64:
                # 1. 将FI.newValue转为bitX
                if FI.isRela:
                    byteSeqX = struct.pack("<q", FI.newValue)
                else:
                    byteSeqX = struct.pack("<Q", FI.newValue)
                bitX = bitarray(endian='little')
                bitX.frombytes(byteSeqX)

                # 2. 检查bit序列的低位(左边)和高位(右边)是否存在溢出
                if FI.checkHighOverFlow:
                    extend = False if bitX[-1] else True
                    # 对于有符号数来说，其剪裁后的符号为应该和高位保持一致
                    # exp:8bit空间下存储有符号数字，bitarray('101111101111111111111111111')是溢出的，因为裁剪后变为正数了
                    if FI.isRela:
                        overflowFlag = extend in bitX[FI.mask[1] - 1:]
                    else:
                        overflowFlag = extend in bitX[FI.mask[1]:]
                    if overflowFlag and show:  # 高位应该是全0或全1，这里取样然后检查是否都是
                        print("Pointer高位发现溢出,详细信息如下：")
                        print("FI: " + str(FI))
                        print("Value: " + str(bitX))
                        print("Mask: " + str(FI.mask))

                if FI.checkLowOverFlow:
                    low = bitX[:FI.mask[0]]
                    if True in low:  # 低位应该都是0
                        overflowFlag = True
                        if show:
                            print("Pointer低位发现溢出,详细信息如下：")
                            print("FI: " + str(FI))
                            print("Value: " + str(bitX))
                            print("Mask: " + str(FI.mask))
            # x64下因为其bit序列并非顺序关系：但byte内高位bit左边，而高位byte在右边————bitarray('10110110 00000010 0000000000000000')
            # 因此直接通过struct.pack来判断是否溢出
            else:
                if FI.isRela:
                    Lower, Upper = C.signedRangeDict[FI.derefSz // 8]
                else:
                    Lower, Upper = C.unSignedRangeDict[FI.derefSz // 8]
                if not (Lower <= FI.newValue <= Upper):
                    overflowFlag = True
                    if show:
                        print("Pointer发现溢出,详细信息如下：")
                        print("FI: " + str(FI))
                        print("newValue: " + hex(FI.newValue))

            return overflowFlag

        if self.fixups == None:
            return
        else:
            FixupsLayout = self.fixups.FixupsLayout

        # ARM64架构下，在Group Relocation时或ADRP时，是需要共同来还原出X的！！！
        # 另外还要注意△x，在Page(S+A)时候仅计算Page(S)是不完整的，这是我们记录A的原因
        isOverflow = False
        for FI in FixupsLayout:
            bar += 1

            # 如果base和target都不变化，直接用原来的bit位即可
            if not FI.baseInRand and not FI.targetInRand:
                FI.newValue = FI.value
                continue

            # 计算base的差值
            deltaBase = 0
            if FI.baseInRand:
                if FI.baseType == C.BaseType.PAGE_PC:
                    newBase = FI.baseFun.newVA + (FI.baseAddr - FI.baseFun.VA)
                    deltaBase = (newBase & ~0xfff) - (FI.baseAddr & ~0xfff)
                else:
                    deltaBase = FI.baseFun.newVA - FI.baseFun.VA

            # 计算target的差值
            deltaTarget = 0
            if FI.targetInRand:
                if FI.targetType == C.TargetType.PAGE_NORMAL:
                    newTarget = FI.targetFun.newVA + (FI.targetAddr - FI.targetFun.VA)
                    deltaTarget = (newTarget + FI.add & ~0xfff) - ((FI.targetFun.VA + FI.add) & ~0xfff)
                else:
                    deltaTarget = FI.targetFun.newVA - FI.targetFun.VA

            # 计算出FI.newValue(考虑步长因素 FIXME: 临时方案，gas创建fix以及gold从重定位中生成fix，都需要注意step)
            if FI.step == 4:
                FI.newValue = int(FI.value + (deltaTarget - deltaBase) / FI.step)
            else:
                FI.newValue = FI.value + deltaTarget - deltaBase

            # print ("VA=%s value=%s=>newValue=%s" % (hex(FI.VA), hex(FI.value), hex(FI.newValue)))

            # 根据doffset检查bitX是否溢出，并在溢出时记录base和target
            overFlowFlag = checkOverFlow(FI, self.options.arch, False)
            if overFlowFlag:
                if FI.targetFun and FI.baseFun:
                    # 函数内的短跳转发生溢出  为对应的BBLs准备更严格的随机化约束
                    if FI.baseFun == FI.targetFun:
                        logging.error(
                            "发现函数内引用存在溢出,这不合法因为我们并没有改变函数内部布局 " + format(str(FI)))
                        exit(2)
                    # 函数间的短跳转发生溢出，报告该引用的reloc_type，但注意我们并不会将其添加到严格约束中，而是再次进行随机化
                    else:
                        logging.info("函数间引用存在溢出, FI: ID={} VA={} FUN#{}->FUN#{} RELOC={} {}".format(
                            FI.idx, FI.VA, FI.baseFun.idx, FI.targetFun.idx, FI.relocType, FI.relocName))
                        isOverflow = True
                else:
                    logging.error("发现target和base并非都在随机化区域内的引用出现溢出 " + str(FI))
                    exit(2)

        return isOverflow

    def performTransformation(self):
        """
        执行随机化
        """

        # 选择随机化种子
        if self.options.seed == 'time':
            _time = time.time()
            random.seed(_time)
            logging.info("  选择的种子为" + str(_time))
        elif self.options.seed in ['ip', 'mac']:
            adapters = psutil.net_if_addrs()
            ip = ""
            mac = ""
            for name in adapters:
                adapter = adapters[name]
                for snicaddr in adapter:
                    if snicaddr.family == 2 and snicaddr.address != '127.0.0.1':
                        ip = snicaddr.address
                    if snicaddr.family == 17:
                        mac = snicaddr.address
                if ip != "" and mac != "":
                    break
            if self.options.seed == 'ip':
                if ip != "":
                    random.seed(ip)
                    logging.info("  选择的种子为" + ip)
                else:
                    logging.error(" 没有找到合适的ip地址")
                    exit(2)
            else:
                if mac != "":
                    random.seed(mac)
                    logging.info("  选择的种子为" + mac)
                else:
                    logging.error(" 没有找到合适的mac地址")
                    exit(2)
        else:
            logging.error(" 指定了无效的种子 seed=" + self.options.seed)
            exit(2)

        step = 0

        # 是否使用文件中记录的randLayout
        randLayout_path = self.newBin + ".randLayout"
        if self.options.randlayout and os.path.exists(randLayout_path):
            step += 1
            logging.info("  Step%d. 发现" % step + randLayout_path + ",使用该文件中记录的顺序")
            fr = open(randLayout_path, "r")
            self.randLayout = json.loads(fr.read())
            fr.close()
            # 检查是否为np格式的randLayout我们接受ps和np两种格式的randLayout输入
            if type(self.randLayout[0]) != type(list()):
                logging.error("输入的{}为ps格式，请在运行ps-randomizer时加上np参数，或是使用np-randomizer的输出".format(
                    randLayout_path))
                exit(2)

            # randLayout来自确定文件的话，无需随机化，可以直接开始更新Layout布局
            self.randomizedFunContainer = list()
            for mergedFun in self.randLayout:
                for funIdx in mergedFun:
                    self.randomizedFunContainer.append(self.layout.FunctionLayout[funIdx])
            firstRandFun = self.randomizedFunContainer[0]
            firstRandFun.newVA = self.layout.randomStartVA
            prevFun = firstRandFun
            for FUN in self.randomizedFunContainer[1:]:
                FUN.newVA = prevFun.newVA + prevFun.size
                prevFun = FUN

            # 重新计算随机化后的Fixup
            logging.info("  Step%d. 按照随机化的代码布局更新Fixup对象..." % step)
            bar = util.ProgressBar(self.fixups.num)
            isOverFlow = self.updateFixup(1, bar)
            bar.finish()

            if isOverFlow:
                logging.error("来自randLayout的文件存在溢出错误 " + randLayout_path)
                exit(2)

        # 开始执行随机化
        else:
            if self.options.no_rand:
                grav = "不随机化"
            else:
                grav = "函数级"

            # 首先根据约束关系进行合并
            step += 1
            logging.info("  Step%d. 对代码布局进行%s合并..." % (step, grav))
            self.mergeLayout()
            logging.info("      [{}] 合并后函数体/总函数={}/{}".format(
                round(len(self.mergedFunsIdx) / len(self.layout.FunctionLayout), 5),
                str(len(self.mergedFunsIdx)), str(len(self.layout.FunctionLayout))))

            # 开始执行代码布局置换
            shuffle_round = 1
            while (1):

                # 代码布局置换以及Layout更新
                step += 1
                logging.info("  Step%d. 第%s次%s代码布局置换中..." % (step, shuffle_round, grav))
                if not self.options.no_rand:
                    random.shuffle(self.mergedFunsIdx)
                self.randomizedFunContainer = list()
                for mergedFun in self.mergedFunsIdx:
                    for funIdx in mergedFun:
                        self.randomizedFunContainer.append(self.layout.FunctionLayout[funIdx])

                firstRandFun = self.randomizedFunContainer[0]
                firstRandFun.newVA = self.layout.randomStartVA
                prevFun = firstRandFun
                for FUN in self.randomizedFunContainer[1:]:
                    FUN.newVA = prevFun.newVA + prevFun.size
                    prevFun = FUN

                # 重新计算随机化后的Fixup
                step += 1
                logging.info("  Step%d. 按照随机化的代码布局更新Fixup对象..." % step)
                bar = util.ProgressBar(self.fixups.num)
                isOverflow = self.updateFixup(1, bar)
                bar.finish()

                if not isOverflow:
                    break
                else:
                    if shuffle_round > 10:
                        logging.error("  随机的尝试次数超过限制")
                        exit(2)
                    shuffle_round += 1

        # 是否要记录randLayout到文件中
        if self.options.randlayout or self.options.debug:
            step += 1
            logging.info("  Step%d. 写入randLayout到文件中" % step)
            fw = open(randLayout_path, "w")
            fw.write(json.dumps(self.mergedFunsIdx))
            fw.flush()
            fw.close()

        # 6. 获得一些额外的统计信息
        funcNum = self.layout.num
        mergedFunNum = len(self.mergedFunsIdx)
        step += 1
        logging.info("  Step%d. 统计信息如下" % step)
        logging.info("      总FUN:%d MergedFun:%d Ratio:%s" % (funcNum, mergedFunNum, mergedFunNum / funcNum))



