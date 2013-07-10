#!/usr/bin/env python2.7
# encoding: UTF-8

import datetime
from StringIO import StringIO
import unittest as functest

from jinja2 import Environment, PackageLoader

from cybele.monitor import summarize


def ipsum_log(name, n=16):
    now = datetime.datetime.utcnow()
    ts = (now - datetime.timedelta(seconds=i) for i in range(n))
    env = Environment(
        loader=PackageLoader("cybele", "templates"))
    tmplt = env.get_template("ipsumlog.j2")
    rv = StringIO(tmplt.render(ts=ts))
    rv.name = name
    return rv


class SummaryTests(functest.TestCase):

    def test_generation_of_log(self):
        log = ipsum_log("log_one", 100)
        self.failUnlessEqual("log_one", log.name)
        self.failUnlessEqual(100, len(log.readlines()))

    def test_summary(self):
        log = ipsum_log("log_two", 1024)
        rv = summarize(log)
        self.assertEqual(4, len(rv.tail))
        self.assertEqual(log.getvalue().splitlines(True)[-4:], rv.tail)


if __name__ == "__main__":
    functest.main()
