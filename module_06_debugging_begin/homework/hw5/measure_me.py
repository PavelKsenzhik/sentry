"""
Каждый лог содержит в себе метку времени, а значит, правильно организовав логирование,
можно отследить, сколько времени выполняется функция.

Программа, которую вы видите, по умолчанию пишет логи в stdout. Внутри неё есть функция measure_me,
в начале и в конце которой пишется "Enter measure_me" и "Leave measure_me".
Сконфигурируйте логгер, запустите программу, соберите логи и посчитайте среднее время выполнения функции measure_me.
"""
import datetime
import logging
import random
import re
from typing import List

logger = logging.getLogger(__name__)


def get_data_line(sz: int) -> List[int]:
    try:
        logger.debug("Enter get_data_line")
        return [random.randint(-(2 ** 31), 2 ** 31 - 1) for _ in range(sz)]
    finally:
        logger.debug("Leave get_data_line")


def measure_me(nums: List[int]) -> List[List[int]]:
    logger.debug("Enter measure_me")
    results = []
    nums.sort()

    for i in range(len(nums) - 2):
        logger.debug(f"Iteration {i}")
        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    logger.debug(f"Found {target}")
                    results.append([nums[i], nums[left], nums[right]])
                    logger.debug(
                        f"Appended {[nums[i], nums[left], nums[right]]} to result"
                    )
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    logger.debug(f"Increment left (left, right) = {left, right}")
                    left += 1
                else:
                    logger.debug(f"Decrement right (left, right) = {left, right}")

                    right -= 1

    logger.debug("Leave measure_me")

    return results


def calculate_average_execution_time():
    start_times = []
    end_times = []

    with open('stdout.log', 'r') as file:
        for line in file:
            start_times += re.findall(r"(\d{2}:\d{2}:\d{2}.\d{3}) - DEBUG - Enter measure_me", line)
            end_times += re.findall(r"(\d{2}:\d{2}:\d{2}.\d{3}) - DEBUG - Leave measure_me", line)

    total_time = 0
    num_executions = min(len(start_times), len(end_times))

    for i in range(num_executions):
        start_time = start_times[i]
        end_time = end_times[i]

        start_timestamp = datetime.datetime.strptime(start_time, "%H:%M:%S.%f")
        end_timestamp = datetime.datetime.strptime(end_time, "%H:%M:%S.%f")
        execution_time = end_timestamp - start_timestamp
        total_time += execution_time.total_seconds()

    if num_executions == 0:
        print("Logs not found")
        return None

    average_time = total_time / num_executions

    print(f"Average execution time: {average_time} seconds")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='stdout.log',
                        format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
                        datefmt='%I:%M:%S')
    for it in range(15):
        data_line = get_data_line(10 ** 3)
        measure_me(data_line)

    calculate_average_execution_time()
