#!/usr/bin/env python
# encoding: utf-8

from worker.job import Job
#import test
from test import run

if __name__ == "__main__":
    j = Job.create(run, kwargs = {'a':2,'b':3})
    print j
    print j.id
    print j.status
    print j.execute()
    print j.msg, j.status
