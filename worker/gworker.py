#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import

import gevent
from gevent import monkey; monkey.patch_all()
from gevent import queue

from .job import Job

class GeventWorker():
    @classmethod
    def create(cls, wqueue, rqueue, greenlet_num = 8):
        gw = cls(wqueue, rqueue)

        if not isinstance(wqueue, queue.JoinableQueue) or \
                not isinstance(rqueue, queue.JoinableQueue):
            raise TypeError('Expected two gevent.queue.JoinableQueue instance, but got %s and %s.'
                    %(type(wqueue), type(rqueue)))

        gw._wqueue_len = wqueue.qsize() if wqueue is not None else 0
        gw._rqueue_len = rqueue.qsize() if rqueue is not None else 0

        if gw._wqueue_len == 0:
            raise ValueError("Work queue is empty, must not be zero.")

        gw.description = gw.get_description()
        gw.greenlets = [gevent.Greenlet(gw.__run)
                for i in range(gw.wqueue_len)]

        return gw

    def __init__(self, wq, rq):
        self._wqueue = wq
        self._rqueue = rq
        self._wqueue_len = None
        self._rqueue_len = None
        self.description = None
        self.greenlets = []

    def __repr__(self):
        return "<GeventWorker: wqueue length %d, rqueue length %d>"\
                %(self.wqueue_len, self.rqueue_len)

    def __run(self):
        while True:
            try:
                j = self.wqueue.get_nowait()
                result = j.func(*j.args, **j.kwargs)
                self.rqueue.put_nowait(result)
                self.wqueue.task_done()
            except gevent.queue.Empty:
                break

    def gogo(self):
        [t.start() for t in self.greenlets]
        gevent.joinall(self.greenlets)

    @property
    def greenlet_num(self):
        return len(self.greenlets)

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
    pass
