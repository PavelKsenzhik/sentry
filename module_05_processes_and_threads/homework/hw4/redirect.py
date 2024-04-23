"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""

import sys
import traceback


from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

    def __enter__(self):
        if self.stdout:
            sys.stdout = self.stdout
        if self.stderr:
            sys.stderr = self.stderr

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        try:
            if self.stderr and exc_type:
                sys.stderr.write(traceback.format_exc())
                return True
            elif exc_type:
                raise exc_val
        finally:
            if self.stdout:
                sys.stdout = self.old_stdout
            if self.stderr:
                sys.stderr = self.old_stderr


if __name__ == '__main__':
    print('Hello stdout')
    stdout_file = open('stdout.txt', 'w')
    stderr_file = open('stderr.txt', 'w')

    with Redirect(stdout=stdout_file, stderr=stderr_file):
        print('Hello stdout.txt')
        raise Exception('Hello stderr.txt')

    stdout_file.close()
    stderr_file.close()

    print('Hello stdout again')
    raise Exception('Hello stderr')
