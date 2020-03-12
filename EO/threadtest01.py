import threading
import time

def test0():
    time.sleep(2)
    print("dal dal")

def test1():
    time.sleep(5)
    print("over")
    
def test2():
    for i in range(5):
        time.sleep(1)
        print("{0} sec".format(i))

t0=threading.Thread(target=test0)
t1=threading.Thread(target=test1)
t2=threading.Thread(target=test2)

t0.start()
t1.start()
t2.start()