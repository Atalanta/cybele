#!/usr/bin/env python2.7
# encoding: UTF-8

from collections import namedtuple
from email import message_from_string
from email.mime.text import MIMEText

Summary = namedtuple("Summary", ["name", "lines", "tail"])


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
