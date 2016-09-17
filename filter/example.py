#!/usr/bin/env python

"""
Defines custom syntax for creating examples in LaTeX using the paracol package.

Syntax is as follows:

    Example 1
    Q: The question to solve.
    A: `Note for right column`.
       $Line of working/maths for left column$.
       -> Final answer.

"""

from pandocfilters import toJSONFilter, Str, Para, RawBlock, DefinitionList
from itertools import groupby


def markup(value):
    if value['t'] == "Strong":
        s = '\\textbf{'
    elif value['t'] == "Emph":
        s = '\\textit{'
    elif value['t'] == "Code":
        s = '{\\textcolor{Gray}{' + value['c'][1] + '}}'
        return s

    for val in value['c']:
        if val['t'] == 'Space':
            s += " "
        else:
            s += val['c']
    s += '}'
    return s.strip()


def math(value):
    for val in value['c']:
        if isinstance(val, dict):
            if val['t'] == "DisplayMath":
                mode = "display"
            else:
                mode = "inline"
    for val in value['c']:
        if not isinstance(val, dict):
            if mode == "inline":
                return "$" + val + "$"
            elif mode == "display":
                return "$$" + val + "$$"


def formattext(value):
    con = ""
    for val in value:
        if val['t'] == 'Space':
            con += " "
        elif val['t'] in ['Strong', 'Emph', 'Code']:
            con += markup(val)
        elif val['t'] == 'Math':
            con += math(val)
        else:
            try:
                con += val['c']
            except TypeError:
                pass
    return con.strip()


def answer(line):
    return "\\\\ $\\rightarrow$ \\textbf{" + line + "}\\\\"

def lines(working, key='.'):
    l = []
    for k, g in groupby(working, lambda x: x == Str(key)):
        if not k:
            l.append(list(g))
    return l

def example(value):
    header = "\\textbf{Example " + value[2]['c'] + "} "
    question = "\\textit{"
    question += formattext(value[value.index(Str("Q:")) + 1:value.index(Str("A:"))])
    question += "}\\\\"

    working = lines(value[value.index(Str("A:")) + 1:])
    workstring = ""
    for line in working:
        s = formattext(line)
        if line[-1]['t'] == 'Code':
            workstring += '\\switchcolumn*'
            workstring += s
            workstring += '\\switchcolumn'
        elif s[:2] == "->":
            workstring += answer(s[2:])
        else:
            workstring += " " + s + "\\\\ "

    return RawBlock("latex",
                    header
                    + question
                    + '\\begin{paracol}{2}'
                    + workstring
                    + '\\end{paracol}')

def replace(key, value, format, meta):
    if key == 'Para':
        if value[0] == Str("Example") and Str("Q:") in value:
            return example(value)

if __name__ == "__main__":
    toJSONFilter(replace)
