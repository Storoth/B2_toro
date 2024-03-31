
import time
import datetime

from telega import baza

def calculator(name, deadline, frequency):
    while True:
        
        now_time = datetime.datetime.now()
        time_left = deadline - now_time
        
        if now_time < deadline:
            print(f'время до конца {name}:{time_left}')
        else:
            print('XXXX')
            break
        time.sleep(frequency)