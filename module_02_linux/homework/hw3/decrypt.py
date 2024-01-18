import re
import sys


def decrypt(encryption: str) -> str:
    regx = '\S\.{2}'

    while re.search(regx, encryption):
        encryption = re.sub(regx, '', encryption)
        if encryption == '':
            return ''
    encryption = encryption.split('.')
    return ''.join(encryption)


if __name__ == '__main__':
    data: str = sys.stdin.read()
    decryption: str = decrypt(data)
    print(decryption)
