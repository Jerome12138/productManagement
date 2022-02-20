import time
from queue import Queue
import threading
from . import codeSettingHandler
from . import DBHandler

task_queue = Queue()    # 先进先出
lock = threading.Lock()  # 申请线程锁

def pushQueue(taskData):
    queueInfo = {
        "taskType": "compile",
        "developTaskId": taskData.id,
        "userId": taskData.sponsorUserId,
        "status": "等待",
    }
    taskQueueObj = DBHandler.saveTaskQueue(queueInfo)
    queueInfo['id'] = taskQueueObj.id
    task_queue.put(queueInfo)

def startQueue():
    t = threading.Thread(target=runQueue)
    t.setDaemon(True)
    t.start()


def runQueue():
    lock.acquire()  # 获取锁
    queueInfo = task_queue.get()
    queueInfo['status'] = '进行中'
    DBHandler.saveTaskQueue(queueInfo)
    # 运行打包命令
    # time.sleep(10)
    result = codeSettingHandler.compile()
    queueInfo['status'] = '已完成'
    queueInfo['result'] = result
    DBHandler.saveTaskQueue(queueInfo)
    time.sleep(30) # 缓解服务器压力，等待30s再释放线程锁
    lock.release()  # 释放线程锁
