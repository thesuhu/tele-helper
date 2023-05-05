import json
import whois as pywhois


def print_whois(domain=None):
    w = pywhois.whois(domain) if domain is not None else {}
    # print(w)
    return w

# panggil fungsi
# print_whois('google.com')

# jika dari command line
# python -c "from scripts.whois_lookup import print_whois; print(print_whois('google.com'))"

# Objek whois memiliki atribut yang berisi informasi whois yang diekstrak, seperti tanggal kadaluarsa, nama, alamat, dll.
# https://pypi.org/project/python-whois/

from ipwhois import IPWhois

def ip_lookup(ip_address):

    # ip_address = "8.8.8.8"  # contoh alamat IP yang akan di-lookup

    ipwhois = IPWhois(ip_address) if ip_address is not None else {}
    result = ipwhois.lookup_rdap()

    # tampilkan hasil lookup
    print(json.dumps(result, indent=4))
    return json.dumps(result, indent=4)

# python -c "from scripts.whois_lookup import ip_lookup; print(ip_lookup('8.8.8.8'))"