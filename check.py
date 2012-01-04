#!/usr/bin/python
"""
Check to see if this program is a valid program for the iocc

    2) The size of your program source must be <= 4096 bytes in length.
       The number of characters excluding whitespace (tab, space,
       newline, formfeed, return), and excluding any ; { or } immediately
       followed by whitespace or end of file, must be <= 2048.
"""

import re
import sys

def check_size(txt):
    size = len(txt)
    if size <= 4096:
        status = "OK"
    else:
        status = "BAD"
    print "Total size %d: %s" % (size, status)

def check_whitespace(txt):
    txt = re.sub(r"\s+", r"", txt)
    size = len(txt)
    if size <= 2048:
        status = "OK"
    else:
        status = "BAD"
    print "Non whitespace %d: %s" % (size, status)

def check_rules_whitespace(txt):
    txt = re.sub("(?s)[;{}](\s|$)", r"\1", txt)
    txt = re.sub(r"\s+", r"", txt)
    size = len(txt)
    if size <= 2048:
        status = "OK"
    else:
        status = "BAD"
    print "Rules whitespace %d: %s" % (size, status)

def main():
    if len(sys.argv) != 2:
        print "Syntax: %s file.c" % sys.argv[0]
        raise SystemExit(1)
    _, in_filename = sys.argv
    txt = open(in_filename).read()
    print len(in_filename)*"-"
    print in_filename
    print len(in_filename)*"-"
    check_size(txt)
    check_whitespace(txt)
    print len(in_filename)*"-"
    #check_rules_whitespace(txt)
    
if __name__ == "__main__":
    main()
