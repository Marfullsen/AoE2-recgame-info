#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob
import mgz
from mgz.summary import Summary

input_file = glob.glob('./*.mgx')[0]

with open(f'{input_file}', 'rb') as data:
        header = Summary(data).get_header()
