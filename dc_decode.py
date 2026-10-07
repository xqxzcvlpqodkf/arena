#!/usr/bin/env python3
"""Static implementation of the wYnFuscate `dC` string decoder found in the wrapper head."""

import re
from pathlib import Path


def read_source(path: Path) -> str:
    return path.read_text(encoding='utf-8')


_default_source = Path(__file__).resolve().with_name('message.txt')
SRC = read_source(_default_source)

def unescape(s):
    out = bytearray()
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            c = s[i+1]
            if c.isdigit():
                j = i + 1
                num = ''
                while j < len(s) and s[j].isdigit() and len(num) < 3:
                    num += s[j]; j += 1
                out.append(int(num) & 0xFF)
                i = j
                continue
            elif c == 'n': out.append(10); i += 2; continue
            elif c == 't': out.append(9); i += 2; continue
            elif c == 'r': out.append(13); i += 2; continue
            elif c == '"': out.append(34); i += 2; continue
            elif c == "'": out.append(39); i += 2; continue
            elif c == '\\': out.append(92); i += 2; continue
            else: out.append(ord(c)); i += 2; continue
        else:
            out.append(ord(s[i]) & 0xFF)
            i += 1
    return bytes(out)

m = re.search(r'local dx="((?:\\.|[^"\\])*)"', SRC)
assert m, "dx not found"
dx = unescape(m.group(1))
print("dx length:", len(dx))

D0 = 2147483647
dr = ((106*1957 + 69*9936 - 874931) % 4294967296) % D0
print("dr0 =", dr)

def dC(bP, dr=dr, dx=dx):
    bD = 1
    bY = dr
    bJ = 48271
    bn = 81
    bU = 256
    bF = 1
    while bF <= bP:
        bq = dx[bD-1]
        bL = bq ^ (bY % bU)
        bY = (bY * bJ + bn) % D0
        bW = bL
        while bW > 0:
            bY = (bY * bJ + bn) % D0
            bW -= 1
        bD = bD + 1 + bL
        bF += 1
    bq = dx[bD-1]
    bL = bq ^ (bY % bU)
    bY = (bY * bJ + bn) % D0
    out = []
    bc = 1
    while bc <= bL:
        bq = dx[bD-1 + bc]
        out.append(chr((bq ^ (bY % bU)) & 0xFF))
        bY = (bY * bJ + bn) % D0
        bc += 1
    return ''.join(out)

if __name__ == '__main__':
    names = {}
    for n in range(0, 90):
        try:
            names[n] = dC(n)
        except Exception as e:
            names[n] = f"<err {e}>"
    for n in sorted(names):
        print(f"dC({n:3d}) = {names[n]!r}")
