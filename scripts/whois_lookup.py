import whois as pywhois


def print_whois(domain=None):
    w = pywhois.whois(domain) if domain is not None else {}
    # print(w)
    return w

# panggil fungsi
# print_whois('google.com')

# jika dari command line
# python -c "from scripts.whois_lookup import print_whois; print(print_whois())"

# Objek whois memiliki atribut yang berisi informasi whois yang diekstrak, seperti tanggal kadaluarsa, nama, alamat, dll.
# https://pypi.org/project/python-whois/
