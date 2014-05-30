__author__ = 'DocHoncho'

import sys
from itertools import count

fn_in = sys.argv[1]
fn_out = sys.argv[2] if sys.argv[2] else sys.stdout

bad_chars=['\xae', '\xaf', '\r']
bff = " "*10

with open(fn_out, 'w') as outf:

    out_buffer = []

    with open(fn_in, 'r', encoding="cp437") as inf:
        for n, line in zip(count(), inf):
            print("\r%s"%(n), end='')

            for c in line:
                if c in bad_chars:
                    print("BAM!")
                    continue
                outf.write(c)
