
import networkx as nx
import planarity as pl
import matplotlib.pyplot as plt
import numpy as np
import sys


#a,b = 2,2   

edges_dist2 = True

dodec = nx.dodecahedral_graph()

par = [[],[],[]]
npar = 0

n_contr = 0
#nei = np.zeros([20,3],dtype = 'i')
nei = []

node_list = []
node_cl = []

def valid(x,y,a,b):
    return ((x>=0) and (y>=0) and (x<=a+b) and (y<=a+b) and (x+y>=b) and (x+y<=a+2*b))


def hexagon_triangular_grid(a,b,z=0):     # generate aq hexagon on the triangular grid with sides a-b-a-b-a-b 
                                          
    g = nx.Graph()    
    for i in range(a+b+1):
        for j in range(a+b+1):
            if valid(i,j,a,b):
#                g.add_node((i,j))
                if valid(i+1,j-1,a,b):
                    g.add_edge((i,j,z),(i+1,j-1,z))
                if valid(i+1,j,a,b):
                    g.add_edge((i,j,z),(i+1,j,z))
                if valid(i,j+1,a,b):
                    g.add_edge((i,j,z),(i,j+1,z))
                if edges_dist2:        #  vertices u,v are adjanced if dist(u,v)=2 in the initial graph
                    if valid(i+2,j-2,a,b):
                        g.add_edge((i,j,z),(i+2,j-2,z))
                    if valid(i+2,j-1,a,b):
                        g.add_edge((i,j,z),(i+2,j-1,z))
                    if valid(i+2,j,a,b):
                        g.add_edge((i,j,z),(i+2,j,z))
                    if valid(i+1,j+1,a,b):
                        g.add_edge((i,j,z),(i+1,j+1,z))
                    if valid(i,j+2,a,b):
                        g.add_edge((i,j,z),(i,j+2,z))
                    if valid(i-1,j+2,a,b):
                        g.add_edge((i,j,z),(i-1,j+2,z))
    return g    

def fill_paral(a,b):   # indices of vertices that belongs to other hexagon
    global npar
    for i in range(b+1):
        for j in range(a+1):
            par[0].append([j+b-i,i])
    for i in range(b+1):
        for j in range(a+1):            
            par[1].append([i,a+b-j])
    for i in range(b+1):
        for j in range(a+1):
            par[2].append([a+b-j,b+j-i])
    npar = len(par[0])-1        

def equiv_nodes(u,v):   # check if two vertices in different hexagons are equivalent
#    global n_contr
    e = (u[2],v[2])
    u1 = [u[0],u[1]]
    v1 = [v[0],v[1]]
    if nei[e[0]].count(e[1])==0:
        return False
    i0 = nei[e[0]].index(e[1])        
    i1 = nei[e[1]].index(e[0])
    if par[i0].count(u1)==0:
        return False
    if par[i1].count(v1)==0:
        return False
    res = (par[i0].index(u1)+par[i1].index(v1) == npar)
#    if res:
#        print(u,v)
#        n_contr += 1
    return res    

def tr_classes(g):    # defining classes of eqiuivalence for networkx.union
    
    def merge_classes(c):
        for i in range(len(node_list)-1):
            if c.count(node_cl[i])>0:
                node_cl[i] = c[0]
    
    cln = 0
    for u in g.nodes():
        cur = []
        for k in range(len(node_list)):
            v = node_list[k]
            if equiv_nodes(u,v):
                if cur.count(node_cl[k])==0:
                    cur.append(node_cl[k])
                                    
        node_list.append(u)
        if len(cur)==0:
            cln+=1
            node_cl.append(cln)
        else:
            if len(cur)>1:
                merge_classes(cur)
            node_cl.append(cur[0])

def contract_nodes(u,v):  # finally u,v are in the same class       
    i0 = node_list.index(u)
    i1 = node_list.index(v)
    return (node_cl[i0]==node_cl[i1])

def write_dimacs(g,filename):
    g1 = nx.convert_node_labels_to_integers(g,first_label=1)
    f = open(filename,'w')
    f.write('p edges '+str(g.number_of_nodes())+' '+str(g.number_of_edges())+'\n')
    for e in g1.edges():
        f.write('e '+str(e[0])+' '+str(e[1])+'\n')
#    print(g1.degree([0,1,2,3,4,5,6,7,8,9,10]))
    f.close()
    
def write_cnf(g,n,filename):    
    g1 = nx.convert_node_labels_to_integers(g,first_label=1)
    f = open(filename,'w')
    f.write('p cnf '+str(g1.number_of_nodes()*n)+' '+str(g1.number_of_nodes()+g1.number_of_edges()*n)+'\n')
    for e in g1.edges():        
        for c in range(n):
            f.write(str(-(int(e[0]-1)*n+c+1))+' '+str(-(int(e[1]-1)*n+c+1))+' 0\n')
    for i in range(g1.number_of_nodes()):
        for c in range(n):
            f.write(str(i*n+c+1)+' ')
        f.write('0\n')    

    f.close()
    

if __name__ == "__main__": 
    try:        
        a = int(sys.argv[1])     
        b = int(sys.argv[2])        
    except:
        print('usage: sphere_triang.py a b \n where a,b are positive integers')
        sys.exit()
              
    tr = nx.Graph()
    for i in range(20):
        h = hexagon_triangular_grid(a,b,i)
        tr = nx.union(tr,h)
    
#print(tr.number_of_edges())    
#tr = hexagon_triangular_grid(2,1)

    L = pl.check_planarity(dodec)[1]
    for i in range(20):
        k = 0
        nei.append([])
        for v in L.neighbors_cw_order(i):
            nei[i].append(v)
            k += 1
                
    fill_paral(a,b)

    tr_classes(tr)

#
    tr_sphere = nx.quotient_graph(tr,contract_nodes)

    tr_sphere = nx.quotient_graph(tr,contract_nodes)

    fn = 'sph_'+str(a)+'_'+str(b)+'.cnf'

    print('Generating icosahedral S^2 triangulation T({0},{1}) and CNF for 8-coloring...'.format(a,b),'\n')
    print('Number of nodes (variables): {0} ({1}) '.format(tr_sphere.number_of_nodes(),tr_sphere.number_of_nodes()*8),'\n')    
    print('Number of edges: ',tr_sphere.number_of_edges(),'\n')    
    print('Number of clauses: ',tr_sphere.number_of_edges()*8+tr_sphere.number_of_nodes(),'\n')    
    print(fn+'\n')

#print(n_contr)
#print(len(np.unique(node_cl)))

#write_dimacs(tr_sphere,'tr_sphere_'+str(a)+'_'+str(b)+'_d2.txt')
    write_cnf(tr_sphere, 8, fn)

#nx.draw(tr_sphere)
#plt.show()