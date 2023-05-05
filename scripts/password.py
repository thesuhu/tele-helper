import random
import string

# Fungsi untuk membuat password
def password_generator(panjang=12):
  # Tentukan panjang password
  # panjang = 12

  # Tentukan karakter yang bisa digunakan
  karakter = string.ascii_letters + string.digits + string.punctuation

  # Acak karakter dan gabungkan menjadi password
  password = "".join(random.choice(karakter) for i in range(panjang))
  
  # Sanitasi karakter jika karakter terakhir adalah \
  if password[-1] == "\\":
      password = password[:-1] + "%"

  # Kembalikan password
  return password

# Panggil fungsi dan cetak hasilnya
# print(password_generator())

# jika dari command line
# python -c "from scripts.password import password_generator; print(password_generator())"