#!/usr/bin/python
"""
Mangle the C code passed in
"""
import re
import sys

# Message in #defines
#       12345678901
defines_message="HUNTPRIMES"

def decomment(txt):
    """Remove comments"""
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    txt = re.sub(r"//.*?$", "", txt, flags=re.M)
    txt = re.sub(r"[ \t]+", r" ", txt, flags=re.S);
    txt = re.sub(r"\n+", r"\n", txt, flags=re.S);
    txt = re.sub(r"^\s+", r"", txt, flags=re.M);
    return txt

defines = (
    ('VOID', 'void'),
    ('INT ', 'int '),
    ('CALLOC_N', 'calloc(n,sizeof(u64))'),
    ('RETURN', 'return'),
    ('FOR ', 'for ('),
    ('IF ', 'if ('),
    ('SHR32', '>>32'),
    ('FLOOPOVERN', "i = 0; i < n; i++)"),
#    ('XOFI', 'x[i]'),
)

# Map single letters to symbols for #define message
defines_message_symbols = {}
for symbol, letter in zip((('u32',),('u64',))+defines, defines_message):
    defines_message_symbols[symbol[0].strip()] = letter

def splitdefines(txt):
    """split the code into two lists of defines and code"""
    pre = []
    c = []
    for line in txt.split("\n"):
        if line.startswith("#"):
            pre.append(line)
        else:
            c.append(line)
    return pre, c

def quotemeta(text):
    """
    Quotes all the meta characters in the text
    """
    return re.sub("(\W)", r"\\\1", text)

def redefine(txt):
    """
    Substitude the defines in
    """
    pre, c = splitdefines(txt)
    txt = "\n".join(c)
    for new, old in defines:
        #txt = re.sub(r"(?s)([^a-zA-Z]|\n)"+quotemeta(old)+r"([^a-zA-Z]|\n)", r"\1"+new+r"\2", txt)
        txt = txt.replace(old, new)
        old = old.replace(" ","")
        pre.append("#define %s %s" % (new, old))
    pre = "\n".join(pre)
    return pre + "\n" + txt

def despace(txt):
    """Remove as much white space as possible"""
    pre, c = splitdefines(txt)
    pre = "\n".join(pre)
    txt = " ".join(c)
    txt = txt.replace("\t", " ")
    txt = re.sub(r"\s+", " ", txt, flags=re.S)
    txt = re.sub(r"([a-zA-Z0-9_])\s+([^a-zA-Z0-9_\s])", r"\1\2", txt, flags=re.S)
    txt = re.sub(r"([^a-zA-Z0-9_\s])\s+([a-zA-Z0-9_])", r"\1\2", txt, flags=re.S)
    txt = re.sub(r"([^a-zA-Z0-9_\s])\s+([^a-zA-Z0-9_\s])", r"\1\2", txt, flags=re.S)
    txt = re.sub(r"([^a-zA-Z0-9_\s])\s+([^a-zA-Z0-9_\s])", r"\1\2", txt, flags=re.S)
    return pre + "\n" + txt

renames = [
    'u8',
    'u32',
    'u64',
    'MOD_P',
    'ROOT_ONE',
    'ROOT_TWO',
    'ROOT_ORDER',
    'U64',
    'U32H',
    'U32L',
    'MOD_INVN',
    'MOD_INVW',
    'MOD_N',
    'MOD_W',
    'bit_reverse',
    'data_start',
    'digit_unweight',
    'digit_weight',
    'digit_width_0_max',
    'digit_width0',
    'digit_width1',
    'digit_widths',
    'exponent',
    'fatal',
    'invTwiddle',
    'invFft_fastish',
    'fft_cols',
    'fft_fastish',
    'fft_initialise',
    'log_n',
    'mersenne_initialise',
    'mersenne_residue',
    'mersenne_add32',
    'mersenne_sub32',
    'mersenne_add64',
    'mersenne_mul',
    'mersenne_zero',
    'mod_adc',
    'mod_add',
    'mod_sub',
    'mod_bit',
    'mod_inv',
    'mod_vector_mul',
    'mod_mul',
    'mod_pow',
    'mod_print',
    'mod_reduce',
    'mod_rnd',
    'mod_sqr_vector',
    'mod_string',
    'mod_top_bit',
    'twiddle',
    'carry_bit',
    'addr64',
    'addr32',
    'iterations',
    'sum',
    'root2',
    'inv_c',
    'invK',
    'old_addr',
    'MASK32',
    'ARRAY_SIZE',
    ]
renames.extend(x[0].strip() for x in defines)

import string
alphabet = list('_'+string.uppercase + string.lowercase)
for c in defines_message:
    alphabet.remove(c)
for a in string.uppercase:
    for b in string.uppercase:
        alphabet.append(a+b)

# Remove local variables
for var in ('abcdijkmnorstuvwxyz'):
    alphabet.remove(var)

def rename(txt):
    for a in renames:
        for b in renames:
            if a != b:
                if a in b:
                    print "%r INSIDE %r" % (a,b)
    if len(renames) > len(alphabet):
        raise ValueError("Too many words")
    # sort the list by number of times it appears in the text * the length
    def f(x):
        return txt.count(x) * len(x)
    renames.sort(key=f, reverse=True)
    # FIXME prefixes?
    #print renames
    for word in renames:
        if word in txt:
            if word in defines_message_symbols:
                replacement = defines_message_symbols[word]
            else:
                replacement = alphabet.pop(0)
            txt = re.sub(word, replacement, txt)
    return txt

from collections import defaultdict

def lz77(txt):
    """
    Suggest strings which could be compressed by use of an lz77 algorithm with #define
    """
    txt = txt.split("\n")[-1]
    savings = []
    for w in range(2,20):
        d = defaultdict(int)
        for i in range(len(txt)-w):
            substring = txt[i:i+w]
            d[substring] += 1
        for substring, count in d.iteritems():
            define = "#define X %s" % substring
            saving = count*(len(substring)-1) - len(define)
            savings.append((saving, "Use: %r to save %d bytes (repeated %d times)" % (define, saving, count)))
    savings.sort(reverse=True)
    for _, saving in savings[:10]:
        print saving

def main():
    if len(sys.argv) != 3:
        print "Syntax: %s in.c out.c" % sys.argv[0]
        raise SystemExit(1)
    _, in_filename, out_filename = sys.argv
    txt = open(in_filename).read()
    txt = redefine(txt)
    txt = decomment(txt)
    txt = despace(txt)
    txt = rename(txt)
    txt = txt.replace("@", " ")
    lz77(txt)
    fd = open(out_filename, "w")
    fd.write(txt)
    fd.close()

if __name__ == "__main__":
    main()
