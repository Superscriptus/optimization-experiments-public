"""
Simple script used to estimate the runtime of ExhaustiveGreedy for different filter sizes (wc).

I was originally running this with _mult=0.1 as the algorithm seemed to be taking about 0.1 seconds
on average to assign hard skills for a given team. However, it looks like this is an underestimate for
larger values of wc (perhaps ~0.15 is better?).
"""
import sys
from itertools import combinations
_wc = int(sys.argv[1])
_mult = float(sys.argv[2])
_denom = int(sys.argv[3])


def calc(wc=_wc, denom=_denom, mult=_mult):

    x = 0
    for ts in [3, 4, 5, 6, 7]:
        x += len(list(combinations(range(wc), ts)))

    return mult * x / denom


if __name__ == '__main__':
    print(calc())
