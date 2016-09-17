#!/usr/bin/env python

"""
Convert all uppercase words to small caps.
"""

from pandocfilters import toJSONFilter, SmallCaps, Str

def small_caps(key, value, format, meta):
    if key == 'Str':
        if value.isupper():
            return SmallCaps([Str(value.lower())])

if __name__ == "__main__":
    toJSONFilter(small_caps)