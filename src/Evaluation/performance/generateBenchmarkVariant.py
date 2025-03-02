#coding=utf-8
import os
import subprocess
import sys
import time
import benchmarkConfig
import json
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


def randomize(runPath, curIdx, threadNum):
    origPath = runPath + "/../../orig/"
    randomPath = runPath + "/../../random/"
    if not os.path.exists(origPath):
        return

    if os.path.exists(origPath):
        print ("================\n" + origPath)
        if os.path.exists(randomPath):
            os.system("rm -rf " + randomPath)
        os.mkdir(randomPath)
        os.mkdir(randomPath + "/fun/")

        origexeList = os.listdir(origPath)
        for origexe in origexeList:
            origexePath = origPath + "/" + origexe

            status = True
            cmd = "python3.10 {prander} {bin}".format(prander=pranderPath, bin=origexePath)

            print("Start with round {}: {}".format(_round, cmd))
            ave_time = 0
            retu = None
            for i in range(_round):
                startTime = time.time()
                retu = subprocess.run(args=[cmd], cwd=origPath, shell=True, capture_output=True)
                endTime = time.time()
                ave_time += endTime - startTime
            ave_time = ave_time/_round
            print("End: Status=%d CMD=%s" % (retu.returncode, retu.stdout))

            if retu.returncode != 0:
                status = False
                failedList.append(origexePath + "_shuffled")

            if status:
                # 统计元数据数量
                # MetadataStatistics = subprocess.getstatusoutput("python3.10 {prander} {bin}".format(prander=pranderPath, bin=origexePath))[1]
                # randomRetu.append([origexePath + "_fun_shuffled", endTime - startTime, json.loads(MetadataStatistics)])
                randomRetu.append([origexePath + "_fun_shuffled", ave_time])
                print("mv {bin}_shuffled {dst}".format(bin=origexePath, dst=randomPath + "/fun/" + origexe))
                os.system("mv {bin}_shuffled {dst}".format(bin=origexePath, dst=randomPath + "/fun/" + origexe))

                # 统计rand节的大小
                shellRetu = subprocess.getstatusoutput("readelf -SW "+origexePath)[1]
                for line in shellRetu.split("\n"):
                    if "rand" in line:
                        temp = []
                        for i in line.split(" "):
                            if i != "":
                                temp.append(i)
                        randomRetu.append(temp[5])


def onFinish():
    fw = open("rewriteTime", "w")
    print ("\n\n\n\n随机化完成！")
    print ("以下二进制文件执行随机化失败：")
    fw.write("以下二进制文件执行随机化失败：\n")
    for i in failedList:
        fw.write(str(i)+"\n")
        print(i)
    print ("以下二进制文件执行随机化成功:")
    fw.write("以下二进制文件执行随机化成功：\n")
    for i in randomRetu:
        fw.write(json.dumps(i) + "\n")
        print (json.dumps(i))
    fw.close()

if __name__ == '__main__':
    taskList = None
    cpu_count = 1
    _round = 1
    if sys.argv[1] == "run":
        taskList = runPathList
        _round = 1
        if len(sys.argv) != 3:
            print("generateBenchmarkVariant.py run cpu_count 缺少指定cpu_count")
            exit(0x233)
        else:
            cpu_count = int(sys.argv[2])
    elif sys.argv[1] == "failed":
        taskList = failedRunPath
        cpu_count = 1
        _round = 1
    elif sys.argv[1] == "performance":
        taskList = runPathList
        cpu_count = 1
        if len(sys.argv) != 3:
            print("generateBenchmarkVariant.py performance round 缺少指定round")
            exit(0x233)
        else:
            _round = int(sys.argv[2])
    else:
        print("请指定run|failed|performance")
        exit(0x233)

    # taskList = runPathList
    # cpu_count = 4

    thread = myThread(taskList, randomize, poolNum=int(cpu_count), onFinish=onFinish)
    thread.start()
