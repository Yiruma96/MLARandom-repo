#coding=utf-8
import subprocess
import sys
import time
import benchmarkConfig
from myThread import myThread

root = benchmarkConfig.root
config = benchmarkConfig.config

suffix = benchmarkConfig.suffix
readelf = benchmarkConfig.readelf
pranderPath = benchmarkConfig.pranderPath
runPathList = benchmarkConfig.runPathList
failedRunPath = benchmarkConfig.failedRunPath





retuDict = {}

def runSpec(runPath, curIdx, threadNum):
    successList = []
    failedList = []

    if grained == "bbl":
        command = "./ShellBBL.sh"
    elif grained == "fun":
        command = "./ShellFUN.sh"
    else:
        command = "./ShellOrig.sh"

    ave_time = 0
    shellRetu = None
    for i in range(_round):
        start = time.time()
        print("[Thread#%d] Start CurIdx=%d CMD=%s" % (threadNum, curIdx, command + " " + runPath))
        shellRetu = subprocess.run([command], cwd=runPath, shell=True, capture_output=True)
        print("[Thread#%d] End: Code=%d CurIdx=%d CMD=%s" % (threadNum, shellRetu.returncode, curIdx, command + " " + runPath))
        end = time.time()
        ave_time += end-start
    ave_time = ave_time/_round

    if shellRetu.returncode > 128:
        failedList.append([runPath, command, shellRetu.returncode])
    else:
        successList.append([runPath, command, ave_time])

    retuDict[runPath] = [failedList, successList]


def onFinish():
    all_failed = []
    fw = open("runTime", "w")
    print("\n\n\n\n完成！")

    for runPath in retuDict:
        print("================\n%s" % runPath)
        fw.write("================\n%s" % runPath)
        if len(retuDict[runPath][0]):
            print("Fail List:")
            fw.write("Fail List:\n")
            tempDict = {}
            tempList = []
            for j in retuDict[runPath][0]:
                all_failed.append(j)
                tempList.append(j)
            tempDict[runPath] = tempList
            print(tempDict)
            fw.write(str(tempDict) + "\n")
        if len(retuDict[runPath][1]):
            print("Success List:")
            fw.write("Success List:\n")
            for j in retuDict[runPath][1]:
                print(j)
                fw.write(str(j) + "\n")
    fw.close()

    for failed in all_failed:
        print(failed)



if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("runBenchmark.py grained[bbl|fun|orig] dataset[run|failed] cpu round")
        exit(0x233)

    if sys.argv[1] in ["bbl", "fun", "orig"]:
        grained = sys.argv[1]
    else:
        print("请指定bbl|fun|orig")
        exit(0x233)

    if sys.argv[2] == "run":
        runPaths = runPathList
    elif sys.argv[2] == "failed":
        runPaths = failedRunPath
    else:
        print("请指定run|failed")
        exit(0x233)

    cpu_count = int(sys.argv[3])
    _round = int(sys.argv[4])

    # runPaths = runPathList
    # cpu_count = 1
    # type = "bbl"

    thread = myThread(runPaths, runSpec, poolNum=int(cpu_count), onFinish=onFinish)
    thread.start()



