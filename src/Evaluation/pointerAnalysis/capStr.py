def x86opcodeStr(id):
    if id == 0:
        return 'X86_INS_INVALID'
    if id == 1:
        return 'X86_INS_AAA'
    if id == 2:
        return 'X86_INS_AAD'
    if id == 3:
        return 'X86_INS_AAM'
    if id == 4:
        return 'X86_INS_AAS'
    if id == 5:
        return 'X86_INS_FABS'
    if id == 6:
        return 'X86_INS_ADC'
    if id == 7:
        return 'X86_INS_ADCX'
    if id == 8:
        return 'X86_INS_ADD'
    if id == 9:
        return 'X86_INS_ADDPD'
    if id == 10:
        return 'X86_INS_ADDPS'
    if id == 11:
        return 'X86_INS_ADDSD'
    if id == 12:
        return 'X86_INS_ADDSS'
    if id == 13:
        return 'X86_INS_ADDSUBPD'
    if id == 14:
        return 'X86_INS_ADDSUBPS'
    if id == 15:
        return 'X86_INS_FADD'
    if id == 16:
        return 'X86_INS_FIADD'
    if id == 17:
        return 'X86_INS_ADOX'
    if id == 18:
        return 'X86_INS_AESDECLAST'
    if id == 19:
        return 'X86_INS_AESDEC'
    if id == 20:
        return 'X86_INS_AESENCLAST'
    if id == 21:
        return 'X86_INS_AESENC'
    if id == 22:
        return 'X86_INS_AESIMC'
    if id == 23:
        return 'X86_INS_AESKEYGENASSIST'
    if id == 24:
        return 'X86_INS_AND'
    if id == 25:
        return 'X86_INS_ANDN'
    if id == 26:
        return 'X86_INS_ANDNPD'
    if id == 27:
        return 'X86_INS_ANDNPS'
    if id == 28:
        return 'X86_INS_ANDPD'
    if id == 29:
        return 'X86_INS_ANDPS'
    if id == 30:
        return 'X86_INS_ARPL'
    if id == 31:
        return 'X86_INS_BEXTR'
    if id == 32:
        return 'X86_INS_BLCFILL'
    if id == 33:
        return 'X86_INS_BLCI'
    if id == 34:
        return 'X86_INS_BLCIC'
    if id == 35:
        return 'X86_INS_BLCMSK'
    if id == 36:
        return 'X86_INS_BLCS'
    if id == 37:
        return 'X86_INS_BLENDPD'
    if id == 38:
        return 'X86_INS_BLENDPS'
    if id == 39:
        return 'X86_INS_BLENDVPD'
    if id == 40:
        return 'X86_INS_BLENDVPS'
    if id == 41:
        return 'X86_INS_BLSFILL'
    if id == 42:
        return 'X86_INS_BLSI'
    if id == 43:
        return 'X86_INS_BLSIC'
    if id == 44:
        return 'X86_INS_BLSMSK'
    if id == 45:
        return 'X86_INS_BLSR'
    if id == 46:
        return 'X86_INS_BNDCL'
    if id == 47:
        return 'X86_INS_BNDCN'
    if id == 48:
        return 'X86_INS_BNDCU'
    if id == 49:
        return 'X86_INS_BNDLDX'
    if id == 50:
        return 'X86_INS_BNDMK'
    if id == 51:
        return 'X86_INS_BNDMOV'
    if id == 52:
        return 'X86_INS_BNDSTX'
    if id == 53:
        return 'X86_INS_BOUND'
    if id == 54:
        return 'X86_INS_BSF'
    if id == 55:
        return 'X86_INS_BSR'
    if id == 56:
        return 'X86_INS_BSWAP'
    if id == 57:
        return 'X86_INS_BT'
    if id == 58:
        return 'X86_INS_BTC'
    if id == 59:
        return 'X86_INS_BTR'
    if id == 60:
        return 'X86_INS_BTS'
    if id == 61:
        return 'X86_INS_BZHI'
    if id == 62:
        return 'X86_INS_CALL'
    if id == 63:
        return 'X86_INS_CBW'
    if id == 64:
        return 'X86_INS_CDQ'
    if id == 65:
        return 'X86_INS_CDQE'
    if id == 66:
        return 'X86_INS_FCHS'
    if id == 67:
        return 'X86_INS_CLAC'
    if id == 68:
        return 'X86_INS_CLC'
    if id == 69:
        return 'X86_INS_CLD'
    if id == 70:
        return 'X86_INS_CLDEMOTE'
    if id == 71:
        return 'X86_INS_CLFLUSH'
    if id == 72:
        return 'X86_INS_CLFLUSHOPT'
    if id == 73:
        return 'X86_INS_CLGI'
    if id == 74:
        return 'X86_INS_CLI'
    if id == 75:
        return 'X86_INS_CLRSSBSY'
    if id == 76:
        return 'X86_INS_CLTS'
    if id == 77:
        return 'X86_INS_CLWB'
    if id == 78:
        return 'X86_INS_CLZERO'
    if id == 79:
        return 'X86_INS_CMC'
    if id == 80:
        return 'X86_INS_CMOVA'
    if id == 81:
        return 'X86_INS_CMOVAE'
    if id == 82:
        return 'X86_INS_CMOVB'
    if id == 83:
        return 'X86_INS_CMOVBE'
    if id == 84:
        return 'X86_INS_FCMOVBE'
    if id == 85:
        return 'X86_INS_FCMOVB'
    if id == 86:
        return 'X86_INS_CMOVE'
    if id == 87:
        return 'X86_INS_FCMOVE'
    if id == 88:
        return 'X86_INS_CMOVG'
    if id == 89:
        return 'X86_INS_CMOVGE'
    if id == 90:
        return 'X86_INS_CMOVL'
    if id == 91:
        return 'X86_INS_CMOVLE'
    if id == 92:
        return 'X86_INS_FCMOVNBE'
    if id == 93:
        return 'X86_INS_FCMOVNB'
    if id == 94:
        return 'X86_INS_CMOVNE'
    if id == 95:
        return 'X86_INS_FCMOVNE'
    if id == 96:
        return 'X86_INS_CMOVNO'
    if id == 97:
        return 'X86_INS_CMOVNP'
    if id == 98:
        return 'X86_INS_FCMOVNU'
    if id == 99:
        return 'X86_INS_FCMOVNP'
    if id == 100:
        return 'X86_INS_CMOVNS'
    if id == 101:
        return 'X86_INS_CMOVO'
    if id == 102:
        return 'X86_INS_CMOVP'
    if id == 103:
        return 'X86_INS_FCMOVU'
    if id == 104:
        return 'X86_INS_CMOVS'
    if id == 105:
        return 'X86_INS_CMP'
    if id == 106:
        return 'X86_INS_CMPPD'
    if id == 107:
        return 'X86_INS_CMPPS'
    if id == 108:
        return 'X86_INS_CMPSB'
    if id == 109:
        return 'X86_INS_CMPSD'
    if id == 110:
        return 'X86_INS_CMPSQ'
    if id == 111:
        return 'X86_INS_CMPSS'
    if id == 112:
        return 'X86_INS_CMPSW'
    if id == 113:
        return 'X86_INS_CMPXCHG16B'
    if id == 114:
        return 'X86_INS_CMPXCHG'
    if id == 115:
        return 'X86_INS_CMPXCHG8B'
    if id == 116:
        return 'X86_INS_COMISD'
    if id == 117:
        return 'X86_INS_COMISS'
    if id == 118:
        return 'X86_INS_FCOMP'
    if id == 119:
        return 'X86_INS_FCOMPI'
    if id == 120:
        return 'X86_INS_FCOMI'
    if id == 121:
        return 'X86_INS_FCOM'
    if id == 122:
        return 'X86_INS_FCOS'
    if id == 123:
        return 'X86_INS_CPUID'
    if id == 124:
        return 'X86_INS_CQO'
    if id == 125:
        return 'X86_INS_CRC32'
    if id == 126:
        return 'X86_INS_CVTDQ2PD'
    if id == 127:
        return 'X86_INS_CVTDQ2PS'
    if id == 128:
        return 'X86_INS_CVTPD2DQ'
    if id == 129:
        return 'X86_INS_CVTPD2PS'
    if id == 130:
        return 'X86_INS_CVTPS2DQ'
    if id == 131:
        return 'X86_INS_CVTPS2PD'
    if id == 132:
        return 'X86_INS_CVTSD2SI'
    if id == 133:
        return 'X86_INS_CVTSD2SS'
    if id == 134:
        return 'X86_INS_CVTSI2SD'
    if id == 135:
        return 'X86_INS_CVTSI2SS'
    if id == 136:
        return 'X86_INS_CVTSS2SD'
    if id == 137:
        return 'X86_INS_CVTSS2SI'
    if id == 138:
        return 'X86_INS_CVTTPD2DQ'
    if id == 139:
        return 'X86_INS_CVTTPS2DQ'
    if id == 140:
        return 'X86_INS_CVTTSD2SI'
    if id == 141:
        return 'X86_INS_CVTTSS2SI'
    if id == 142:
        return 'X86_INS_CWD'
    if id == 143:
        return 'X86_INS_CWDE'
    if id == 144:
        return 'X86_INS_DAA'
    if id == 145:
        return 'X86_INS_DAS'
    if id == 146:
        return 'X86_INS_DATA16'
    if id == 147:
        return 'X86_INS_DEC'
    if id == 148:
        return 'X86_INS_DIV'
    if id == 149:
        return 'X86_INS_DIVPD'
    if id == 150:
        return 'X86_INS_DIVPS'
    if id == 151:
        return 'X86_INS_FDIVR'
    if id == 152:
        return 'X86_INS_FIDIVR'
    if id == 153:
        return 'X86_INS_FDIVRP'
    if id == 154:
        return 'X86_INS_DIVSD'
    if id == 155:
        return 'X86_INS_DIVSS'
    if id == 156:
        return 'X86_INS_FDIV'
    if id == 157:
        return 'X86_INS_FIDIV'
    if id == 158:
        return 'X86_INS_FDIVP'
    if id == 159:
        return 'X86_INS_DPPD'
    if id == 160:
        return 'X86_INS_DPPS'
    if id == 161:
        return 'X86_INS_ENCLS'
    if id == 162:
        return 'X86_INS_ENCLU'
    if id == 163:
        return 'X86_INS_ENCLV'
    if id == 164:
        return 'X86_INS_ENDBR32'
    if id == 165:
        return 'X86_INS_ENDBR64'
    if id == 166:
        return 'X86_INS_ENTER'
    if id == 167:
        return 'X86_INS_EXTRACTPS'
    if id == 168:
        return 'X86_INS_EXTRQ'
    if id == 169:
        return 'X86_INS_F2XM1'
    if id == 170:
        return 'X86_INS_LCALL'
    if id == 171:
        return 'X86_INS_LJMP'
    if id == 172:
        return 'X86_INS_JMP'
    if id == 173:
        return 'X86_INS_FBLD'
    if id == 174:
        return 'X86_INS_FBSTP'
    if id == 175:
        return 'X86_INS_FCOMPP'
    if id == 176:
        return 'X86_INS_FDECSTP'
    if id == 177:
        return 'X86_INS_FDISI8087_NOP'
    if id == 178:
        return 'X86_INS_FEMMS'
    if id == 179:
        return 'X86_INS_FENI8087_NOP'
    if id == 180:
        return 'X86_INS_FFREE'
    if id == 181:
        return 'X86_INS_FFREEP'
    if id == 182:
        return 'X86_INS_FICOM'
    if id == 183:
        return 'X86_INS_FICOMP'
    if id == 184:
        return 'X86_INS_FINCSTP'
    if id == 185:
        return 'X86_INS_FLDCW'
    if id == 186:
        return 'X86_INS_FLDENV'
    if id == 187:
        return 'X86_INS_FLDL2E'
    if id == 188:
        return 'X86_INS_FLDL2T'
    if id == 189:
        return 'X86_INS_FLDLG2'
    if id == 190:
        return 'X86_INS_FLDLN2'
    if id == 191:
        return 'X86_INS_FLDPI'
    if id == 192:
        return 'X86_INS_FNCLEX'
    if id == 193:
        return 'X86_INS_FNINIT'
    if id == 194:
        return 'X86_INS_FNOP'
    if id == 195:
        return 'X86_INS_FNSTCW'
    if id == 196:
        return 'X86_INS_FNSTSW'
    if id == 197:
        return 'X86_INS_FPATAN'
    if id == 198:
        return 'X86_INS_FSTPNCE'
    if id == 199:
        return 'X86_INS_FPREM'
    if id == 200:
        return 'X86_INS_FPREM1'
    if id == 201:
        return 'X86_INS_FPTAN'
    if id == 202:
        return 'X86_INS_FRNDINT'
    if id == 203:
        return 'X86_INS_FRSTOR'
    if id == 204:
        return 'X86_INS_FNSAVE'
    if id == 205:
        return 'X86_INS_FSCALE'
    if id == 206:
        return 'X86_INS_FSETPM'
    if id == 207:
        return 'X86_INS_FSINCOS'
    if id == 208:
        return 'X86_INS_FNSTENV'
    if id == 209:
        return 'X86_INS_FXAM'
    if id == 210:
        return 'X86_INS_FXRSTOR'
    if id == 211:
        return 'X86_INS_FXRSTOR64'
    if id == 212:
        return 'X86_INS_FXSAVE'
    if id == 213:
        return 'X86_INS_FXSAVE64'
    if id == 214:
        return 'X86_INS_FXTRACT'
    if id == 215:
        return 'X86_INS_FYL2X'
    if id == 216:
        return 'X86_INS_FYL2XP1'
    if id == 217:
        return 'X86_INS_GETSEC'
    if id == 218:
        return 'X86_INS_GF2P8AFFINEINVQB'
    if id == 219:
        return 'X86_INS_GF2P8AFFINEQB'
    if id == 220:
        return 'X86_INS_GF2P8MULB'
    if id == 221:
        return 'X86_INS_HADDPD'
    if id == 222:
        return 'X86_INS_HADDPS'
    if id == 223:
        return 'X86_INS_HLT'
    if id == 224:
        return 'X86_INS_HSUBPD'
    if id == 225:
        return 'X86_INS_HSUBPS'
    if id == 226:
        return 'X86_INS_IDIV'
    if id == 227:
        return 'X86_INS_FILD'
    if id == 228:
        return 'X86_INS_IMUL'
    if id == 229:
        return 'X86_INS_IN'
    if id == 230:
        return 'X86_INS_INC'
    if id == 231:
        return 'X86_INS_INCSSPD'
    if id == 232:
        return 'X86_INS_INCSSPQ'
    if id == 233:
        return 'X86_INS_INSB'
    if id == 234:
        return 'X86_INS_INSERTPS'
    if id == 235:
        return 'X86_INS_INSERTQ'
    if id == 236:
        return 'X86_INS_INSD'
    if id == 237:
        return 'X86_INS_INSW'
    if id == 238:
        return 'X86_INS_INT'
    if id == 239:
        return 'X86_INS_INT1'
    if id == 240:
        return 'X86_INS_INT3'
    if id == 241:
        return 'X86_INS_INTO'
    if id == 242:
        return 'X86_INS_INVD'
    if id == 243:
        return 'X86_INS_INVEPT'
    if id == 244:
        return 'X86_INS_INVLPG'
    if id == 245:
        return 'X86_INS_INVLPGA'
    if id == 246:
        return 'X86_INS_INVPCID'
    if id == 247:
        return 'X86_INS_INVVPID'
    if id == 248:
        return 'X86_INS_IRET'
    if id == 249:
        return 'X86_INS_IRETD'
    if id == 250:
        return 'X86_INS_IRETQ'
    if id == 251:
        return 'X86_INS_FISTTP'
    if id == 252:
        return 'X86_INS_FIST'
    if id == 253:
        return 'X86_INS_FISTP'
    if id == 254:
        return 'X86_INS_JAE'
    if id == 255:
        return 'X86_INS_JA'
    if id == 256:
        return 'X86_INS_JBE'
    if id == 257:
        return 'X86_INS_JB'
    if id == 258:
        return 'X86_INS_JCXZ'
    if id == 259:
        return 'X86_INS_JECXZ'
    if id == 260:
        return 'X86_INS_JE'
    if id == 261:
        return 'X86_INS_JGE'
    if id == 262:
        return 'X86_INS_JG'
    if id == 263:
        return 'X86_INS_JLE'
    if id == 264:
        return 'X86_INS_JL'
    if id == 265:
        return 'X86_INS_JNE'
    if id == 266:
        return 'X86_INS_JNO'
    if id == 267:
        return 'X86_INS_JNP'
    if id == 268:
        return 'X86_INS_JNS'
    if id == 269:
        return 'X86_INS_JO'
    if id == 270:
        return 'X86_INS_JP'
    if id == 271:
        return 'X86_INS_JRCXZ'
    if id == 272:
        return 'X86_INS_JS'
    if id == 273:
        return 'X86_INS_KADDB'
    if id == 274:
        return 'X86_INS_KADDD'
    if id == 275:
        return 'X86_INS_KADDQ'
    if id == 276:
        return 'X86_INS_KADDW'
    if id == 277:
        return 'X86_INS_KANDB'
    if id == 278:
        return 'X86_INS_KANDD'
    if id == 279:
        return 'X86_INS_KANDNB'
    if id == 280:
        return 'X86_INS_KANDND'
    if id == 281:
        return 'X86_INS_KANDNQ'
    if id == 282:
        return 'X86_INS_KANDNW'
    if id == 283:
        return 'X86_INS_KANDQ'
    if id == 284:
        return 'X86_INS_KANDW'
    if id == 285:
        return 'X86_INS_KMOVB'
    if id == 286:
        return 'X86_INS_KMOVD'
    if id == 287:
        return 'X86_INS_KMOVQ'
    if id == 288:
        return 'X86_INS_KMOVW'
    if id == 289:
        return 'X86_INS_KNOTB'
    if id == 290:
        return 'X86_INS_KNOTD'
    if id == 291:
        return 'X86_INS_KNOTQ'
    if id == 292:
        return 'X86_INS_KNOTW'
    if id == 293:
        return 'X86_INS_KORB'
    if id == 294:
        return 'X86_INS_KORD'
    if id == 295:
        return 'X86_INS_KORQ'
    if id == 296:
        return 'X86_INS_KORTESTB'
    if id == 297:
        return 'X86_INS_KORTESTD'
    if id == 298:
        return 'X86_INS_KORTESTQ'
    if id == 299:
        return 'X86_INS_KORTESTW'
    if id == 300:
        return 'X86_INS_KORW'
    if id == 301:
        return 'X86_INS_KSHIFTLB'
    if id == 302:
        return 'X86_INS_KSHIFTLD'
    if id == 303:
        return 'X86_INS_KSHIFTLQ'
    if id == 304:
        return 'X86_INS_KSHIFTLW'
    if id == 305:
        return 'X86_INS_KSHIFTRB'
    if id == 306:
        return 'X86_INS_KSHIFTRD'
    if id == 307:
        return 'X86_INS_KSHIFTRQ'
    if id == 308:
        return 'X86_INS_KSHIFTRW'
    if id == 309:
        return 'X86_INS_KTESTB'
    if id == 310:
        return 'X86_INS_KTESTD'
    if id == 311:
        return 'X86_INS_KTESTQ'
    if id == 312:
        return 'X86_INS_KTESTW'
    if id == 313:
        return 'X86_INS_KUNPCKBW'
    if id == 314:
        return 'X86_INS_KUNPCKDQ'
    if id == 315:
        return 'X86_INS_KUNPCKWD'
    if id == 316:
        return 'X86_INS_KXNORB'
    if id == 317:
        return 'X86_INS_KXNORD'
    if id == 318:
        return 'X86_INS_KXNORQ'
    if id == 319:
        return 'X86_INS_KXNORW'
    if id == 320:
        return 'X86_INS_KXORB'
    if id == 321:
        return 'X86_INS_KXORD'
    if id == 322:
        return 'X86_INS_KXORQ'
    if id == 323:
        return 'X86_INS_KXORW'
    if id == 324:
        return 'X86_INS_LAHF'
    if id == 325:
        return 'X86_INS_LAR'
    if id == 326:
        return 'X86_INS_LDDQU'
    if id == 327:
        return 'X86_INS_LDMXCSR'
    if id == 328:
        return 'X86_INS_LDS'
    if id == 329:
        return 'X86_INS_FLDZ'
    if id == 330:
        return 'X86_INS_FLD1'
    if id == 331:
        return 'X86_INS_FLD'
    if id == 332:
        return 'X86_INS_LEA'
    if id == 333:
        return 'X86_INS_LEAVE'
    if id == 334:
        return 'X86_INS_LES'
    if id == 335:
        return 'X86_INS_LFENCE'
    if id == 336:
        return 'X86_INS_LFS'
    if id == 337:
        return 'X86_INS_LGDT'
    if id == 338:
        return 'X86_INS_LGS'
    if id == 339:
        return 'X86_INS_LIDT'
    if id == 340:
        return 'X86_INS_LLDT'
    if id == 341:
        return 'X86_INS_LLWPCB'
    if id == 342:
        return 'X86_INS_LMSW'
    if id == 343:
        return 'X86_INS_LOCK'
    if id == 344:
        return 'X86_INS_LODSB'
    if id == 345:
        return 'X86_INS_LODSD'
    if id == 346:
        return 'X86_INS_LODSQ'
    if id == 347:
        return 'X86_INS_LODSW'
    if id == 348:
        return 'X86_INS_LOOP'
    if id == 349:
        return 'X86_INS_LOOPE'
    if id == 350:
        return 'X86_INS_LOOPNE'
    if id == 351:
        return 'X86_INS_RETF'
    if id == 352:
        return 'X86_INS_RETFQ'
    if id == 353:
        return 'X86_INS_LSL'
    if id == 354:
        return 'X86_INS_LSS'
    if id == 355:
        return 'X86_INS_LTR'
    if id == 356:
        return 'X86_INS_LWPINS'
    if id == 357:
        return 'X86_INS_LWPVAL'
    if id == 358:
        return 'X86_INS_LZCNT'
    if id == 359:
        return 'X86_INS_MASKMOVDQU'
    if id == 360:
        return 'X86_INS_MAXPD'
    if id == 361:
        return 'X86_INS_MAXPS'
    if id == 362:
        return 'X86_INS_MAXSD'
    if id == 363:
        return 'X86_INS_MAXSS'
    if id == 364:
        return 'X86_INS_MFENCE'
    if id == 365:
        return 'X86_INS_MINPD'
    if id == 366:
        return 'X86_INS_MINPS'
    if id == 367:
        return 'X86_INS_MINSD'
    if id == 368:
        return 'X86_INS_MINSS'
    if id == 369:
        return 'X86_INS_CVTPD2PI'
    if id == 370:
        return 'X86_INS_CVTPI2PD'
    if id == 371:
        return 'X86_INS_CVTPI2PS'
    if id == 372:
        return 'X86_INS_CVTPS2PI'
    if id == 373:
        return 'X86_INS_CVTTPD2PI'
    if id == 374:
        return 'X86_INS_CVTTPS2PI'
    if id == 375:
        return 'X86_INS_EMMS'
    if id == 376:
        return 'X86_INS_MASKMOVQ'
    if id == 377:
        return 'X86_INS_MOVD'
    if id == 378:
        return 'X86_INS_MOVQ'
    if id == 379:
        return 'X86_INS_MOVDQ2Q'
    if id == 380:
        return 'X86_INS_MOVNTQ'
    if id == 381:
        return 'X86_INS_MOVQ2DQ'
    if id == 382:
        return 'X86_INS_PABSB'
    if id == 383:
        return 'X86_INS_PABSD'
    if id == 384:
        return 'X86_INS_PABSW'
    if id == 385:
        return 'X86_INS_PACKSSDW'
    if id == 386:
        return 'X86_INS_PACKSSWB'
    if id == 387:
        return 'X86_INS_PACKUSWB'
    if id == 388:
        return 'X86_INS_PADDB'
    if id == 389:
        return 'X86_INS_PADDD'
    if id == 390:
        return 'X86_INS_PADDQ'
    if id == 391:
        return 'X86_INS_PADDSB'
    if id == 392:
        return 'X86_INS_PADDSW'
    if id == 393:
        return 'X86_INS_PADDUSB'
    if id == 394:
        return 'X86_INS_PADDUSW'
    if id == 395:
        return 'X86_INS_PADDW'
    if id == 396:
        return 'X86_INS_PALIGNR'
    if id == 397:
        return 'X86_INS_PANDN'
    if id == 398:
        return 'X86_INS_PAND'
    if id == 399:
        return 'X86_INS_PAVGB'
    if id == 400:
        return 'X86_INS_PAVGW'
    if id == 401:
        return 'X86_INS_PCMPEQB'
    if id == 402:
        return 'X86_INS_PCMPEQD'
    if id == 403:
        return 'X86_INS_PCMPEQW'
    if id == 404:
        return 'X86_INS_PCMPGTB'
    if id == 405:
        return 'X86_INS_PCMPGTD'
    if id == 406:
        return 'X86_INS_PCMPGTW'
    if id == 407:
        return 'X86_INS_PEXTRW'
    if id == 408:
        return 'X86_INS_PHADDD'
    if id == 409:
        return 'X86_INS_PHADDSW'
    if id == 410:
        return 'X86_INS_PHADDW'
    if id == 411:
        return 'X86_INS_PHSUBD'
    if id == 412:
        return 'X86_INS_PHSUBSW'
    if id == 413:
        return 'X86_INS_PHSUBW'
    if id == 414:
        return 'X86_INS_PINSRW'
    if id == 415:
        return 'X86_INS_PMADDUBSW'
    if id == 416:
        return 'X86_INS_PMADDWD'
    if id == 417:
        return 'X86_INS_PMAXSW'
    if id == 418:
        return 'X86_INS_PMAXUB'
    if id == 419:
        return 'X86_INS_PMINSW'
    if id == 420:
        return 'X86_INS_PMINUB'
    if id == 421:
        return 'X86_INS_PMOVMSKB'
    if id == 422:
        return 'X86_INS_PMULHRSW'
    if id == 423:
        return 'X86_INS_PMULHUW'
    if id == 424:
        return 'X86_INS_PMULHW'
    if id == 425:
        return 'X86_INS_PMULLW'
    if id == 426:
        return 'X86_INS_PMULUDQ'
    if id == 427:
        return 'X86_INS_POR'
    if id == 428:
        return 'X86_INS_PSADBW'
    if id == 429:
        return 'X86_INS_PSHUFB'
    if id == 430:
        return 'X86_INS_PSHUFW'
    if id == 431:
        return 'X86_INS_PSIGNB'
    if id == 432:
        return 'X86_INS_PSIGND'
    if id == 433:
        return 'X86_INS_PSIGNW'
    if id == 434:
        return 'X86_INS_PSLLD'
    if id == 435:
        return 'X86_INS_PSLLQ'
    if id == 436:
        return 'X86_INS_PSLLW'
    if id == 437:
        return 'X86_INS_PSRAD'
    if id == 438:
        return 'X86_INS_PSRAW'
    if id == 439:
        return 'X86_INS_PSRLD'
    if id == 440:
        return 'X86_INS_PSRLQ'
    if id == 441:
        return 'X86_INS_PSRLW'
    if id == 442:
        return 'X86_INS_PSUBB'
    if id == 443:
        return 'X86_INS_PSUBD'
    if id == 444:
        return 'X86_INS_PSUBQ'
    if id == 445:
        return 'X86_INS_PSUBSB'
    if id == 446:
        return 'X86_INS_PSUBSW'
    if id == 447:
        return 'X86_INS_PSUBUSB'
    if id == 448:
        return 'X86_INS_PSUBUSW'
    if id == 449:
        return 'X86_INS_PSUBW'
    if id == 450:
        return 'X86_INS_PUNPCKHBW'
    if id == 451:
        return 'X86_INS_PUNPCKHDQ'
    if id == 452:
        return 'X86_INS_PUNPCKHWD'
    if id == 453:
        return 'X86_INS_PUNPCKLBW'
    if id == 454:
        return 'X86_INS_PUNPCKLDQ'
    if id == 455:
        return 'X86_INS_PUNPCKLWD'
    if id == 456:
        return 'X86_INS_PXOR'
    if id == 457:
        return 'X86_INS_MONITORX'
    if id == 458:
        return 'X86_INS_MONITOR'
    if id == 459:
        return 'X86_INS_MONTMUL'
    if id == 460:
        return 'X86_INS_MOV'
    if id == 461:
        return 'X86_INS_MOVABS'
    if id == 462:
        return 'X86_INS_MOVAPD'
    if id == 463:
        return 'X86_INS_MOVAPS'
    if id == 464:
        return 'X86_INS_MOVBE'
    if id == 465:
        return 'X86_INS_MOVDDUP'
    if id == 466:
        return 'X86_INS_MOVDIR64B'
    if id == 467:
        return 'X86_INS_MOVDIRI'
    if id == 468:
        return 'X86_INS_MOVDQA'
    if id == 469:
        return 'X86_INS_MOVDQU'
    if id == 470:
        return 'X86_INS_MOVHLPS'
    if id == 471:
        return 'X86_INS_MOVHPD'
    if id == 472:
        return 'X86_INS_MOVHPS'
    if id == 473:
        return 'X86_INS_MOVLHPS'
    if id == 474:
        return 'X86_INS_MOVLPD'
    if id == 475:
        return 'X86_INS_MOVLPS'
    if id == 476:
        return 'X86_INS_MOVMSKPD'
    if id == 477:
        return 'X86_INS_MOVMSKPS'
    if id == 478:
        return 'X86_INS_MOVNTDQA'
    if id == 479:
        return 'X86_INS_MOVNTDQ'
    if id == 480:
        return 'X86_INS_MOVNTI'
    if id == 481:
        return 'X86_INS_MOVNTPD'
    if id == 482:
        return 'X86_INS_MOVNTPS'
    if id == 483:
        return 'X86_INS_MOVNTSD'
    if id == 484:
        return 'X86_INS_MOVNTSS'
    if id == 485:
        return 'X86_INS_MOVSB'
    if id == 486:
        return 'X86_INS_MOVSD'
    if id == 487:
        return 'X86_INS_MOVSHDUP'
    if id == 488:
        return 'X86_INS_MOVSLDUP'
    if id == 489:
        return 'X86_INS_MOVSQ'
    if id == 490:
        return 'X86_INS_MOVSS'
    if id == 491:
        return 'X86_INS_MOVSW'
    if id == 492:
        return 'X86_INS_MOVSX'
    if id == 493:
        return 'X86_INS_MOVSXD'
    if id == 494:
        return 'X86_INS_MOVUPD'
    if id == 495:
        return 'X86_INS_MOVUPS'
    if id == 496:
        return 'X86_INS_MOVZX'
    if id == 497:
        return 'X86_INS_MPSADBW'
    if id == 498:
        return 'X86_INS_MUL'
    if id == 499:
        return 'X86_INS_MULPD'
    if id == 500:
        return 'X86_INS_MULPS'
    if id == 501:
        return 'X86_INS_MULSD'
    if id == 502:
        return 'X86_INS_MULSS'
    if id == 503:
        return 'X86_INS_MULX'
    if id == 504:
        return 'X86_INS_FMUL'
    if id == 505:
        return 'X86_INS_FIMUL'
    if id == 506:
        return 'X86_INS_FMULP'
    if id == 507:
        return 'X86_INS_MWAITX'
    if id == 508:
        return 'X86_INS_MWAIT'
    if id == 509:
        return 'X86_INS_NEG'
    if id == 510:
        return 'X86_INS_NOP'
    if id == 511:
        return 'X86_INS_NOT'
    if id == 512:
        return 'X86_INS_OR'
    if id == 513:
        return 'X86_INS_ORPD'
    if id == 514:
        return 'X86_INS_ORPS'
    if id == 515:
        return 'X86_INS_OUT'
    if id == 516:
        return 'X86_INS_OUTSB'
    if id == 517:
        return 'X86_INS_OUTSD'
    if id == 518:
        return 'X86_INS_OUTSW'
    if id == 519:
        return 'X86_INS_PACKUSDW'
    if id == 520:
        return 'X86_INS_PAUSE'
    if id == 521:
        return 'X86_INS_PAVGUSB'
    if id == 522:
        return 'X86_INS_PBLENDVB'
    if id == 523:
        return 'X86_INS_PBLENDW'
    if id == 524:
        return 'X86_INS_PCLMULQDQ'
    if id == 525:
        return 'X86_INS_PCMPEQQ'
    if id == 526:
        return 'X86_INS_PCMPESTRI'
    if id == 527:
        return 'X86_INS_PCMPESTRM'
    if id == 528:
        return 'X86_INS_PCMPGTQ'
    if id == 529:
        return 'X86_INS_PCMPISTRI'
    if id == 530:
        return 'X86_INS_PCMPISTRM'
    if id == 531:
        return 'X86_INS_PCONFIG'
    if id == 532:
        return 'X86_INS_PDEP'
    if id == 533:
        return 'X86_INS_PEXT'
    if id == 534:
        return 'X86_INS_PEXTRB'
    if id == 535:
        return 'X86_INS_PEXTRD'
    if id == 536:
        return 'X86_INS_PEXTRQ'
    if id == 537:
        return 'X86_INS_PF2ID'
    if id == 538:
        return 'X86_INS_PF2IW'
    if id == 539:
        return 'X86_INS_PFACC'
    if id == 540:
        return 'X86_INS_PFADD'
    if id == 541:
        return 'X86_INS_PFCMPEQ'
    if id == 542:
        return 'X86_INS_PFCMPGE'
    if id == 543:
        return 'X86_INS_PFCMPGT'
    if id == 544:
        return 'X86_INS_PFMAX'
    if id == 545:
        return 'X86_INS_PFMIN'
    if id == 546:
        return 'X86_INS_PFMUL'
    if id == 547:
        return 'X86_INS_PFNACC'
    if id == 548:
        return 'X86_INS_PFPNACC'
    if id == 549:
        return 'X86_INS_PFRCPIT1'
    if id == 550:
        return 'X86_INS_PFRCPIT2'
    if id == 551:
        return 'X86_INS_PFRCP'
    if id == 552:
        return 'X86_INS_PFRSQIT1'
    if id == 553:
        return 'X86_INS_PFRSQRT'
    if id == 554:
        return 'X86_INS_PFSUBR'
    if id == 555:
        return 'X86_INS_PFSUB'
    if id == 556:
        return 'X86_INS_PHMINPOSUW'
    if id == 557:
        return 'X86_INS_PI2FD'
    if id == 558:
        return 'X86_INS_PI2FW'
    if id == 559:
        return 'X86_INS_PINSRB'
    if id == 560:
        return 'X86_INS_PINSRD'
    if id == 561:
        return 'X86_INS_PINSRQ'
    if id == 562:
        return 'X86_INS_PMAXSB'
    if id == 563:
        return 'X86_INS_PMAXSD'
    if id == 564:
        return 'X86_INS_PMAXUD'
    if id == 565:
        return 'X86_INS_PMAXUW'
    if id == 566:
        return 'X86_INS_PMINSB'
    if id == 567:
        return 'X86_INS_PMINSD'
    if id == 568:
        return 'X86_INS_PMINUD'
    if id == 569:
        return 'X86_INS_PMINUW'
    if id == 570:
        return 'X86_INS_PMOVSXBD'
    if id == 571:
        return 'X86_INS_PMOVSXBQ'
    if id == 572:
        return 'X86_INS_PMOVSXBW'
    if id == 573:
        return 'X86_INS_PMOVSXDQ'
    if id == 574:
        return 'X86_INS_PMOVSXWD'
    if id == 575:
        return 'X86_INS_PMOVSXWQ'
    if id == 576:
        return 'X86_INS_PMOVZXBD'
    if id == 577:
        return 'X86_INS_PMOVZXBQ'
    if id == 578:
        return 'X86_INS_PMOVZXBW'
    if id == 579:
        return 'X86_INS_PMOVZXDQ'
    if id == 580:
        return 'X86_INS_PMOVZXWD'
    if id == 581:
        return 'X86_INS_PMOVZXWQ'
    if id == 582:
        return 'X86_INS_PMULDQ'
    if id == 583:
        return 'X86_INS_PMULHRW'
    if id == 584:
        return 'X86_INS_PMULLD'
    if id == 585:
        return 'X86_INS_POP'
    if id == 586:
        return 'X86_INS_POPAW'
    if id == 587:
        return 'X86_INS_POPAL'
    if id == 588:
        return 'X86_INS_POPCNT'
    if id == 589:
        return 'X86_INS_POPF'
    if id == 590:
        return 'X86_INS_POPFD'
    if id == 591:
        return 'X86_INS_POPFQ'
    if id == 592:
        return 'X86_INS_PREFETCH'
    if id == 593:
        return 'X86_INS_PREFETCHNTA'
    if id == 594:
        return 'X86_INS_PREFETCHT0'
    if id == 595:
        return 'X86_INS_PREFETCHT1'
    if id == 596:
        return 'X86_INS_PREFETCHT2'
    if id == 597:
        return 'X86_INS_PREFETCHW'
    if id == 598:
        return 'X86_INS_PREFETCHWT1'
    if id == 599:
        return 'X86_INS_PSHUFD'
    if id == 600:
        return 'X86_INS_PSHUFHW'
    if id == 601:
        return 'X86_INS_PSHUFLW'
    if id == 602:
        return 'X86_INS_PSLLDQ'
    if id == 603:
        return 'X86_INS_PSRLDQ'
    if id == 604:
        return 'X86_INS_PSWAPD'
    if id == 605:
        return 'X86_INS_PTEST'
    if id == 606:
        return 'X86_INS_PTWRITE'
    if id == 607:
        return 'X86_INS_PUNPCKHQDQ'
    if id == 608:
        return 'X86_INS_PUNPCKLQDQ'
    if id == 609:
        return 'X86_INS_PUSH'
    if id == 610:
        return 'X86_INS_PUSHAW'
    if id == 611:
        return 'X86_INS_PUSHAL'
    if id == 612:
        return 'X86_INS_PUSHF'
    if id == 613:
        return 'X86_INS_PUSHFD'
    if id == 614:
        return 'X86_INS_PUSHFQ'
    if id == 615:
        return 'X86_INS_RCL'
    if id == 616:
        return 'X86_INS_RCPPS'
    if id == 617:
        return 'X86_INS_RCPSS'
    if id == 618:
        return 'X86_INS_RCR'
    if id == 619:
        return 'X86_INS_RDFSBASE'
    if id == 620:
        return 'X86_INS_RDGSBASE'
    if id == 621:
        return 'X86_INS_RDMSR'
    if id == 622:
        return 'X86_INS_RDPID'
    if id == 623:
        return 'X86_INS_RDPKRU'
    if id == 624:
        return 'X86_INS_RDPMC'
    if id == 625:
        return 'X86_INS_RDRAND'
    if id == 626:
        return 'X86_INS_RDSEED'
    if id == 627:
        return 'X86_INS_RDSSPD'
    if id == 628:
        return 'X86_INS_RDSSPQ'
    if id == 629:
        return 'X86_INS_RDTSC'
    if id == 630:
        return 'X86_INS_RDTSCP'
    if id == 631:
        return 'X86_INS_REPNE'
    if id == 632:
        return 'X86_INS_REP'
    if id == 633:
        return 'X86_INS_RET'
    if id == 634:
        return 'X86_INS_REX64'
    if id == 635:
        return 'X86_INS_ROL'
    if id == 636:
        return 'X86_INS_ROR'
    if id == 637:
        return 'X86_INS_RORX'
    if id == 638:
        return 'X86_INS_ROUNDPD'
    if id == 639:
        return 'X86_INS_ROUNDPS'
    if id == 640:
        return 'X86_INS_ROUNDSD'
    if id == 641:
        return 'X86_INS_ROUNDSS'
    if id == 642:
        return 'X86_INS_RSM'
    if id == 643:
        return 'X86_INS_RSQRTPS'
    if id == 644:
        return 'X86_INS_RSQRTSS'
    if id == 645:
        return 'X86_INS_RSTORSSP'
    if id == 646:
        return 'X86_INS_SAHF'
    if id == 647:
        return 'X86_INS_SAL'
    if id == 648:
        return 'X86_INS_SALC'
    if id == 649:
        return 'X86_INS_SAR'
    if id == 650:
        return 'X86_INS_SARX'
    if id == 651:
        return 'X86_INS_SAVEPREVSSP'
    if id == 652:
        return 'X86_INS_SBB'
    if id == 653:
        return 'X86_INS_SCASB'
    if id == 654:
        return 'X86_INS_SCASD'
    if id == 655:
        return 'X86_INS_SCASQ'
    if id == 656:
        return 'X86_INS_SCASW'
    if id == 657:
        return 'X86_INS_SETAE'
    if id == 658:
        return 'X86_INS_SETA'
    if id == 659:
        return 'X86_INS_SETBE'
    if id == 660:
        return 'X86_INS_SETB'
    if id == 661:
        return 'X86_INS_SETE'
    if id == 662:
        return 'X86_INS_SETGE'
    if id == 663:
        return 'X86_INS_SETG'
    if id == 664:
        return 'X86_INS_SETLE'
    if id == 665:
        return 'X86_INS_SETL'
    if id == 666:
        return 'X86_INS_SETNE'
    if id == 667:
        return 'X86_INS_SETNO'
    if id == 668:
        return 'X86_INS_SETNP'
    if id == 669:
        return 'X86_INS_SETNS'
    if id == 670:
        return 'X86_INS_SETO'
    if id == 671:
        return 'X86_INS_SETP'
    if id == 672:
        return 'X86_INS_SETSSBSY'
    if id == 673:
        return 'X86_INS_SETS'
    if id == 674:
        return 'X86_INS_SFENCE'
    if id == 675:
        return 'X86_INS_SGDT'
    if id == 676:
        return 'X86_INS_SHA1MSG1'
    if id == 677:
        return 'X86_INS_SHA1MSG2'
    if id == 678:
        return 'X86_INS_SHA1NEXTE'
    if id == 679:
        return 'X86_INS_SHA1RNDS4'
    if id == 680:
        return 'X86_INS_SHA256MSG1'
    if id == 681:
        return 'X86_INS_SHA256MSG2'
    if id == 682:
        return 'X86_INS_SHA256RNDS2'
    if id == 683:
        return 'X86_INS_SHL'
    if id == 684:
        return 'X86_INS_SHLD'
    if id == 685:
        return 'X86_INS_SHLX'
    if id == 686:
        return 'X86_INS_SHR'
    if id == 687:
        return 'X86_INS_SHRD'
    if id == 688:
        return 'X86_INS_SHRX'
    if id == 689:
        return 'X86_INS_SHUFPD'
    if id == 690:
        return 'X86_INS_SHUFPS'
    if id == 691:
        return 'X86_INS_SIDT'
    if id == 692:
        return 'X86_INS_FSIN'
    if id == 693:
        return 'X86_INS_SKINIT'
    if id == 694:
        return 'X86_INS_SLDT'
    if id == 695:
        return 'X86_INS_SLWPCB'
    if id == 696:
        return 'X86_INS_SMSW'
    if id == 697:
        return 'X86_INS_SQRTPD'
    if id == 698:
        return 'X86_INS_SQRTPS'
    if id == 699:
        return 'X86_INS_SQRTSD'
    if id == 700:
        return 'X86_INS_SQRTSS'
    if id == 701:
        return 'X86_INS_FSQRT'
    if id == 702:
        return 'X86_INS_STAC'
    if id == 703:
        return 'X86_INS_STC'
    if id == 704:
        return 'X86_INS_STD'
    if id == 705:
        return 'X86_INS_STGI'
    if id == 706:
        return 'X86_INS_STI'
    if id == 707:
        return 'X86_INS_STMXCSR'
    if id == 708:
        return 'X86_INS_STOSB'
    if id == 709:
        return 'X86_INS_STOSD'
    if id == 710:
        return 'X86_INS_STOSQ'
    if id == 711:
        return 'X86_INS_STOSW'
    if id == 712:
        return 'X86_INS_STR'
    if id == 713:
        return 'X86_INS_FST'
    if id == 714:
        return 'X86_INS_FSTP'
    if id == 715:
        return 'X86_INS_SUB'
    if id == 716:
        return 'X86_INS_SUBPD'
    if id == 717:
        return 'X86_INS_SUBPS'
    if id == 718:
        return 'X86_INS_FSUBR'
    if id == 719:
        return 'X86_INS_FISUBR'
    if id == 720:
        return 'X86_INS_FSUBRP'
    if id == 721:
        return 'X86_INS_SUBSD'
    if id == 722:
        return 'X86_INS_SUBSS'
    if id == 723:
        return 'X86_INS_FSUB'
    if id == 724:
        return 'X86_INS_FISUB'
    if id == 725:
        return 'X86_INS_FSUBP'
    if id == 726:
        return 'X86_INS_SWAPGS'
    if id == 727:
        return 'X86_INS_SYSCALL'
    if id == 728:
        return 'X86_INS_SYSENTER'
    if id == 729:
        return 'X86_INS_SYSEXIT'
    if id == 730:
        return 'X86_INS_SYSEXITQ'
    if id == 731:
        return 'X86_INS_SYSRET'
    if id == 732:
        return 'X86_INS_SYSRETQ'
    if id == 733:
        return 'X86_INS_T1MSKC'
    if id == 734:
        return 'X86_INS_TEST'
    if id == 735:
        return 'X86_INS_TPAUSE'
    if id == 736:
        return 'X86_INS_FTST'
    if id == 737:
        return 'X86_INS_TZCNT'
    if id == 738:
        return 'X86_INS_TZMSK'
    if id == 739:
        return 'X86_INS_UCOMISD'
    if id == 740:
        return 'X86_INS_UCOMISS'
    if id == 741:
        return 'X86_INS_FUCOMPI'
    if id == 742:
        return 'X86_INS_FUCOMI'
    if id == 743:
        return 'X86_INS_FUCOMPP'
    if id == 744:
        return 'X86_INS_FUCOMP'
    if id == 745:
        return 'X86_INS_FUCOM'
    if id == 746:
        return 'X86_INS_UD0'
    if id == 747:
        return 'X86_INS_UD1'
    if id == 748:
        return 'X86_INS_UD2'
    if id == 749:
        return 'X86_INS_UMONITOR'
    if id == 750:
        return 'X86_INS_UMWAIT'
    if id == 751:
        return 'X86_INS_UNPCKHPD'
    if id == 752:
        return 'X86_INS_UNPCKHPS'
    if id == 753:
        return 'X86_INS_UNPCKLPD'
    if id == 754:
        return 'X86_INS_UNPCKLPS'
    if id == 755:
        return 'X86_INS_V4FMADDPS'
    if id == 756:
        return 'X86_INS_V4FMADDSS'
    if id == 757:
        return 'X86_INS_V4FNMADDPS'
    if id == 758:
        return 'X86_INS_V4FNMADDSS'
    if id == 759:
        return 'X86_INS_VADDPD'
    if id == 760:
        return 'X86_INS_VADDPS'
    if id == 761:
        return 'X86_INS_VADDSD'
    if id == 762:
        return 'X86_INS_VADDSS'
    if id == 763:
        return 'X86_INS_VADDSUBPD'
    if id == 764:
        return 'X86_INS_VADDSUBPS'
    if id == 765:
        return 'X86_INS_VAESDECLAST'
    if id == 766:
        return 'X86_INS_VAESDEC'
    if id == 767:
        return 'X86_INS_VAESENCLAST'
    if id == 768:
        return 'X86_INS_VAESENC'
    if id == 769:
        return 'X86_INS_VAESIMC'
    if id == 770:
        return 'X86_INS_VAESKEYGENASSIST'
    if id == 771:
        return 'X86_INS_VALIGND'
    if id == 772:
        return 'X86_INS_VALIGNQ'
    if id == 773:
        return 'X86_INS_VANDNPD'
    if id == 774:
        return 'X86_INS_VANDNPS'
    if id == 775:
        return 'X86_INS_VANDPD'
    if id == 776:
        return 'X86_INS_VANDPS'
    if id == 777:
        return 'X86_INS_VBLENDMPD'
    if id == 778:
        return 'X86_INS_VBLENDMPS'
    if id == 779:
        return 'X86_INS_VBLENDPD'
    if id == 780:
        return 'X86_INS_VBLENDPS'
    if id == 781:
        return 'X86_INS_VBLENDVPD'
    if id == 782:
        return 'X86_INS_VBLENDVPS'
    if id == 783:
        return 'X86_INS_VBROADCASTF128'
    if id == 784:
        return 'X86_INS_VBROADCASTF32X2'
    if id == 785:
        return 'X86_INS_VBROADCASTF32X4'
    if id == 786:
        return 'X86_INS_VBROADCASTF32X8'
    if id == 787:
        return 'X86_INS_VBROADCASTF64X2'
    if id == 788:
        return 'X86_INS_VBROADCASTF64X4'
    if id == 789:
        return 'X86_INS_VBROADCASTI128'
    if id == 790:
        return 'X86_INS_VBROADCASTI32X2'
    if id == 791:
        return 'X86_INS_VBROADCASTI32X4'
    if id == 792:
        return 'X86_INS_VBROADCASTI32X8'
    if id == 793:
        return 'X86_INS_VBROADCASTI64X2'
    if id == 794:
        return 'X86_INS_VBROADCASTI64X4'
    if id == 795:
        return 'X86_INS_VBROADCASTSD'
    if id == 796:
        return 'X86_INS_VBROADCASTSS'
    if id == 797:
        return 'X86_INS_VCMP'
    if id == 798:
        return 'X86_INS_VCMPPD'
    if id == 799:
        return 'X86_INS_VCMPPS'
    if id == 800:
        return 'X86_INS_VCMPSD'
    if id == 801:
        return 'X86_INS_VCMPSS'
    if id == 802:
        return 'X86_INS_VCOMISD'
    if id == 803:
        return 'X86_INS_VCOMISS'
    if id == 804:
        return 'X86_INS_VCOMPRESSPD'
    if id == 805:
        return 'X86_INS_VCOMPRESSPS'
    if id == 806:
        return 'X86_INS_VCVTDQ2PD'
    if id == 807:
        return 'X86_INS_VCVTDQ2PS'
    if id == 808:
        return 'X86_INS_VCVTPD2DQ'
    if id == 809:
        return 'X86_INS_VCVTPD2PS'
    if id == 810:
        return 'X86_INS_VCVTPD2QQ'
    if id == 811:
        return 'X86_INS_VCVTPD2UDQ'
    if id == 812:
        return 'X86_INS_VCVTPD2UQQ'
    if id == 813:
        return 'X86_INS_VCVTPH2PS'
    if id == 814:
        return 'X86_INS_VCVTPS2DQ'
    if id == 815:
        return 'X86_INS_VCVTPS2PD'
    if id == 816:
        return 'X86_INS_VCVTPS2PH'
    if id == 817:
        return 'X86_INS_VCVTPS2QQ'
    if id == 818:
        return 'X86_INS_VCVTPS2UDQ'
    if id == 819:
        return 'X86_INS_VCVTPS2UQQ'
    if id == 820:
        return 'X86_INS_VCVTQQ2PD'
    if id == 821:
        return 'X86_INS_VCVTQQ2PS'
    if id == 822:
        return 'X86_INS_VCVTSD2SI'
    if id == 823:
        return 'X86_INS_VCVTSD2SS'
    if id == 824:
        return 'X86_INS_VCVTSD2USI'
    if id == 825:
        return 'X86_INS_VCVTSI2SD'
    if id == 826:
        return 'X86_INS_VCVTSI2SS'
    if id == 827:
        return 'X86_INS_VCVTSS2SD'
    if id == 828:
        return 'X86_INS_VCVTSS2SI'
    if id == 829:
        return 'X86_INS_VCVTSS2USI'
    if id == 830:
        return 'X86_INS_VCVTTPD2DQ'
    if id == 831:
        return 'X86_INS_VCVTTPD2QQ'
    if id == 832:
        return 'X86_INS_VCVTTPD2UDQ'
    if id == 833:
        return 'X86_INS_VCVTTPD2UQQ'
    if id == 834:
        return 'X86_INS_VCVTTPS2DQ'
    if id == 835:
        return 'X86_INS_VCVTTPS2QQ'
    if id == 836:
        return 'X86_INS_VCVTTPS2UDQ'
    if id == 837:
        return 'X86_INS_VCVTTPS2UQQ'
    if id == 838:
        return 'X86_INS_VCVTTSD2SI'
    if id == 839:
        return 'X86_INS_VCVTTSD2USI'
    if id == 840:
        return 'X86_INS_VCVTTSS2SI'
    if id == 841:
        return 'X86_INS_VCVTTSS2USI'
    if id == 842:
        return 'X86_INS_VCVTUDQ2PD'
    if id == 843:
        return 'X86_INS_VCVTUDQ2PS'
    if id == 844:
        return 'X86_INS_VCVTUQQ2PD'
    if id == 845:
        return 'X86_INS_VCVTUQQ2PS'
    if id == 846:
        return 'X86_INS_VCVTUSI2SD'
    if id == 847:
        return 'X86_INS_VCVTUSI2SS'
    if id == 848:
        return 'X86_INS_VDBPSADBW'
    if id == 849:
        return 'X86_INS_VDIVPD'
    if id == 850:
        return 'X86_INS_VDIVPS'
    if id == 851:
        return 'X86_INS_VDIVSD'
    if id == 852:
        return 'X86_INS_VDIVSS'
    if id == 853:
        return 'X86_INS_VDPPD'
    if id == 854:
        return 'X86_INS_VDPPS'
    if id == 855:
        return 'X86_INS_VERR'
    if id == 856:
        return 'X86_INS_VERW'
    if id == 857:
        return 'X86_INS_VEXP2PD'
    if id == 858:
        return 'X86_INS_VEXP2PS'
    if id == 859:
        return 'X86_INS_VEXPANDPD'
    if id == 860:
        return 'X86_INS_VEXPANDPS'
    if id == 861:
        return 'X86_INS_VEXTRACTF128'
    if id == 862:
        return 'X86_INS_VEXTRACTF32X4'
    if id == 863:
        return 'X86_INS_VEXTRACTF32X8'
    if id == 864:
        return 'X86_INS_VEXTRACTF64X2'
    if id == 865:
        return 'X86_INS_VEXTRACTF64X4'
    if id == 866:
        return 'X86_INS_VEXTRACTI128'
    if id == 867:
        return 'X86_INS_VEXTRACTI32X4'
    if id == 868:
        return 'X86_INS_VEXTRACTI32X8'
    if id == 869:
        return 'X86_INS_VEXTRACTI64X2'
    if id == 870:
        return 'X86_INS_VEXTRACTI64X4'
    if id == 871:
        return 'X86_INS_VEXTRACTPS'
    if id == 872:
        return 'X86_INS_VFIXUPIMMPD'
    if id == 873:
        return 'X86_INS_VFIXUPIMMPS'
    if id == 874:
        return 'X86_INS_VFIXUPIMMSD'
    if id == 875:
        return 'X86_INS_VFIXUPIMMSS'
    if id == 876:
        return 'X86_INS_VFMADD132PD'
    if id == 877:
        return 'X86_INS_VFMADD132PS'
    if id == 878:
        return 'X86_INS_VFMADD132SD'
    if id == 879:
        return 'X86_INS_VFMADD132SS'
    if id == 880:
        return 'X86_INS_VFMADD213PD'
    if id == 881:
        return 'X86_INS_VFMADD213PS'
    if id == 882:
        return 'X86_INS_VFMADD213SD'
    if id == 883:
        return 'X86_INS_VFMADD213SS'
    if id == 884:
        return 'X86_INS_VFMADD231PD'
    if id == 885:
        return 'X86_INS_VFMADD231PS'
    if id == 886:
        return 'X86_INS_VFMADD231SD'
    if id == 887:
        return 'X86_INS_VFMADD231SS'
    if id == 888:
        return 'X86_INS_VFMADDPD'
    if id == 889:
        return 'X86_INS_VFMADDPS'
    if id == 890:
        return 'X86_INS_VFMADDSD'
    if id == 891:
        return 'X86_INS_VFMADDSS'
    if id == 892:
        return 'X86_INS_VFMADDSUB132PD'
    if id == 893:
        return 'X86_INS_VFMADDSUB132PS'
    if id == 894:
        return 'X86_INS_VFMADDSUB213PD'
    if id == 895:
        return 'X86_INS_VFMADDSUB213PS'
    if id == 896:
        return 'X86_INS_VFMADDSUB231PD'
    if id == 897:
        return 'X86_INS_VFMADDSUB231PS'
    if id == 898:
        return 'X86_INS_VFMADDSUBPD'
    if id == 899:
        return 'X86_INS_VFMADDSUBPS'
    if id == 900:
        return 'X86_INS_VFMSUB132PD'
    if id == 901:
        return 'X86_INS_VFMSUB132PS'
    if id == 902:
        return 'X86_INS_VFMSUB132SD'
    if id == 903:
        return 'X86_INS_VFMSUB132SS'
    if id == 904:
        return 'X86_INS_VFMSUB213PD'
    if id == 905:
        return 'X86_INS_VFMSUB213PS'
    if id == 906:
        return 'X86_INS_VFMSUB213SD'
    if id == 907:
        return 'X86_INS_VFMSUB213SS'
    if id == 908:
        return 'X86_INS_VFMSUB231PD'
    if id == 909:
        return 'X86_INS_VFMSUB231PS'
    if id == 910:
        return 'X86_INS_VFMSUB231SD'
    if id == 911:
        return 'X86_INS_VFMSUB231SS'
    if id == 912:
        return 'X86_INS_VFMSUBADD132PD'
    if id == 913:
        return 'X86_INS_VFMSUBADD132PS'
    if id == 914:
        return 'X86_INS_VFMSUBADD213PD'
    if id == 915:
        return 'X86_INS_VFMSUBADD213PS'
    if id == 916:
        return 'X86_INS_VFMSUBADD231PD'
    if id == 917:
        return 'X86_INS_VFMSUBADD231PS'
    if id == 918:
        return 'X86_INS_VFMSUBADDPD'
    if id == 919:
        return 'X86_INS_VFMSUBADDPS'
    if id == 920:
        return 'X86_INS_VFMSUBPD'
    if id == 921:
        return 'X86_INS_VFMSUBPS'
    if id == 922:
        return 'X86_INS_VFMSUBSD'
    if id == 923:
        return 'X86_INS_VFMSUBSS'
    if id == 924:
        return 'X86_INS_VFNMADD132PD'
    if id == 925:
        return 'X86_INS_VFNMADD132PS'
    if id == 926:
        return 'X86_INS_VFNMADD132SD'
    if id == 927:
        return 'X86_INS_VFNMADD132SS'
    if id == 928:
        return 'X86_INS_VFNMADD213PD'
    if id == 929:
        return 'X86_INS_VFNMADD213PS'
    if id == 930:
        return 'X86_INS_VFNMADD213SD'
    if id == 931:
        return 'X86_INS_VFNMADD213SS'
    if id == 932:
        return 'X86_INS_VFNMADD231PD'
    if id == 933:
        return 'X86_INS_VFNMADD231PS'
    if id == 934:
        return 'X86_INS_VFNMADD231SD'
    if id == 935:
        return 'X86_INS_VFNMADD231SS'
    if id == 936:
        return 'X86_INS_VFNMADDPD'
    if id == 937:
        return 'X86_INS_VFNMADDPS'
    if id == 938:
        return 'X86_INS_VFNMADDSD'
    if id == 939:
        return 'X86_INS_VFNMADDSS'
    if id == 940:
        return 'X86_INS_VFNMSUB132PD'
    if id == 941:
        return 'X86_INS_VFNMSUB132PS'
    if id == 942:
        return 'X86_INS_VFNMSUB132SD'
    if id == 943:
        return 'X86_INS_VFNMSUB132SS'
    if id == 944:
        return 'X86_INS_VFNMSUB213PD'
    if id == 945:
        return 'X86_INS_VFNMSUB213PS'
    if id == 946:
        return 'X86_INS_VFNMSUB213SD'
    if id == 947:
        return 'X86_INS_VFNMSUB213SS'
    if id == 948:
        return 'X86_INS_VFNMSUB231PD'
    if id == 949:
        return 'X86_INS_VFNMSUB231PS'
    if id == 950:
        return 'X86_INS_VFNMSUB231SD'
    if id == 951:
        return 'X86_INS_VFNMSUB231SS'
    if id == 952:
        return 'X86_INS_VFNMSUBPD'
    if id == 953:
        return 'X86_INS_VFNMSUBPS'
    if id == 954:
        return 'X86_INS_VFNMSUBSD'
    if id == 955:
        return 'X86_INS_VFNMSUBSS'
    if id == 956:
        return 'X86_INS_VFPCLASSPD'
    if id == 957:
        return 'X86_INS_VFPCLASSPS'
    if id == 958:
        return 'X86_INS_VFPCLASSSD'
    if id == 959:
        return 'X86_INS_VFPCLASSSS'
    if id == 960:
        return 'X86_INS_VFRCZPD'
    if id == 961:
        return 'X86_INS_VFRCZPS'
    if id == 962:
        return 'X86_INS_VFRCZSD'
    if id == 963:
        return 'X86_INS_VFRCZSS'
    if id == 964:
        return 'X86_INS_VGATHERDPD'
    if id == 965:
        return 'X86_INS_VGATHERDPS'
    if id == 966:
        return 'X86_INS_VGATHERPF0DPD'
    if id == 967:
        return 'X86_INS_VGATHERPF0DPS'
    if id == 968:
        return 'X86_INS_VGATHERPF0QPD'
    if id == 969:
        return 'X86_INS_VGATHERPF0QPS'
    if id == 970:
        return 'X86_INS_VGATHERPF1DPD'
    if id == 971:
        return 'X86_INS_VGATHERPF1DPS'
    if id == 972:
        return 'X86_INS_VGATHERPF1QPD'
    if id == 973:
        return 'X86_INS_VGATHERPF1QPS'
    if id == 974:
        return 'X86_INS_VGATHERQPD'
    if id == 975:
        return 'X86_INS_VGATHERQPS'
    if id == 976:
        return 'X86_INS_VGETEXPPD'
    if id == 977:
        return 'X86_INS_VGETEXPPS'
    if id == 978:
        return 'X86_INS_VGETEXPSD'
    if id == 979:
        return 'X86_INS_VGETEXPSS'
    if id == 980:
        return 'X86_INS_VGETMANTPD'
    if id == 981:
        return 'X86_INS_VGETMANTPS'
    if id == 982:
        return 'X86_INS_VGETMANTSD'
    if id == 983:
        return 'X86_INS_VGETMANTSS'
    if id == 984:
        return 'X86_INS_VGF2P8AFFINEINVQB'
    if id == 985:
        return 'X86_INS_VGF2P8AFFINEQB'
    if id == 986:
        return 'X86_INS_VGF2P8MULB'
    if id == 987:
        return 'X86_INS_VHADDPD'
    if id == 988:
        return 'X86_INS_VHADDPS'
    if id == 989:
        return 'X86_INS_VHSUBPD'
    if id == 990:
        return 'X86_INS_VHSUBPS'
    if id == 991:
        return 'X86_INS_VINSERTF128'
    if id == 992:
        return 'X86_INS_VINSERTF32X4'
    if id == 993:
        return 'X86_INS_VINSERTF32X8'
    if id == 994:
        return 'X86_INS_VINSERTF64X2'
    if id == 995:
        return 'X86_INS_VINSERTF64X4'
    if id == 996:
        return 'X86_INS_VINSERTI128'
    if id == 997:
        return 'X86_INS_VINSERTI32X4'
    if id == 998:
        return 'X86_INS_VINSERTI32X8'
    if id == 999:
        return 'X86_INS_VINSERTI64X2'
    if id == 1000:
        return 'X86_INS_VINSERTI64X4'
    if id == 1001:
        return 'X86_INS_VINSERTPS'
    if id == 1002:
        return 'X86_INS_VLDDQU'
    if id == 1003:
        return 'X86_INS_VLDMXCSR'
    if id == 1004:
        return 'X86_INS_VMASKMOVDQU'
    if id == 1005:
        return 'X86_INS_VMASKMOVPD'
    if id == 1006:
        return 'X86_INS_VMASKMOVPS'
    if id == 1007:
        return 'X86_INS_VMAXPD'
    if id == 1008:
        return 'X86_INS_VMAXPS'
    if id == 1009:
        return 'X86_INS_VMAXSD'
    if id == 1010:
        return 'X86_INS_VMAXSS'
    if id == 1011:
        return 'X86_INS_VMCALL'
    if id == 1012:
        return 'X86_INS_VMCLEAR'
    if id == 1013:
        return 'X86_INS_VMFUNC'
    if id == 1014:
        return 'X86_INS_VMINPD'
    if id == 1015:
        return 'X86_INS_VMINPS'
    if id == 1016:
        return 'X86_INS_VMINSD'
    if id == 1017:
        return 'X86_INS_VMINSS'
    if id == 1018:
        return 'X86_INS_VMLAUNCH'
    if id == 1019:
        return 'X86_INS_VMLOAD'
    if id == 1020:
        return 'X86_INS_VMMCALL'
    if id == 1021:
        return 'X86_INS_VMOVQ'
    if id == 1022:
        return 'X86_INS_VMOVAPD'
    if id == 1023:
        return 'X86_INS_VMOVAPS'
    if id == 1024:
        return 'X86_INS_VMOVDDUP'
    if id == 1025:
        return 'X86_INS_VMOVD'
    if id == 1026:
        return 'X86_INS_VMOVDQA32'
    if id == 1027:
        return 'X86_INS_VMOVDQA64'
    if id == 1028:
        return 'X86_INS_VMOVDQA'
    if id == 1029:
        return 'X86_INS_VMOVDQU16'
    if id == 1030:
        return 'X86_INS_VMOVDQU32'
    if id == 1031:
        return 'X86_INS_VMOVDQU64'
    if id == 1032:
        return 'X86_INS_VMOVDQU8'
    if id == 1033:
        return 'X86_INS_VMOVDQU'
    if id == 1034:
        return 'X86_INS_VMOVHLPS'
    if id == 1035:
        return 'X86_INS_VMOVHPD'
    if id == 1036:
        return 'X86_INS_VMOVHPS'
    if id == 1037:
        return 'X86_INS_VMOVLHPS'
    if id == 1038:
        return 'X86_INS_VMOVLPD'
    if id == 1039:
        return 'X86_INS_VMOVLPS'
    if id == 1040:
        return 'X86_INS_VMOVMSKPD'
    if id == 1041:
        return 'X86_INS_VMOVMSKPS'
    if id == 1042:
        return 'X86_INS_VMOVNTDQA'
    if id == 1043:
        return 'X86_INS_VMOVNTDQ'
    if id == 1044:
        return 'X86_INS_VMOVNTPD'
    if id == 1045:
        return 'X86_INS_VMOVNTPS'
    if id == 1046:
        return 'X86_INS_VMOVSD'
    if id == 1047:
        return 'X86_INS_VMOVSHDUP'
    if id == 1048:
        return 'X86_INS_VMOVSLDUP'
    if id == 1049:
        return 'X86_INS_VMOVSS'
    if id == 1050:
        return 'X86_INS_VMOVUPD'
    if id == 1051:
        return 'X86_INS_VMOVUPS'
    if id == 1052:
        return 'X86_INS_VMPSADBW'
    if id == 1053:
        return 'X86_INS_VMPTRLD'
    if id == 1054:
        return 'X86_INS_VMPTRST'
    if id == 1055:
        return 'X86_INS_VMREAD'
    if id == 1056:
        return 'X86_INS_VMRESUME'
    if id == 1057:
        return 'X86_INS_VMRUN'
    if id == 1058:
        return 'X86_INS_VMSAVE'
    if id == 1059:
        return 'X86_INS_VMULPD'
    if id == 1060:
        return 'X86_INS_VMULPS'
    if id == 1061:
        return 'X86_INS_VMULSD'
    if id == 1062:
        return 'X86_INS_VMULSS'
    if id == 1063:
        return 'X86_INS_VMWRITE'
    if id == 1064:
        return 'X86_INS_VMXOFF'
    if id == 1065:
        return 'X86_INS_VMXON'
    if id == 1066:
        return 'X86_INS_VORPD'
    if id == 1067:
        return 'X86_INS_VORPS'
    if id == 1068:
        return 'X86_INS_VP4DPWSSDS'
    if id == 1069:
        return 'X86_INS_VP4DPWSSD'
    if id == 1070:
        return 'X86_INS_VPABSB'
    if id == 1071:
        return 'X86_INS_VPABSD'
    if id == 1072:
        return 'X86_INS_VPABSQ'
    if id == 1073:
        return 'X86_INS_VPABSW'
    if id == 1074:
        return 'X86_INS_VPACKSSDW'
    if id == 1075:
        return 'X86_INS_VPACKSSWB'
    if id == 1076:
        return 'X86_INS_VPACKUSDW'
    if id == 1077:
        return 'X86_INS_VPACKUSWB'
    if id == 1078:
        return 'X86_INS_VPADDB'
    if id == 1079:
        return 'X86_INS_VPADDD'
    if id == 1080:
        return 'X86_INS_VPADDQ'
    if id == 1081:
        return 'X86_INS_VPADDSB'
    if id == 1082:
        return 'X86_INS_VPADDSW'
    if id == 1083:
        return 'X86_INS_VPADDUSB'
    if id == 1084:
        return 'X86_INS_VPADDUSW'
    if id == 1085:
        return 'X86_INS_VPADDW'
    if id == 1086:
        return 'X86_INS_VPALIGNR'
    if id == 1087:
        return 'X86_INS_VPANDD'
    if id == 1088:
        return 'X86_INS_VPANDND'
    if id == 1089:
        return 'X86_INS_VPANDNQ'
    if id == 1090:
        return 'X86_INS_VPANDN'
    if id == 1091:
        return 'X86_INS_VPANDQ'
    if id == 1092:
        return 'X86_INS_VPAND'
    if id == 1093:
        return 'X86_INS_VPAVGB'
    if id == 1094:
        return 'X86_INS_VPAVGW'
    if id == 1095:
        return 'X86_INS_VPBLENDD'
    if id == 1096:
        return 'X86_INS_VPBLENDMB'
    if id == 1097:
        return 'X86_INS_VPBLENDMD'
    if id == 1098:
        return 'X86_INS_VPBLENDMQ'
    if id == 1099:
        return 'X86_INS_VPBLENDMW'
    if id == 1100:
        return 'X86_INS_VPBLENDVB'
    if id == 1101:
        return 'X86_INS_VPBLENDW'
    if id == 1102:
        return 'X86_INS_VPBROADCASTB'
    if id == 1103:
        return 'X86_INS_VPBROADCASTD'
    if id == 1104:
        return 'X86_INS_VPBROADCASTMB2Q'
    if id == 1105:
        return 'X86_INS_VPBROADCASTMW2D'
    if id == 1106:
        return 'X86_INS_VPBROADCASTQ'
    if id == 1107:
        return 'X86_INS_VPBROADCASTW'
    if id == 1108:
        return 'X86_INS_VPCLMULQDQ'
    if id == 1109:
        return 'X86_INS_VPCMOV'
    if id == 1110:
        return 'X86_INS_VPCMP'
    if id == 1111:
        return 'X86_INS_VPCMPB'
    if id == 1112:
        return 'X86_INS_VPCMPD'
    if id == 1113:
        return 'X86_INS_VPCMPEQB'
    if id == 1114:
        return 'X86_INS_VPCMPEQD'
    if id == 1115:
        return 'X86_INS_VPCMPEQQ'
    if id == 1116:
        return 'X86_INS_VPCMPEQW'
    if id == 1117:
        return 'X86_INS_VPCMPESTRI'
    if id == 1118:
        return 'X86_INS_VPCMPESTRM'
    if id == 1119:
        return 'X86_INS_VPCMPGTB'
    if id == 1120:
        return 'X86_INS_VPCMPGTD'
    if id == 1121:
        return 'X86_INS_VPCMPGTQ'
    if id == 1122:
        return 'X86_INS_VPCMPGTW'
    if id == 1123:
        return 'X86_INS_VPCMPISTRI'
    if id == 1124:
        return 'X86_INS_VPCMPISTRM'
    if id == 1125:
        return 'X86_INS_VPCMPQ'
    if id == 1126:
        return 'X86_INS_VPCMPUB'
    if id == 1127:
        return 'X86_INS_VPCMPUD'
    if id == 1128:
        return 'X86_INS_VPCMPUQ'
    if id == 1129:
        return 'X86_INS_VPCMPUW'
    if id == 1130:
        return 'X86_INS_VPCMPW'
    if id == 1131:
        return 'X86_INS_VPCOM'
    if id == 1132:
        return 'X86_INS_VPCOMB'
    if id == 1133:
        return 'X86_INS_VPCOMD'
    if id == 1134:
        return 'X86_INS_VPCOMPRESSB'
    if id == 1135:
        return 'X86_INS_VPCOMPRESSD'
    if id == 1136:
        return 'X86_INS_VPCOMPRESSQ'
    if id == 1137:
        return 'X86_INS_VPCOMPRESSW'
    if id == 1138:
        return 'X86_INS_VPCOMQ'
    if id == 1139:
        return 'X86_INS_VPCOMUB'
    if id == 1140:
        return 'X86_INS_VPCOMUD'
    if id == 1141:
        return 'X86_INS_VPCOMUQ'
    if id == 1142:
        return 'X86_INS_VPCOMUW'
    if id == 1143:
        return 'X86_INS_VPCOMW'
    if id == 1144:
        return 'X86_INS_VPCONFLICTD'
    if id == 1145:
        return 'X86_INS_VPCONFLICTQ'
    if id == 1146:
        return 'X86_INS_VPDPBUSDS'
    if id == 1147:
        return 'X86_INS_VPDPBUSD'
    if id == 1148:
        return 'X86_INS_VPDPWSSDS'
    if id == 1149:
        return 'X86_INS_VPDPWSSD'
    if id == 1150:
        return 'X86_INS_VPERM2F128'
    if id == 1151:
        return 'X86_INS_VPERM2I128'
    if id == 1152:
        return 'X86_INS_VPERMB'
    if id == 1153:
        return 'X86_INS_VPERMD'
    if id == 1154:
        return 'X86_INS_VPERMI2B'
    if id == 1155:
        return 'X86_INS_VPERMI2D'
    if id == 1156:
        return 'X86_INS_VPERMI2PD'
    if id == 1157:
        return 'X86_INS_VPERMI2PS'
    if id == 1158:
        return 'X86_INS_VPERMI2Q'
    if id == 1159:
        return 'X86_INS_VPERMI2W'
    if id == 1160:
        return 'X86_INS_VPERMIL2PD'
    if id == 1161:
        return 'X86_INS_VPERMILPD'
    if id == 1162:
        return 'X86_INS_VPERMIL2PS'
    if id == 1163:
        return 'X86_INS_VPERMILPS'
    if id == 1164:
        return 'X86_INS_VPERMPD'
    if id == 1165:
        return 'X86_INS_VPERMPS'
    if id == 1166:
        return 'X86_INS_VPERMQ'
    if id == 1167:
        return 'X86_INS_VPERMT2B'
    if id == 1168:
        return 'X86_INS_VPERMT2D'
    if id == 1169:
        return 'X86_INS_VPERMT2PD'
    if id == 1170:
        return 'X86_INS_VPERMT2PS'
    if id == 1171:
        return 'X86_INS_VPERMT2Q'
    if id == 1172:
        return 'X86_INS_VPERMT2W'
    if id == 1173:
        return 'X86_INS_VPERMW'
    if id == 1174:
        return 'X86_INS_VPEXPANDB'
    if id == 1175:
        return 'X86_INS_VPEXPANDD'
    if id == 1176:
        return 'X86_INS_VPEXPANDQ'
    if id == 1177:
        return 'X86_INS_VPEXPANDW'
    if id == 1178:
        return 'X86_INS_VPEXTRB'
    if id == 1179:
        return 'X86_INS_VPEXTRD'
    if id == 1180:
        return 'X86_INS_VPEXTRQ'
    if id == 1181:
        return 'X86_INS_VPEXTRW'
    if id == 1182:
        return 'X86_INS_VPGATHERDD'
    if id == 1183:
        return 'X86_INS_VPGATHERDQ'
    if id == 1184:
        return 'X86_INS_VPGATHERQD'
    if id == 1185:
        return 'X86_INS_VPGATHERQQ'
    if id == 1186:
        return 'X86_INS_VPHADDBD'
    if id == 1187:
        return 'X86_INS_VPHADDBQ'
    if id == 1188:
        return 'X86_INS_VPHADDBW'
    if id == 1189:
        return 'X86_INS_VPHADDDQ'
    if id == 1190:
        return 'X86_INS_VPHADDD'
    if id == 1191:
        return 'X86_INS_VPHADDSW'
    if id == 1192:
        return 'X86_INS_VPHADDUBD'
    if id == 1193:
        return 'X86_INS_VPHADDUBQ'
    if id == 1194:
        return 'X86_INS_VPHADDUBW'
    if id == 1195:
        return 'X86_INS_VPHADDUDQ'
    if id == 1196:
        return 'X86_INS_VPHADDUWD'
    if id == 1197:
        return 'X86_INS_VPHADDUWQ'
    if id == 1198:
        return 'X86_INS_VPHADDWD'
    if id == 1199:
        return 'X86_INS_VPHADDWQ'
    if id == 1200:
        return 'X86_INS_VPHADDW'
    if id == 1201:
        return 'X86_INS_VPHMINPOSUW'
    if id == 1202:
        return 'X86_INS_VPHSUBBW'
    if id == 1203:
        return 'X86_INS_VPHSUBDQ'
    if id == 1204:
        return 'X86_INS_VPHSUBD'
    if id == 1205:
        return 'X86_INS_VPHSUBSW'
    if id == 1206:
        return 'X86_INS_VPHSUBWD'
    if id == 1207:
        return 'X86_INS_VPHSUBW'
    if id == 1208:
        return 'X86_INS_VPINSRB'
    if id == 1209:
        return 'X86_INS_VPINSRD'
    if id == 1210:
        return 'X86_INS_VPINSRQ'
    if id == 1211:
        return 'X86_INS_VPINSRW'
    if id == 1212:
        return 'X86_INS_VPLZCNTD'
    if id == 1213:
        return 'X86_INS_VPLZCNTQ'
    if id == 1214:
        return 'X86_INS_VPMACSDD'
    if id == 1215:
        return 'X86_INS_VPMACSDQH'
    if id == 1216:
        return 'X86_INS_VPMACSDQL'
    if id == 1217:
        return 'X86_INS_VPMACSSDD'
    if id == 1218:
        return 'X86_INS_VPMACSSDQH'
    if id == 1219:
        return 'X86_INS_VPMACSSDQL'
    if id == 1220:
        return 'X86_INS_VPMACSSWD'
    if id == 1221:
        return 'X86_INS_VPMACSSWW'
    if id == 1222:
        return 'X86_INS_VPMACSWD'
    if id == 1223:
        return 'X86_INS_VPMACSWW'
    if id == 1224:
        return 'X86_INS_VPMADCSSWD'
    if id == 1225:
        return 'X86_INS_VPMADCSWD'
    if id == 1226:
        return 'X86_INS_VPMADD52HUQ'
    if id == 1227:
        return 'X86_INS_VPMADD52LUQ'
    if id == 1228:
        return 'X86_INS_VPMADDUBSW'
    if id == 1229:
        return 'X86_INS_VPMADDWD'
    if id == 1230:
        return 'X86_INS_VPMASKMOVD'
    if id == 1231:
        return 'X86_INS_VPMASKMOVQ'
    if id == 1232:
        return 'X86_INS_VPMAXSB'
    if id == 1233:
        return 'X86_INS_VPMAXSD'
    if id == 1234:
        return 'X86_INS_VPMAXSQ'
    if id == 1235:
        return 'X86_INS_VPMAXSW'
    if id == 1236:
        return 'X86_INS_VPMAXUB'
    if id == 1237:
        return 'X86_INS_VPMAXUD'
    if id == 1238:
        return 'X86_INS_VPMAXUQ'
    if id == 1239:
        return 'X86_INS_VPMAXUW'
    if id == 1240:
        return 'X86_INS_VPMINSB'
    if id == 1241:
        return 'X86_INS_VPMINSD'
    if id == 1242:
        return 'X86_INS_VPMINSQ'
    if id == 1243:
        return 'X86_INS_VPMINSW'
    if id == 1244:
        return 'X86_INS_VPMINUB'
    if id == 1245:
        return 'X86_INS_VPMINUD'
    if id == 1246:
        return 'X86_INS_VPMINUQ'
    if id == 1247:
        return 'X86_INS_VPMINUW'
    if id == 1248:
        return 'X86_INS_VPMOVB2M'
    if id == 1249:
        return 'X86_INS_VPMOVD2M'
    if id == 1250:
        return 'X86_INS_VPMOVDB'
    if id == 1251:
        return 'X86_INS_VPMOVDW'
    if id == 1252:
        return 'X86_INS_VPMOVM2B'
    if id == 1253:
        return 'X86_INS_VPMOVM2D'
    if id == 1254:
        return 'X86_INS_VPMOVM2Q'
    if id == 1255:
        return 'X86_INS_VPMOVM2W'
    if id == 1256:
        return 'X86_INS_VPMOVMSKB'
    if id == 1257:
        return 'X86_INS_VPMOVQ2M'
    if id == 1258:
        return 'X86_INS_VPMOVQB'
    if id == 1259:
        return 'X86_INS_VPMOVQD'
    if id == 1260:
        return 'X86_INS_VPMOVQW'
    if id == 1261:
        return 'X86_INS_VPMOVSDB'
    if id == 1262:
        return 'X86_INS_VPMOVSDW'
    if id == 1263:
        return 'X86_INS_VPMOVSQB'
    if id == 1264:
        return 'X86_INS_VPMOVSQD'
    if id == 1265:
        return 'X86_INS_VPMOVSQW'
    if id == 1266:
        return 'X86_INS_VPMOVSWB'
    if id == 1267:
        return 'X86_INS_VPMOVSXBD'
    if id == 1268:
        return 'X86_INS_VPMOVSXBQ'
    if id == 1269:
        return 'X86_INS_VPMOVSXBW'
    if id == 1270:
        return 'X86_INS_VPMOVSXDQ'
    if id == 1271:
        return 'X86_INS_VPMOVSXWD'
    if id == 1272:
        return 'X86_INS_VPMOVSXWQ'
    if id == 1273:
        return 'X86_INS_VPMOVUSDB'
    if id == 1274:
        return 'X86_INS_VPMOVUSDW'
    if id == 1275:
        return 'X86_INS_VPMOVUSQB'
    if id == 1276:
        return 'X86_INS_VPMOVUSQD'
    if id == 1277:
        return 'X86_INS_VPMOVUSQW'
    if id == 1278:
        return 'X86_INS_VPMOVUSWB'
    if id == 1279:
        return 'X86_INS_VPMOVW2M'
    if id == 1280:
        return 'X86_INS_VPMOVWB'
    if id == 1281:
        return 'X86_INS_VPMOVZXBD'
    if id == 1282:
        return 'X86_INS_VPMOVZXBQ'
    if id == 1283:
        return 'X86_INS_VPMOVZXBW'
    if id == 1284:
        return 'X86_INS_VPMOVZXDQ'
    if id == 1285:
        return 'X86_INS_VPMOVZXWD'
    if id == 1286:
        return 'X86_INS_VPMOVZXWQ'
    if id == 1287:
        return 'X86_INS_VPMULDQ'
    if id == 1288:
        return 'X86_INS_VPMULHRSW'
    if id == 1289:
        return 'X86_INS_VPMULHUW'
    if id == 1290:
        return 'X86_INS_VPMULHW'
    if id == 1291:
        return 'X86_INS_VPMULLD'
    if id == 1292:
        return 'X86_INS_VPMULLQ'
    if id == 1293:
        return 'X86_INS_VPMULLW'
    if id == 1294:
        return 'X86_INS_VPMULTISHIFTQB'
    if id == 1295:
        return 'X86_INS_VPMULUDQ'
    if id == 1296:
        return 'X86_INS_VPOPCNTB'
    if id == 1297:
        return 'X86_INS_VPOPCNTD'
    if id == 1298:
        return 'X86_INS_VPOPCNTQ'
    if id == 1299:
        return 'X86_INS_VPOPCNTW'
    if id == 1300:
        return 'X86_INS_VPORD'
    if id == 1301:
        return 'X86_INS_VPORQ'
    if id == 1302:
        return 'X86_INS_VPOR'
    if id == 1303:
        return 'X86_INS_VPPERM'
    if id == 1304:
        return 'X86_INS_VPROLD'
    if id == 1305:
        return 'X86_INS_VPROLQ'
    if id == 1306:
        return 'X86_INS_VPROLVD'
    if id == 1307:
        return 'X86_INS_VPROLVQ'
    if id == 1308:
        return 'X86_INS_VPRORD'
    if id == 1309:
        return 'X86_INS_VPRORQ'
    if id == 1310:
        return 'X86_INS_VPRORVD'
    if id == 1311:
        return 'X86_INS_VPRORVQ'
    if id == 1312:
        return 'X86_INS_VPROTB'
    if id == 1313:
        return 'X86_INS_VPROTD'
    if id == 1314:
        return 'X86_INS_VPROTQ'
    if id == 1315:
        return 'X86_INS_VPROTW'
    if id == 1316:
        return 'X86_INS_VPSADBW'
    if id == 1317:
        return 'X86_INS_VPSCATTERDD'
    if id == 1318:
        return 'X86_INS_VPSCATTERDQ'
    if id == 1319:
        return 'X86_INS_VPSCATTERQD'
    if id == 1320:
        return 'X86_INS_VPSCATTERQQ'
    if id == 1321:
        return 'X86_INS_VPSHAB'
    if id == 1322:
        return 'X86_INS_VPSHAD'
    if id == 1323:
        return 'X86_INS_VPSHAQ'
    if id == 1324:
        return 'X86_INS_VPSHAW'
    if id == 1325:
        return 'X86_INS_VPSHLB'
    if id == 1326:
        return 'X86_INS_VPSHLDD'
    if id == 1327:
        return 'X86_INS_VPSHLDQ'
    if id == 1328:
        return 'X86_INS_VPSHLDVD'
    if id == 1329:
        return 'X86_INS_VPSHLDVQ'
    if id == 1330:
        return 'X86_INS_VPSHLDVW'
    if id == 1331:
        return 'X86_INS_VPSHLDW'
    if id == 1332:
        return 'X86_INS_VPSHLD'
    if id == 1333:
        return 'X86_INS_VPSHLQ'
    if id == 1334:
        return 'X86_INS_VPSHLW'
    if id == 1335:
        return 'X86_INS_VPSHRDD'
    if id == 1336:
        return 'X86_INS_VPSHRDQ'
    if id == 1337:
        return 'X86_INS_VPSHRDVD'
    if id == 1338:
        return 'X86_INS_VPSHRDVQ'
    if id == 1339:
        return 'X86_INS_VPSHRDVW'
    if id == 1340:
        return 'X86_INS_VPSHRDW'
    if id == 1341:
        return 'X86_INS_VPSHUFBITQMB'
    if id == 1342:
        return 'X86_INS_VPSHUFB'
    if id == 1343:
        return 'X86_INS_VPSHUFD'
    if id == 1344:
        return 'X86_INS_VPSHUFHW'
    if id == 1345:
        return 'X86_INS_VPSHUFLW'
    if id == 1346:
        return 'X86_INS_VPSIGNB'
    if id == 1347:
        return 'X86_INS_VPSIGND'
    if id == 1348:
        return 'X86_INS_VPSIGNW'
    if id == 1349:
        return 'X86_INS_VPSLLDQ'
    if id == 1350:
        return 'X86_INS_VPSLLD'
    if id == 1351:
        return 'X86_INS_VPSLLQ'
    if id == 1352:
        return 'X86_INS_VPSLLVD'
    if id == 1353:
        return 'X86_INS_VPSLLVQ'
    if id == 1354:
        return 'X86_INS_VPSLLVW'
    if id == 1355:
        return 'X86_INS_VPSLLW'
    if id == 1356:
        return 'X86_INS_VPSRAD'
    if id == 1357:
        return 'X86_INS_VPSRAQ'
    if id == 1358:
        return 'X86_INS_VPSRAVD'
    if id == 1359:
        return 'X86_INS_VPSRAVQ'
    if id == 1360:
        return 'X86_INS_VPSRAVW'
    if id == 1361:
        return 'X86_INS_VPSRAW'
    if id == 1362:
        return 'X86_INS_VPSRLDQ'
    if id == 1363:
        return 'X86_INS_VPSRLD'
    if id == 1364:
        return 'X86_INS_VPSRLQ'
    if id == 1365:
        return 'X86_INS_VPSRLVD'
    if id == 1366:
        return 'X86_INS_VPSRLVQ'
    if id == 1367:
        return 'X86_INS_VPSRLVW'
    if id == 1368:
        return 'X86_INS_VPSRLW'
    if id == 1369:
        return 'X86_INS_VPSUBB'
    if id == 1370:
        return 'X86_INS_VPSUBD'
    if id == 1371:
        return 'X86_INS_VPSUBQ'
    if id == 1372:
        return 'X86_INS_VPSUBSB'
    if id == 1373:
        return 'X86_INS_VPSUBSW'
    if id == 1374:
        return 'X86_INS_VPSUBUSB'
    if id == 1375:
        return 'X86_INS_VPSUBUSW'
    if id == 1376:
        return 'X86_INS_VPSUBW'
    if id == 1377:
        return 'X86_INS_VPTERNLOGD'
    if id == 1378:
        return 'X86_INS_VPTERNLOGQ'
    if id == 1379:
        return 'X86_INS_VPTESTMB'
    if id == 1380:
        return 'X86_INS_VPTESTMD'
    if id == 1381:
        return 'X86_INS_VPTESTMQ'
    if id == 1382:
        return 'X86_INS_VPTESTMW'
    if id == 1383:
        return 'X86_INS_VPTESTNMB'
    if id == 1384:
        return 'X86_INS_VPTESTNMD'
    if id == 1385:
        return 'X86_INS_VPTESTNMQ'
    if id == 1386:
        return 'X86_INS_VPTESTNMW'
    if id == 1387:
        return 'X86_INS_VPTEST'
    if id == 1388:
        return 'X86_INS_VPUNPCKHBW'
    if id == 1389:
        return 'X86_INS_VPUNPCKHDQ'
    if id == 1390:
        return 'X86_INS_VPUNPCKHQDQ'
    if id == 1391:
        return 'X86_INS_VPUNPCKHWD'
    if id == 1392:
        return 'X86_INS_VPUNPCKLBW'
    if id == 1393:
        return 'X86_INS_VPUNPCKLDQ'
    if id == 1394:
        return 'X86_INS_VPUNPCKLQDQ'
    if id == 1395:
        return 'X86_INS_VPUNPCKLWD'
    if id == 1396:
        return 'X86_INS_VPXORD'
    if id == 1397:
        return 'X86_INS_VPXORQ'
    if id == 1398:
        return 'X86_INS_VPXOR'
    if id == 1399:
        return 'X86_INS_VRANGEPD'
    if id == 1400:
        return 'X86_INS_VRANGEPS'
    if id == 1401:
        return 'X86_INS_VRANGESD'
    if id == 1402:
        return 'X86_INS_VRANGESS'
    if id == 1403:
        return 'X86_INS_VRCP14PD'
    if id == 1404:
        return 'X86_INS_VRCP14PS'
    if id == 1405:
        return 'X86_INS_VRCP14SD'
    if id == 1406:
        return 'X86_INS_VRCP14SS'
    if id == 1407:
        return 'X86_INS_VRCP28PD'
    if id == 1408:
        return 'X86_INS_VRCP28PS'
    if id == 1409:
        return 'X86_INS_VRCP28SD'
    if id == 1410:
        return 'X86_INS_VRCP28SS'
    if id == 1411:
        return 'X86_INS_VRCPPS'
    if id == 1412:
        return 'X86_INS_VRCPSS'
    if id == 1413:
        return 'X86_INS_VREDUCEPD'
    if id == 1414:
        return 'X86_INS_VREDUCEPS'
    if id == 1415:
        return 'X86_INS_VREDUCESD'
    if id == 1416:
        return 'X86_INS_VREDUCESS'
    if id == 1417:
        return 'X86_INS_VRNDSCALEPD'
    if id == 1418:
        return 'X86_INS_VRNDSCALEPS'
    if id == 1419:
        return 'X86_INS_VRNDSCALESD'
    if id == 1420:
        return 'X86_INS_VRNDSCALESS'
    if id == 1421:
        return 'X86_INS_VROUNDPD'
    if id == 1422:
        return 'X86_INS_VROUNDPS'
    if id == 1423:
        return 'X86_INS_VROUNDSD'
    if id == 1424:
        return 'X86_INS_VROUNDSS'
    if id == 1425:
        return 'X86_INS_VRSQRT14PD'
    if id == 1426:
        return 'X86_INS_VRSQRT14PS'
    if id == 1427:
        return 'X86_INS_VRSQRT14SD'
    if id == 1428:
        return 'X86_INS_VRSQRT14SS'
    if id == 1429:
        return 'X86_INS_VRSQRT28PD'
    if id == 1430:
        return 'X86_INS_VRSQRT28PS'
    if id == 1431:
        return 'X86_INS_VRSQRT28SD'
    if id == 1432:
        return 'X86_INS_VRSQRT28SS'
    if id == 1433:
        return 'X86_INS_VRSQRTPS'
    if id == 1434:
        return 'X86_INS_VRSQRTSS'
    if id == 1435:
        return 'X86_INS_VSCALEFPD'
    if id == 1436:
        return 'X86_INS_VSCALEFPS'
    if id == 1437:
        return 'X86_INS_VSCALEFSD'
    if id == 1438:
        return 'X86_INS_VSCALEFSS'
    if id == 1439:
        return 'X86_INS_VSCATTERDPD'
    if id == 1440:
        return 'X86_INS_VSCATTERDPS'
    if id == 1441:
        return 'X86_INS_VSCATTERPF0DPD'
    if id == 1442:
        return 'X86_INS_VSCATTERPF0DPS'
    if id == 1443:
        return 'X86_INS_VSCATTERPF0QPD'
    if id == 1444:
        return 'X86_INS_VSCATTERPF0QPS'
    if id == 1445:
        return 'X86_INS_VSCATTERPF1DPD'
    if id == 1446:
        return 'X86_INS_VSCATTERPF1DPS'
    if id == 1447:
        return 'X86_INS_VSCATTERPF1QPD'
    if id == 1448:
        return 'X86_INS_VSCATTERPF1QPS'
    if id == 1449:
        return 'X86_INS_VSCATTERQPD'
    if id == 1450:
        return 'X86_INS_VSCATTERQPS'
    if id == 1451:
        return 'X86_INS_VSHUFF32X4'
    if id == 1452:
        return 'X86_INS_VSHUFF64X2'
    if id == 1453:
        return 'X86_INS_VSHUFI32X4'
    if id == 1454:
        return 'X86_INS_VSHUFI64X2'
    if id == 1455:
        return 'X86_INS_VSHUFPD'
    if id == 1456:
        return 'X86_INS_VSHUFPS'
    if id == 1457:
        return 'X86_INS_VSQRTPD'
    if id == 1458:
        return 'X86_INS_VSQRTPS'
    if id == 1459:
        return 'X86_INS_VSQRTSD'
    if id == 1460:
        return 'X86_INS_VSQRTSS'
    if id == 1461:
        return 'X86_INS_VSTMXCSR'
    if id == 1462:
        return 'X86_INS_VSUBPD'
    if id == 1463:
        return 'X86_INS_VSUBPS'
    if id == 1464:
        return 'X86_INS_VSUBSD'
    if id == 1465:
        return 'X86_INS_VSUBSS'
    if id == 1466:
        return 'X86_INS_VTESTPD'
    if id == 1467:
        return 'X86_INS_VTESTPS'
    if id == 1468:
        return 'X86_INS_VUCOMISD'
    if id == 1469:
        return 'X86_INS_VUCOMISS'
    if id == 1470:
        return 'X86_INS_VUNPCKHPD'
    if id == 1471:
        return 'X86_INS_VUNPCKHPS'
    if id == 1472:
        return 'X86_INS_VUNPCKLPD'
    if id == 1473:
        return 'X86_INS_VUNPCKLPS'
    if id == 1474:
        return 'X86_INS_VXORPD'
    if id == 1475:
        return 'X86_INS_VXORPS'
    if id == 1476:
        return 'X86_INS_VZEROALL'
    if id == 1477:
        return 'X86_INS_VZEROUPPER'
    if id == 1478:
        return 'X86_INS_WAIT'
    if id == 1479:
        return 'X86_INS_WBINVD'
    if id == 1480:
        return 'X86_INS_WBNOINVD'
    if id == 1481:
        return 'X86_INS_WRFSBASE'
    if id == 1482:
        return 'X86_INS_WRGSBASE'
    if id == 1483:
        return 'X86_INS_WRMSR'
    if id == 1484:
        return 'X86_INS_WRPKRU'
    if id == 1485:
        return 'X86_INS_WRSSD'
    if id == 1486:
        return 'X86_INS_WRSSQ'
    if id == 1487:
        return 'X86_INS_WRUSSD'
    if id == 1488:
        return 'X86_INS_WRUSSQ'
    if id == 1489:
        return 'X86_INS_XABORT'
    if id == 1490:
        return 'X86_INS_XACQUIRE'
    if id == 1491:
        return 'X86_INS_XADD'
    if id == 1492:
        return 'X86_INS_XBEGIN'
    if id == 1493:
        return 'X86_INS_XCHG'
    if id == 1494:
        return 'X86_INS_FXCH'
    if id == 1495:
        return 'X86_INS_XCRYPTCBC'
    if id == 1496:
        return 'X86_INS_XCRYPTCFB'
    if id == 1497:
        return 'X86_INS_XCRYPTCTR'
    if id == 1498:
        return 'X86_INS_XCRYPTECB'
    if id == 1499:
        return 'X86_INS_XCRYPTOFB'
    if id == 1500:
        return 'X86_INS_XEND'
    if id == 1501:
        return 'X86_INS_XGETBV'
    if id == 1502:
        return 'X86_INS_XLATB'
    if id == 1503:
        return 'X86_INS_XOR'
    if id == 1504:
        return 'X86_INS_XORPD'
    if id == 1505:
        return 'X86_INS_XORPS'
    if id == 1506:
        return 'X86_INS_XRELEASE'
    if id == 1507:
        return 'X86_INS_XRSTOR'
    if id == 1508:
        return 'X86_INS_XRSTOR64'
    if id == 1509:
        return 'X86_INS_XRSTORS'
    if id == 1510:
        return 'X86_INS_XRSTORS64'
    if id == 1511:
        return 'X86_INS_XSAVE'
    if id == 1512:
        return 'X86_INS_XSAVE64'
    if id == 1513:
        return 'X86_INS_XSAVEC'
    if id == 1514:
        return 'X86_INS_XSAVEC64'
    if id == 1515:
        return 'X86_INS_XSAVEOPT'
    if id == 1516:
        return 'X86_INS_XSAVEOPT64'
    if id == 1517:
        return 'X86_INS_XSAVES'
    if id == 1518:
        return 'X86_INS_XSAVES64'
    if id == 1519:
        return 'X86_INS_XSETBV'
    if id == 1520:
        return 'X86_INS_XSHA1'
    if id == 1521:
        return 'X86_INS_XSHA256'
    if id == 1522:
        return 'X86_INS_XSTORE'
    if id == 1523:
        return 'X86_INS_XTEST'
    if id == 1524:
        return 'X86_INS_ENDING'

def x86regStr(reg):
    if reg == 0:
        return 'X86_REG_INVALID'
    if reg == 1:
        return 'X86_REG_AH'
    if reg == 2:
        return 'X86_REG_AL'
    if reg == 3:
        return 'X86_REG_AX'
    if reg == 4:
        return 'X86_REG_BH'
    if reg == 5:
        return 'X86_REG_BL'
    if reg == 6:
        return 'X86_REG_BP'
    if reg == 7:
        return 'X86_REG_BPL'
    if reg == 8:
        return 'X86_REG_BX'
    if reg == 9:
        return 'X86_REG_CH'
    if reg == 10:
        return 'X86_REG_CL'
    if reg == 11:
        return 'X86_REG_CS'
    if reg == 12:
        return 'X86_REG_CX'
    if reg == 13:
        return 'X86_REG_DH'
    if reg == 14:
        return 'X86_REG_DI'
    if reg == 15:
        return 'X86_REG_DIL'
    if reg == 16:
        return 'X86_REG_DL'
    if reg == 17:
        return 'X86_REG_DS'
    if reg == 18:
        return 'X86_REG_DX'
    if reg == 19:
        return 'X86_REG_EAX'
    if reg == 20:
        return 'X86_REG_EBP'
    if reg == 21:
        return 'X86_REG_EBX'
    if reg == 22:
        return 'X86_REG_ECX'
    if reg == 23:
        return 'X86_REG_EDI'
    if reg == 24:
        return 'X86_REG_EDX'
    if reg == 25:
        return 'X86_REG_EFLAGS'
    if reg == 26:
        return 'X86_REG_EIP'
    if reg == 27:
        return 'X86_REG_EIZ'
    if reg == 28:
        return 'X86_REG_ES'
    if reg == 29:
        return 'X86_REG_ESI'
    if reg == 30:
        return 'X86_REG_ESP'
    if reg == 31:
        return 'X86_REG_FPSW'
    if reg == 32:
        return 'X86_REG_FS'
    if reg == 33:
        return 'X86_REG_GS'
    if reg == 34:
        return 'X86_REG_IP'
    if reg == 35:
        return 'X86_REG_RAX'
    if reg == 36:
        return 'X86_REG_RBP'
    if reg == 37:
        return 'X86_REG_RBX'
    if reg == 38:
        return 'X86_REG_RCX'
    if reg == 39:
        return 'X86_REG_RDI'
    if reg == 40:
        return 'X86_REG_RDX'
    if reg == 41:
        return 'X86_REG_RIP'
    if reg == 42:
        return 'X86_REG_RIZ'
    if reg == 43:
        return 'X86_REG_RSI'
    if reg == 44:
        return 'X86_REG_RSP'
    if reg == 45:
        return 'X86_REG_SI'
    if reg == 46:
        return 'X86_REG_SIL'
    if reg == 47:
        return 'X86_REG_SP'
    if reg == 48:
        return 'X86_REG_SPL'
    if reg == 49:
        return 'X86_REG_SS'
    if reg == 50:
        return 'X86_REG_CR0'
    if reg == 51:
        return 'X86_REG_CR1'
    if reg == 52:
        return 'X86_REG_CR2'
    if reg == 53:
        return 'X86_REG_CR3'
    if reg == 54:
        return 'X86_REG_CR4'
    if reg == 55:
        return 'X86_REG_CR5'
    if reg == 56:
        return 'X86_REG_CR6'
    if reg == 57:
        return 'X86_REG_CR7'
    if reg == 58:
        return 'X86_REG_CR8'
    if reg == 59:
        return 'X86_REG_CR9'
    if reg == 60:
        return 'X86_REG_CR10'
    if reg == 61:
        return 'X86_REG_CR11'
    if reg == 62:
        return 'X86_REG_CR12'
    if reg == 63:
        return 'X86_REG_CR13'
    if reg == 64:
        return 'X86_REG_CR14'
    if reg == 65:
        return 'X86_REG_CR15'
    if reg == 66:
        return 'X86_REG_DR0'
    if reg == 67:
        return 'X86_REG_DR1'
    if reg == 68:
        return 'X86_REG_DR2'
    if reg == 69:
        return 'X86_REG_DR3'
    if reg == 70:
        return 'X86_REG_DR4'
    if reg == 71:
        return 'X86_REG_DR5'
    if reg == 72:
        return 'X86_REG_DR6'
    if reg == 73:
        return 'X86_REG_DR7'
    if reg == 74:
        return 'X86_REG_DR8'
    if reg == 75:
        return 'X86_REG_DR9'
    if reg == 76:
        return 'X86_REG_DR10'
    if reg == 77:
        return 'X86_REG_DR11'
    if reg == 78:
        return 'X86_REG_DR12'
    if reg == 79:
        return 'X86_REG_DR13'
    if reg == 80:
        return 'X86_REG_DR14'
    if reg == 81:
        return 'X86_REG_DR15'
    if reg == 82:
        return 'X86_REG_FP0'
    if reg == 83:
        return 'X86_REG_FP1'
    if reg == 84:
        return 'X86_REG_FP2'
    if reg == 85:
        return 'X86_REG_FP3'
    if reg == 86:
        return 'X86_REG_FP4'
    if reg == 87:
        return 'X86_REG_FP5'
    if reg == 88:
        return 'X86_REG_FP6'
    if reg == 89:
        return 'X86_REG_FP7'
    if reg == 90:
        return 'X86_REG_K0'
    if reg == 91:
        return 'X86_REG_K1'
    if reg == 92:
        return 'X86_REG_K2'
    if reg == 93:
        return 'X86_REG_K3'
    if reg == 94:
        return 'X86_REG_K4'
    if reg == 95:
        return 'X86_REG_K5'
    if reg == 96:
        return 'X86_REG_K6'
    if reg == 97:
        return 'X86_REG_K7'
    if reg == 98:
        return 'X86_REG_MM0'
    if reg == 99:
        return 'X86_REG_MM1'
    if reg == 100:
        return 'X86_REG_MM2'
    if reg == 101:
        return 'X86_REG_MM3'
    if reg == 102:
        return 'X86_REG_MM4'
    if reg == 103:
        return 'X86_REG_MM5'
    if reg == 104:
        return 'X86_REG_MM6'
    if reg == 105:
        return 'X86_REG_MM7'
    if reg == 106:
        return 'X86_REG_R8'
    if reg == 107:
        return 'X86_REG_R9'
    if reg == 108:
        return 'X86_REG_R10'
    if reg == 109:
        return 'X86_REG_R11'
    if reg == 110:
        return 'X86_REG_R12'
    if reg == 111:
        return 'X86_REG_R13'
    if reg == 112:
        return 'X86_REG_R14'
    if reg == 113:
        return 'X86_REG_R15'
    if reg == 114:
        return 'X86_REG_ST0'
    if reg == 115:
        return 'X86_REG_ST1'
    if reg == 116:
        return 'X86_REG_ST2'
    if reg == 117:
        return 'X86_REG_ST3'
    if reg == 118:
        return 'X86_REG_ST4'
    if reg == 119:
        return 'X86_REG_ST5'
    if reg == 120:
        return 'X86_REG_ST6'
    if reg == 121:
        return 'X86_REG_ST7'
    if reg == 122:
        return 'X86_REG_XMM0'
    if reg == 123:
        return 'X86_REG_XMM1'
    if reg == 124:
        return 'X86_REG_XMM2'
    if reg == 125:
        return 'X86_REG_XMM3'
    if reg == 126:
        return 'X86_REG_XMM4'
    if reg == 127:
        return 'X86_REG_XMM5'
    if reg == 128:
        return 'X86_REG_XMM6'
    if reg == 129:
        return 'X86_REG_XMM7'
    if reg == 130:
        return 'X86_REG_XMM8'
    if reg == 131:
        return 'X86_REG_XMM9'
    if reg == 132:
        return 'X86_REG_XMM10'
    if reg == 133:
        return 'X86_REG_XMM11'
    if reg == 134:
        return 'X86_REG_XMM12'
    if reg == 135:
        return 'X86_REG_XMM13'
    if reg == 136:
        return 'X86_REG_XMM14'
    if reg == 137:
        return 'X86_REG_XMM15'
    if reg == 138:
        return 'X86_REG_XMM16'
    if reg == 139:
        return 'X86_REG_XMM17'
    if reg == 140:
        return 'X86_REG_XMM18'
    if reg == 141:
        return 'X86_REG_XMM19'
    if reg == 142:
        return 'X86_REG_XMM20'
    if reg == 143:
        return 'X86_REG_XMM21'
    if reg == 144:
        return 'X86_REG_XMM22'
    if reg == 145:
        return 'X86_REG_XMM23'
    if reg == 146:
        return 'X86_REG_XMM24'
    if reg == 147:
        return 'X86_REG_XMM25'
    if reg == 148:
        return 'X86_REG_XMM26'
    if reg == 149:
        return 'X86_REG_XMM27'
    if reg == 150:
        return 'X86_REG_XMM28'
    if reg == 151:
        return 'X86_REG_XMM29'
    if reg == 152:
        return 'X86_REG_XMM30'
    if reg == 153:
        return 'X86_REG_XMM31'
    if reg == 154:
        return 'X86_REG_YMM0'
    if reg == 155:
        return 'X86_REG_YMM1'
    if reg == 156:
        return 'X86_REG_YMM2'
    if reg == 157:
        return 'X86_REG_YMM3'
    if reg == 158:
        return 'X86_REG_YMM4'
    if reg == 159:
        return 'X86_REG_YMM5'
    if reg == 160:
        return 'X86_REG_YMM6'
    if reg == 161:
        return 'X86_REG_YMM7'
    if reg == 162:
        return 'X86_REG_YMM8'
    if reg == 163:
        return 'X86_REG_YMM9'
    if reg == 164:
        return 'X86_REG_YMM10'
    if reg == 165:
        return 'X86_REG_YMM11'
    if reg == 166:
        return 'X86_REG_YMM12'
    if reg == 167:
        return 'X86_REG_YMM13'
    if reg == 168:
        return 'X86_REG_YMM14'
    if reg == 169:
        return 'X86_REG_YMM15'
    if reg == 170:
        return 'X86_REG_YMM16'
    if reg == 171:
        return 'X86_REG_YMM17'
    if reg == 172:
        return 'X86_REG_YMM18'
    if reg == 173:
        return 'X86_REG_YMM19'
    if reg == 174:
        return 'X86_REG_YMM20'
    if reg == 175:
        return 'X86_REG_YMM21'
    if reg == 176:
        return 'X86_REG_YMM22'
    if reg == 177:
        return 'X86_REG_YMM23'
    if reg == 178:
        return 'X86_REG_YMM24'
    if reg == 179:
        return 'X86_REG_YMM25'
    if reg == 180:
        return 'X86_REG_YMM26'
    if reg == 181:
        return 'X86_REG_YMM27'
    if reg == 182:
        return 'X86_REG_YMM28'
    if reg == 183:
        return 'X86_REG_YMM29'
    if reg == 184:
        return 'X86_REG_YMM30'
    if reg == 185:
        return 'X86_REG_YMM31'
    if reg == 186:
        return 'X86_REG_ZMM0'
    if reg == 187:
        return 'X86_REG_ZMM1'
    if reg == 188:
        return 'X86_REG_ZMM2'
    if reg == 189:
        return 'X86_REG_ZMM3'
    if reg == 190:
        return 'X86_REG_ZMM4'
    if reg == 191:
        return 'X86_REG_ZMM5'
    if reg == 192:
        return 'X86_REG_ZMM6'
    if reg == 193:
        return 'X86_REG_ZMM7'
    if reg == 194:
        return 'X86_REG_ZMM8'
    if reg == 195:
        return 'X86_REG_ZMM9'
    if reg == 196:
        return 'X86_REG_ZMM10'
    if reg == 197:
        return 'X86_REG_ZMM11'
    if reg == 198:
        return 'X86_REG_ZMM12'
    if reg == 199:
        return 'X86_REG_ZMM13'
    if reg == 200:
        return 'X86_REG_ZMM14'
    if reg == 201:
        return 'X86_REG_ZMM15'
    if reg == 202:
        return 'X86_REG_ZMM16'
    if reg == 203:
        return 'X86_REG_ZMM17'
    if reg == 204:
        return 'X86_REG_ZMM18'
    if reg == 205:
        return 'X86_REG_ZMM19'
    if reg == 206:
        return 'X86_REG_ZMM20'
    if reg == 207:
        return 'X86_REG_ZMM21'
    if reg == 208:
        return 'X86_REG_ZMM22'
    if reg == 209:
        return 'X86_REG_ZMM23'
    if reg == 210:
        return 'X86_REG_ZMM24'
    if reg == 211:
        return 'X86_REG_ZMM25'
    if reg == 212:
        return 'X86_REG_ZMM26'
    if reg == 213:
        return 'X86_REG_ZMM27'
    if reg == 214:
        return 'X86_REG_ZMM28'
    if reg == 215:
        return 'X86_REG_ZMM29'
    if reg == 216:
        return 'X86_REG_ZMM30'
    if reg == 217:
        return 'X86_REG_ZMM31'
    if reg == 218:
        return 'X86_REG_R8B'
    if reg == 219:
        return 'X86_REG_R9B'
    if reg == 220:
        return 'X86_REG_R10B'
    if reg == 221:
        return 'X86_REG_R11B'
    if reg == 222:
        return 'X86_REG_R12B'
    if reg == 223:
        return 'X86_REG_R13B'
    if reg == 224:
        return 'X86_REG_R14B'
    if reg == 225:
        return 'X86_REG_R15B'
    if reg == 226:
        return 'X86_REG_R8D'
    if reg == 227:
        return 'X86_REG_R9D'
    if reg == 228:
        return 'X86_REG_R10D'
    if reg == 229:
        return 'X86_REG_R11D'
    if reg == 230:
        return 'X86_REG_R12D'
    if reg == 231:
        return 'X86_REG_R13D'
    if reg == 232:
        return 'X86_REG_R14D'
    if reg == 233:
        return 'X86_REG_R15D'
    if reg == 234:
        return 'X86_REG_R8W'
    if reg == 235:
        return 'X86_REG_R9W'
    if reg == 236:
        return 'X86_REG_R10W'
    if reg == 237:
        return 'X86_REG_R11W'
    if reg == 238:
        return 'X86_REG_R12W'
    if reg == 239:
        return 'X86_REG_R13W'
    if reg == 240:
        return 'X86_REG_R14W'
    if reg == 241:
        return 'X86_REG_R15W'
    if reg == 242:
        return 'X86_REG_BND0'
    if reg == 243:
        return 'X86_REG_BND1'
    if reg == 244:
        return 'X86_REG_BND2'
    if reg == 245:
        return 'X86_REG_BND3'
    if reg == 246:
        return 'X86_REG_ENDING'
    return None

def arm64opcodeStr(id):
    if id == 0:
        return 'ARM64_INS_INVALID'
    if id == 1:
        return 'ARM64_INS_ABS'
    if id == 2:
        return 'ARM64_INS_ADC'
    if id == 3:
        return 'ARM64_INS_ADCS'
    if id == 4:
        return 'ARM64_INS_ADD'
    if id == 5:
        return 'ARM64_INS_ADDHN'
    if id == 6:
        return 'ARM64_INS_ADDHN2'
    if id == 7:
        return 'ARM64_INS_ADDP'
    if id == 8:
        return 'ARM64_INS_ADDPL'
    if id == 9:
        return 'ARM64_INS_ADDS'
    if id == 10:
        return 'ARM64_INS_ADDV'
    if id == 11:
        return 'ARM64_INS_ADDVL'
    if id == 12:
        return 'ARM64_INS_ADR'
    if id == 13:
        return 'ARM64_INS_ADRP'
    if id == 14:
        return 'ARM64_INS_AESD'
    if id == 15:
        return 'ARM64_INS_AESE'
    if id == 16:
        return 'ARM64_INS_AESIMC'
    if id == 17:
        return 'ARM64_INS_AESMC'
    if id == 18:
        return 'ARM64_INS_AND'
    if id == 19:
        return 'ARM64_INS_ANDS'
    if id == 20:
        return 'ARM64_INS_ANDV'
    if id == 21:
        return 'ARM64_INS_ASR'
    if id == 22:
        return 'ARM64_INS_ASRD'
    if id == 23:
        return 'ARM64_INS_ASRR'
    if id == 24:
        return 'ARM64_INS_ASRV'
    if id == 25:
        return 'ARM64_INS_AUTDA'
    if id == 26:
        return 'ARM64_INS_AUTDB'
    if id == 27:
        return 'ARM64_INS_AUTDZA'
    if id == 28:
        return 'ARM64_INS_AUTDZB'
    if id == 29:
        return 'ARM64_INS_AUTIA'
    if id == 30:
        return 'ARM64_INS_AUTIA1716'
    if id == 31:
        return 'ARM64_INS_AUTIASP'
    if id == 32:
        return 'ARM64_INS_AUTIAZ'
    if id == 33:
        return 'ARM64_INS_AUTIB'
    if id == 34:
        return 'ARM64_INS_AUTIB1716'
    if id == 35:
        return 'ARM64_INS_AUTIBSP'
    if id == 36:
        return 'ARM64_INS_AUTIBZ'
    if id == 37:
        return 'ARM64_INS_AUTIZA'
    if id == 38:
        return 'ARM64_INS_AUTIZB'
    if id == 39:
        return 'ARM64_INS_B'
    if id == 40:
        return 'ARM64_INS_BCAX'
    if id == 41:
        return 'ARM64_INS_BFM'
    if id == 42:
        return 'ARM64_INS_BIC'
    if id == 43:
        return 'ARM64_INS_BICS'
    if id == 44:
        return 'ARM64_INS_BIF'
    if id == 45:
        return 'ARM64_INS_BIT'
    if id == 46:
        return 'ARM64_INS_BL'
    if id == 47:
        return 'ARM64_INS_BLR'
    if id == 48:
        return 'ARM64_INS_BLRAA'
    if id == 49:
        return 'ARM64_INS_BLRAAZ'
    if id == 50:
        return 'ARM64_INS_BLRAB'
    if id == 51:
        return 'ARM64_INS_BLRABZ'
    if id == 52:
        return 'ARM64_INS_BR'
    if id == 53:
        return 'ARM64_INS_BRAA'
    if id == 54:
        return 'ARM64_INS_BRAAZ'
    if id == 55:
        return 'ARM64_INS_BRAB'
    if id == 56:
        return 'ARM64_INS_BRABZ'
    if id == 57:
        return 'ARM64_INS_BRK'
    if id == 58:
        return 'ARM64_INS_BRKA'
    if id == 59:
        return 'ARM64_INS_BRKAS'
    if id == 60:
        return 'ARM64_INS_BRKB'
    if id == 61:
        return 'ARM64_INS_BRKBS'
    if id == 62:
        return 'ARM64_INS_BRKN'
    if id == 63:
        return 'ARM64_INS_BRKNS'
    if id == 64:
        return 'ARM64_INS_BRKPA'
    if id == 65:
        return 'ARM64_INS_BRKPAS'
    if id == 66:
        return 'ARM64_INS_BRKPB'
    if id == 67:
        return 'ARM64_INS_BRKPBS'
    if id == 68:
        return 'ARM64_INS_BSL'
    if id == 69:
        return 'ARM64_INS_CAS'
    if id == 70:
        return 'ARM64_INS_CASA'
    if id == 71:
        return 'ARM64_INS_CASAB'
    if id == 72:
        return 'ARM64_INS_CASAH'
    if id == 73:
        return 'ARM64_INS_CASAL'
    if id == 74:
        return 'ARM64_INS_CASALB'
    if id == 75:
        return 'ARM64_INS_CASALH'
    if id == 76:
        return 'ARM64_INS_CASB'
    if id == 77:
        return 'ARM64_INS_CASH'
    if id == 78:
        return 'ARM64_INS_CASL'
    if id == 79:
        return 'ARM64_INS_CASLB'
    if id == 80:
        return 'ARM64_INS_CASLH'
    if id == 81:
        return 'ARM64_INS_CASP'
    if id == 82:
        return 'ARM64_INS_CASPA'
    if id == 83:
        return 'ARM64_INS_CASPAL'
    if id == 84:
        return 'ARM64_INS_CASPL'
    if id == 85:
        return 'ARM64_INS_CBNZ'
    if id == 86:
        return 'ARM64_INS_CBZ'
    if id == 87:
        return 'ARM64_INS_CCMN'
    if id == 88:
        return 'ARM64_INS_CCMP'
    if id == 89:
        return 'ARM64_INS_CFINV'
    if id == 90:
        return 'ARM64_INS_CINC'
    if id == 91:
        return 'ARM64_INS_CINV'
    if id == 92:
        return 'ARM64_INS_CLASTA'
    if id == 93:
        return 'ARM64_INS_CLASTB'
    if id == 94:
        return 'ARM64_INS_CLREX'
    if id == 95:
        return 'ARM64_INS_CLS'
    if id == 96:
        return 'ARM64_INS_CLZ'
    if id == 97:
        return 'ARM64_INS_CMEQ'
    if id == 98:
        return 'ARM64_INS_CMGE'
    if id == 99:
        return 'ARM64_INS_CMGT'
    if id == 100:
        return 'ARM64_INS_CMHI'
    if id == 101:
        return 'ARM64_INS_CMHS'
    if id == 102:
        return 'ARM64_INS_CMLE'
    if id == 103:
        return 'ARM64_INS_CMLO'
    if id == 104:
        return 'ARM64_INS_CMLS'
    if id == 105:
        return 'ARM64_INS_CMLT'
    if id == 106:
        return 'ARM64_INS_CMN'
    if id == 107:
        return 'ARM64_INS_CMP'
    if id == 108:
        return 'ARM64_INS_CMPEQ'
    if id == 109:
        return 'ARM64_INS_CMPGE'
    if id == 110:
        return 'ARM64_INS_CMPGT'
    if id == 111:
        return 'ARM64_INS_CMPHI'
    if id == 112:
        return 'ARM64_INS_CMPHS'
    if id == 113:
        return 'ARM64_INS_CMPLE'
    if id == 114:
        return 'ARM64_INS_CMPLO'
    if id == 115:
        return 'ARM64_INS_CMPLS'
    if id == 116:
        return 'ARM64_INS_CMPLT'
    if id == 117:
        return 'ARM64_INS_CMPNE'
    if id == 118:
        return 'ARM64_INS_CMTST'
    if id == 119:
        return 'ARM64_INS_CNEG'
    if id == 120:
        return 'ARM64_INS_CNOT'
    if id == 121:
        return 'ARM64_INS_CNT'
    if id == 122:
        return 'ARM64_INS_CNTB'
    if id == 123:
        return 'ARM64_INS_CNTD'
    if id == 124:
        return 'ARM64_INS_CNTH'
    if id == 125:
        return 'ARM64_INS_CNTP'
    if id == 126:
        return 'ARM64_INS_CNTW'
    if id == 127:
        return 'ARM64_INS_COMPACT'
    if id == 128:
        return 'ARM64_INS_CPY'
    if id == 129:
        return 'ARM64_INS_CRC32B'
    if id == 130:
        return 'ARM64_INS_CRC32CB'
    if id == 131:
        return 'ARM64_INS_CRC32CH'
    if id == 132:
        return 'ARM64_INS_CRC32CW'
    if id == 133:
        return 'ARM64_INS_CRC32CX'
    if id == 134:
        return 'ARM64_INS_CRC32H'
    if id == 135:
        return 'ARM64_INS_CRC32W'
    if id == 136:
        return 'ARM64_INS_CRC32X'
    if id == 137:
        return 'ARM64_INS_CSDB'
    if id == 138:
        return 'ARM64_INS_CSEL'
    if id == 139:
        return 'ARM64_INS_CSET'
    if id == 140:
        return 'ARM64_INS_CSETM'
    if id == 141:
        return 'ARM64_INS_CSINC'
    if id == 142:
        return 'ARM64_INS_CSINV'
    if id == 143:
        return 'ARM64_INS_CSNEG'
    if id == 144:
        return 'ARM64_INS_CTERMEQ'
    if id == 145:
        return 'ARM64_INS_CTERMNE'
    if id == 146:
        return 'ARM64_INS_DCPS1'
    if id == 147:
        return 'ARM64_INS_DCPS2'
    if id == 148:
        return 'ARM64_INS_DCPS3'
    if id == 149:
        return 'ARM64_INS_DECB'
    if id == 150:
        return 'ARM64_INS_DECD'
    if id == 151:
        return 'ARM64_INS_DECH'
    if id == 152:
        return 'ARM64_INS_DECP'
    if id == 153:
        return 'ARM64_INS_DECW'
    if id == 154:
        return 'ARM64_INS_DMB'
    if id == 155:
        return 'ARM64_INS_DRPS'
    if id == 156:
        return 'ARM64_INS_DSB'
    if id == 157:
        return 'ARM64_INS_DUP'
    if id == 158:
        return 'ARM64_INS_DUPM'
    if id == 159:
        return 'ARM64_INS_EON'
    if id == 160:
        return 'ARM64_INS_EOR'
    if id == 161:
        return 'ARM64_INS_EOR3'
    if id == 162:
        return 'ARM64_INS_EORS'
    if id == 163:
        return 'ARM64_INS_EORV'
    if id == 164:
        return 'ARM64_INS_ERET'
    if id == 165:
        return 'ARM64_INS_ERETAA'
    if id == 166:
        return 'ARM64_INS_ERETAB'
    if id == 167:
        return 'ARM64_INS_ESB'
    if id == 168:
        return 'ARM64_INS_EXT'
    if id == 169:
        return 'ARM64_INS_EXTR'
    if id == 170:
        return 'ARM64_INS_FABD'
    if id == 171:
        return 'ARM64_INS_FABS'
    if id == 172:
        return 'ARM64_INS_FACGE'
    if id == 173:
        return 'ARM64_INS_FACGT'
    if id == 174:
        return 'ARM64_INS_FACLE'
    if id == 175:
        return 'ARM64_INS_FACLT'
    if id == 176:
        return 'ARM64_INS_FADD'
    if id == 177:
        return 'ARM64_INS_FADDA'
    if id == 178:
        return 'ARM64_INS_FADDP'
    if id == 179:
        return 'ARM64_INS_FADDV'
    if id == 180:
        return 'ARM64_INS_FCADD'
    if id == 181:
        return 'ARM64_INS_FCCMP'
    if id == 182:
        return 'ARM64_INS_FCCMPE'
    if id == 183:
        return 'ARM64_INS_FCMEQ'
    if id == 184:
        return 'ARM64_INS_FCMGE'
    if id == 185:
        return 'ARM64_INS_FCMGT'
    if id == 186:
        return 'ARM64_INS_FCMLA'
    if id == 187:
        return 'ARM64_INS_FCMLE'
    if id == 188:
        return 'ARM64_INS_FCMLT'
    if id == 189:
        return 'ARM64_INS_FCMNE'
    if id == 190:
        return 'ARM64_INS_FCMP'
    if id == 191:
        return 'ARM64_INS_FCMPE'
    if id == 192:
        return 'ARM64_INS_FCMUO'
    if id == 193:
        return 'ARM64_INS_FCPY'
    if id == 194:
        return 'ARM64_INS_FCSEL'
    if id == 195:
        return 'ARM64_INS_FCVT'
    if id == 196:
        return 'ARM64_INS_FCVTAS'
    if id == 197:
        return 'ARM64_INS_FCVTAU'
    if id == 198:
        return 'ARM64_INS_FCVTL'
    if id == 199:
        return 'ARM64_INS_FCVTL2'
    if id == 200:
        return 'ARM64_INS_FCVTMS'
    if id == 201:
        return 'ARM64_INS_FCVTMU'
    if id == 202:
        return 'ARM64_INS_FCVTN'
    if id == 203:
        return 'ARM64_INS_FCVTN2'
    if id == 204:
        return 'ARM64_INS_FCVTNS'
    if id == 205:
        return 'ARM64_INS_FCVTNU'
    if id == 206:
        return 'ARM64_INS_FCVTPS'
    if id == 207:
        return 'ARM64_INS_FCVTPU'
    if id == 208:
        return 'ARM64_INS_FCVTXN'
    if id == 209:
        return 'ARM64_INS_FCVTXN2'
    if id == 210:
        return 'ARM64_INS_FCVTZS'
    if id == 211:
        return 'ARM64_INS_FCVTZU'
    if id == 212:
        return 'ARM64_INS_FDIV'
    if id == 213:
        return 'ARM64_INS_FDIVR'
    if id == 214:
        return 'ARM64_INS_FDUP'
    if id == 215:
        return 'ARM64_INS_FEXPA'
    if id == 216:
        return 'ARM64_INS_FJCVTZS'
    if id == 217:
        return 'ARM64_INS_FMAD'
    if id == 218:
        return 'ARM64_INS_FMADD'
    if id == 219:
        return 'ARM64_INS_FMAX'
    if id == 220:
        return 'ARM64_INS_FMAXNM'
    if id == 221:
        return 'ARM64_INS_FMAXNMP'
    if id == 222:
        return 'ARM64_INS_FMAXNMV'
    if id == 223:
        return 'ARM64_INS_FMAXP'
    if id == 224:
        return 'ARM64_INS_FMAXV'
    if id == 225:
        return 'ARM64_INS_FMIN'
    if id == 226:
        return 'ARM64_INS_FMINNM'
    if id == 227:
        return 'ARM64_INS_FMINNMP'
    if id == 228:
        return 'ARM64_INS_FMINNMV'
    if id == 229:
        return 'ARM64_INS_FMINP'
    if id == 230:
        return 'ARM64_INS_FMINV'
    if id == 231:
        return 'ARM64_INS_FMLA'
    if id == 232:
        return 'ARM64_INS_FMLS'
    if id == 233:
        return 'ARM64_INS_FMOV'
    if id == 234:
        return 'ARM64_INS_FMSB'
    if id == 235:
        return 'ARM64_INS_FMSUB'
    if id == 236:
        return 'ARM64_INS_FMUL'
    if id == 237:
        return 'ARM64_INS_FMULX'
    if id == 238:
        return 'ARM64_INS_FNEG'
    if id == 239:
        return 'ARM64_INS_FNMAD'
    if id == 240:
        return 'ARM64_INS_FNMADD'
    if id == 241:
        return 'ARM64_INS_FNMLA'
    if id == 242:
        return 'ARM64_INS_FNMLS'
    if id == 243:
        return 'ARM64_INS_FNMSB'
    if id == 244:
        return 'ARM64_INS_FNMSUB'
    if id == 245:
        return 'ARM64_INS_FNMUL'
    if id == 246:
        return 'ARM64_INS_FRECPE'
    if id == 247:
        return 'ARM64_INS_FRECPS'
    if id == 248:
        return 'ARM64_INS_FRECPX'
    if id == 249:
        return 'ARM64_INS_FRINTA'
    if id == 250:
        return 'ARM64_INS_FRINTI'
    if id == 251:
        return 'ARM64_INS_FRINTM'
    if id == 252:
        return 'ARM64_INS_FRINTN'
    if id == 253:
        return 'ARM64_INS_FRINTP'
    if id == 254:
        return 'ARM64_INS_FRINTX'
    if id == 255:
        return 'ARM64_INS_FRINTZ'
    if id == 256:
        return 'ARM64_INS_FRSQRTE'
    if id == 257:
        return 'ARM64_INS_FRSQRTS'
    if id == 258:
        return 'ARM64_INS_FSCALE'
    if id == 259:
        return 'ARM64_INS_FSQRT'
    if id == 260:
        return 'ARM64_INS_FSUB'
    if id == 261:
        return 'ARM64_INS_FSUBR'
    if id == 262:
        return 'ARM64_INS_FTMAD'
    if id == 263:
        return 'ARM64_INS_FTSMUL'
    if id == 264:
        return 'ARM64_INS_FTSSEL'
    if id == 265:
        return 'ARM64_INS_HINT'
    if id == 266:
        return 'ARM64_INS_HLT'
    if id == 267:
        return 'ARM64_INS_HVC'
    if id == 268:
        return 'ARM64_INS_INCB'
    if id == 269:
        return 'ARM64_INS_INCD'
    if id == 270:
        return 'ARM64_INS_INCH'
    if id == 271:
        return 'ARM64_INS_INCP'
    if id == 272:
        return 'ARM64_INS_INCW'
    if id == 273:
        return 'ARM64_INS_INDEX'
    if id == 274:
        return 'ARM64_INS_INS'
    if id == 275:
        return 'ARM64_INS_INSR'
    if id == 276:
        return 'ARM64_INS_ISB'
    if id == 277:
        return 'ARM64_INS_LASTA'
    if id == 278:
        return 'ARM64_INS_LASTB'
    if id == 279:
        return 'ARM64_INS_LD1'
    if id == 280:
        return 'ARM64_INS_LD1B'
    if id == 281:
        return 'ARM64_INS_LD1D'
    if id == 282:
        return 'ARM64_INS_LD1H'
    if id == 283:
        return 'ARM64_INS_LD1R'
    if id == 284:
        return 'ARM64_INS_LD1RB'
    if id == 285:
        return 'ARM64_INS_LD1RD'
    if id == 286:
        return 'ARM64_INS_LD1RH'
    if id == 287:
        return 'ARM64_INS_LD1RQB'
    if id == 288:
        return 'ARM64_INS_LD1RQD'
    if id == 289:
        return 'ARM64_INS_LD1RQH'
    if id == 290:
        return 'ARM64_INS_LD1RQW'
    if id == 291:
        return 'ARM64_INS_LD1RSB'
    if id == 292:
        return 'ARM64_INS_LD1RSH'
    if id == 293:
        return 'ARM64_INS_LD1RSW'
    if id == 294:
        return 'ARM64_INS_LD1RW'
    if id == 295:
        return 'ARM64_INS_LD1SB'
    if id == 296:
        return 'ARM64_INS_LD1SH'
    if id == 297:
        return 'ARM64_INS_LD1SW'
    if id == 298:
        return 'ARM64_INS_LD1W'
    if id == 299:
        return 'ARM64_INS_LD2'
    if id == 300:
        return 'ARM64_INS_LD2B'
    if id == 301:
        return 'ARM64_INS_LD2D'
    if id == 302:
        return 'ARM64_INS_LD2H'
    if id == 303:
        return 'ARM64_INS_LD2R'
    if id == 304:
        return 'ARM64_INS_LD2W'
    if id == 305:
        return 'ARM64_INS_LD3'
    if id == 306:
        return 'ARM64_INS_LD3B'
    if id == 307:
        return 'ARM64_INS_LD3D'
    if id == 308:
        return 'ARM64_INS_LD3H'
    if id == 309:
        return 'ARM64_INS_LD3R'
    if id == 310:
        return 'ARM64_INS_LD3W'
    if id == 311:
        return 'ARM64_INS_LD4'
    if id == 312:
        return 'ARM64_INS_LD4B'
    if id == 313:
        return 'ARM64_INS_LD4D'
    if id == 314:
        return 'ARM64_INS_LD4H'
    if id == 315:
        return 'ARM64_INS_LD4R'
    if id == 316:
        return 'ARM64_INS_LD4W'
    if id == 317:
        return 'ARM64_INS_LDADD'
    if id == 318:
        return 'ARM64_INS_LDADDA'
    if id == 319:
        return 'ARM64_INS_LDADDAB'
    if id == 320:
        return 'ARM64_INS_LDADDAH'
    if id == 321:
        return 'ARM64_INS_LDADDAL'
    if id == 322:
        return 'ARM64_INS_LDADDALB'
    if id == 323:
        return 'ARM64_INS_LDADDALH'
    if id == 324:
        return 'ARM64_INS_LDADDB'
    if id == 325:
        return 'ARM64_INS_LDADDH'
    if id == 326:
        return 'ARM64_INS_LDADDL'
    if id == 327:
        return 'ARM64_INS_LDADDLB'
    if id == 328:
        return 'ARM64_INS_LDADDLH'
    if id == 329:
        return 'ARM64_INS_LDAPR'
    if id == 330:
        return 'ARM64_INS_LDAPRB'
    if id == 331:
        return 'ARM64_INS_LDAPRH'
    if id == 332:
        return 'ARM64_INS_LDAPUR'
    if id == 333:
        return 'ARM64_INS_LDAPURB'
    if id == 334:
        return 'ARM64_INS_LDAPURH'
    if id == 335:
        return 'ARM64_INS_LDAPURSB'
    if id == 336:
        return 'ARM64_INS_LDAPURSH'
    if id == 337:
        return 'ARM64_INS_LDAPURSW'
    if id == 338:
        return 'ARM64_INS_LDAR'
    if id == 339:
        return 'ARM64_INS_LDARB'
    if id == 340:
        return 'ARM64_INS_LDARH'
    if id == 341:
        return 'ARM64_INS_LDAXP'
    if id == 342:
        return 'ARM64_INS_LDAXR'
    if id == 343:
        return 'ARM64_INS_LDAXRB'
    if id == 344:
        return 'ARM64_INS_LDAXRH'
    if id == 345:
        return 'ARM64_INS_LDCLR'
    if id == 346:
        return 'ARM64_INS_LDCLRA'
    if id == 347:
        return 'ARM64_INS_LDCLRAB'
    if id == 348:
        return 'ARM64_INS_LDCLRAH'
    if id == 349:
        return 'ARM64_INS_LDCLRAL'
    if id == 350:
        return 'ARM64_INS_LDCLRALB'
    if id == 351:
        return 'ARM64_INS_LDCLRALH'
    if id == 352:
        return 'ARM64_INS_LDCLRB'
    if id == 353:
        return 'ARM64_INS_LDCLRH'
    if id == 354:
        return 'ARM64_INS_LDCLRL'
    if id == 355:
        return 'ARM64_INS_LDCLRLB'
    if id == 356:
        return 'ARM64_INS_LDCLRLH'
    if id == 357:
        return 'ARM64_INS_LDEOR'
    if id == 358:
        return 'ARM64_INS_LDEORA'
    if id == 359:
        return 'ARM64_INS_LDEORAB'
    if id == 360:
        return 'ARM64_INS_LDEORAH'
    if id == 361:
        return 'ARM64_INS_LDEORAL'
    if id == 362:
        return 'ARM64_INS_LDEORALB'
    if id == 363:
        return 'ARM64_INS_LDEORALH'
    if id == 364:
        return 'ARM64_INS_LDEORB'
    if id == 365:
        return 'ARM64_INS_LDEORH'
    if id == 366:
        return 'ARM64_INS_LDEORL'
    if id == 367:
        return 'ARM64_INS_LDEORLB'
    if id == 368:
        return 'ARM64_INS_LDEORLH'
    if id == 369:
        return 'ARM64_INS_LDFF1B'
    if id == 370:
        return 'ARM64_INS_LDFF1D'
    if id == 371:
        return 'ARM64_INS_LDFF1H'
    if id == 372:
        return 'ARM64_INS_LDFF1SB'
    if id == 373:
        return 'ARM64_INS_LDFF1SH'
    if id == 374:
        return 'ARM64_INS_LDFF1SW'
    if id == 375:
        return 'ARM64_INS_LDFF1W'
    if id == 376:
        return 'ARM64_INS_LDLAR'
    if id == 377:
        return 'ARM64_INS_LDLARB'
    if id == 378:
        return 'ARM64_INS_LDLARH'
    if id == 379:
        return 'ARM64_INS_LDNF1B'
    if id == 380:
        return 'ARM64_INS_LDNF1D'
    if id == 381:
        return 'ARM64_INS_LDNF1H'
    if id == 382:
        return 'ARM64_INS_LDNF1SB'
    if id == 383:
        return 'ARM64_INS_LDNF1SH'
    if id == 384:
        return 'ARM64_INS_LDNF1SW'
    if id == 385:
        return 'ARM64_INS_LDNF1W'
    if id == 386:
        return 'ARM64_INS_LDNP'
    if id == 387:
        return 'ARM64_INS_LDNT1B'
    if id == 388:
        return 'ARM64_INS_LDNT1D'
    if id == 389:
        return 'ARM64_INS_LDNT1H'
    if id == 390:
        return 'ARM64_INS_LDNT1W'
    if id == 391:
        return 'ARM64_INS_LDP'
    if id == 392:
        return 'ARM64_INS_LDPSW'
    if id == 393:
        return 'ARM64_INS_LDR'
    if id == 394:
        return 'ARM64_INS_LDRAA'
    if id == 395:
        return 'ARM64_INS_LDRAB'
    if id == 396:
        return 'ARM64_INS_LDRB'
    if id == 397:
        return 'ARM64_INS_LDRH'
    if id == 398:
        return 'ARM64_INS_LDRSB'
    if id == 399:
        return 'ARM64_INS_LDRSH'
    if id == 400:
        return 'ARM64_INS_LDRSW'
    if id == 401:
        return 'ARM64_INS_LDSET'
    if id == 402:
        return 'ARM64_INS_LDSETA'
    if id == 403:
        return 'ARM64_INS_LDSETAB'
    if id == 404:
        return 'ARM64_INS_LDSETAH'
    if id == 405:
        return 'ARM64_INS_LDSETAL'
    if id == 406:
        return 'ARM64_INS_LDSETALB'
    if id == 407:
        return 'ARM64_INS_LDSETALH'
    if id == 408:
        return 'ARM64_INS_LDSETB'
    if id == 409:
        return 'ARM64_INS_LDSETH'
    if id == 410:
        return 'ARM64_INS_LDSETL'
    if id == 411:
        return 'ARM64_INS_LDSETLB'
    if id == 412:
        return 'ARM64_INS_LDSETLH'
    if id == 413:
        return 'ARM64_INS_LDSMAX'
    if id == 414:
        return 'ARM64_INS_LDSMAXA'
    if id == 415:
        return 'ARM64_INS_LDSMAXAB'
    if id == 416:
        return 'ARM64_INS_LDSMAXAH'
    if id == 417:
        return 'ARM64_INS_LDSMAXAL'
    if id == 418:
        return 'ARM64_INS_LDSMAXALB'
    if id == 419:
        return 'ARM64_INS_LDSMAXALH'
    if id == 420:
        return 'ARM64_INS_LDSMAXB'
    if id == 421:
        return 'ARM64_INS_LDSMAXH'
    if id == 422:
        return 'ARM64_INS_LDSMAXL'
    if id == 423:
        return 'ARM64_INS_LDSMAXLB'
    if id == 424:
        return 'ARM64_INS_LDSMAXLH'
    if id == 425:
        return 'ARM64_INS_LDSMIN'
    if id == 426:
        return 'ARM64_INS_LDSMINA'
    if id == 427:
        return 'ARM64_INS_LDSMINAB'
    if id == 428:
        return 'ARM64_INS_LDSMINAH'
    if id == 429:
        return 'ARM64_INS_LDSMINAL'
    if id == 430:
        return 'ARM64_INS_LDSMINALB'
    if id == 431:
        return 'ARM64_INS_LDSMINALH'
    if id == 432:
        return 'ARM64_INS_LDSMINB'
    if id == 433:
        return 'ARM64_INS_LDSMINH'
    if id == 434:
        return 'ARM64_INS_LDSMINL'
    if id == 435:
        return 'ARM64_INS_LDSMINLB'
    if id == 436:
        return 'ARM64_INS_LDSMINLH'
    if id == 437:
        return 'ARM64_INS_LDTR'
    if id == 438:
        return 'ARM64_INS_LDTRB'
    if id == 439:
        return 'ARM64_INS_LDTRH'
    if id == 440:
        return 'ARM64_INS_LDTRSB'
    if id == 441:
        return 'ARM64_INS_LDTRSH'
    if id == 442:
        return 'ARM64_INS_LDTRSW'
    if id == 443:
        return 'ARM64_INS_LDUMAX'
    if id == 444:
        return 'ARM64_INS_LDUMAXA'
    if id == 445:
        return 'ARM64_INS_LDUMAXAB'
    if id == 446:
        return 'ARM64_INS_LDUMAXAH'
    if id == 447:
        return 'ARM64_INS_LDUMAXAL'
    if id == 448:
        return 'ARM64_INS_LDUMAXALB'
    if id == 449:
        return 'ARM64_INS_LDUMAXALH'
    if id == 450:
        return 'ARM64_INS_LDUMAXB'
    if id == 451:
        return 'ARM64_INS_LDUMAXH'
    if id == 452:
        return 'ARM64_INS_LDUMAXL'
    if id == 453:
        return 'ARM64_INS_LDUMAXLB'
    if id == 454:
        return 'ARM64_INS_LDUMAXLH'
    if id == 455:
        return 'ARM64_INS_LDUMIN'
    if id == 456:
        return 'ARM64_INS_LDUMINA'
    if id == 457:
        return 'ARM64_INS_LDUMINAB'
    if id == 458:
        return 'ARM64_INS_LDUMINAH'
    if id == 459:
        return 'ARM64_INS_LDUMINAL'
    if id == 460:
        return 'ARM64_INS_LDUMINALB'
    if id == 461:
        return 'ARM64_INS_LDUMINALH'
    if id == 462:
        return 'ARM64_INS_LDUMINB'
    if id == 463:
        return 'ARM64_INS_LDUMINH'
    if id == 464:
        return 'ARM64_INS_LDUMINL'
    if id == 465:
        return 'ARM64_INS_LDUMINLB'
    if id == 466:
        return 'ARM64_INS_LDUMINLH'
    if id == 467:
        return 'ARM64_INS_LDUR'
    if id == 468:
        return 'ARM64_INS_LDURB'
    if id == 469:
        return 'ARM64_INS_LDURH'
    if id == 470:
        return 'ARM64_INS_LDURSB'
    if id == 471:
        return 'ARM64_INS_LDURSH'
    if id == 472:
        return 'ARM64_INS_LDURSW'
    if id == 473:
        return 'ARM64_INS_LDXP'
    if id == 474:
        return 'ARM64_INS_LDXR'
    if id == 475:
        return 'ARM64_INS_LDXRB'
    if id == 476:
        return 'ARM64_INS_LDXRH'
    if id == 477:
        return 'ARM64_INS_LSL'
    if id == 478:
        return 'ARM64_INS_LSLR'
    if id == 479:
        return 'ARM64_INS_LSLV'
    if id == 480:
        return 'ARM64_INS_LSR'
    if id == 481:
        return 'ARM64_INS_LSRR'
    if id == 482:
        return 'ARM64_INS_LSRV'
    if id == 483:
        return 'ARM64_INS_MAD'
    if id == 484:
        return 'ARM64_INS_MADD'
    if id == 485:
        return 'ARM64_INS_MLA'
    if id == 486:
        return 'ARM64_INS_MLS'
    if id == 487:
        return 'ARM64_INS_MNEG'
    if id == 488:
        return 'ARM64_INS_MOV'
    if id == 489:
        return 'ARM64_INS_MOVI'
    if id == 490:
        return 'ARM64_INS_MOVK'
    if id == 491:
        return 'ARM64_INS_MOVN'
    if id == 492:
        return 'ARM64_INS_MOVPRFX'
    if id == 493:
        return 'ARM64_INS_MOVS'
    if id == 494:
        return 'ARM64_INS_MOVZ'
    if id == 495:
        return 'ARM64_INS_MRS'
    if id == 496:
        return 'ARM64_INS_MSB'
    if id == 497:
        return 'ARM64_INS_MSR'
    if id == 498:
        return 'ARM64_INS_MSUB'
    if id == 499:
        return 'ARM64_INS_MUL'
    if id == 500:
        return 'ARM64_INS_MVN'
    if id == 501:
        return 'ARM64_INS_MVNI'
    if id == 502:
        return 'ARM64_INS_NAND'
    if id == 503:
        return 'ARM64_INS_NANDS'
    if id == 504:
        return 'ARM64_INS_NEG'
    if id == 505:
        return 'ARM64_INS_NEGS'
    if id == 506:
        return 'ARM64_INS_NGC'
    if id == 507:
        return 'ARM64_INS_NGCS'
    if id == 508:
        return 'ARM64_INS_NOP'
    if id == 509:
        return 'ARM64_INS_NOR'
    if id == 510:
        return 'ARM64_INS_NORS'
    if id == 511:
        return 'ARM64_INS_NOT'
    if id == 512:
        return 'ARM64_INS_NOTS'
    if id == 513:
        return 'ARM64_INS_ORN'
    if id == 514:
        return 'ARM64_INS_ORNS'
    if id == 515:
        return 'ARM64_INS_ORR'
    if id == 516:
        return 'ARM64_INS_ORRS'
    if id == 517:
        return 'ARM64_INS_ORV'
    if id == 518:
        return 'ARM64_INS_PACDA'
    if id == 519:
        return 'ARM64_INS_PACDB'
    if id == 520:
        return 'ARM64_INS_PACDZA'
    if id == 521:
        return 'ARM64_INS_PACDZB'
    if id == 522:
        return 'ARM64_INS_PACGA'
    if id == 523:
        return 'ARM64_INS_PACIA'
    if id == 524:
        return 'ARM64_INS_PACIA1716'
    if id == 525:
        return 'ARM64_INS_PACIASP'
    if id == 526:
        return 'ARM64_INS_PACIAZ'
    if id == 527:
        return 'ARM64_INS_PACIB'
    if id == 528:
        return 'ARM64_INS_PACIB1716'
    if id == 529:
        return 'ARM64_INS_PACIBSP'
    if id == 530:
        return 'ARM64_INS_PACIBZ'
    if id == 531:
        return 'ARM64_INS_PACIZA'
    if id == 532:
        return 'ARM64_INS_PACIZB'
    if id == 533:
        return 'ARM64_INS_PFALSE'
    if id == 534:
        return 'ARM64_INS_PFIRST'
    if id == 535:
        return 'ARM64_INS_PMUL'
    if id == 536:
        return 'ARM64_INS_PMULL'
    if id == 537:
        return 'ARM64_INS_PMULL2'
    if id == 538:
        return 'ARM64_INS_PNEXT'
    if id == 539:
        return 'ARM64_INS_PRFB'
    if id == 540:
        return 'ARM64_INS_PRFD'
    if id == 541:
        return 'ARM64_INS_PRFH'
    if id == 542:
        return 'ARM64_INS_PRFM'
    if id == 543:
        return 'ARM64_INS_PRFUM'
    if id == 544:
        return 'ARM64_INS_PRFW'
    if id == 545:
        return 'ARM64_INS_PSB'
    if id == 546:
        return 'ARM64_INS_PTEST'
    if id == 547:
        return 'ARM64_INS_PTRUE'
    if id == 548:
        return 'ARM64_INS_PTRUES'
    if id == 549:
        return 'ARM64_INS_PUNPKHI'
    if id == 550:
        return 'ARM64_INS_PUNPKLO'
    if id == 551:
        return 'ARM64_INS_RADDHN'
    if id == 552:
        return 'ARM64_INS_RADDHN2'
    if id == 553:
        return 'ARM64_INS_RAX1'
    if id == 554:
        return 'ARM64_INS_RBIT'
    if id == 555:
        return 'ARM64_INS_RDFFR'
    if id == 556:
        return 'ARM64_INS_RDFFRS'
    if id == 557:
        return 'ARM64_INS_RDVL'
    if id == 558:
        return 'ARM64_INS_RET'
    if id == 559:
        return 'ARM64_INS_RETAA'
    if id == 560:
        return 'ARM64_INS_RETAB'
    if id == 561:
        return 'ARM64_INS_REV'
    if id == 562:
        return 'ARM64_INS_REV16'
    if id == 563:
        return 'ARM64_INS_REV32'
    if id == 564:
        return 'ARM64_INS_REV64'
    if id == 565:
        return 'ARM64_INS_REVB'
    if id == 566:
        return 'ARM64_INS_REVH'
    if id == 567:
        return 'ARM64_INS_REVW'
    if id == 568:
        return 'ARM64_INS_RMIF'
    if id == 569:
        return 'ARM64_INS_ROR'
    if id == 570:
        return 'ARM64_INS_RORV'
    if id == 571:
        return 'ARM64_INS_RSHRN'
    if id == 572:
        return 'ARM64_INS_RSHRN2'
    if id == 573:
        return 'ARM64_INS_RSUBHN'
    if id == 574:
        return 'ARM64_INS_RSUBHN2'
    if id == 575:
        return 'ARM64_INS_SABA'
    if id == 576:
        return 'ARM64_INS_SABAL'
    if id == 577:
        return 'ARM64_INS_SABAL2'
    if id == 578:
        return 'ARM64_INS_SABD'
    if id == 579:
        return 'ARM64_INS_SABDL'
    if id == 580:
        return 'ARM64_INS_SABDL2'
    if id == 581:
        return 'ARM64_INS_SADALP'
    if id == 582:
        return 'ARM64_INS_SADDL'
    if id == 583:
        return 'ARM64_INS_SADDL2'
    if id == 584:
        return 'ARM64_INS_SADDLP'
    if id == 585:
        return 'ARM64_INS_SADDLV'
    if id == 586:
        return 'ARM64_INS_SADDV'
    if id == 587:
        return 'ARM64_INS_SADDW'
    if id == 588:
        return 'ARM64_INS_SADDW2'
    if id == 589:
        return 'ARM64_INS_SBC'
    if id == 590:
        return 'ARM64_INS_SBCS'
    if id == 591:
        return 'ARM64_INS_SBFM'
    if id == 592:
        return 'ARM64_INS_SCVTF'
    if id == 593:
        return 'ARM64_INS_SDIV'
    if id == 594:
        return 'ARM64_INS_SDIVR'
    if id == 595:
        return 'ARM64_INS_SDOT'
    if id == 596:
        return 'ARM64_INS_SEL'
    if id == 597:
        return 'ARM64_INS_SETF16'
    if id == 598:
        return 'ARM64_INS_SETF8'
    if id == 599:
        return 'ARM64_INS_SETFFR'
    if id == 600:
        return 'ARM64_INS_SEV'
    if id == 601:
        return 'ARM64_INS_SEVL'
    if id == 602:
        return 'ARM64_INS_SHA1C'
    if id == 603:
        return 'ARM64_INS_SHA1H'
    if id == 604:
        return 'ARM64_INS_SHA1M'
    if id == 605:
        return 'ARM64_INS_SHA1P'
    if id == 606:
        return 'ARM64_INS_SHA1SU0'
    if id == 607:
        return 'ARM64_INS_SHA1SU1'
    if id == 608:
        return 'ARM64_INS_SHA256H'
    if id == 609:
        return 'ARM64_INS_SHA256H2'
    if id == 610:
        return 'ARM64_INS_SHA256SU0'
    if id == 611:
        return 'ARM64_INS_SHA256SU1'
    if id == 612:
        return 'ARM64_INS_SHA512H'
    if id == 613:
        return 'ARM64_INS_SHA512H2'
    if id == 614:
        return 'ARM64_INS_SHA512SU0'
    if id == 615:
        return 'ARM64_INS_SHA512SU1'
    if id == 616:
        return 'ARM64_INS_SHADD'
    if id == 617:
        return 'ARM64_INS_SHL'
    if id == 618:
        return 'ARM64_INS_SHLL'
    if id == 619:
        return 'ARM64_INS_SHLL2'
    if id == 620:
        return 'ARM64_INS_SHRN'
    if id == 621:
        return 'ARM64_INS_SHRN2'
    if id == 622:
        return 'ARM64_INS_SHSUB'
    if id == 623:
        return 'ARM64_INS_SLI'
    if id == 624:
        return 'ARM64_INS_SM3PARTW1'
    if id == 625:
        return 'ARM64_INS_SM3PARTW2'
    if id == 626:
        return 'ARM64_INS_SM3SS1'
    if id == 627:
        return 'ARM64_INS_SM3TT1A'
    if id == 628:
        return 'ARM64_INS_SM3TT1B'
    if id == 629:
        return 'ARM64_INS_SM3TT2A'
    if id == 630:
        return 'ARM64_INS_SM3TT2B'
    if id == 631:
        return 'ARM64_INS_SM4E'
    if id == 632:
        return 'ARM64_INS_SM4EKEY'
    if id == 633:
        return 'ARM64_INS_SMADDL'
    if id == 634:
        return 'ARM64_INS_SMAX'
    if id == 635:
        return 'ARM64_INS_SMAXP'
    if id == 636:
        return 'ARM64_INS_SMAXV'
    if id == 637:
        return 'ARM64_INS_SMC'
    if id == 638:
        return 'ARM64_INS_SMIN'
    if id == 639:
        return 'ARM64_INS_SMINP'
    if id == 640:
        return 'ARM64_INS_SMINV'
    if id == 641:
        return 'ARM64_INS_SMLAL'
    if id == 642:
        return 'ARM64_INS_SMLAL2'
    if id == 643:
        return 'ARM64_INS_SMLSL'
    if id == 644:
        return 'ARM64_INS_SMLSL2'
    if id == 645:
        return 'ARM64_INS_SMNEGL'
    if id == 646:
        return 'ARM64_INS_SMOV'
    if id == 647:
        return 'ARM64_INS_SMSUBL'
    if id == 648:
        return 'ARM64_INS_SMULH'
    if id == 649:
        return 'ARM64_INS_SMULL'
    if id == 650:
        return 'ARM64_INS_SMULL2'
    if id == 651:
        return 'ARM64_INS_SPLICE'
    if id == 652:
        return 'ARM64_INS_SQABS'
    if id == 653:
        return 'ARM64_INS_SQADD'
    if id == 654:
        return 'ARM64_INS_SQDECB'
    if id == 655:
        return 'ARM64_INS_SQDECD'
    if id == 656:
        return 'ARM64_INS_SQDECH'
    if id == 657:
        return 'ARM64_INS_SQDECP'
    if id == 658:
        return 'ARM64_INS_SQDECW'
    if id == 659:
        return 'ARM64_INS_SQDMLAL'
    if id == 660:
        return 'ARM64_INS_SQDMLAL2'
    if id == 661:
        return 'ARM64_INS_SQDMLSL'
    if id == 662:
        return 'ARM64_INS_SQDMLSL2'
    if id == 663:
        return 'ARM64_INS_SQDMULH'
    if id == 664:
        return 'ARM64_INS_SQDMULL'
    if id == 665:
        return 'ARM64_INS_SQDMULL2'
    if id == 666:
        return 'ARM64_INS_SQINCB'
    if id == 667:
        return 'ARM64_INS_SQINCD'
    if id == 668:
        return 'ARM64_INS_SQINCH'
    if id == 669:
        return 'ARM64_INS_SQINCP'
    if id == 670:
        return 'ARM64_INS_SQINCW'
    if id == 671:
        return 'ARM64_INS_SQNEG'
    if id == 672:
        return 'ARM64_INS_SQRDMLAH'
    if id == 673:
        return 'ARM64_INS_SQRDMLSH'
    if id == 674:
        return 'ARM64_INS_SQRDMULH'
    if id == 675:
        return 'ARM64_INS_SQRSHL'
    if id == 676:
        return 'ARM64_INS_SQRSHRN'
    if id == 677:
        return 'ARM64_INS_SQRSHRN2'
    if id == 678:
        return 'ARM64_INS_SQRSHRUN'
    if id == 679:
        return 'ARM64_INS_SQRSHRUN2'
    if id == 680:
        return 'ARM64_INS_SQSHL'
    if id == 681:
        return 'ARM64_INS_SQSHLU'
    if id == 682:
        return 'ARM64_INS_SQSHRN'
    if id == 683:
        return 'ARM64_INS_SQSHRN2'
    if id == 684:
        return 'ARM64_INS_SQSHRUN'
    if id == 685:
        return 'ARM64_INS_SQSHRUN2'
    if id == 686:
        return 'ARM64_INS_SQSUB'
    if id == 687:
        return 'ARM64_INS_SQXTN'
    if id == 688:
        return 'ARM64_INS_SQXTN2'
    if id == 689:
        return 'ARM64_INS_SQXTUN'
    if id == 690:
        return 'ARM64_INS_SQXTUN2'
    if id == 691:
        return 'ARM64_INS_SRHADD'
    if id == 692:
        return 'ARM64_INS_SRI'
    if id == 693:
        return 'ARM64_INS_SRSHL'
    if id == 694:
        return 'ARM64_INS_SRSHR'
    if id == 695:
        return 'ARM64_INS_SRSRA'
    if id == 696:
        return 'ARM64_INS_SSHL'
    if id == 697:
        return 'ARM64_INS_SSHLL'
    if id == 698:
        return 'ARM64_INS_SSHLL2'
    if id == 699:
        return 'ARM64_INS_SSHR'
    if id == 700:
        return 'ARM64_INS_SSRA'
    if id == 701:
        return 'ARM64_INS_SSUBL'
    if id == 702:
        return 'ARM64_INS_SSUBL2'
    if id == 703:
        return 'ARM64_INS_SSUBW'
    if id == 704:
        return 'ARM64_INS_SSUBW2'
    if id == 705:
        return 'ARM64_INS_ST1'
    if id == 706:
        return 'ARM64_INS_ST1B'
    if id == 707:
        return 'ARM64_INS_ST1D'
    if id == 708:
        return 'ARM64_INS_ST1H'
    if id == 709:
        return 'ARM64_INS_ST1W'
    if id == 710:
        return 'ARM64_INS_ST2'
    if id == 711:
        return 'ARM64_INS_ST2B'
    if id == 712:
        return 'ARM64_INS_ST2D'
    if id == 713:
        return 'ARM64_INS_ST2H'
    if id == 714:
        return 'ARM64_INS_ST2W'
    if id == 715:
        return 'ARM64_INS_ST3'
    if id == 716:
        return 'ARM64_INS_ST3B'
    if id == 717:
        return 'ARM64_INS_ST3D'
    if id == 718:
        return 'ARM64_INS_ST3H'
    if id == 719:
        return 'ARM64_INS_ST3W'
    if id == 720:
        return 'ARM64_INS_ST4'
    if id == 721:
        return 'ARM64_INS_ST4B'
    if id == 722:
        return 'ARM64_INS_ST4D'
    if id == 723:
        return 'ARM64_INS_ST4H'
    if id == 724:
        return 'ARM64_INS_ST4W'
    if id == 725:
        return 'ARM64_INS_STADD'
    if id == 726:
        return 'ARM64_INS_STADDB'
    if id == 727:
        return 'ARM64_INS_STADDH'
    if id == 728:
        return 'ARM64_INS_STADDL'
    if id == 729:
        return 'ARM64_INS_STADDLB'
    if id == 730:
        return 'ARM64_INS_STADDLH'
    if id == 731:
        return 'ARM64_INS_STCLR'
    if id == 732:
        return 'ARM64_INS_STCLRB'
    if id == 733:
        return 'ARM64_INS_STCLRH'
    if id == 734:
        return 'ARM64_INS_STCLRL'
    if id == 735:
        return 'ARM64_INS_STCLRLB'
    if id == 736:
        return 'ARM64_INS_STCLRLH'
    if id == 737:
        return 'ARM64_INS_STEOR'
    if id == 738:
        return 'ARM64_INS_STEORB'
    if id == 739:
        return 'ARM64_INS_STEORH'
    if id == 740:
        return 'ARM64_INS_STEORL'
    if id == 741:
        return 'ARM64_INS_STEORLB'
    if id == 742:
        return 'ARM64_INS_STEORLH'
    if id == 743:
        return 'ARM64_INS_STLLR'
    if id == 744:
        return 'ARM64_INS_STLLRB'
    if id == 745:
        return 'ARM64_INS_STLLRH'
    if id == 746:
        return 'ARM64_INS_STLR'
    if id == 747:
        return 'ARM64_INS_STLRB'
    if id == 748:
        return 'ARM64_INS_STLRH'
    if id == 749:
        return 'ARM64_INS_STLUR'
    if id == 750:
        return 'ARM64_INS_STLURB'
    if id == 751:
        return 'ARM64_INS_STLURH'
    if id == 752:
        return 'ARM64_INS_STLXP'
    if id == 753:
        return 'ARM64_INS_STLXR'
    if id == 754:
        return 'ARM64_INS_STLXRB'
    if id == 755:
        return 'ARM64_INS_STLXRH'
    if id == 756:
        return 'ARM64_INS_STNP'
    if id == 757:
        return 'ARM64_INS_STNT1B'
    if id == 758:
        return 'ARM64_INS_STNT1D'
    if id == 759:
        return 'ARM64_INS_STNT1H'
    if id == 760:
        return 'ARM64_INS_STNT1W'
    if id == 761:
        return 'ARM64_INS_STP'
    if id == 762:
        return 'ARM64_INS_STR'
    if id == 763:
        return 'ARM64_INS_STRB'
    if id == 764:
        return 'ARM64_INS_STRH'
    if id == 765:
        return 'ARM64_INS_STSET'
    if id == 766:
        return 'ARM64_INS_STSETB'
    if id == 767:
        return 'ARM64_INS_STSETH'
    if id == 768:
        return 'ARM64_INS_STSETL'
    if id == 769:
        return 'ARM64_INS_STSETLB'
    if id == 770:
        return 'ARM64_INS_STSETLH'
    if id == 771:
        return 'ARM64_INS_STSMAX'
    if id == 772:
        return 'ARM64_INS_STSMAXB'
    if id == 773:
        return 'ARM64_INS_STSMAXH'
    if id == 774:
        return 'ARM64_INS_STSMAXL'
    if id == 775:
        return 'ARM64_INS_STSMAXLB'
    if id == 776:
        return 'ARM64_INS_STSMAXLH'
    if id == 777:
        return 'ARM64_INS_STSMIN'
    if id == 778:
        return 'ARM64_INS_STSMINB'
    if id == 779:
        return 'ARM64_INS_STSMINH'
    if id == 780:
        return 'ARM64_INS_STSMINL'
    if id == 781:
        return 'ARM64_INS_STSMINLB'
    if id == 782:
        return 'ARM64_INS_STSMINLH'
    if id == 783:
        return 'ARM64_INS_STTR'
    if id == 784:
        return 'ARM64_INS_STTRB'
    if id == 785:
        return 'ARM64_INS_STTRH'
    if id == 786:
        return 'ARM64_INS_STUMAX'
    if id == 787:
        return 'ARM64_INS_STUMAXB'
    if id == 788:
        return 'ARM64_INS_STUMAXH'
    if id == 789:
        return 'ARM64_INS_STUMAXL'
    if id == 790:
        return 'ARM64_INS_STUMAXLB'
    if id == 791:
        return 'ARM64_INS_STUMAXLH'
    if id == 792:
        return 'ARM64_INS_STUMIN'
    if id == 793:
        return 'ARM64_INS_STUMINB'
    if id == 794:
        return 'ARM64_INS_STUMINH'
    if id == 795:
        return 'ARM64_INS_STUMINL'
    if id == 796:
        return 'ARM64_INS_STUMINLB'
    if id == 797:
        return 'ARM64_INS_STUMINLH'
    if id == 798:
        return 'ARM64_INS_STUR'
    if id == 799:
        return 'ARM64_INS_STURB'
    if id == 800:
        return 'ARM64_INS_STURH'
    if id == 801:
        return 'ARM64_INS_STXP'
    if id == 802:
        return 'ARM64_INS_STXR'
    if id == 803:
        return 'ARM64_INS_STXRB'
    if id == 804:
        return 'ARM64_INS_STXRH'
    if id == 805:
        return 'ARM64_INS_SUB'
    if id == 806:
        return 'ARM64_INS_SUBHN'
    if id == 807:
        return 'ARM64_INS_SUBHN2'
    if id == 808:
        return 'ARM64_INS_SUBR'
    if id == 809:
        return 'ARM64_INS_SUBS'
    if id == 810:
        return 'ARM64_INS_SUNPKHI'
    if id == 811:
        return 'ARM64_INS_SUNPKLO'
    if id == 812:
        return 'ARM64_INS_SUQADD'
    if id == 813:
        return 'ARM64_INS_SVC'
    if id == 814:
        return 'ARM64_INS_SWP'
    if id == 815:
        return 'ARM64_INS_SWPA'
    if id == 816:
        return 'ARM64_INS_SWPAB'
    if id == 817:
        return 'ARM64_INS_SWPAH'
    if id == 818:
        return 'ARM64_INS_SWPAL'
    if id == 819:
        return 'ARM64_INS_SWPALB'
    if id == 820:
        return 'ARM64_INS_SWPALH'
    if id == 821:
        return 'ARM64_INS_SWPB'
    if id == 822:
        return 'ARM64_INS_SWPH'
    if id == 823:
        return 'ARM64_INS_SWPL'
    if id == 824:
        return 'ARM64_INS_SWPLB'
    if id == 825:
        return 'ARM64_INS_SWPLH'
    if id == 826:
        return 'ARM64_INS_SXTB'
    if id == 827:
        return 'ARM64_INS_SXTH'
    if id == 828:
        return 'ARM64_INS_SXTL'
    if id == 829:
        return 'ARM64_INS_SXTL2'
    if id == 830:
        return 'ARM64_INS_SXTW'
    if id == 831:
        return 'ARM64_INS_SYS'
    if id == 832:
        return 'ARM64_INS_SYSL'
    if id == 833:
        return 'ARM64_INS_TBL'
    if id == 834:
        return 'ARM64_INS_TBNZ'
    if id == 835:
        return 'ARM64_INS_TBX'
    if id == 836:
        return 'ARM64_INS_TBZ'
    if id == 837:
        return 'ARM64_INS_TRN1'
    if id == 838:
        return 'ARM64_INS_TRN2'
    if id == 839:
        return 'ARM64_INS_TSB'
    if id == 840:
        return 'ARM64_INS_TST'
    if id == 841:
        return 'ARM64_INS_UABA'
    if id == 842:
        return 'ARM64_INS_UABAL'
    if id == 843:
        return 'ARM64_INS_UABAL2'
    if id == 844:
        return 'ARM64_INS_UABD'
    if id == 845:
        return 'ARM64_INS_UABDL'
    if id == 846:
        return 'ARM64_INS_UABDL2'
    if id == 847:
        return 'ARM64_INS_UADALP'
    if id == 848:
        return 'ARM64_INS_UADDL'
    if id == 849:
        return 'ARM64_INS_UADDL2'
    if id == 850:
        return 'ARM64_INS_UADDLP'
    if id == 851:
        return 'ARM64_INS_UADDLV'
    if id == 852:
        return 'ARM64_INS_UADDV'
    if id == 853:
        return 'ARM64_INS_UADDW'
    if id == 854:
        return 'ARM64_INS_UADDW2'
    if id == 855:
        return 'ARM64_INS_UBFM'
    if id == 856:
        return 'ARM64_INS_UCVTF'
    if id == 857:
        return 'ARM64_INS_UDIV'
    if id == 858:
        return 'ARM64_INS_UDIVR'
    if id == 859:
        return 'ARM64_INS_UDOT'
    if id == 860:
        return 'ARM64_INS_UHADD'
    if id == 861:
        return 'ARM64_INS_UHSUB'
    if id == 862:
        return 'ARM64_INS_UMADDL'
    if id == 863:
        return 'ARM64_INS_UMAX'
    if id == 864:
        return 'ARM64_INS_UMAXP'
    if id == 865:
        return 'ARM64_INS_UMAXV'
    if id == 866:
        return 'ARM64_INS_UMIN'
    if id == 867:
        return 'ARM64_INS_UMINP'
    if id == 868:
        return 'ARM64_INS_UMINV'
    if id == 869:
        return 'ARM64_INS_UMLAL'
    if id == 870:
        return 'ARM64_INS_UMLAL2'
    if id == 871:
        return 'ARM64_INS_UMLSL'
    if id == 872:
        return 'ARM64_INS_UMLSL2'
    if id == 873:
        return 'ARM64_INS_UMNEGL'
    if id == 874:
        return 'ARM64_INS_UMOV'
    if id == 875:
        return 'ARM64_INS_UMSUBL'
    if id == 876:
        return 'ARM64_INS_UMULH'
    if id == 877:
        return 'ARM64_INS_UMULL'
    if id == 878:
        return 'ARM64_INS_UMULL2'
    if id == 879:
        return 'ARM64_INS_UQADD'
    if id == 880:
        return 'ARM64_INS_UQDECB'
    if id == 881:
        return 'ARM64_INS_UQDECD'
    if id == 882:
        return 'ARM64_INS_UQDECH'
    if id == 883:
        return 'ARM64_INS_UQDECP'
    if id == 884:
        return 'ARM64_INS_UQDECW'
    if id == 885:
        return 'ARM64_INS_UQINCB'
    if id == 886:
        return 'ARM64_INS_UQINCD'
    if id == 887:
        return 'ARM64_INS_UQINCH'
    if id == 888:
        return 'ARM64_INS_UQINCP'
    if id == 889:
        return 'ARM64_INS_UQINCW'
    if id == 890:
        return 'ARM64_INS_UQRSHL'
    if id == 891:
        return 'ARM64_INS_UQRSHRN'
    if id == 892:
        return 'ARM64_INS_UQRSHRN2'
    if id == 893:
        return 'ARM64_INS_UQSHL'
    if id == 894:
        return 'ARM64_INS_UQSHRN'
    if id == 895:
        return 'ARM64_INS_UQSHRN2'
    if id == 896:
        return 'ARM64_INS_UQSUB'
    if id == 897:
        return 'ARM64_INS_UQXTN'
    if id == 898:
        return 'ARM64_INS_UQXTN2'
    if id == 899:
        return 'ARM64_INS_URECPE'
    if id == 900:
        return 'ARM64_INS_URHADD'
    if id == 901:
        return 'ARM64_INS_URSHL'
    if id == 902:
        return 'ARM64_INS_URSHR'
    if id == 903:
        return 'ARM64_INS_URSQRTE'
    if id == 904:
        return 'ARM64_INS_URSRA'
    if id == 905:
        return 'ARM64_INS_USHL'
    if id == 906:
        return 'ARM64_INS_USHLL'
    if id == 907:
        return 'ARM64_INS_USHLL2'
    if id == 908:
        return 'ARM64_INS_USHR'
    if id == 909:
        return 'ARM64_INS_USQADD'
    if id == 910:
        return 'ARM64_INS_USRA'
    if id == 911:
        return 'ARM64_INS_USUBL'
    if id == 912:
        return 'ARM64_INS_USUBL2'
    if id == 913:
        return 'ARM64_INS_USUBW'
    if id == 914:
        return 'ARM64_INS_USUBW2'
    if id == 915:
        return 'ARM64_INS_UUNPKHI'
    if id == 916:
        return 'ARM64_INS_UUNPKLO'
    if id == 917:
        return 'ARM64_INS_UXTB'
    if id == 918:
        return 'ARM64_INS_UXTH'
    if id == 919:
        return 'ARM64_INS_UXTL'
    if id == 920:
        return 'ARM64_INS_UXTL2'
    if id == 921:
        return 'ARM64_INS_UXTW'
    if id == 922:
        return 'ARM64_INS_UZP1'
    if id == 923:
        return 'ARM64_INS_UZP2'
    if id == 924:
        return 'ARM64_INS_WFE'
    if id == 925:
        return 'ARM64_INS_WFI'
    if id == 926:
        return 'ARM64_INS_WHILELE'
    if id == 927:
        return 'ARM64_INS_WHILELO'
    if id == 928:
        return 'ARM64_INS_WHILELS'
    if id == 929:
        return 'ARM64_INS_WHILELT'
    if id == 930:
        return 'ARM64_INS_WRFFR'
    if id == 931:
        return 'ARM64_INS_XAR'
    if id == 932:
        return 'ARM64_INS_XPACD'
    if id == 933:
        return 'ARM64_INS_XPACI'
    if id == 934:
        return 'ARM64_INS_XPACLRI'
    if id == 935:
        return 'ARM64_INS_XTN'
    if id == 936:
        return 'ARM64_INS_XTN2'
    if id == 937:
        return 'ARM64_INS_YIELD'
    if id == 938:
        return 'ARM64_INS_ZIP1'
    if id == 939:
        return 'ARM64_INS_ZIP2'
    if id == 940:
        return 'ARM64_INS_SBFIZ'
    if id == 941:
        return 'ARM64_INS_UBFIZ'
    if id == 942:
        return 'ARM64_INS_SBFX'
    if id == 943:
        return 'ARM64_INS_UBFX'
    if id == 944:
        return 'ARM64_INS_BFI'
    if id == 945:
        return 'ARM64_INS_BFXIL'
    if id == 946:
        return 'ARM64_INS_IC'
    if id == 947:
        return 'ARM64_INS_DC'
    if id == 948:
        return 'ARM64_INS_AT'
    if id == 949:
        return 'ARM64_INS_TLBI'
    if id == 950:
        return 'ARM64_INS_ENDING'

def arm64regStr(reg):
    if reg == 0:
        return 'ARM64_REG_INVALID'
    if reg == 1:
        return 'ARM64_REG_FFR'
    if reg == 2:
        return 'ARM64_REG_FP/ARM64_REG_X29'
    if reg == 3:
        return 'ARM64_REG_LR/ARM64_REG_X30'
    if reg == 4:
        return 'ARM64_REG_NZCV'
    if reg == 5:
        return 'ARM64_REG_SP'
    if reg == 6:
        return 'ARM64_REG_WSP'
    if reg == 7:
        return 'ARM64_REG_WZR'
    if reg == 8:
        return 'ARM64_REG_XZR'
    if reg == 9:
        return 'ARM64_REG_B0'
    if reg == 10:
        return 'ARM64_REG_B1'
    if reg == 11:
        return 'ARM64_REG_B2'
    if reg == 12:
        return 'ARM64_REG_B3'
    if reg == 13:
        return 'ARM64_REG_B4'
    if reg == 14:
        return 'ARM64_REG_B5'
    if reg == 15:
        return 'ARM64_REG_B6'
    if reg == 16:
        return 'ARM64_REG_B7'
    if reg == 17:
        return 'ARM64_REG_B8'
    if reg == 18:
        return 'ARM64_REG_B9'
    if reg == 19:
        return 'ARM64_REG_B10'
    if reg == 20:
        return 'ARM64_REG_B11'
    if reg == 21:
        return 'ARM64_REG_B12'
    if reg == 22:
        return 'ARM64_REG_B13'
    if reg == 23:
        return 'ARM64_REG_B14'
    if reg == 24:
        return 'ARM64_REG_B15'
    if reg == 25:
        return 'ARM64_REG_B16'
    if reg == 26:
        return 'ARM64_REG_B17'
    if reg == 27:
        return 'ARM64_REG_B18'
    if reg == 28:
        return 'ARM64_REG_B19'
    if reg == 29:
        return 'ARM64_REG_B20'
    if reg == 30:
        return 'ARM64_REG_B21'
    if reg == 31:
        return 'ARM64_REG_B22'
    if reg == 32:
        return 'ARM64_REG_B23'
    if reg == 33:
        return 'ARM64_REG_B24'
    if reg == 34:
        return 'ARM64_REG_B25'
    if reg == 35:
        return 'ARM64_REG_B26'
    if reg == 36:
        return 'ARM64_REG_B27'
    if reg == 37:
        return 'ARM64_REG_B28'
    if reg == 38:
        return 'ARM64_REG_B29'
    if reg == 39:
        return 'ARM64_REG_B30'
    if reg == 40:
        return 'ARM64_REG_B31'
    if reg == 41:
        return 'ARM64_REG_D0'
    if reg == 42:
        return 'ARM64_REG_D1'
    if reg == 43:
        return 'ARM64_REG_D2'
    if reg == 44:
        return 'ARM64_REG_D3'
    if reg == 45:
        return 'ARM64_REG_D4'
    if reg == 46:
        return 'ARM64_REG_D5'
    if reg == 47:
        return 'ARM64_REG_D6'
    if reg == 48:
        return 'ARM64_REG_D7'
    if reg == 49:
        return 'ARM64_REG_D8'
    if reg == 50:
        return 'ARM64_REG_D9'
    if reg == 51:
        return 'ARM64_REG_D10'
    if reg == 52:
        return 'ARM64_REG_D11'
    if reg == 53:
        return 'ARM64_REG_D12'
    if reg == 54:
        return 'ARM64_REG_D13'
    if reg == 55:
        return 'ARM64_REG_D14'
    if reg == 56:
        return 'ARM64_REG_D15'
    if reg == 57:
        return 'ARM64_REG_D16'
    if reg == 58:
        return 'ARM64_REG_D17'
    if reg == 59:
        return 'ARM64_REG_D18'
    if reg == 60:
        return 'ARM64_REG_D19'
    if reg == 61:
        return 'ARM64_REG_D20'
    if reg == 62:
        return 'ARM64_REG_D21'
    if reg == 63:
        return 'ARM64_REG_D22'
    if reg == 64:
        return 'ARM64_REG_D23'
    if reg == 65:
        return 'ARM64_REG_D24'
    if reg == 66:
        return 'ARM64_REG_D25'
    if reg == 67:
        return 'ARM64_REG_D26'
    if reg == 68:
        return 'ARM64_REG_D27'
    if reg == 69:
        return 'ARM64_REG_D28'
    if reg == 70:
        return 'ARM64_REG_D29'
    if reg == 71:
        return 'ARM64_REG_D30'
    if reg == 72:
        return 'ARM64_REG_D31'
    if reg == 73:
        return 'ARM64_REG_H0'
    if reg == 74:
        return 'ARM64_REG_H1'
    if reg == 75:
        return 'ARM64_REG_H2'
    if reg == 76:
        return 'ARM64_REG_H3'
    if reg == 77:
        return 'ARM64_REG_H4'
    if reg == 78:
        return 'ARM64_REG_H5'
    if reg == 79:
        return 'ARM64_REG_H6'
    if reg == 80:
        return 'ARM64_REG_H7'
    if reg == 81:
        return 'ARM64_REG_H8'
    if reg == 82:
        return 'ARM64_REG_H9'
    if reg == 83:
        return 'ARM64_REG_H10'
    if reg == 84:
        return 'ARM64_REG_H11'
    if reg == 85:
        return 'ARM64_REG_H12'
    if reg == 86:
        return 'ARM64_REG_H13'
    if reg == 87:
        return 'ARM64_REG_H14'
    if reg == 88:
        return 'ARM64_REG_H15'
    if reg == 89:
        return 'ARM64_REG_H16'
    if reg == 90:
        return 'ARM64_REG_H17'
    if reg == 91:
        return 'ARM64_REG_H18'
    if reg == 92:
        return 'ARM64_REG_H19'
    if reg == 93:
        return 'ARM64_REG_H20'
    if reg == 94:
        return 'ARM64_REG_H21'
    if reg == 95:
        return 'ARM64_REG_H22'
    if reg == 96:
        return 'ARM64_REG_H23'
    if reg == 97:
        return 'ARM64_REG_H24'
    if reg == 98:
        return 'ARM64_REG_H25'
    if reg == 99:
        return 'ARM64_REG_H26'
    if reg == 100:
        return 'ARM64_REG_H27'
    if reg == 101:
        return 'ARM64_REG_H28'
    if reg == 102:
        return 'ARM64_REG_H29'
    if reg == 103:
        return 'ARM64_REG_H30'
    if reg == 104:
        return 'ARM64_REG_H31'
    if reg == 105:
        return 'ARM64_REG_P0'
    if reg == 106:
        return 'ARM64_REG_P1'
    if reg == 107:
        return 'ARM64_REG_P2'
    if reg == 108:
        return 'ARM64_REG_P3'
    if reg == 109:
        return 'ARM64_REG_P4'
    if reg == 110:
        return 'ARM64_REG_P5'
    if reg == 111:
        return 'ARM64_REG_P6'
    if reg == 112:
        return 'ARM64_REG_P7'
    if reg == 113:
        return 'ARM64_REG_P8'
    if reg == 114:
        return 'ARM64_REG_P9'
    if reg == 115:
        return 'ARM64_REG_P10'
    if reg == 116:
        return 'ARM64_REG_P11'
    if reg == 117:
        return 'ARM64_REG_P12'
    if reg == 118:
        return 'ARM64_REG_P13'
    if reg == 119:
        return 'ARM64_REG_P14'
    if reg == 120:
        return 'ARM64_REG_P15'
    if reg == 121:
        return 'ARM64_REG_Q0'
    if reg == 122:
        return 'ARM64_REG_Q1'
    if reg == 123:
        return 'ARM64_REG_Q2'
    if reg == 124:
        return 'ARM64_REG_Q3'
    if reg == 125:
        return 'ARM64_REG_Q4'
    if reg == 126:
        return 'ARM64_REG_Q5'
    if reg == 127:
        return 'ARM64_REG_Q6'
    if reg == 128:
        return 'ARM64_REG_Q7'
    if reg == 129:
        return 'ARM64_REG_Q8'
    if reg == 130:
        return 'ARM64_REG_Q9'
    if reg == 131:
        return 'ARM64_REG_Q10'
    if reg == 132:
        return 'ARM64_REG_Q11'
    if reg == 133:
        return 'ARM64_REG_Q12'
    if reg == 134:
        return 'ARM64_REG_Q13'
    if reg == 135:
        return 'ARM64_REG_Q14'
    if reg == 136:
        return 'ARM64_REG_Q15'
    if reg == 137:
        return 'ARM64_REG_Q16'
    if reg == 138:
        return 'ARM64_REG_Q17'
    if reg == 139:
        return 'ARM64_REG_Q18'
    if reg == 140:
        return 'ARM64_REG_Q19'
    if reg == 141:
        return 'ARM64_REG_Q20'
    if reg == 142:
        return 'ARM64_REG_Q21'
    if reg == 143:
        return 'ARM64_REG_Q22'
    if reg == 144:
        return 'ARM64_REG_Q23'
    if reg == 145:
        return 'ARM64_REG_Q24'
    if reg == 146:
        return 'ARM64_REG_Q25'
    if reg == 147:
        return 'ARM64_REG_Q26'
    if reg == 148:
        return 'ARM64_REG_Q27'
    if reg == 149:
        return 'ARM64_REG_Q28'
    if reg == 150:
        return 'ARM64_REG_Q29'
    if reg == 151:
        return 'ARM64_REG_Q30'
    if reg == 152:
        return 'ARM64_REG_Q31'
    if reg == 153:
        return 'ARM64_REG_S0'
    if reg == 154:
        return 'ARM64_REG_S1'
    if reg == 155:
        return 'ARM64_REG_S2'
    if reg == 156:
        return 'ARM64_REG_S3'
    if reg == 157:
        return 'ARM64_REG_S4'
    if reg == 158:
        return 'ARM64_REG_S5'
    if reg == 159:
        return 'ARM64_REG_S6'
    if reg == 160:
        return 'ARM64_REG_S7'
    if reg == 161:
        return 'ARM64_REG_S8'
    if reg == 162:
        return 'ARM64_REG_S9'
    if reg == 163:
        return 'ARM64_REG_S10'
    if reg == 164:
        return 'ARM64_REG_S11'
    if reg == 165:
        return 'ARM64_REG_S12'
    if reg == 166:
        return 'ARM64_REG_S13'
    if reg == 167:
        return 'ARM64_REG_S14'
    if reg == 168:
        return 'ARM64_REG_S15'
    if reg == 169:
        return 'ARM64_REG_S16'
    if reg == 170:
        return 'ARM64_REG_S17'
    if reg == 171:
        return 'ARM64_REG_S18'
    if reg == 172:
        return 'ARM64_REG_S19'
    if reg == 173:
        return 'ARM64_REG_S20'
    if reg == 174:
        return 'ARM64_REG_S21'
    if reg == 175:
        return 'ARM64_REG_S22'
    if reg == 176:
        return 'ARM64_REG_S23'
    if reg == 177:
        return 'ARM64_REG_S24'
    if reg == 178:
        return 'ARM64_REG_S25'
    if reg == 179:
        return 'ARM64_REG_S26'
    if reg == 180:
        return 'ARM64_REG_S27'
    if reg == 181:
        return 'ARM64_REG_S28'
    if reg == 182:
        return 'ARM64_REG_S29'
    if reg == 183:
        return 'ARM64_REG_S30'
    if reg == 184:
        return 'ARM64_REG_S31'
    if reg == 185:
        return 'ARM64_REG_W0'
    if reg == 186:
        return 'ARM64_REG_W1'
    if reg == 187:
        return 'ARM64_REG_W2'
    if reg == 188:
        return 'ARM64_REG_W3'
    if reg == 189:
        return 'ARM64_REG_W4'
    if reg == 190:
        return 'ARM64_REG_W5'
    if reg == 191:
        return 'ARM64_REG_W6'
    if reg == 192:
        return 'ARM64_REG_W7'
    if reg == 193:
        return 'ARM64_REG_W8'
    if reg == 194:
        return 'ARM64_REG_W9'
    if reg == 195:
        return 'ARM64_REG_W10'
    if reg == 196:
        return 'ARM64_REG_W11'
    if reg == 197:
        return 'ARM64_REG_W12'
    if reg == 198:
        return 'ARM64_REG_W13'
    if reg == 199:
        return 'ARM64_REG_W14'
    if reg == 200:
        return 'ARM64_REG_W15'
    if reg == 201:
        return 'ARM64_REG_W16'
    if reg == 202:
        return 'ARM64_REG_W17'
    if reg == 203:
        return 'ARM64_REG_W18'
    if reg == 204:
        return 'ARM64_REG_W19'
    if reg == 205:
        return 'ARM64_REG_W20'
    if reg == 206:
        return 'ARM64_REG_W21'
    if reg == 207:
        return 'ARM64_REG_W22'
    if reg == 208:
        return 'ARM64_REG_W23'
    if reg == 209:
        return 'ARM64_REG_W24'
    if reg == 210:
        return 'ARM64_REG_W25'
    if reg == 211:
        return 'ARM64_REG_W26'
    if reg == 212:
        return 'ARM64_REG_W27'
    if reg == 213:
        return 'ARM64_REG_W28'
    if reg == 214:
        return 'ARM64_REG_W29'
    if reg == 215:
        return 'ARM64_REG_W30'
    if reg == 216:
        return 'ARM64_REG_X0'
    if reg == 217:
        return 'ARM64_REG_X1'
    if reg == 218:
        return 'ARM64_REG_X2'
    if reg == 219:
        return 'ARM64_REG_X3'
    if reg == 220:
        return 'ARM64_REG_X4'
    if reg == 221:
        return 'ARM64_REG_X5'
    if reg == 222:
        return 'ARM64_REG_X6'
    if reg == 223:
        return 'ARM64_REG_X7'
    if reg == 224:
        return 'ARM64_REG_X8'
    if reg == 225:
        return 'ARM64_REG_X9'
    if reg == 226:
        return 'ARM64_REG_X10'
    if reg == 227:
        return 'ARM64_REG_X11'
    if reg == 228:
        return 'ARM64_REG_X12'
    if reg == 229:
        return 'ARM64_REG_X13'
    if reg == 230:
        return 'ARM64_REG_X14'
    if reg == 231:
        return 'ARM64_REG_X15'
    if reg == 232:
        return 'ARM64_REG_X16/ARM64_REG_IP0'
    if reg == 233:
        return 'ARM64_REG_X17/ARM64_REG_IP1'
    if reg == 234:
        return 'ARM64_REG_X18'
    if reg == 235:
        return 'ARM64_REG_X19'
    if reg == 236:
        return 'ARM64_REG_X20'
    if reg == 237:
        return 'ARM64_REG_X21'
    if reg == 238:
        return 'ARM64_REG_X22'
    if reg == 239:
        return 'ARM64_REG_X23'
    if reg == 240:
        return 'ARM64_REG_X24'
    if reg == 241:
        return 'ARM64_REG_X25'
    if reg == 242:
        return 'ARM64_REG_X26'
    if reg == 243:
        return 'ARM64_REG_X27'
    if reg == 244:
        return 'ARM64_REG_X28'
    if reg == 245:
        return 'ARM64_REG_Z0'
    if reg == 246:
        return 'ARM64_REG_Z1'
    if reg == 247:
        return 'ARM64_REG_Z2'
    if reg == 248:
        return 'ARM64_REG_Z3'
    if reg == 249:
        return 'ARM64_REG_Z4'
    if reg == 250:
        return 'ARM64_REG_Z5'
    if reg == 251:
        return 'ARM64_REG_Z6'
    if reg == 252:
        return 'ARM64_REG_Z7'
    if reg == 253:
        return 'ARM64_REG_Z8'
    if reg == 254:
        return 'ARM64_REG_Z9'
    if reg == 255:
        return 'ARM64_REG_Z10'
    if reg == 256:
        return 'ARM64_REG_Z11'
    if reg == 257:
        return 'ARM64_REG_Z12'
    if reg == 258:
        return 'ARM64_REG_Z13'
    if reg == 259:
        return 'ARM64_REG_Z14'
    if reg == 260:
        return 'ARM64_REG_Z15'
    if reg == 261:
        return 'ARM64_REG_Z16'
    if reg == 262:
        return 'ARM64_REG_Z17'
    if reg == 263:
        return 'ARM64_REG_Z18'
    if reg == 264:
        return 'ARM64_REG_Z19'
    if reg == 265:
        return 'ARM64_REG_Z20'
    if reg == 266:
        return 'ARM64_REG_Z21'
    if reg == 267:
        return 'ARM64_REG_Z22'
    if reg == 268:
        return 'ARM64_REG_Z23'
    if reg == 269:
        return 'ARM64_REG_Z24'
    if reg == 270:
        return 'ARM64_REG_Z25'
    if reg == 271:
        return 'ARM64_REG_Z26'
    if reg == 272:
        return 'ARM64_REG_Z27'
    if reg == 273:
        return 'ARM64_REG_Z28'
    if reg == 274:
        return 'ARM64_REG_Z29'
    if reg == 275:
        return 'ARM64_REG_Z30'
    if reg == 276:
        return 'ARM64_REG_Z31'
    if reg == 277:
        return 'ARM64_REG_V0'
    if reg == 278:
        return 'ARM64_REG_V1'
    if reg == 279:
        return 'ARM64_REG_V2'
    if reg == 280:
        return 'ARM64_REG_V3'
    if reg == 281:
        return 'ARM64_REG_V4'
    if reg == 282:
        return 'ARM64_REG_V5'
    if reg == 283:
        return 'ARM64_REG_V6'
    if reg == 284:
        return 'ARM64_REG_V7'
    if reg == 285:
        return 'ARM64_REG_V8'
    if reg == 286:
        return 'ARM64_REG_V9'
    if reg == 287:
        return 'ARM64_REG_V10'
    if reg == 288:
        return 'ARM64_REG_V11'
    if reg == 289:
        return 'ARM64_REG_V12'
    if reg == 290:
        return 'ARM64_REG_V13'
    if reg == 291:
        return 'ARM64_REG_V14'
    if reg == 292:
        return 'ARM64_REG_V15'
    if reg == 293:
        return 'ARM64_REG_V16'
    if reg == 294:
        return 'ARM64_REG_V17'
    if reg == 295:
        return 'ARM64_REG_V18'
    if reg == 296:
        return 'ARM64_REG_V19'
    if reg == 297:
        return 'ARM64_REG_V20'
    if reg == 298:
        return 'ARM64_REG_V21'
    if reg == 299:
        return 'ARM64_REG_V22'
    if reg == 300:
        return 'ARM64_REG_V23'
    if reg == 301:
        return 'ARM64_REG_V24'
    if reg == 302:
        return 'ARM64_REG_V25'
    if reg == 303:
        return 'ARM64_REG_V26'
    if reg == 304:
        return 'ARM64_REG_V27'
    if reg == 305:
        return 'ARM64_REG_V28'
    if reg == 306:
        return 'ARM64_REG_V29'
    if reg == 307:
        return 'ARM64_REG_V30'
    if reg == 308:
        return 'ARM64_REG_V31'
    if reg == 309:
        return 'ARM64_REG_ENDING'
