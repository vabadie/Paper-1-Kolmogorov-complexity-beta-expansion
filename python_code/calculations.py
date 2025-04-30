from mpmath import mp
# from tqdm import tqdm
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import statistics

mp.dps = 500

n_numbers = 1000
n_tree = 500
# s = mp.mpf(0.5)
#beta = mp.mpf((1+mp.sqrt(5))/2)
beta = 1.61
epsilon = mp.mpf(2**(-10))
threshold = mp.mpf(0.67)

alpha = np.log(2/beta)/np.log(1+(2-beta)/(2*beta*(beta-1)))

print(alpha)