import requests
import h5py
import time
import sys
import numpy as np
from datetime import datetime

url='http://143.239.73.224/api/v1/printer/heads/0/position'

loop = 0
lasttime = 0
try:
    while True:
        loop += 1
        response=requests.get(url)
        if response.status_code==200:
            data=response.json()

        now = time.perf_counter()
        timestamp = now - lasttime
        lasttime = now
        head_z = data["z"]
        print(f'{loop}: {head_z}.   {timestamp}.    ctrl+c to stop')
except KeyboardInterrupt:
            print("       logging stopped")

