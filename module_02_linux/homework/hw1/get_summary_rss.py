import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, 'output_file.txt')


def get_summary_rss(ps_output_file_path: str) -> str:
    with open(ps_output_file_path, 'r') as output_file:
        lines = output_file.readlines()[1:]
    memory_sum = 0
    for line in lines:
        columns = line.split()
        memory_sum += int(columns[5])

    size_key = 0
    size_labels = {
        0: 'Б',
        1: 'Кб',
        2: 'Мб;',
        3: 'Гб',
        4: 'Тб',
    }

    while memory_sum > 1024:
        size_key += 1

        if size_key not in size_labels:
            return f"Объём памяти {round(memory_sum, 2)} {size_labels[size_key -1 ]}"
            break

        memory_sum /= 1024
    return f"Объём памяти {round(memory_sum, 2)} {size_labels[size_key]}"


if __name__ == '__main__':
    path: str = OUTPUT_FILE
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
