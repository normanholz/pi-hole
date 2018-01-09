from __future__ import print_function

import time
import subprocess
import os
import json
import requests
from terminaltables import AsciiTable

api_url = 'http://localhost/admin/api.php'

while True:

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-disp$
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "hostname"
    HOST = subprocess.check_output(cmd, shell=True)
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"%s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)

    # Pi Hole data!
    try:
        r = requests.get(api_url)
        data = json.loads(r.text)

        DOMAINS = data['unique_domains']
        BLOCKEDDOMAINS = data['domains_being_blocked']

        QUERIES_FORWARDED = data['queries_forwarded']
        QUERIES_CACHED = data['queries_cached']
        DNSQUERIES = data['dns_queries_today']

        ADSBLOCKED = data['ads_blocked_today']
        ADSTODAY = data['ads_percentage_today']

        CLIENTS = data['unique_clients']


    except:
        time.sleep(1)
        continue

    piData = []
    piData.append(['Host', str(HOST).strip()])
    piData.append(["CPU Load", str(CPU)])
    piData.append(['Memory', str(MemUsage)])
    piData.append(["Disk", str(Disk)])

    piDataTable = AsciiTable(piData)
    piDataTable.inner_heading_row_border = False
    piDataTable.inner_row_border = True
    piDataTable.title = '--RASPBERRY PI'

    piHoleData = []
    piHoleData.append(['IP (Add this as DNS)', str(IP).strip()])
    piHoleData.append(["Clients", str(CLIENTS)])
    # piHoleData.append(["Domains", str(DOMAINS)])
    # piHoleData.append(["Domains blocked", str(BLOCKEDDOMAINS)])
    piHoleData.append(["DNS Queries", str(DNSQUERIES)])

    # QUERIES_FORWARDED = data['queries_forwarded']
    # QUERIES_CACHED = data['queries_cached']
    piHoleData.append(["Ads blocked", str(ADSBLOCKED)])
    piHoleData.append(["Ads blocked (%)", str(ADSTODAY).strip() + " %"])

    piHoleDataTable = AsciiTable(piHoleData)
    piHoleDataTable.inner_heading_row_border = False
    piHoleDataTable.inner_row_border = True
    piHoleDataTable.title = "--PI - HOLE AD BLOCKER"

    # clear screen
    os.system('clear')
    print("")
    print(piHoleDataTable.table)
    print("")
    print(piDataTable.table)


    time.sleep(0.9)
