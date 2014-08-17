#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import

import importlib

text_type = str
def enum(**kwargs):
    return type('Enum', (object,), kwargs)

def import_attribute(name):
    module_name, attribute = name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attribute)

