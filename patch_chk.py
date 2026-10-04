#!/usr/bin/env python3
"""Instrument the delegate checker body (T4[dn[39166]])."""
src = open('build_run.py').read()

N1 = "local Pf = T4 [ dQ [ 65050 ] ] local Pt = T4 [ dQ [ 47823 ] ] if not Pt and Pf then"
P1 = ("local Pf = T4 [ dQ [ 65050 ] ] local Pt = T4 [ dQ [ 47823 ] ] "
      "__print([[CHK-Pt]] , tostring ( Pt ) , [[Pf=]] , tostring ( Pf )) if not Pt and Pf then")
N2 = "local Ph = T4 [ dQ [ 28686 ] ] if not Ph and Pf then"
P2 = ("__print([[CHK-PR]] , [[PR=]] , tostring ( PR ) , [[PD=]] , tostring ( PD ) , "
      "[[Pd=]] , tostring ( Pd ) , [[Pb=]] , tostring ( Pb ) , [[PP=]] , tostring ( PP ) ) "
      "local Ph = T4 [ dQ [ 28686 ] ] if not Ph and Pf then")

block = '\n'.join([
    "# 21. instrument delegate checker body",
    "assert payload.count(" + repr(N1) + ") == 1",
    "payload = payload.replace(" + repr(N1) + ", " + repr(P1) + ", 1)",
    "assert payload.count(" + repr(N2) + ") == 1, 'N2 hits %d' % payload.count(" + repr(N2) + ")",
    "payload = payload.replace(" + repr(N2) + ", " + repr(P2) + ", 1)",
    "inj.append('chk-body')",
    "",
]) + '\n'
if 'chk-body' not in src:
    src = src.replace("# 10. THE BIG ONE", block + "# 10. THE BIG ONE")
    open('build_run.py', 'w').write(src)
    print("patched")
else:
    print("already")
