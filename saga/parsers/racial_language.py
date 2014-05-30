import codecs
import re
from itertools import count
import json

def parse_line(st):
    res = _tag_re.search(st)
    if res:
        k = res.groups()[0]
        items = k.split(':')
    else:
        items = []

    return items

_tag_re = re.compile("\[(.*)\]")

accent_map = {
    'à': 'a',
    'á': 'a',
    'â': 'a',
    'ä': 'a',
    'å': 'a',
    'è': 'e',
    'é': 'e',
    'ê': 'e',
    'ë': 'e',
    'ì': 'i',
    'í': 'i',
    'î': 'i',
    'ï': 'i',
    'ñ': 'n',
    'ò': 'o',
    'ó': 'o',
    'ô': 'o',
    'ö': 'o',
    'ù': 'u',
    'ú': 'u',
    'û': 'u',
    'ÿ': 'y',
    'ç': 'c'
}

def process_file(filename):
    with codecs.open(filename, 'r', 'cp437') as inf:
        data = inf.readlines()

    data_generator = ((c, x.strip()) for c, x in zip(count(), data[1:]))

    words = []
    for lineno, line in data_generator:
        if line == "":
            pass
        else:
            t = parse_line(line)

            if len(t) == 0:
                continue

            if t[0] == 'T_WORD':
                words.append((t[1].lower(), t[2]))


    plain_letters = [chr(x) for x in range(65, 91)] + [chr(x) for x in range(97, 123)]
    words = sorted(words, key=lambda x: x[0])
    t = []
    accents = set()
    for english, dwarvish in words:
        w = []
        for char in dwarvish:
            if char not in plain_letters:
                try:
                    w.append(accent_map[char])
                except KeyError:
                    accents.add(char)

            else:
                w.append(char)
        t.append((english, dwarvish, "".join(w)))

    if len(accents) > 0:
        raise ValueError("Found unknown accents, '{}'".format("".join(x for x in accents)))

    return t


