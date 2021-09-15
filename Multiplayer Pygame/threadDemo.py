import _thread
import time

sharedVar = 0
sharedVarLock = _thread.allocate_lock()

class simpleClass:
    def __init__(self):
        self.var = 0
        self.varLock = _thread.allocate_lock()

def accumulate(threadID):
    global sharedVar

    for i in range(10):
        sharedVar += 1
        print(f"Thread {threadID} did its thing, sharedVar is {sharedVar}")

def accumulateThreadSafe(threadID,sharedVarLock):
    global sharedVar

    sharedVarLock.acquire()
    for i in range(10):
        sharedVar += 1
        print(f"Thread {threadID} did its thing, sharedVar is {sharedVar}")
    sharedVarLock.release()

def accumulateThreadSafeOOP(threadID,variable):
    variable.varLock.acquire()
    for i in range(10):
        variable.var += 1
        print(f"Thread {threadID} did its thing, sharedVar is {variable.var}")
    variable.varLock.release()

threadID = 1
myVar = simpleClass()
for i in range(10):
    #_thread.start_new_thread(accumulate, (threadID,))
    #_thread.start_new_thread(accumulateThreadSafe, (threadID,sharedVarLock))
    _thread.start_new_thread(accumulateThreadSafeOOP, (threadID,myVar))
    threadID += 1

time.sleep(1)
#print(f"Final value of the shared variable is {sharedVar}")
print(f"Final value of the shared variable is {myVar.var}")