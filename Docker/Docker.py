# coding: utf-8 
import sys 
import threading 
from Queue import Queue 

import requests 


def test(url): 
    try: 
        res = requests.get(url="http://" + url + ":2375/version", timeout=2, verify=False) 
        if res.status_code != 200: 
            return False 
        if 'ApiVersion' in res.content: 
            print url + '\n' 
    except Exception, e: 
        pass 


class MyThread(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 

    def run(self): 
        global queue 
        while True: 
            if queue.empty(): 
                break 
            try: 
                ip = queue.get() 
                test(ip) 
            except Queue.Empty: 
                break 


if __name__ == "__main__": 
    queue = Queue() 
    threads = int(sys.argv[2]) 
    a = open(sys.argv[1], 'r') 
    for ip in a.readlines(): 
        if ip.endswith('\r\n'): 
            ip = ip.strip('\r\n') 
        if ip.endswith('\n'): 
            ip = ip.strip('\n') 
        queue.put(ip) 
    for i in range(threads): 
        c = MyThread() 
        c.start()