#!/usr/bin/env python
# encoding: utf-8

import threading
import Queue

class ThreadWorker():

    @classmethod
    def create(cls, wqueue, rqueue, thread_num = 8):
        tw = cls(wqueue, rqueue)

        if not isinstance(wqueue, Queue) or \
                not isinstance(rqueue, Queue):
            raise TypeError('Expected two Queue instance, but got %s and %s'
                    %(type(wqueue), type(rqueue)))

        tw._wqueue_len = len(wqueue) if wqueue is not None else 0
        tw._rqueue_len = len(rqueue) if rqueue is not None else 0

        if tw._wqueue_len == 0:
            raise ValueError("Work queue is empty, must not be zero.")

        tw.description = tw.get_description()

        return tw

    def __init__(self, wq, rq):
        self._wqueue = wq
        self._rqueue = rq
        self._wqueue_len = None
        self._rqueue_len = None
        self.description = None
        #self._status

    @property
    def wqueue(self):
        return self._wqueue

    @property
    def rqueue(self):
        return self._rqueue

    @property
    def wqueue_len(self):
        return len(self._wqueue)

    @property
    def rqueue_len(self):
        return len(self._rqueue)

    def get_description(self):
        wq_l = self.wqueue_len
        rq_l = self.rqueue_len

        return "Total jobs:%d, finished:%d, doing:%d." %(wq_l + rq_l, wq_l, rq_l)
