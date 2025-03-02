#coding=utf-8
import os
import subprocess
import time
import benchmarkConfig
from myThread import myThread

root = benchmarkConfig.root
config = benchmarkConfig.config
runPathList = benchmarkConfig.runPathList
failedRunPath = benchmarkConfig.failedRunPath
suffix = benchmarkConfig.suffix
readelf = benchmarkConfig.readelf
pranderPath = benchmarkConfig.pranderPath

exeDict = {}
failedList = [] # 记录随机化失败的名单
randomRetu = []  # 记录随机化的时间开销以及统计信息


def randomize(elf, curIdx, threadNum):
    print("[*] " + elf)

    cmd = "python3.10 {prander} {bin}".format(prander="/ccr/randomizer/NoCompiler/prander.py", bin=elf)
    ave_time = 0
    retu = None
    for i in range(_round):
        startTime = time.time()
        retu = subprocess.run(args=[cmd], cwd="/ccr/code", shell=True, capture_output=True)
        endTime = time.time()
        curTime = endTime - startTime
        if retu.returncode != 0:
            print("{} 编译失败".format(elf))
        else:
            os.system("rm -rf {}".format(elf+"_shuffled"))
        print(curTime)
        ave_time += curTime
    ave_time = ave_time/_round
    print("Ave Time={}".format(str(ave_time)))


if __name__ == '__main__':
    taskList = None
    cpu_count = 1
    _round = 1

    runPathList = []
    # binDir = "/E/binaryset/binaries-spec-arm64/O3/"
    # binDir = "/ccr/binaryset/rw-rustmix"
    binDir = "/E/binaryset/rustmix"
    for exe in os.listdir(binDir):
        exePath = binDir + "/" + exe
        runPathList.append(exePath)

    thread = myThread(runPathList, randomize, poolNum=int(cpu_count))
    thread.start()
