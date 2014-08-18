#!/usr/bin/env python
# encoding: utf-8

import random
import requests
import time

from worker.job import Job
from worker.tworker import ThreadWorker
from Queue import Queue
from test import run_website

if __name__ == "__main__":
    rq = Queue()
    wq = Queue()

#    for i in xrange(20):
#        randomvar = random.random()
#        j = Job.create(run, args=(randomvar,))
#        wq.put_nowait(j)

#    t = ThreadWorker.create(wq, rq)
#    t.gogo()
#
#    while not t.rqueue.empty():
#        item = t.rqueue.get_nowait()
#        print item
    t1 = time.time()

    with open('top500websites.txt', 'r') as f:
        websites = f.read().split('\n')

    for web in websites[:20]:
        j = Job.create(run_website, args=('GET', 'http://' + web,),
                kwargs = {'timeout':1})
        wq.put_nowait(j)

    t = ThreadWorker.create(wq, rq)
    t.gogo()

    t2 = time.time()
    print("Time: %s" %(t2 - t1))

    while not t.rqueue.empty():
        item = t.rqueue.get_nowait()
        print item
