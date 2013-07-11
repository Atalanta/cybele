#!/usr/bin/env python2.7
# encoding: UTF-8

from collections import namedtuple
from email import message_from_string
from email.mime.text import MIMEText
import glob
import os.path

Summary = namedtuple("Summary", ["name", "lines", "tail"])


def put_summary(src, dst):
    with open(src, 'r') as log:
        with open(dst, 'w') as out:
            out.write(summary2text(summarize(log)))
            out.flush()

def summarize(fObj):
    entries = [i.strip() for i in fObj.readlines()]
    return Summary(fObj.name, len(entries), entries[-4:])

def summary2text(smry):
    msg = MIMEText('\n'.join(smry.tail))
    msg["name"] = smry.name
    msg["lines"] = str(smry.lines)
    return msg.as_string()

def text2summary(txt):
    msg = message_from_string(txt)
    name = msg["name"]
    lines = int(msg["lines"])
    return Summary(name, lines, msg.get_payload().splitlines()) 

def history(locn, chan):
    """List summary files for this channel, newest first"""
    pass

def suffix(chan):
    return "-{:02}.dat".format(chan)

def get_channels(locn):
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
