#coding=utf-8
import os
import elfParser
import shuffleInfo_pb2
import unit
import constants as C

# 读取randLayout文件
randLayoutPath = "/E/dataset/specpu/benchspec/CPU/511.povray_r/orig/povray_r_base.np-x64-O3-m64_shuffled.layout"

rand2orig = {}
orig2rand = {}
for i in open(randLayoutPath, "r").readlines():
    if i != "":
        if i.endswith("\n"):
            i = i[:-1]

        orig = i.split(" ")[0]
        if orig.endswith("L"):
            orig = orig[:-1]
        rand = i.split(" ")[1]
        if rand.endswith("L"):
            rand = rand[:-1]
        orig = int(orig, 16)
        rand = int(rand, 16)
        rand2orig[rand] = orig
        orig2rand[orig] = rand
randList = rand2orig.keys()
randList = sorted(randList)
origList = rand2orig.values()
origList = sorted(origList)



def r2o(VA):
    for i in range(len(randList)):
        if VA >= randList[i] and VA <randList[i+1]:
            print("位于RandBBL = "+hex(randList[i]))
            origVA = rand2orig[randList[i]] + (VA-randList[i])
            print (hex(origVA))
            return origVA



def o2r(VA):
    for i in range(len(origList)):
        if VA >= origList[i] and VA <origList[i+1]:
            print("位于OrigBBL = " + hex(origList[i]))
            randVA = orig2rand[origList[i]] + (VA-origList[i])
            print (hex(randVA))
            return randVA

# temp = []
# for i in range(0x403938 , 0x403a4c)[::4]:
#     temp.append(o2r(i))
#
# temp.sort()
#
# print (hex(temp[0]))
# print (hex(temp[-1]))

# r2o(0x516189)
o2r(0x511dd0)