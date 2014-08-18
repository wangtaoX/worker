#!/usr/bin/env python
# encoding: utf-8

from gevent import monkey;monkey.patch_all()
import random
import requests
import time
from gevent import queue

from worker.job import Job
from worker.gworker import GeventWorker
from test import run_website

if __name__ == "__main__":
    rq = queue.JoinableQueue()
    wq = queue.JoinableQueue()

    t1 = time.time()

    with open('top500websites.txt', 'r') as f:
        websites = f.read().split('\n')

    for web in websites[:100]:
        j = Job.create(run_website, args=('GET', 'http://' + web,),
                kwargs = {'timeout':1})
        wq.put_nowait(j)

    t = GeventWorker.create(wq, rq)
    t.gogo()

    t2 = time.time()
    print("Time: %s" %(t2 - t1))

#    while not t.rqueue.empty():
#        item = t.rqueue.get_nowait()
#        print item
