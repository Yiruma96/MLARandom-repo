## MultiRandom
### Overview
MultiRandom

### How to build MultiRandom


### How to use MultiRandom
```
ln -s /usr/bin/as <MultiRandom_gas_path>
ln -s /usr/bin/as <MultiRandom_gold_path>
```

#### Compiling with GCC
```shell
gcc -O0 -o main main.c
```

#### Compiling with LLVM
```shell
clang --fno-integreted-as -O0 -o main main.c
```

#### Compiling with Rust
```shell
rustup toolchain link myrust67 <rust_project_path>
cd <project_path>
cargo build
```

#### Reading Metadata
```shell
python3.10 /ccr/randomizer/shuffleInfoReader.py <elf_path>
```
**Output**
```shell
>>> Layout: 16479
Fun#0 <audio_read_header from libavdevice/alsa_dec.o>: VA=0x100300 section_idx=.text
    inst#0: VA=0x100300 Size=0x4
    inst#1: VA=0x100304 Size=0x4
    inst#2: VA=0x100308 Size=0x4
    inst#3: VA=0x10030c Size=0x4
    ...
Fun#1 <audio_write_header from libavdevice/alsa_enc.o>: VA=0x100424 section_idx=.text
    inst#0: VA=0x100424 Size=0x4
    inst#1: VA=0x100428 Size=0x4
    inst#2: VA=0x10042c Size=0x4
    inst#3: VA=0x100430 Size=0x4
    ...

>>> Fixups: 562672
Fixup#   0 VA:0x176c9c, Offset:0x7699c, Reloc:R_AARCH64_ADR_PREL_PG_HI21, Target:Unknown-0xc964f0(VALUE), add:0x0000 (@Sec .text fftools/ffmpeg_opt.o) (RAND) (RELOC)1
Fixup#   1 VA:0x176ca0, Offset:0x769a0, Reloc:R_AARCH64_ADD_ABS_LO12_NC, Target:Unknown-0xc964f0(VALUE), add:0x0000 (@Sec .text fftools/ffmpeg_opt.o) (RAND) (RELOC)1
Fixup#   2 VA:0x176ca4, Offset:0x769a4, Reloc:R_AARCH64_CALL26, Target:Unknown-0xc49218(VALUE), add:0x0000 (@Sec .text fftools/ffmpeg_opt.o) (RAND) (RELOC)1
Fixup#   3 VA:0x176cdc, Offset:0x769dc, Reloc:R_AARCH64_CALL26, Target:Unknown-0x18c410(VALUE), add:0x0000 (@Sec .text fftools/ffmpeg_opt.o) (RAND) (RELOC)1
...
```

#### Binary Rewritting using randomizer
```shell
python3.10 /ccr/randomizer/prander.py <elf_path>
```
**Output**
```shell
修复元数据... (prander.py:108)
      解析eh_frame节和gcc_except_table节... (unit.py:84)
      校验中... (unit.py:99)

 (prander.py:28)
初始化元数据... (prander.py:29)
  Step1. 初始化Layout元数据 (reorderInfo.py:421)
  找到最大的子元数据连续记录区域为0xb1dfd0: 0x176c88-0xc94c58，其占text节0x100300-0xc964a0的0.9595 (reorderInfo.py:92)
  Step2. 初始化Fixup元数据 (reorderInfo.py:424)
					100% [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]
元数据初始化结束, Fun=14781, Fixup=564610, 其中拥有lsda的FDE=0 (reorderInfo.py:427)

 (prander.py:33)
执行随机化... (prander.py:34)
  选择的种子为1700830752.2857244 (reorderEngine.py:350)
  Step1. 对代码布局进行函数级合并... (reorderEngine.py:429)
      [0.99418] 合并后函数体/总函数=14695/14781 (reorderEngine.py:431)
  Step2. 第1次函数级代码布局置换中... (reorderEngine.py:441)
  Step3. 按照随机化的代码布局更新Fixup对象... (reorderEngine.py:458)
					100% [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]
Step4. 统计信息如下 (reorderEngine.py:484)
    总FUN:14781 MergedFun:14695 Ratio:0.9941817197753873 (reorderEngine.py:485)

 (prander.py:39)
重写二进制文件... (prander.py:40)
	Processing section [.interp] (binaryBuilder.py:683)
	Processing section [.note.ABI-tag] (binaryBuilder.py:683)
	Processing section [.note.gnu.build-id] (binaryBuilder.py:683)
	Processing section [.dynsym] (binaryBuilder.py:683)
	Processing section [.dynstr] (binaryBuilder.py:683)
	Processing section [.gnu.hash] (binaryBuilder.py:683)
	Processing section [.gnu.version] (binaryBuilder.py:683)
	Processing section [.gnu.version_r] (binaryBuilder.py:683)
	Processing section [.rela.dyn] (binaryBuilder.py:683)
		100% [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]
	Processing section [.rela.plt] (binaryBuilder.py:683)
	Processing section [.init] (binaryBuilder.py:683)
	Processing section [.plt] (binaryBuilder.py:683)
	Processing section [.text] (binaryBuilder.py:683)
		100% [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]
	Processing section [.fini] (binaryBuilder.py:683)
	Processing section [.rodata] (binaryBuilder.py:683)
	Processing section [.eh_frame] (binaryBuilder.py:683)
	Processing section [.eh_frame_hdr] (binaryBuilder.py:683)
	Processing section [.data.rel.ro.local] (binaryBuilder.py:683)
		100% [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]
	Processing section [.fini_array] (binaryBuilder.py:683)
	Processing section [.init_array] (binaryBuilder.py:683)
	Processing section [.data.rel.ro] (binaryBuilder.py:683)
		100% [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]
	Processing section [.dynamic] (binaryBuilder.py:683)
	Processing section [.got] (binaryBuilder.py:683)
	Processing section [.got.plt] (binaryBuilder.py:683)
	Processing section [.data] (binaryBuilder.py:683)
	Processing section [.tm_clone_table] (binaryBuilder.py:683)
	Processing section [.comment] (binaryBuilder.py:683)
	Processing section [.note.gnu.gold-version] (binaryBuilder.py:683)
	Processing section [.symtab] (binaryBuilder.py:683)
		100% [>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]
	Processing section [.strtab] (binaryBuilder.py:683)
	Processing section [.shstrtab] (binaryBuilder.py:683)
随机化结束，消耗时间为 45.667 sec(s) (prander.py:136)
```




