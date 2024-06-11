import json
import multiprocessing
import time
from multiprocessing.pool import ThreadPool
from typing import Callable

import requests

import logging

# logging.basicConfig(level=logging.DEBUG)


class BookClient:
    URL: str = 'http://127.0.0.1:5000/api/books'
    TIMEOUT: int = 5

    def __init__(self):
        self.session = requests.Session()

    def get_all_books(self) -> dict:
        response = self.session.get(self.URL, timeout=self.TIMEOUT)
        return response.json()

    def add_new_book(self, data: dict):
        response = self.session.post(self.URL, json=data, timeout=self.TIMEOUT)
        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def update_book(self, data: dict, book_id: int):
        response = self.session.put(f'{self.URL}/{book_id}', json=data, timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def get_book(self, book_id: int):
        response = self.session.get(f'{self.URL}/{book_id}', timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))

    def delete_book(self, book_id: int):
        response = self.session.delete(f'{self.URL}/{book_id}', timeout=self.TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError('Wrong params. Response message: {}'.format(response.json()))


def work(client: BookClient, name):
    client.get_all_books()
    book = client.add_new_book({'title': f'{name}1', 'author': 1})
    client.update_book({'title': f'{name}2', 'author': 1}, book['id'])
    client.get_book(book['id'])
    client.delete_book(book['id'])


def work_with_session(total_count: int):
    client = BookClient()
    for i in range(total_count):
        work(client, f'work_with_session{i}')


def work_with_session_thread(total_count: int):
    client = BookClient()
    with ThreadPool(processes=multiprocessing.cpu_count()) as pool:
        pool.starmap(work, [(client, f'work_with_session_thread{i}') for i in range(total_count)])


def work_without_session(total_count: int):
    for i in range(total_count):
        client = BookClient()
        work(client, f'work_without_session{i}')


def work_without_session_thread(total_count: int):
    with ThreadPool(processes=multiprocessing.cpu_count()) as pool:
        pool.starmap(work, [(BookClient(), f'work_with_session_thread{i}') for i in range(total_count)])


def log_work(func: Callable, total_count: int):
    start_time = time.time()

    func(total_count)

    end_time = time.time()
    print(f"--- {(end_time - start_time)} seconds --- { func.__name__} --- {total_count} ---")


if __name__ == '__main__':
    total_counts = [10, 100, 1000]

    for i_count in total_counts:
        log_work(work_with_session, i_count)
        log_work(work_without_session, i_count)
        log_work(work_with_session_thread, i_count)
        log_work(work_without_session_thread, i_count)


