"""
Day 1.

################################################################################
Before you leave, the Elves in accounting just need you to fix your expense
report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then
multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456

In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying
them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum
to 2020; what do you get if you multiply them together?
################################################################################

This is a small (2 element) version of the subset sum problem, which is known
to be NP-complete.
"""
import numpy as np
from itertools import combinations

def findSubsets(X,n,s):
    """
    Find subsets of X, which are size n, which sum to s
    """
    solutions = np.empty((1,n))
    combs = combinations(X,n)

    for comb in combs:
        if np.sum(comb) == s:
            solutions = np.append(solutions,[comb],axis=0)

    return solutions[1:,:]

################################################################################
if __name__ == "__main__":
    X = np.loadtxt('day1.dat')
    ## Part 1
    ssets = findSubsets(X,2,2020)
    # Return the product of the entries
    print(np.prod(ssets,axis=1))

    ## Part 2
    ssets = findSubsets(X,3,2020)
    # Return the product of the entries
    print(np.prod(ssets,axis=1))
