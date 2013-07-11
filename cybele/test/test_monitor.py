#!/usr/bin/env python2.7
# encoding: UTF-8

import datetime
import os
import shutil
from StringIO import StringIO
import tempfile
import timeit
import unittest
import unittest as functest

from jinja2 import Environment, PackageLoader

from cybele.monitor import get_channels
from cybele.monitor import put_summary
from cybele.monitor import suffix
from cybele.monitor import summarize
from cybele.monitor import summary2text
from cybele.monitor import text2summary


def ipsum_log(name, n=16):
    now = datetime.datetime.utcnow()
    ts = (now - datetime.timedelta(seconds=i) for i in range(int(n)))
    env = Environment(
        loader=PackageLoader("cybele", "templates"))
    tmplt = env.get_template("ipsumlog.j2")
    rv = StringIO(tmplt.render(ts=ts))
    rv.name = name
    return rv


class SummaryTests(unittest.TestCase):

    def test_generation_of_log(self):
        log = ipsum_log("hundred", 100)
        self.failUnlessEqual("hundred", log.name)
        self.failUnlessEqual(100, len(log.readlines()))

    def test_summary(self):
        log = ipsum_log("1K_log", 1024)
        rv = summarize(log)
        self.assertEqual("1K_log", rv.name)
        self.assertEqual(4, len(rv.tail))
        self.assertEqual(log.getvalue().splitlines()[-4:], rv.tail)

class SerializerTests(unittest.TestCase):

    def test_string_content(self):
        log = ipsum_log("1K_log", 1024)
        s = summarize(log)
        txt = summary2text(s)
        self.assertIn("name: 1K_log", txt)
        self.assertIn("lines: 1024", txt)
        self.assertIn('\n'.join(s.tail), txt)

    def test_round_trip(self):
        log = ipsum_log("1K_log", 1024)
        s = summarize(log)
        self.assertEqual(s, text2summary(summary2text(s)))

class DeliveryTests(functest.TestCase):

    def test_summary_delivery(self):
        log = ipsum_log(None, 1024)
        with tempfile.NamedTemporaryFile() as fakeLog:
            fakeLog.write(log.getvalue())
            fakeLog.flush()

            with tempfile.NamedTemporaryFile() as dst:
                put_summary(fakeLog.name, dst.name)

                content = dst.read()
                smry = text2summary(content)
                self.assertEqual(fakeLog.name, smry.name)
                self.assertEqual(1024, smry.lines)

    def test_channel_naming(self):
        locn = tempfile.mkdtemp()
        try:
            for i in range(32):
                tempfile.mkstemp(suffix=suffix(i), dir=locn)
                self.assertEqual(range(i+1), get_channels(locn))
            for n, fP in enumerate(os.listdir(locn)):
                os.remove(os.path.join(locn, fP))
                self.assertEqual(31-n, len(get_channels(locn)))
        finally:
            shutil.rmtree(locn)

    def test_channel_history(self):
        locn = tempfile.mkdtemp()
        try:
            for i in range(32):
                tempfile.mkstemp(suffix=suffix(0), dir=locn)
                self.assertEqual(range(i+1), get_channels(locn))
            for n, fP in enumerate(os.listdir(locn)):
                os.remove(os.path.join(locn, fP))
                self.assertEqual(31-n, len(get_channels(locn)))
        finally:
            shutil.rmtree(locn)

class UtilityTests(unittest.TestCase):

    def test_zero_packing_of_suffixes(self):
        self.assertEqual("-00.dat", suffix(0))
        self.assertEqual("-09.dat", suffix(9))
        self.assertEqual("-10.dat", suffix(10))

@functest.skip("Require test data files")
class TimingTests(functest.TestCase):

    def test_round_robin(self):
        """
        Not worth running; takes longer to generate data
        than to summarize it. Keeping here for when we
        have test data in static files.
        """
        
        def build_biglog():
            globals()["bigLog"] = ipsum_log("bigLog", 1E6)

        def summarize_biglog():
            summarize(bigLog)

        t = timeit.timeit(summarize_biglog, build_biglog)
        print(t)

if __name__ == "__main__":
    functest.main()
