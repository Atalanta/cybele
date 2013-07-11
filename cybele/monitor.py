#!/usr/bin/env python2.7
# encoding: UTF-8

from collections import namedtuple
from email import message_from_string
from email.mime.text import MIMEText
import glob
import operator
import os.path

__doc__ = """
The `monitor` module runs as a continuing process which reads a
number of log files. It produces a summary of each and places the
summary in a configured location. To see possible options::

    monitor.py --help

The module also defines two API functions to access the summary
files:

    * get_channels
    * get_summary
"""

Summary = namedtuple("Summary", ["name", "lines", "tail"])


def summary2text(smry):
    """Return a text representation of a Summary object"""
    msg = MIMEText('\n'.join(smry.tail))
    msg["name"] = smry.name
    msg["lines"] = str(smry.lines)
    return msg.as_string()


def text2summary(txt):
    """Return a summary object from its text representation"""
    msg = message_from_string(txt)
    name = msg["name"]
    lines = int(msg["lines"])
    return Summary(name, lines, msg.get_payload().splitlines())


def summarize(fObj):
    """Return a summary object from a log file"""
    entries = [i.strip() for i in fObj.readlines()]
    return Summary(fObj.name, len(entries), entries[-4:])


def put_summary(src, dst):
    """Place at `dst` a text summary of the log file `src`"""
    with open(src, 'r') as log:
        with open(dst, 'w') as out:
            out.write(summary2text(summarize(log)))
            out.flush()


def suffix(chan):
    return "-{:02}.dat".format(chan)


def history(locn, chan):
    """List summary files for this channel, newest first"""
    pttrn = os.path.join(locn, "*{}".format(suffix(chan)))
    stats = [(os.path.getmtime(fP), fP) for fP in glob.glob(pttrn)]
    stats.sort(key=operator.itemgetter(0), reverse=True)
    return [i[1] for i in stats]


def get_channels(locn):
    """
    Return a list of log channels for which there are summary
    files available.
    """
    pttrn = os.path.join(locn, "*-??.dat")
    return sorted({int(i[-6:-4]) for i in glob.glob(pttrn)})


def get_summary(locn, chan):
    """
    Return a summary for channel `chan` from path `locn`.

    Windows 2000 file renaming is not atomic, so we can't
    maintain a single summary file and guarantee it's always
    ready to read.

    Instead, we try to read the newest summary file for the
    channel. If not complete, we move on to the next most
    recent. Finally, we remove files older than the one we
    just successfully read.
    """
    rv = None
    hist = history(locn, chan)
    for n, path in enumerate(hist):
        try:
            with open(path, 'r') as in_:
                rv = text2summary(in_.read())
        except:
            continue
        else:
            for past in hist[n+1:]:
                try:
                    os.remove(past)
                except:
                    continue
    return rv
