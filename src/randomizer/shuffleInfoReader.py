# coding=utf-8
import json
import optparse
import os, sys
import shuffleInfo_pb2
import constants as C
import logging
import elfParser


def readOnly(metadata, elf):

    def print_fixup(fixups):
        for fixup_idx, fixup in enumerate(fixups):
            if fixup.section not in elf.section_ranges_idx:
                print("fixup offset={} info={} 的section={}不合法，请排查".format(hex(fixup.offset), fixup.info,
                                                                                 str(fixup.section)))
                exit(0x233)
            fixup_va = elf.section_ranges_idx[fixup.section][0] + fixup.offset

            _type = fixup.type
            baseType = _type & 3
            targetType = (_type >> 2) & 3
            isJumpTable = (_type >> 6) & 1
            isFromRand = (_type >> 7) & 1
            isFromReloc = (_type >> 8) & 1
            isFromGOT = (_type >> 9) & 1
            reloc_type_num = (_type >> 16) & 0xffff
            if reloc_type_num not in C.relocDict:
                print("fixup VA={} 其reloc_type为{}，请排查该问题".format(hex(fixup_va), reloc_type_num))
                exit(0x233)
            reloc_type = C.relocDict[reloc_type_num][0]

            base_str = ""
            if baseType > 1:
                if baseType == 2:
                    type = "VALUE"
                    if fixup.base_section:
                        sec_name = elf.section_name[fixup.base_section]
                        num = sec_name + "-" + hex(elf.section_ranges_idx[fixup.base_section][0] + fixup.base_bbl_sym)
                    else:
                        num = "Unknown-" + hex(fixup.base_bbl_sym)
                else:
                    type = "INDEX"
                    num = hex(fixup.base_bbl_sym)
                base_str = 'Base:{num}({type}), '.format(num=num, type=type)

            target_str = ""
            if targetType > 1:
                if targetType == 2:
                    type = "VALUE"
                    if fixup.target_section:
                        sec_name = elf.section_name[fixup.target_section]
                        num = sec_name + "-" + hex(
                            elf.section_ranges_idx[fixup.target_section][0] + fixup.target_bbl_sym)
                    else:
                        num = "Unknown-" + hex(fixup.target_bbl_sym)
                else:
                    type = "INDEX"
                    num = hex(fixup.target_bbl_sym)
                target_str = 'Target:{num}({type}),'.format(num=num, type=type)

            if fixup.info:
                sec_str = fixup.info
            else:
                try:
                    sec_str = elf.section_name[fixup.section]
                except:
                    sec_str = "Unknown " + str(fixup.section)

            if not options.count:
                print("Fixup#%4d VA:0x%04x, Offset:0x%04x, Reloc:%s, %s%s add:0x%04x (@Sec %s)%s%s%s%s%d" % \
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
                       fixup.step))


    # 打印Layout
    if not options.count:
        print("")
    total_fun = len(metadata.funs) # 随机化的所有单位，这里面包括了来自missing sub-metadata的input section对应的np-temp
    total_collected_fun = 0        # 能够收集到信息的fun数量
    for fun_idx, fun in enumerate(metadata.funs):
        fun_section_idx = fun.section
        fun_offset = fun.offset
        fun_va = elf.section_ranges_idx[fun_section_idx][0] + fun_offset
        fun_info = fun.info
        fun_section_name = elf.section_name[fun_section_idx]

        if not options.count:
            print("Fun#{} <{}>: VA={} section_idx={}".format(
                str(fun_idx),
                fun_info,
                hex(fun_va),
                fun_section_name))

        if fun_info.startswith("np-temp"):
            continue

        total_collected_fun += 1
        for inst_idx, inst in enumerate(fun.insts):
            inst_offset = inst.offset
            inst_va = elf.section_ranges_idx[fun_section_idx][0] + inst_offset
            inst_size = inst.size
            if not options.count:
                print("    inst#{}: VA={} Size={}".format(
                    str(inst_idx),
                    hex(inst_va),
                    hex(inst_size)
                ))
        if not options.count:
            print()


    # 打印Fixup
    if not options.count:
        print("\n\n\n>>> Fixups: {}".format(len(metadata.fixups)))
        print_fixup(metadata.fixups)

    # 打印OtherFixup
    if not options.count:
        print("\n\n\n>>> Other Fixups: {}".format(len(metadata.otherfixups)))
        print_fixup(metadata.otherfixups)


    # 打印统计信息，比如函数和指令数量，可疑的data bytes数量
    total_fun_num = len(metadata.funs)
    total_inst_num = 0
    for fun in metadata.funs:
        total_inst_num += len(fun.insts)
    if not options.count:
        print(""">>> Total fun num={} ({}/{})
    >>> Total inst num={}
    >>> Total fixup={}
    """.format(
            str(total_fun),
            str(metadata.goldinfo.c_fun),
            str(total_collected_fun),
            str(total_inst_num),
            str(len(metadata.fixups)+len(metadata.otherfixups))
        ))

    print(json.dumps([total_fun, metadata.goldinfo.c_fun, total_collected_fun, total_inst_num, len(metadata.fixups)+len(metadata.otherfixups)]))



def showCount(metadata):
    return []






if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: reader-xx.sh bin_path")
        exit(0)

    usage = "Usage: %prog [-s|-l|-m] <FilePath> (Use -h for help)"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-c", "--count", action='store_true', dest='count', default=False)
    (options, args) = parser.parse_args()

    # 判断架构类型，选择相应的reloc_list
    arch_retu = os.popen("readelf -hW {}".format(args[0])).read()
    if "AArch64" in arch_retu:
        arch = 'arm'
        C.relocDict = C.aarch64_reloc_dict
    elif "X86-64" in arch_retu:
        arch = 'x64'
        C.relocDict = C.x64_reloc_dict
    else:
        exit("ELF文件的架构类型未知")

    elf = elfParser.ELFParser(args[0])

    # 从文件中读取rand节
    randBytes = None
    if ".rand" not in elf.section_offset:
        if os.path.exists(args[0] + '.metadata'):
            fr = open(args[0] + '.metadata', 'rb')
            randBytes = fr.read()
            fr.close()
        else:
            logging.error("%s中不含有rand节" % sys.argv[1])
            exit(1)
    else:
        randStart = elf.section_offset['.rand'][0]
        randSize = elf.section_offset['.rand'][1]
        fr = open(args[0], "rb")
        fr.seek(randStart, 0)
        randBytes = fr.read(randSize)
        fr.close()

    # 反序列化
    metadata = shuffleInfo_pb2.Metadata()
    metadata.ParseFromString(randBytes)
    readOnly(metadata, elf)

