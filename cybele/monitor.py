#!/usr/bin/env python2.7
# encoding: UTF-8

from collections import namedtuple

Summary = namedtuple("Summary", ["lines", "tail"])


def summarize(fObj):
    entries = fObj.readlines()
    return Summary(len(entries), entries[-4:])
