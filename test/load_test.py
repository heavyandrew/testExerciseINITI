import time

import requests
import random as r

server_url = '127.0.0.1'
place = 10

names = ['Alexander','Benjamin','Charlotte','David','Emily','Fiona','Gabriel','Hannah','Isabella','Katherine','Nathan','Penelope','Rachel','Taylor','Ulysses','Victoria','William','Xander','Yasmine', 'Zachary']
english = ['A1', 'A2', 'A2+', 'B1', 'B2', 'B2+', 'C1', 'C2']

while True:
    method = ages = r.randrange(1, 3)
    if method == 1:
        requests.post(f'http://{server_url}/add?place={r.randrange(place)}&name={r.choice(names)}&age={r.randrange(60)}&heights={r.randrange(140, 200)}&foot={r.randrange(35, 48)}&english={r.choice(english)}')
    elif method == 2:
        requests.post(f'http://{server_url}/update?place={r.randrange(place)}&name={r.choice(names)}&age={r.randrange(60)}&heights={r.randrange(140, 200)}&foot={r.randrange(35, 48)}&english={r.choice(english)}')
    else:
        requests.delete(f'http://{server_url}/delete?place={r.randrange(place)}')

    time.sleep(4)