import requests
import time
from threading import Thread, Lock
from queue import Queue

lock = Lock()
queue = Queue()


def get_date(timestamp):
    response = requests.get(f"http://127.0.0.1:8080/timestamp/{timestamp}")
    if response.status_code == 200:
        return response.text
    else:
        return None


def write_log(timestamp, date):
    with lock:
        with open("logs.txt", "a") as file:
            file.write(f"{timestamp} {date}\n")


def worker():
    for _ in range(20):
        timestamp = int(time.time())
        date = get_date(timestamp)
        write_log(timestamp, date)
        time.sleep(1)
    queue.task_done()


if __name__ == "__main__":
    # threads = []
    # for _ in range(10):
    #     t = Thread(target=worker)
    #     t.start()
    #     threads.append(t)
    #     time.sleep(1)
    #
    # for t in threads:
    #     t.join()

    for i in range(10):
        queue.put(Thread(target=worker))

    while not queue.empty():
        job = queue.get_nowait()
        job.start()
        time.sleep(1)

    queue.join()
