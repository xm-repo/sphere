import math
import numpy as np
from numpy import linalg as LA
import networkx as nx

#import matplotlib.pylab as plt

#from google.colab import files 
#files.upload() 
#files.download("file.txt")

#https://pysathq.github.io/
#!pip install python-sat
import pysat
from pysat.formula import CNF
from pysat.solvers import *

import os
import sys
import random
from zipfile import ZipFile
from tqdm import tqdm_notebook as tqdm
from itertools import combinations, permutations

out_dir = ""

class Utils:
    
    def read_dimacs_graph(file = 'graph.col'):
        
        if not (os.path.exists(file) and os.path.getsize(file) > 0):        
            raise Exception("File " + file + " not found")
        
        nodes = []    
        edges = []
        labels = []
        got_labels = False
        nnodes = nedges = 0
        
        with open(file, 'r') as f:
            for line in f:
                line = [l.strip() for l in line.split(' ')]
                if line[0] == 'c': #comment
                    continue
                elif line[0] == 'p': #problem
                    nnodes = int(line[2])
                    nedges = int(line[3])
                    nodes = list(range(1, nnodes + 1))
                    labels = [0] * nnodes
                elif line[0] == 'e': #edge
                    edges.append((int(line[1]), int(line[2])))
                elif line[0] == 'l':
                    labels[int(line[1]) - 1] = int(line[2])
                    got_labels = True

        if got_labels:        
            nodes = [(n, {'c' : l}) for n, l in zip(nodes, labels)]

        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        return g

    def write_dimacs_graph(file = 'graph.col', g = nx.Graph(), comments = []):
        with open(file, 'w') as f:
            for c in comments:
                f.write("c " + c + "\n")
            f.write("p EDGE {} {}\n".format(g.number_of_nodes(), g.number_of_edges()))
            for u, v in g.edges():
                f.write("e {} {}\n".format(u, v))
            for node in g.nodes():
                if 'c' in g.node[node]:
                    f.write("l {} {}\n".format(node, g.node[node]['c']))

    def draw_with_colors(g = nx.Graph()):
        color_map = []
        for node in g.nodes():
            if 'c' in g.node[node]:
                color_map.append(g.node[node]['c'] * 10)            
        nx.draw(g, pos = nx.spring_layout(g, scale=2), node_color=color_map, with_labels=True, cmap = plt.cm.jet)

    def write_proof(file = "proof.txt", proof = []):
        with open(file, 'w') as f:
            for p in proof:
                f.write("%s\n" % str(p))

    def zip_files(file = "archive.zip", files = []):
        with ZipFile(file, 'w') as archive:
            for f in set(files):                
                if not (os.path.exists(file) and os.path.getsize(file) > 0):        
                    raise Exception("File " + file + " not found")
                archive.write(f)
                
def find_triangle(g = nx.Graph()):
    for a in g:
        for b, c in combinations(g[a], 2):
            if b in g[c]:
                return [a, b, c]
    return []
             
    #return set(frozenset([a, b, c]) for a in g for b, c in combinations(g[a], 2) if b in g[c])


def find_isolates(g = nx.Graph()):
    isolates = []
    for n in g:
        if g.degree(n) == 0:
            isolates.append(n)
    return isolates

class ColMap:
    
    def __init__(self, g = nx.Graph(), ncolors = 40):
        
        self.ncolors = ncolors
        self.cmap = dict()
        self.cunmap = dict()
    
        i = 1
        for node in g.nodes():
            for color in range(1, ncolors + 1):            
                self.cmap[(node, color)] = i
                self.cunmap[i] = (node, color)
                i += 1    

    def enc(self, node, color):
        return self.cmap[(node, color)]

    def dec(self, node_color):
        return self.cunmap[node_color]

class ColSAT:
   
    def __init__(self, g = nx.Graph(), ncolors = 10):
        
        self.ncolors = ncolors
        self.g = g.copy()
        self.cmap = ColMap(g, ncolors)        

    def check_coloring(self):
        for n1, n2 in self.g.edges():
            if 'c' not in self.g.node[n1] or 'c' not in self.g.node[n2]:
                return False
            if self.g.node[n1]['c'] == self.g.node[n2]['c']:
                return False
        return True
    
    def apply_model(self):
        
        check = set()
        for var in self.model[self.model > 0]:        
            node, color = self.cmap.dec(var)
            self.g.node[node]['c'] = color
            if (node, color) in check:
                raise Exception("Two colors for one node???")
            else:
                check.add((node, color))
        
        self.colored = self.check_coloring()
        
        if self.colored != self.solved:
            raise Exception("Something went wrong!")
        
        return self.colored
        
    def build_cnf(self):
        
        self.formula = CNF()
        colors = list(range(1, self.ncolors + 1))    

        for n1, n2 in self.g.edges():
            for c in colors:            
                self.formula.append([-self.cmap.enc(n1, c), -self.cmap.enc(n2, c)])

        #specials = [28, 194, 242, 355, 387, 397, 468]
        #ii = 1
        #for n in specials:
        #   self.formula.append([self.cmap.enc(n, ii)])
        #  ii += 1


        for n in self.g.nodes():
            #if not n in specials:
            self.formula.append([self.cmap.enc(n, c) for c in colors])
            for c1 in colors:
                for c2 in colors:
                    if c1 < c2:
                        self.formula.append([-self.cmap.enc(n, c1), -self.cmap.enc(n, c2)])
        
        return self.formula
    
    def solve_cnf(self, solver = ''):
        
        triangle = find_triangle(self.g)
        assumptions = []
        if len(triangle) > 0:            
            assumptions = [self.cmap.enc(triangle[0], 1), self.cmap.enc(triangle[1], 2), self.cmap.enc(triangle[2], 3)]
            
        #Glucose3, Glucose4, Lingeling, MapleChrono, MapleCM, Maplesat, Minisat22, MinisatGH
        #with Glucose4(bootstrap_with=self.formula.clauses, with_proof=True) as ms:        
        with Lingeling(bootstrap_with=self.formula.clauses) as ms:
            self.solved = ms.solve(assumptions=assumptions)
            if self.solved:
                self.model = np.array(ms.get_model())
                self.apply_model()
            else:                
                self.proof = []#ms.get_proof()
                self.colored = False
                
        return self.solved

if __name__ == "__main__":

    if len(sys.argv) < 4:
        raise "I need in_file out_file ncolors"

    infile = sys.argv[1]
    outfile = sys.argv[2]
    ncolors = int(sys.argv[3])
    g = Utils.read_dimacs_graph(infile)
    problem = ColSAT(g, ncolors)
    problem.build_cnf().to_file(outfile)


