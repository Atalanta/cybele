#!/usr/bin/env python2.7
# encoding: UTF-8

import argparse
import logging
import sys

from cybele.monitor import DFLT_LOCN
from cybele.monitor import get_channels
from cybele.monitor import get_summary

from flask import Flask
from flask import flash
from flask import render_template

__doc__ = """
The `main` module runs as a web service on your local host.
It displays the summaries of monitored files.
"""

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    log = logging.getLogger("cybele.web")
    locn = app.config["input"]
    smrs = [(chan, get_summary(locn, chan)) for chan in get_channels(locn)]
    return render_template("base.html", summaries=smrs)


def main(args):
    app.config.update(vars(args))
    app.run()
    return 1


def parser():
    rv = argparse.ArgumentParser(
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    rv.add_argument(
        "--input", default=DFLT_LOCN,
        help="path to input directory [{}]".format(DFLT_LOCN))
    rv.add_argument(
        "-v", "--verbose", required=False,
        action="store_const", dest="log_level",
        const=logging.DEBUG, default=logging.INFO,
        help="increase the verbosity of output")
    return rv


def run():
    p = parser()
    args = p.parse_args()
    logging.basicConfig(
    format="%(asctime)s %(levelname)-7s %(name)-10s %(message)s")
    root = logging.getLogger("")
    root.setLevel(args.log_level)
    rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()
