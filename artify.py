#!/usr/bin/python
"""
Take the C program and the image file on the command line and attempt
to create an ascii art C program from the two!

FIXME remove spaces at end of line
"""

import sys
import Image
import re

threshold = 160

tokens = ('+=', '-=', '++','>=','<=','==','<<','>>','!=')

def get_dark_pixel(line):
    """
    Gets a dark pixel to plot off the line, returning the pixel and the new line

    The pixel may be more than one character long
    """
    for token in tokens:
        if line.startswith(token):
            return token, line[len(token):]
    m = re.search(r'''^(".*?")(.*$)''', line)
    if m:
        return m.groups()
    if re.search(r"^[^a-zA-Z0-9_]", line):
        return line[0], line[1:]
    m = re.search(r"^([a-zA-Z0-9_]+)(.*$)", line)
    return m.groups()

def get_light_pixel(line):
    """
    Returns whitespace off the line or a space
    """
    if line[0] == " ":
        return line[0], line[1:]
    return " ", line
    
def plot(im, line):
    w, h = im.size
    for y in xrange(h):
        out = ""
        skip = 0
        for x in xrange(w):
            if skip > 0:
                skip -= 1
                continue
            pixel = im.getpixel((x, y))
            if pixel < threshold:
                pixel, line = get_dark_pixel(line)
            else:
                pixel, line = get_light_pixel(line)
            out += pixel
            skip = len(pixel)-1
            if not line:
                break
        print out.rstrip()
        if not line:
            break
    if line:
        print line
    # FIXME dither the missing

def process(im, program):
    for line in program.split("\n"):
        if line.startswith("#"):
            print line
        else:
            plot(im, line)

def main():
    if len(sys.argv) != 3:
        raise ValueError("Syntax: program.c image")
    _, program_filename, image_filename = sys.argv
    program = open(program_filename).read()
    im = Image.open(image_filename)
    w, h = im.size
    new_w = 68
    new_h = int(h*float(new_w)/w/3)
    im = im.resize((new_w, new_h), Image.ANTIALIAS)    # best down-sizing filter
    #im.show()
    process(im, program)

if __name__ == "__main__":
    main()
