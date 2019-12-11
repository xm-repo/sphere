import os
import numpy as np
import itertools
import networkx as nx
import scipy.optimize as opt
from numpy.linalg import norm
from scipy.spatial import SphericalVoronoi

def read_points2(filename):
    points = []
    f = open(filename, 'r')
    k = int(f.readline())
    f.readline()
    for s in f:
        s = ' '.join(s.split())
        l = s.split(' ')        
        points.append(np.array([float(l[1]), float(l[2]), float(l[3])], dtype=np.float64))
    f.close()
    return np.array(points)

def read_triang2(filename):
    points = []
    f = open(filename, 'r')
    k = int(f.readline())    
    for s in f:
        s = ' '.join(s.split())
        l = s.split(' ')        
        points.append(np.array([int(l[0]), int(l[1]), int(l[2])], dtype=np.int32))
    f.close()
    return np.array(points)

def write_dimacs(g, filename):
    g1 = g #nx.convert_node_labels_to_integers(g, first_label=1)
    f = open(filename, 'w')
    f.write('p edges ' + str(g.number_of_nodes()) + ' ' + str(g.number_of_edges()) + '\n')
    for e in g1.edges():
        f.write('e ' + str(e[0]) + ' ' + str(e[1]) + '\n')
    f.close()

def write_faces(faces, filename):
    f = open(filename, 'w')
    for face in faces:
        for p in face:
            f.write(' '.join(map(str, p)) + '\n')
        f.write(' \n')    
    f.close()

'''
def build_g2(g):
    paths = dict(nx.all_pairs_shortest_path(g, 2))

    G2 = G.copy()
    keys = list(paths.keys())
    for key in keys:
        for nn in list(paths.get(key).keys()):
            G2.add_edge(key, nn)

    return G2
'''

def connect_dist2(g):    
    
    gg = g.copy()
    
    to_connect = []
    for i in gg.nodes():
        for j in gg.nodes():
            if nx.shortest_path_length(gg, i, j) == 2:
                to_connect.append([i,j])
    for e in to_connect:
        gg.add_edge(e[0], e[1])            
    return gg

def dist(u, v):
    return norm(u - v)

# угол между радиус-векторами
def angle(p1 ,p2):    
    c = np.dot(p1, p2) / norm(p1) / norm(p2)
    return np.arccos(np.clip(c, -1, 1))
    
# середина дуги между x, y
def middle(x, y):    
    z = (x + y) / 2
    return z / norm(z)

# диаметр области
def get_diam(faces): 
    diam = 0.0
    for f in faces:
        ij = itertools.combinations(range(len(f)), 2)
        dists = np.array([dist(f[i], f[j]) for i, j in ij])
        diam = np.max([diam, np.max(dists)])
    return diam
    
def plane_equation(x, y, z):    
    a1 = x[1] - x[0] 
    b1 = y[1] - y[0] 
    c1 = z[1] - z[0] 
    a2 = x[2] - x[0] 
    b2 = y[2] - y[0] 
    c2 = z[2] - z[0] 
    a = b1 * c2 - b2 * c1 
    b = a2 * c1 - a1 * c2 
    c = a1 * b2 - b1 * a2 
    d = (- a * x[0] - b * y[0] - c * z[0]) 
    return np.array([a, b, c, d])

def foot(x,y,z,v):
    p = plane_equation(x, y, z)
    n = np.array([p[0], p[1], p[2]])
    l = norm(n)
    n = n / l #[n[0]/l,n[1]/l,n[2]/l]
    h = p[0]*v[0] + p[1]*v[1] + p[2]*v[2] + p[3]
    n1 = n * h / l #[n[0]*h/l,n[1]*h/l,n[2]*h/l]
    return v - n1 #[v[0]-n1[0],v[1]-n1[1],v[2]-n1[2]]

def circ_dist(x,y,v,eps=1E-8):
    z = np.array([0.0, 0.0, 0.0])
    f = foot(x,y,z,v)
    
    l = norm(f)
    f = f / l #[f[0]/l,f[1]/l,f[2]/l]
    a1 = angle(x,f)
    a2 = angle(f,y)
    a3 = angle(x,y)
    d = min(dist(x,v), dist(y,v))    
    if abs(a1+a2-a3)<eps:
        d = min(d,dist(f,v))
    return d    
        
# расстояние между областями
def faces_dist(face1, face2):
    f1 = face1
    f2 = face2
    d = 2.0
    for i in range(len(f1)):        
        for j in range(len(f2)):
            v = f1[i]
            x = f2[j]
            if j==len(f2)-1:
                y = f2[0]
            else:
                y = f2[j+1]
            d = min(d,circ_dist(x,y,v))    
    for i in range(len(f2)):
        for j in range(len(f1)):
            v = f2[i]
            x = f1[j]
            if j==len(f1)-1:
                y = f1[0]
            else:
                y = f1[j+1]
            d = min(d,circ_dist(x,y,v))    
    return d

# 'центр описанной окружности' сферического треугольника, вершина диаграммы Вороного
def center(x, y, z):
    c = np.vstack([x, y, z])
    x0 = np.mean(c, axis=0)
    x0 = x0 / norm(x0)
    f = lambda v: np.square(np.dot(v, x - y)) + np.square(np.dot(v, x - z)) + np.square(np.dot(v, v) - 1)    
    sol = opt.minimize(f, x0, method='nelder-mead')
    return sol.x

def get_dual(g, points):
    faces = []
    for v in g.nodes():
        neigh = g.neighbors(v)
        
        try: 
            n_cyc = nx.cycle_basis(g.subgraph(neigh))[0]   # цикл на соседних вершинах
            n_cyc.append(n_cyc[0])
        except IndexError:
            pass
            #print(nx.cycle_basis(g.subgraph(neigh)))
        
        face = []   # вершины области
        for i in range(len(n_cyc) - 1):
            c = center(points[v - 1], points[n_cyc[i] - 1], points[n_cyc[i+1] - 1])
            face.append(c)
            
        faces.append(face)
    return faces

def get_dual2(g, points):
    sv = SphericalVoronoi(points)
    sv.sort_vertices_of_regions()
    faces = []
    for region in sv.regions:
        face = sv.vertices[region]
        faces.append(face)
    return np.array(faces)
        
# минимум из расстояний между областями на расстоянии >3
def faces_d3_dist2(g, faces):
    n = g.number_of_nodes()
    d = 2.0
    for i in g.nodes():
        for j in g.nodes():
            if nx.shortest_path_length(g, i, j) == 3:                
                d = np.min([d, faces_dist(faces[i - 1], faces[j - 1])])
    return d

def faces_d3_dist(g, faces):

    d = 2.0
    paths = dict(nx.all_pairs_shortest_path_length(g, 3))    
    
    for i in g.nodes():
        for j in g.nodes():
            if i in paths:
                if j in paths[i]:
                    if paths[i][j] == 3:
                        d = np.min([d, faces_dist(faces[i - 1], faces[j - 1])])

    return d


thomsons = [f.strip() for f in open('thomson/list_of_files.txt')]

thomsons.sort(key=lambda x: int(x.replace('.xyz', '')))

for thomson in thomsons:
    try:
        print(thomson)
    
        n_thomson = int(thomson.replace('.xyz', ''))
        points = read_points2('thomson/' + thomson)

        f = open('tmp', 'w')
        f.write('3 \n')
        f.write(str(len(points)) + '\n')
        for p in points:
            f.write(' '.join(map(str, p)) + '\n')
        f.close()

        cmd = 'C:\\cpp\\qhull-2019.1\\bin\\qconvex.exe i < tmp > ' + 'thomson1/' + str(n_thomson) + '.g'
        os.system(cmd)
    
        triangles = read_triang2('thomson1/' + str(n_thomson) + '.g')
    
        G = nx.Graph()

        for t in triangles:
            t = t + 1        
            G.add_edge(t[0], t[1])
            G.add_edge(t[1], t[2])
            G.add_edge(t[0], t[2])
    
        write_dimacs(G, 'g/' + str(n_thomson) + '.g')
    
        good = True
    
        for v,d in G.degree:        
            if (d != 5) and (d != 6):
                good = False
                break
                    
        if good:
            write_dimacs(connect_dist2(G), 'g2/' + str(n_thomson) + '.g2')

            faces = get_dual2(G, points)
            d0 = get_diam(faces)
            d1 = faces_d3_dist(G, faces)

            #if d1/d0 > 1:
            print(thomson + ' ' + str(d0) + ' ' + str(d1) + ' ' + str(d1/d0))
            write_faces(faces, 'vor/' + str(n_thomson) + '.vor')
    except Exception as e:
        print('err' + str(e))        
        
        
    