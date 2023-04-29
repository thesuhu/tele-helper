# import requests

# def what_my_ip():
#     response = requests.get("https://httpbin.org/ip")
#     ip_address = response.json()["origin"]
#     return ip_address

# ip_address = what_my_ip()
# print("Your public IP address is:", ip_address)

import requests

def what_my_ip():
    response = requests.get("https://ipinfo.io/")
    data = response.json()
    return data

# panggil fungsi:
# ip_info = what_my_ip()
# print("Your IP Address:", ip_info["ip"])
# print("ISP:", ip_info["org"])
# print("City:", ip_info["city"])
# print("Region:", ip_info["region"])
# print("Country:", ip_info["country"])
# print("Latitude:", ip_info["loc"].split(",")[0])
# print("Longitude:", ip_info["loc"].split(",")[1])
# print(ip_info)

# command line:
# python -c "from scripts.myip import what_my_ip; print(what_my_ip())"