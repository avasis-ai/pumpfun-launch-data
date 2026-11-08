#!/usr/bin/env python3
"""Reproduce the headline numbers from the free pump.fun launch sample (standard library only).

    python3 stats.py [pumpfun-launch-sample-20261030-20261105.csv.gz]
"""
import csv
import datetime as dt
import gzip
import hashlib
import statistics
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "pumpfun-launch-sample-20261030-20261105.csv.gz"
rows = list(csv.DictReader(gzip.open(path, "rt", encoding="utf-8")))
tape = [r for r in rows if r["verdict_basis"] != "no_tape_features"]


def num(r, k):
    try:
        return float(r[k])
    except ValueError:
        return None


def share(rs, k, test):
    vals = [v for v in (num(r, k) for r in rs) if v is not None]
    return sum(1 for v in vals if test(v)), len(vals)


def pct(a, b, d=1):
    return f"{100.0 * a / b:.{d}f}%" if b else "n/a"


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


# the sample is deterministic: every row satisfies the published 1-in-32 rule
bad = [r["mint"] for r in rows if int(hashlib.md5(r["mint"].encode()).hexdigest()[:8], 16) % 32 != 0]

a, n = share(tape, "early_1s_buyers", lambda v: v >= 1)
b, m = share(tape, "serial_snipers", lambda v: v >= 1)
clones = sum(1 for r in rows if any((num(r, k) or 0) >= 1 for k in ("name_collisions_7d", "symbol_collisions_7d", "image_collisions")))
grads = [r for r in rows if r["graduated_at"]]
secs = [(ts(r["graduated_at"]) - ts(r["created_at"])).total_seconds() for r in grads]
verdicts = {k: sum(1 for r in rows if r["verdict"] == k) for k in ("SAFE", "WARN", "DANGER")}

print(f"rows: {len(rows):,} launches (1 in 32 of all pump.fun launches, 30 Oct-5 Nov 2026 UTC); {len(tape):,} with launch-tape features")
print(f"sampling rule holds for every row: {not bad}")
print(f"a buyer within 1 second of the mint: {pct(a, n)} of {n:,} launches with tape")
print(f"at least one serial sniper among the first buyers: {pct(b, m)} of {m:,}")
print(f"name, symbol or image reused within 7 days: {pct(clones, len(rows))}")
print(f"graduated from the bonding curve: {len(grads)} ({pct(len(grads), len(rows), 2)}); median time to graduate {statistics.median(secs):.1f} s")
print("verdicts: " + ", ".join(f"{k} {v:,} ({pct(v, len(rows))})" for k, v in verdicts.items()))
