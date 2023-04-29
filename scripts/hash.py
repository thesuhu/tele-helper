# Python 3 code to demonstrate the
# working of MD5 (string - hexadecimal)

import hashlib


def md5(str2hash):
    # sending to md5()
    result = hashlib.md5(str2hash.encode())
    return result.hexdigest()

# Panggil fungsi dan cetak hasilnya
# print(md5('my text'))

# jika dari command line
# python -c "from scripts.hash import md5; print(md5('my text'))"
