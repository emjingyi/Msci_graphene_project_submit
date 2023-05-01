# -*- coding: utf-8 -*-

#importing packages from pyqula
import numpy as np
from pyqula import geometry
from pyqula import specialgeometry
from pyqula import specialhamiltonian
from pyqula import hamiltonians
from pyqula import klist
from pyqula import ribbonizate 
from pyqula.kpointstk.labels import label2k
from pyqula.specialhopping import twisted_matrix
import matplotlib.pyplot as plt
from pyqula import geometry, ribbon
from pyqula import topology
from pyqula import sculpt
import numpy as np
import os
from pyqula import supercell
import sys  # for progress bar (sys.stdout)
from pyqula import islands
# Import time module
import time
from pygame import mixer # L

#%%
ti=0.15#intralayer hopping amplitude

def material(m,n,layer):#function defining the material
       if m==0: #mlg
           g = geometry.honeycomb_lattice()
           h = g.get_hamiltonian()
       elif m==1:#general multilayer
           h=specialhamiltonian.multilayer_graphene(l=layer,ti=ti)
       elif m==2: #twisted multiayer
           g = specialgeometry.twisted_multilayer(n,rot=layer)
           g.write()
           h = g.get_hamiltonian(is_sparse=True,has_spin=False,is_multicell=False,
                mgenerator=twisted_matrix(ti=ti,lambi=7.0))
       return h
   
def geo(m,layer,n):#returns geometry of the lattice: lattice vectors
    if m==0: #mlg
        g = geometry.honeycomb_lattice()
    elif m==1:#general multilayer
        g=specialgeometry.multilayer_graphene(l=layer)
    elif m==2: #twisted multiayer
        g = specialgeometry.twisted_multilayer(n,rot=layer)
        
    return g
    

def title(t,n,layer):#to simplify plot title
       tstring= ''.join(str(i) for i in layer)
       if t==0:
           h="MLG"
       elif t==1:
           h='Multilayer graphene, layer index'+tstring
       elif t==2:
           h = "twisted multilayer angle %1.3f layer index"%n+tstring
     

          
       return h
   #%%
s=0.1 #size of scatter dot
renum=[] #list of variable1
rrnum=[] #list of variable2
nk=400 #number of k points run through, the larger the more resolved
numb=50 #number of bands to plot for the nanoribbon geometry 
plt.rcParams.update({'font.size': 15}) #plot parameters
csfont = {'fontname':'Times New Roman'}
plt.rcParams['figure.dpi'] = 300
i=0 #iterative variable
mat=0#0 graphene 1 multilayer 2 twisted
layer=[0,1]
n=1 

for re in renum:
    p=[]
    for rr in rrnum:
        i+=1
        
        h=material(mat,n,layer)
        plot_title=title(mat,n,layer)
       
        
        '''ribbon/nanoisland related functions'''
        
        #h = ribbon.bulk2ribbon(h,n=20) # generate a ribbon from the bulk Hamiltonians
        #g = geometry.honeycomb_armchair_ribbon(nribbon)
        #g=geometry.honeycomb_zigzag_ribbon(15)
        #h=ribbon.hamiltonian_ribbon(h,nribbon)
        #g=h.geometry
        #h_ribbon & g_ribbon identical
        #g=geometry.kagome_ribbon(n=5)
        #g=islands.get_polygon_island(n=15,nedges=6,rot=45,geo=g)
        #g=h.geometry
        #gs = g.get_supercell(10) 
        #plt.scatter(gs.r[:,0],gs.r[:,1],c=gs.r[:,2],s=5);plt.axis("equal"); plt.axis("off")#,c=gs.r[:,1],s=5) ; plt.axis("equal") #; plt.axis("off")
        #plt.title('Section of the MLG Nanorribon',**csfont)
        #plt.show()
        #h=g.get_hamiltonian()
        #h=g.get_hamiltonian(tij=specialhopping.multilayer)
        '''modulators'''
        h.set_filling(0.5,nk=5) # put at half filling
        #h.add_rashba(0.5) # Rashba spin-orbit coupling
        #h.add_soc(0.02) #intrinsic SOC
        #h.add_haldane(thal)
        #h.add_exchange([0.,0.,0.1])
        #h.add_sublattice_imbalance(re)
        #h.add_orbital_magnetic_field(0.1) # add an out-of plane magnetic field# add the magnetic field
        #h.add_zeeman([0,0,0.1])
        #h.add_onsite(lambda r: r[2]*re)#/np.max(h.geometry.r[:,2])) 
        #op = h.get_operator("valley",projector=True) # valley operator              
        
        (k,e) = h.get_bands(nk=nk,num_bands=numb,kpath=['K','G','M','K'])
        
        plt.scatter(k,e,s=s)  

        plt.title('title of plot',**csfont)
   
        plt.ylabel('Energy(eV)',**csfont)
        plt.xlabel('Momentum',**csfont)
        plt.show()