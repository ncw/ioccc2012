#!/usr/bin/python
"""
Explore FFT sizes to make sure we aren't overflowing
"""

P = 0xFFFFFFFF00000001L

def fft_ok(log_n, p, verbose=True):
    """
    The best possible estimate as to whether an FFT size will overflow
    """
    n = 1 << log_n
    smaller_digit_width = p // n
    bigger_digit_width = smaller_digit_width + 1
    bigger_digits = p - n * smaller_digit_width
    assert bigger_digits < n and bigger_digits >= 0
    smaller_digits = n - bigger_digits
    assert smaller_digits * smaller_digit_width + bigger_digits * bigger_digit_width == p
    if verbose:
        print "log_n=%s, n=%s, smaller_digit_width=%s, bigger_digits=%s, smaller_digits=%s" % (log_n, n, smaller_digit_width, bigger_digits, smaller_digits)
    bigger_digit_max = (1 << bigger_digit_width) -1
    smaller_digit_max = (1 << smaller_digit_width) -1
    max_value_after_convolution = bigger_digit_max**2 * bigger_digits + smaller_digit_max ** 2 * smaller_digits
    ok = max_value_after_convolution < P
    if verbose:
        print "Max value after convolution %X - ok %s" % (max_value_after_convolution, ok)
        print "Currently", 2*bigger_digit_width + log_n < 63
    return ok

def fft_ok_conservative(log_n, p, verbose=True):
    """
    The crude estimate we are using at the moment
    """
    n = 1 << log_n
    smaller_digit_width = p // n
    bigger_digit_width = smaller_digit_width + 1
    ok = (2*bigger_digit_width + log_n < 63)
    if verbose:
        print "log_n=%s, n=%s, smaller_digit_width=%s" % (log_n, n, smaller_digit_width, ok)
    return ok

def fft_ok_better(log_n, p, verbose=True):
    """
    The crude estimate we are using at the moment
    """
    n = 1 << log_n
    smaller_digit_width = p // n
    bigger_digit_width = smaller_digit_width + 1
    ok = (2*smaller_digit_width + log_n < 63)
    if verbose:
        print "log_n=%s, n=%s, smaller_digit_width=%s" % (log_n, n, smaller_digit_width, ok)
    return ok

def bisect(fft_ok_fn, log_n):
    """
    Finds the biggest p for which log_n is OK according to fft_ok_fn
    """
    ok = 1
    assert fft_ok_fn(log_n, ok, verbose=False)
    not_ok = ok*2
    # Find highest point
    while True:
        if not fft_ok_fn(log_n, not_ok, verbose=False):
            break
        not_ok *= 2
    while ok != not_ok -1:
        mid = (ok + not_ok) // 2
        if fft_ok_fn(log_n, mid, verbose=False):
            ok = mid
        else:
            not_ok = mid
        #print ok, mid, not_ok
    assert fft_ok_fn(log_n, ok, verbose=False)
    assert not fft_ok_fn(log_n, ok+1, verbose=False)
    return ok

def main():
    print "FFT size and maximum p to check with it using 3 different limit calculations"
    print "tight, conservative and better"
    print "log_n, tight, conservative,      %,     better,      %"
    for log_n in range(2,28):
        tight = bisect(fft_ok, log_n)
        conservative = bisect(fft_ok_conservative, log_n)
        better = bisect(fft_ok_better, log_n)
        assert conservative <= tight
        assert better <= tight
        print "%2d, %10d, %10d, %5.2f%%, %10d, %5.2f%%" % (log_n, tight,
                                                           conservative, (float(tight)/conservative-1)*100, 
                                                           better, (float(tight)/better-1)*100)

if __name__ == "__main__":
    main()

