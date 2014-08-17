#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import

import inspect
from uuid import uuid4

from .utils import enum, text_type, import_attribute

#job status
Status = enum(INIT='initialized', DONE='done',
        DOING='doing', ERROR='error')

class Job(object):
    @classmethod
    def create(cls, func, args=None, kwargs=None,
            status=None, description=None, timeout=None):
        """create a new job instance"""
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}

        if not isinstance(args, (tuple, list)):
            raise TypeError("{0!r} is not a valid args list.".format(args))
        if not isinstance(kwargs, dict):
            raise TypeError('{0!r} is not a valid kwargs dict'.format(kwargs))

        job = cls()

        job._instance =  None
        if inspect.ismethod(func):
            #class instance method
            job._instance = func.__self__
            job._func_name = func.__name__
        elif inspect.isfunction(func) or inspect.isbuiltin(func):
            #function
            job._func_name = '%s.%s' %(func.__module__, func.__name__)
        elif not inspect.isclass() and hasattr(func, '__call__'):
            #callable class instance
            job._instance = func
            job._func_name = '__call__'
        else:
            raise TypeError('Expected a callable or string, but got: {}'.format(func))
        job._args = args
        job._kwargs = kwargs

        job.description = description or job.get_call_string()
        #job.timeout = timeout

        return job

    def __init__(self, id=None):
        self._id = id
        #self.timeout = None
        self.description = None
        self._func_name = None
        self._instance = None
        self._args = None
        self._kwargs = None
        self._status = Status.INIT
        self._result = None
        self._msg = None

    def __repr__(self):
        return '<Job: %s>' %(self.get_call_string())

    @property
    def func_name(self):
        return self._func_name

    @func_name.setter
    def func_name(self, v):
        self._func_name = v

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, v):
        self._args = v

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, v):
        self._kwargs = v

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, v):
        self._instance = v

    def get_id(self):
        if self._id is None:
            self._id = text_type(uuid4())

        return self._id.split('-')[0]

    def set_id(self, v):
        self._id = v

    id = property(get_id, set_id)

    def get_status(self):
        return self._status

    def set_status(self, v):
        if isinstance(v, Status):
            self._status = v
        return

    status = property(get_status, set_status)

    @property
    def is_finished(self):
        return self.status == Status.DONE

    @property
    def is_started(self):
        return self.status == Status.DOING

    @property
    def is_errored(self):
        return self.status == Status.ERROR

    @property
    def msg(self):
        return self._msg

    @property
    def func(self):
        if self.func_name is None:
            return None

        if self.instance:
            return getattr(self.instance, self.func_name)

        return import_attribute(self.func_name)

    @property
    def result(self):
        return self._result

    def get_call_string(self):
        if self.func_name is None:
            return None

        arg_l = [repr(a) for a in self.args]
        arg_l += ["%s=%r" %(k, v) for k, v in self.kwargs.items()]
        args = ', '.join(arg_l)
        return "%s(%s)" %(self.func_name, args)

    def execute(self):
        try:
            self._status = Status.DOING
            self._result = self.func(*self.args, **self.kwargs)
            self._status = Status.DONE
        except Exception as e:
            self._status = Status.ERROR
            self._msg = str(e)

        return self._result

if __name__ == '__main__':
    j = Job.create(len)
