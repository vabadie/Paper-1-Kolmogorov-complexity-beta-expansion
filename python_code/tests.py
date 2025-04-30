import numpy as np
from itertools import product


beta = 1.6

n = 4

binary_seqs = product([0,1], repeat = n)

def delta(seq,beta = 2):
    m = len(seq)
    betas = beta**(-np.arange(1,n+1))
    return np.sum(np.array(seq)*betas)

for seq in binary_seqs:
    print(delta(seq, beta=beta))

print(1.6**(-4))