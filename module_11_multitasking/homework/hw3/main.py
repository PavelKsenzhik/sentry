import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
TOTAL_SELL_TICKETS: int = 0
TOTAL_SEATS: int = 30
TOTAL_SELLERS: int = 4

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        global TOTAL_SELL_TICKETS
        global TOTAL_SEATS

        while True:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0 or TOTAL_SELL_TICKETS >= TOTAL_SEATS:
                    break
                self.tickets_sold += 1

                TOTAL_TICKETS -= 1
                TOTAL_SELL_TICKETS += 1

                logger.info(f'{self.name} sold one;  {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_added: int = 0
        logger.info('Director started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        global TOTAL_SELL_TICKETS
        global TOTAL_SEATS

        while True:
            self.random_sleep()
            with self.sem:
                if TOTAL_SELL_TICKETS + TOTAL_TICKETS >= TOTAL_SEATS:
                    break
                if TOTAL_TICKETS <= TOTAL_SELLERS:
                    added_tickets = random.randint(1, 10)
                    self.tickets_added += added_tickets
                    TOTAL_TICKETS += added_tickets
                    logger.info(f'Director {self.name} added {added_tickets} tickets')
        logger.info(f'Director {self.name} all added {self.tickets_added} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()
    sellers: List[Seller] = []
    for _ in range(TOTAL_SELLERS):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    director = Director(semaphore)
    director.start()
    director.join()

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
