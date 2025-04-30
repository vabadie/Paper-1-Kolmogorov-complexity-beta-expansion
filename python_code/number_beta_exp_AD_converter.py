from mpmath import mp
# from tqdm import tqdm
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import statistics

mp.dps = 500

n_numbers = 1000
n_tree = 100
# s = mp.mpf(0.5)
#beta = mp.mpf((1+mp.sqrt(5))/2)
beta = 3/2
epsilon = (2-beta)/(beta*(beta-1))#mp.mpf(2**(-10))
threshold = 1/beta

def R(s):
    if s < threshold:
        return (beta*s,beta*s)
    if s >= threshold and s < threshold + epsilon:
        return (beta*s, beta*s-1)
    else:
        return (beta*s-1, beta*s-1)



class TreeNode:
    def __init__(self, value, depth=0):
        self.value = value
        self.children = []
        self.parent = None  # Track parent node
        self.depth = depth  # Track depth in the tree

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

class Tree:
    def __init__(self, root_value, R):
        self.root = TreeNode(root_value)
        self.R = R

    def get_leaves(self):
        leaves = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if not node.children:
                leaves.append(node)
            else:
                queue.extend(node.children)
        return leaves

    def grow(self):
        leaves = self.get_leaves()
        for leaf in leaves:
            o1, o2 = self.R(leaf.value)
            if o1 == o2:
                leaf.add_child(TreeNode(o1, leaf.depth + 1))
            else:
                leaf.add_child(TreeNode(o1, leaf.depth + 1))
                leaf.add_child(TreeNode(o2, leaf.depth + 1))

    def get_generating_nodes(self, node):
        generating_nodes = []
        while node.parent:
            if len(node.parent.children) == 2:
                generating_nodes.append(node.parent)
            node = node.parent
        return generating_nodes

    def display(self):
        G = nx.DiGraph()
        labels = {}
        queue = deque([(self.root, None)])
        positions = {}  # To store positions for layering
        layer_nodes = {}  # Group nodes by depth

        while queue:
            node, parent = queue.popleft()
            node_label = mp.nstr(node.value, 2)
            labels[node] = node_label
            
            if parent:
                G.add_edge(parent, node)
            
            # Store nodes by depth
            if node.depth not in layer_nodes:
                layer_nodes[node.depth] = []
            layer_nodes[node.depth].append(node)
            
            for child in node.children:
                queue.append((child, node))
        
        # Assign positions for layered layout
        y_spacing = 1  # Adjust vertical spacing
        for depth, nodes in layer_nodes.items():
            x_spacing = 2  # Adjust horizontal spacing
            for i, node in enumerate(nodes):
                positions[node] = (i * x_spacing - len(nodes) * x_spacing / 2, -depth * y_spacing)
        
        plt.figure(figsize=(10, 6))
        nx.draw(G, pos=positions, labels=labels, with_labels=True, node_size=300, node_color='lightblue', edge_color='gray')
        plt.show()

# Example function R(s)
# def R(s):
#     return (s / 2, s / 3)

# Initialize and grow the tree

# n_leaves_per_number = []
# numbers = np.linspace(0,1,n_numbers)
# for precision
# for s in numbers:
#     t = mp.mpf(s)
#     tree = Tree(t, R)
#     n_leaves = []
#     for _ in range(n_tree):  # Grow for 4 steps
#         n_leaves.append(len(tree.get_leaves()))
#         tree.grow()
#     # plt.plot(np.arange(n_tree), n_leaves)
#     n_leaves_per_number.append(n_leaves[-1])

# print(numbers[np.argmax(n_leaves_per_number)])

#s = 0.6756756756756757
s = mp.mpf('0.6600000000001')
#s = 0.5
n_leaves_per_number = []
median_number_of_bifurcations = []
precisions = np.logspace(-13, -6, 100, base =2)
for i, precision in enumerate(precisions):

    print(i)

    def R(s):
        if s < threshold:
            return (beta*s,beta*s)
        if s >= threshold and s < threshold + precision:
            return (beta*s, beta*s-1)
        else:
            return (beta*s-1, beta*s-1)

    t = mp.mpf(s)
    tree = Tree(t, R)
    n_leaves = []
    for _ in range(n_tree):  # Grow for 4 steps
        n_leaves.append(len(tree.get_leaves()))
        tree.grow()
    #plt.plot(np.arange(n_tree), n_leaves)
    n_leaves_per_number.append(n_leaves[-1])
    # number_of_bifurcations = []
    # for leaf in tree.get_leaves():
    #     number_of_bifurcations.append(len(tree.get_generating_nodes(leaf)))
    
    # median_number_of_bifurcations.append(statistics.median(number_of_bifurcations))

#print(number_of_bifurcations)
# tree.display()
precs = []
nlfs = []
for i,n in enumerate(n_leaves_per_number):
    if n > 1:
        precs.append(precisions[i])
        nlfs.append(n)

precs = np.array(precs)
nlfs = np.array(nlfs)
slope, intercept = np.polyfit(np.log(1+precs), np.log(nlfs), 1)
print(slope, intercept, slope/n_tree)

y = np.exp(intercept)*np.exp(slope*np.log(1+precs))

# precision = 
plt.plot(precs, nlfs)
plt.plot(precs,y)
# plt.show()

# plt.hist(number_of_bifurcations, bins=5, density=True, alpha=0.7, color='blue', edgecolor='black')

# plt.plot(precisions, median_number_of_bifurcations)
plt.xscale('log')
plt.yscale('log')

plt.show()

