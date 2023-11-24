import sys, logging

try:
    from elftools.elf.elffile import ELFFile
    from elftools.elf.relocation import RelocationSection
    from elftools.elf.sections import SymbolTableSection
    from elftools.elf.dynamic import DynamicSection
except ImportError as e:
    logging.critical("You need to install the following packages: elftools")
    sys.exit(1)


class ELFParser:
    """  Class to help ELF parsing """

    class ELFSectionflags:
        SHF_WRITE = 0x01
        SHF_ALLOC = 0x02
        SHF_EXECINSTR = 0x04

    def __init__(self, filename):
        self.fn = filename
        self.f = open(self.fn, 'rb')
        self.bin = self.f.read()
        self.elf = ELFFile(self.f)

        self.struct_elf = {
            'e_type': "Object File Type",
            'e_machine': "Architecture",
            'e_entry': "Entry Point VA",
            'e_phoff': "Program header table file offset",
            'e_shoff': "Section header table file offset",
            'e_ehsize': "ELF header size in bytes",
            'e_phentsize': "Program header table entry size",
            'e_phnum': "Program header table entry count",
            'e_shentsize': "Section header table entry size",
            'e_shnum': "Section header table entry count",
            'e_shstrndx': "Section header string table index"
        }

        self.struct_section = {
            'sh_type': "Section Type",
            'sh_addralign': "Section Address Align",
            'sh_offset': "Section Offset",
            'sh_entsize': "Section Entry Size",
            'sh_name': "Section Name",
            'sh_flags': "Section Flags",
            'sh_size': "Section Size",
            'sh_addr': "Section VA",
            'sh_link': "Section Link",
            'sh_info': "Section Info"
        }

        # Relocation Types: Value, Name, Field and Calculation from linux64-ABI
        self.struct_relocation = {
            0: "R_X86_64_NONE",  # none, none
            1: "R_X86_64_64",  # word64, S + A
            2: "R_X86_64_PC32",  # word32, S + A - P
            3: "R_X86_64_GOT32",  # word32, G + A
            4: "R_X86_64_PLT32",  # word32, L + A - P
            5: "R_X86_64_COPY",  # none, none
            6: "R_X86_64_GLOB_DAT",  # wordclass, S
            7: "R_X86_64_JUMP_SLOT",  # wordclass, S
            8: "R_X86_64_RELATIVE",  # wordclass, B + A
            9: "R_X86_64_GOTPCREL",  # word32, G + GOT + A - P
            10: "R_X86_64_32",  # word32, S + A
            11: "R_X86_64_32S",  # word32, S + A
            12: "R_X86_64_16",  # word16, S + A
            13: "R_X86_64_PC16",  # word16, S + A - P
            14: "R_X86_64_8",  # word8, S + A
            15: "R_X86_64_PC8",  # word8, S + A - P
            16: "R_X86_64_DTPMOD64",  # word64
            17: "R_X86_64_DTPOFF64",  # word64
            18: "R_X86_64_TPOFF64",  # word64
            19: "R_X86_64_TLSGD",  # word32
            20: "R_X86_64_TLSLD",  # word32
            21: "R_X86_64_DTPOFF32",  # word32
            22: "R_X86_64_GOTTPOFF",  # word32
            23: "R_X86_64_TPOFF32",  # word32
            24: "R_X86_64_PC64",  # word64, S + A - P (only for LP64)
            25: "R_X86_64_GOTOFF64",  # word64, S + A - GOT (only for LP64)
            26: "R_X86_64_GOTPC32",  # word32, GOT + A - P
            32: "R_X86_64_SIZE32",  # word32, Z + A
            33: "R_X86_64_SIZE64",  # word64, Z + A (only for LP64)
            34: "R_X86_64_GOTPC32_TLSDESC",  # word32
            35: "R_X86_64_TLSDESC_CALL",  # none
            36: "R_X86_64_TLSDESC",  # word64 * 2
            37: "R_X86_64_IRELATIVE",  # wordclass, indirect (B + A)
            38: "R_X86_64_RELATIVE64"  # word64, B + A (only for ILP32 executable or shared objects)
        }

        self.section_ranges = {}
        self.section_ranges_idx = {}
        self.section_offset = {}
        self.section_offset_idx = {}
        self.section_index = {}
        self.section_name = {}
        self.extractSectionVAs()

    def readElfHdr(self):
        print ('ELF Header (%s)' % self.fn)
        elf_info = self.elf._parse_elf_header()

        for i in sorted(self.struct_elf.keys()):
            elf_decr = self.struct_elf[i].ljust(35)
            if isinstance(elf_info[i], int):
                val = '(' + hex(elf_info[i]) + ')'
                print ("  %s: %s%s" % (elf_decr, elf_info[i], val.rjust(15)))
            else:
                print ("  %s: %s" % (elf_decr, elf_info[i]))

    def readRelocations(self):
        """
        Read the relocation sections in a given ELF binary
        :return:
        """
        # There are several different sections for relocation:
        # '.rela.plt', '.rela.dyn', '.rel.plt', '.rel.dyn'
        # The postfix .dyn represents the table for dynamic linker
        reloc_section_names = ['.rela.plt', '.rela.dyn', '.rel.plt', '.rel.dyn']

        for reloc_name in reloc_section_names:
            rel = self.elf.get_section_by_name(reloc_name)
            if isinstance(rel, RelocationSection):
                print ('Relocation Section: %s (%d)' % (reloc_name, rel.num_relocations()))
                # Lookup all entry attributes
                for i, r in enumerate(rel.iter_relocations()):
                    print ('\t[%3d] Offset + Addend: %s +' % (i + 1, hex(r['r_offset']))),
                    if 'rela' in reloc_name:
                        print (r['r_addend']),
                    print ('\tInfo (Type, Symbol): %s (%s, %s)' \
                          % (hex(r['r_info']), self.struct_relocation[r['r_info_type']], r['r_info_sym']))

    def readSections(self):
        """ Read all sections in a given ELF binary """

        def sectionInfo(s):
            section = self.elf.get_section(s)

            # A section type is in its header, but the name was decoded and placed in a public attribute.
            print ('  [%2d] Section %s' % (s, section.name))
            for s in sorted(self.struct_section.keys()):
                sec_desc = self.struct_section[s].ljust(25)
                print ('\t%s : %s' % (sec_desc, section[s]))

            # Case: a section table contains a symbol table section
            if isinstance(section, SymbolTableSection):
                for sym_no in range(section.num_symbols()):

                    symbol = section.get_symbol(sym_no)
                    print ("      [%2d] Symbol: %s (Ty=%-7s, Bind=%-6s, Sym_Other=%-7s, Shndx=%4s, Val=0x%x, Sz=0x%x)" % \
                          (sym_no, symbol.name, symbol['st_info']['type'], symbol['st_info']['bind'],
                           symbol['st_other']['visibility'], symbol['st_shndx'], symbol['st_value'], symbol['st_size']))

        sec_cnt = self.elf.num_sections()
        print ('Found %s sections' % sec_cnt)
        for s in range(sec_cnt):
            sectionInfo(s)

    def extractSectionVAs(self):
        for s in range(1, self.elf.num_sections()):
            sec = self.elf.get_section(s)
            va = sec['sh_addr']
            off = sec['sh_offset']
            sz = sec['sh_size']
            if va > 0:
                self.section_ranges[sec.name] = (va, va + sz)
                self.section_ranges_idx[s] = (va, va + sz)
            else:
                self.section_ranges[sec.name] = (0, sz)
                self.section_ranges_idx[s] = (0, sz)

            self.section_offset[sec.name] = (off, sz)
            self.section_offset_idx[s] = (off, sz)
            self.section_index[sec.name] = s
            self.section_name[s] = sec.name

    def getSectionVA(self, sn):
        return self.section_ranges[sn][0]

    def getSectionIdx(self, sn):
        if sn in self.section_index:
            return self.section_index[sn]
        return None

    def getSectionRanges(self, sn):
        return self.section_ranges[sn]

    def getExecSectionRange(self):
        retu = []
        for s in range(1, self.elf.num_sections()):
            sec = self.elf.get_section(s)
            if sec.header["sh_flags"] == self.ELFSectionflags.SHF_EXECINSTR + self.ELFSectionflags.SHF_ALLOC:
                retu.append([self.section_ranges_idx[s][0], self.section_ranges_idx[s][1], self.section_name[s]])
        return retu

    def getSectionRangesIdx(self, sn):
        return self.section_ranges_idx[sn]

    def getNextSectionRange(self, sn):
        sectionEnd = self.section_ranges[sn][1]
        findSetion = [0xffffffffffffffff, 0xffffffffffffffff]
        for i in self.section_ranges:
            if self.section_ranges[i][0] >= sectionEnd and self.section_ranges[i][0] <= findSetion[0]:
                findSetion = self.section_ranges[i]
        return findSetion

    def getSectionByVA(self, va):
        secNames = self.section_ranges.keys()
        for sn in secNames:
            s, e = self.section_ranges[sn]
            if s <= va < e:
                return sn

    def isVAinSection(self, kind, va):
        for s, e in self.section_ranges[kind]:
            if s <= va < e:
                return True

        return False


if __name__ == '__main__':
    import os

    if len(sys.argv) != 2:
        print ("Usage: %s [ELF file to parse]" % (sys.argv[0]))
        sys.exit(1)
    else:
        f = sys.argv[1]
        if os.path.exists(f):
            ep = ELFParser(f)
            ep.readSections()
            ep.readRelocations()
        else:
            print ("No such file!")
