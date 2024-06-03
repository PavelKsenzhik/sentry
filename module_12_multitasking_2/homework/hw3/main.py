from threading import Semaphore, Thread
import time

sem: Semaphore = Semaphore()
IS_RUNNING = True


def fun1():
    while IS_RUNNING:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while IS_RUNNING:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


try:
    t1: Thread = Thread(target=fun1)
    t2: Thread = Thread(target=fun2)

    t1.start()
    t2.start()

    while IS_RUNNING:
        pass
except KeyboardInterrupt:
    IS_RUNNING = False
    print('\nReceived keyboard interrupt, quitting threads.')
    exit(1)
