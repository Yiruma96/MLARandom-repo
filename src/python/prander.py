# coding=utf-8
import os
import time
import logging
import optparse
import reorderInfo
import reorderEngine
import binaryBuilder
import unit
import util
import constants as C
import shuffleInfo_pb2
import shuffleInfoReader
import elfParser
import json


def transformBinary(fixedMetadata, filePath, options):
    """
    随机化程序
    """

    # 开始执行随机化
    oldBin = filePath
    newBin = filePath + C.NEWBIN_POSTFIX

    # Step1: 在reorderInfo中初始化元数据
    logging.info("\n\n\n")
    logging.info('初始化元数据...')
    EI = reorderInfo.EssentialInfo(fixedMetadata, oldBin, options)

    # Step2: 在reorderEngine中执行随机化的代码置换和指针修复
    logging.info("\n\n\n")
    logging.info('执行随机化...')
    RE = reorderEngine.ReorderCore(EI, oldBin, newBin, options)
    RE.performTransformation()

    # Step3: 传入reorderEngine的结果到binaryBuild，执行重写重写器中，以进行重写
    logging.info("\n\n\n")
    logging.info("重写二进制文件...")
    BB = binaryBuilder.BinaryBuilder(EI, RE, oldBin, newBin, options)
    BB.instrumentBin()


if __name__ == '__main__':

    usage = "Usage: %prog <FilePath> (Use -h for help)"
    parser = optparse.OptionParser(usage=usage)

    """
    -l fun -s ip -d nginx
    选项:           -r -s -d
    行动(action):   action=store                      向后消耗一个，以找到需要选项，结合type使用('string','int','float')
                    action=store_true或store_false   不向后消耗，说明该选项为布尔选项  
    分析：
    -l -s 的action为store，向后消耗fun和ip  
    -d -r是布尔选项
    nginx是位置参数，即在分析选项后，遗留下来的东西
    """
    parser.add_option("-s", "--seed", action='store', type='string', dest="seed", default='time',
                      help="Selecting randomized seed [time|ip|mac]")

    parser.add_option("-a", "--arch", action='store', type='string', dest="arch",
                      help="Selecting the arch of the randomized bin. If not specified, call readelf to automatic identification.")

    parser.add_option("-m", "--show-metadata", action='store_true', dest="show_metadata", default=False,
                      help="Show the metadata in the elf file and then exit")

    parser.add_option("-t", "--text", action='store_true', dest='alltext', default=False,
                      help="Randomize all code in .text")

    # 下面是调试用参数
    parser.add_option("-d", "--debug", action='store_true', dest="debug", default=False,
                      help="(Debug)Output debug info(disasm,)")

    parser.add_option("-c", "--count", action='store_true', dest="count", default=False,
                      help="(Debug) Show statistic of metadata in the elf file")

    parser.add_option("-r", "--randlayout", action='store_true', dest="randlayout", default=False,
                      help="(Debug) Record the randomized layout in the elf_randLayout file, or use the last randomized layout")

    parser.add_option("-n", "--no-rand", action='store_true', dest="no_rand", default=False,
                      help="(Debug) Do not rand. This parameter can be used to verify the correctness of randomization.")

    # options: 存储选项的dict结构
    # args:    存储位置参数的list结构
    (options, args) = parser.parse_args()

    # 配置logging
    logging.basicConfig(filename='/tmp/nothing', level=logging.ERROR if options.count else logging.INFO)
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(util.ColorFormatter())
    consoleHandler.flush()
    rootLogger.addHandler(consoleHandler)

    # 参数校验
    if options.seed not in ['time', 'ip', 'mac']:
        parser.error("'{}' 请选择[time|ip|mac]三个随机化种子中的其中一种".format(options.seed))
    if len(args) == 0:
        parser.error("No input file")
    if len(args) > 1:
        parser.error("More than one input files")
    if not os.path.exists(args[0]):
        logging.error("The target file [%s] has not been found!", args[0])
        exit(1)

    logging.info("修复元数据...")
    status, fixedMetadata = unit.FixedMetadata.fixedMetadataFactory(args[0], fast=True)
    if status == 1:
        logging.error(fixedMetadata)
        exit(1)
    if len(fixedMetadata.codeMisCollection) != 0:
        logging.warning(
            "    有{}个PendingBytes被确认为NP缺失收集的指令".format(len(fixedMetadata.codeMisCollection)))
    if len(fixedMetadata.DatainCode) != 0:
        logging.warning("    有{}个PendingBytes被确认为Data in Code(不一定)".format(len(fixedMetadata.DatainCode)))

    options.arch = fixedMetadata.arch
    if options.arch == C.ARM64:
        C.relocDict = C.aarch64_reloc_dict
    elif options.arch == C.X64:
        C.relocDict = C.x64_reloc_dict

    # dump并格式化输出metadata到终端
    if options.show_metadata:
        shuffleInfoReader.readOnly(fixedMetadata.metadata, fixedMetadata.elfParser)
    # 输出统计信息
    elif options.count:
        print (json.dumps(shuffleInfoReader.showCount(fixedMetadata.metadata)))
    # 开始随机化并统计时间
    else:
        startTime = time.time()
        transformBinary(fixedMetadata, args[0], options)
        endTime = time.time()
        logging.info("随机化结束，消耗时间为 %s", util._show_elapsed(startTime, endTime))
