#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import

import threading
import Queue

from .job import Job

class ThreadWorker():
    @classmethod
    def create(cls, wqueue, rqueue, thread_num = 8):
        tw = cls(wqueue, rqueue)

        if not isinstance(wqueue, Queue.Queue) or \
                not isinstance(rqueue, Queue.Queue):
            raise TypeError('Expected two Queue instance, but got %s and %s.'
                    %(type(wqueue), type(rqueue)))

        tw._wqueue_len = wqueue.qsize() if wqueue is not None else 0
        tw._rqueue_len = rqueue.qsize() if rqueue is not None else 0

        if tw._wqueue_len == 0:
            raise ValueError("Work queue is empty, must not be zero.")

        tw.description = tw.get_description()
        tw.workers = [threading.Thread(target=tw.__run, name=i)
                for i in range(thread_num)]

        return tw

    def __init__(self, wq, rq):
        self._wqueue = wq
        self._rqueue = rq
        self._wqueue_len = None
        self._rqueue_len = None
        self.description = None
        self.workers = []

    def __repr__(self):
        return "<ThreadWorker: wqueue length %d, rqueue length %d>"\
                %(self.wqueue_len, self.rqueue_len)

    def __run(self):
        while True:
            try:
                j = self.wqueue.get_nowait()
                result = j.func(*j.args, **j.kwargs)
                self.rqueue.put_nowait(result)
                self.wqueue.task_done()
            except Queue.Empty:
                break

    def gogo(self):
        [t.start() for t in self.workers]
        for t in self.workers:
            if t.is_alive():
                t.join()

    @property
    def thread_num(self):
        return len(self.workers)

    @property
    def wqueue(self):
        return self._wqueue

    @property
    def rqueue(self):
        return self._rqueue

    @property
    def wqueue_len(self):
        return self._wqueue.qsize()

    @property
    def rqueue_len(self):
        return self._rqueue.qsize()

    def get_description(self):
        wq_l = self.wqueue_len
        rq_l = self.rqueue_len

        return "Total jobs:%d, finished:%d, doing:%d." %(
                wq_l + rq_l, wq_l, rq_l)

if __name__ == '__main__':
    rq = Queue.Queue()
    wq = Queue.Queue()
    [wq.put_nowait(t) for t in xrange(20)]
    t = ThreadWorker.create(wq, rq)
    t.gogo()
