from __future__ import print_function

import time
import subprocess
import os
import json
import requests

api_url = 'http://localhost/admin/api.php'

while True:

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-disp$
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    # cmd = "hostname"
    # HOST = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)

    # Pi Hole data!
    try:
        r = requests.get(api_url)
        data = json.loads(r.text)
        DNSQUERIES = data['dns_queries_today']
        ADSBLOCKED = data['ads_blocked_today']
        CLIENTS = data['unique_clients']
    except:
        time.sleep(1)
        continue

    # clear screen
    os.system('clear')

    # print("IP: " + str(IP) + "(" + str(HOST) + ")")
    print("IP: " + str(IP))
    print(str(CPU))
    print(str(MemUsage))
    print(str(Disk))
    print("Ads Blocked: " + str(ADSBLOCKED))
    print("Clients:     " + str(CLIENTS))
    print("DNS Queries: " + str(DNSQUERIES))

    time.sleep(0.9)
