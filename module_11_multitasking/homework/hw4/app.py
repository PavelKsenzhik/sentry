import threading
import time
import random
from queue import PriorityQueue


class Producer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Producer: Running")

        for i_priority in [random.randint(0, 6) for _ in range(10)]:
            self.queue.put((i_priority, f"Task(priority={i_priority})."))

        while not self.queue.empty():
            time.sleep(0.5)

        print("Producer: Done")


class Consumer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("Consumer: Running")
        while not self.queue.empty():
            priority, task = self.queue.get()

            sleep = random.random()
            print(f">running {task} \t\t sleep({sleep})")
            time.sleep(sleep)
            self.queue.task_done()

        print("Consumer: Done")


def main():
    queue = PriorityQueue()
    producer = Producer(queue)
    consumer = Consumer(queue)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    queue.join()


if __name__ == "__main__":
    main()
