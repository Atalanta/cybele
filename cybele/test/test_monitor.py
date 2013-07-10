#!/usr/bin/env python2.7
# encoding: UTF-8

import unittest as functest

from jinja2 import Environment, PackageLoader

class SummaryTests(functest.TestCase):

    def test_001(self):
        env = Environment(
            loader=PackageLoader("cybele", "templates"))
        print(env.get_template("ipsumlog.j2"))

if __name__ == "__main__":
    functest.main()
