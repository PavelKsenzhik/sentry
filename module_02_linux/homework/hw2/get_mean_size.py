import sys


def get_mean_size(ls_output: list) -> float:
    count = len(ls_output)
    size_sum = 0
    for line in ls_output:
        columns = line.split()
        size_sum += int(columns[4])
    return round(size_sum / count, 2)


if __name__ == '__main__':
    data: list = sys.stdin.readlines()[1:]
    if not data:
        print('Нет файлов в директории')
    else:
        mean_size: float = get_mean_size(data)
        print(f'Средний размер файлов {mean_size}')
