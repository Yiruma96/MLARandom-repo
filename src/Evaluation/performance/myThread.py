import threading
import multiprocessing
import time


class myThread():

    def __init__(self, threadData, threadFun, poolNum=multiprocessing.cpu_count(), onFinish=None):
        self.threadPool = []
        self.poolNum = poolNum
        self.threadFun = threadFun
        self.onFinish = onFinish

        self.threadData = threadData
        self.dataIndex = 0
        self.dataNum = len(self.threadData)
        self.status = [0]*self.poolNum

        for i in range(poolNum):
            self.threadPool.append(threading.Thread(target=self.wrapper, args=(i,)))

        print("线程池数量" + str(poolNum))
        print("任务数量" + str(self.dataNum))

    def wrapper(self, threadNum):
        while self.dataIndex < self.dataNum:
            data = self.threadData[self.dataIndex]
            self.dataIndex += 1
            # xie. 不做异常处理的话，可能该wrapper就卡在这里，其status一直为0导致该线程池一直在等待结束
            try:
                self.threadFun(data, self.dataIndex, threadNum)
            except:
                pass

        self.status[threadNum] = 1

    def start(self):
        for i in range(self.poolNum):
            self.threadPool[i].start()

        while True:
            if 0 not in self.status:
                if self.onFinish:
                    self.onFinish()
                return
            else:
                time.sleep(0.01)

