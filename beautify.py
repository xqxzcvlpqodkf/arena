#!/usr/bin/env python3
"""Minimal Lua/Luau tokenizer + pretty-printer for minified sources."""
import re, sys

TOKEN_RE = re.compile(r"""
    (?P<lcomment>\-\-\[\[(?:.|\n)*?\]\]|\-\-\[=*\[(?:.|\n)*?\]=*\])
  | (?P<comment>\-\-[^\n]*)
  | (?P<lstring>\[(?:=*)\[(?:.|\n)*?\]\1\])
  | (?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<number>0[xX][0-9a-fA-F]+|\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)
  | (?P<name>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<op>\.\.\.|\.\.|==|~=|<=|>=|::|//|<<|>>|[+\-*/%^#<>=(){}\[\];:,.])
  | (?P<ws>\s+)
""", re.VERBOSE)

def tokenize(src):
    toks = []
    i = 0
    n = len(src)
    while i < n:
        m = TOKEN_RE.match(src, i)
        if not m:
            raise SystemExit(f"tokenize error at offset {i}: {src[i:i+40]!r}")
        i = m.end()
        kind = m.lastgroup
        if kind == 'ws':
            continue
        toks.append((kind, m.group()))
    return toks

OPENERS = {'function', 'do', 'repeat'}
CLOSERS = {'end', 'until'}

def beautify(src):
    toks = tokenize(src)
    out = []
    depth = 0
    i = 0
    prev_sig = ''  # previous significant token text
    line = []
    def newline():
        nonlocal line
        if line:
            out.append('  ' * depth + ' '.join(line))
            line = []
    while i < len(toks):
        kind, tok = toks[i]
        if tok == 'then':
            # opener unless preceded by elseif
            line.append(tok)
            if prev_sig != 'elseif':
                depth += 1
                newline()
            else:
                newline()
        elif tok in OPENERS:
            # 'function' opens body; 'do' opens; 'repeat' opens
            line.append(tok)
            depth += 1
            # if 'function', everything until ')' stays on this line; newline after ')'
            if tok == 'function':
                # find the closing ')' of params (function name parts may precede)
                j = i + 1
                # skip name parts and . / :
                saw_paren = False
                while j < len(toks):
                    k2, t2 = toks[j]
                    if t2 == '(':
                        saw_paren = True
                    if saw_paren and t2 == ')':
                        break
                    if not saw_paren and k2 == 'name':
                        j += 1
                        continue
                    if not saw_paren and t2 in ('.', ':'):
                        j += 1
                        continue
                    if saw_paren and k2 in ('name', 'op', 'string', 'number'):
                        j += 1
                        continue
                    j += 1
                # emit tokens up to j inclusive on this line
                while i < j:
                    i += 1
                    k2, t2 = toks[i]
                    line.append(t2)
                newline()
            else:
                newline()
        elif tok in CLOSERS:
            newline()
            depth -= 1
            line.append(tok)
            # lookahead: if next sig token is ;, ), ,, or closers chain, keep on line
            j = i + 1
            nxt = toks[j][1] if j < len(toks) else ''
            if nxt in (';', ')', '}', ',', 'end', 'until', 'else', 'elseif'):
                pass  # keep line open; loop continues appending
            else:
                newline()
        elif tok == ';':
            line.append(tok)
            newline()
        elif tok in ('else', 'elseif'):
            newline()
            line.append(tok)
        else:
            line.append(tok)
        if tok not in (';',):
            prev_sig = tok
        i += 1
    newline()
    return '\n'.join(out)

if __name__ == '__main__':
    src = open(sys.argv[1], 'r', encoding='utf-8', errors='replace').read()
    open(sys.argv[2], 'w', encoding='utf-8').write(beautify(src))
    print("done")
