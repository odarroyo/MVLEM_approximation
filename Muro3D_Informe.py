# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 10:42:38 2022

@author: Dirsa
"""

from openseespy.opensees import *

# hay que llamar al opsvis para poder plotear la visualización
import opsvis as opsv
# esta es una librería estándar para plotear otras cosasy poder crear figuras.
import matplotlib.pyplot as plt

import analisis as an

import numpy as np

import vfo.vfo as vfo

import os as os

import time
import math
# from analisis import *

wipe()
# creación del modelo
model('basic', '-ndm', 3, '-ndf', 6)
plt.rcParams.update({'font.size': 16})
plt.figure(figsize=(6,5), dpi=500)

# %% NODOS ====================================================================

e = 0.15  # grosor de los muros
lm1 = 1.5
lm2 = 1.5
lm3 = 4.0
h = 2.7  # altura del muro

node(1, 0.0, 0.0, 0.0)
node(2, 0.0, lm1, 0.0)
node(3, 0.0, lm1+lm2, 0.0)
node(4, lm3, lm1, 0.0)

node(5, 0.0, 0.0, h)
node(6, 0.0, lm1, h)
node(7, 0.0, lm1+lm2, h)
node(8, lm3, lm1, h)

opsv.plot_model()
fixZ(0.0, 1, 1, 1, 1, 1, 1)

# %% MATERIALES ================================================================
# Concreto sin confinar

fpc = 21000.0
Ec= 4300000*math.sqrt(fpc/1000)
ec = 2*fpc/Ec
fcu = 0.1*fpc
ecu = 0.006
# Concreto confinado
k = 1.3
fcc = fpc*k
ecc = 2*fcc/Ec
fucc = 0.2*fcc
eucc = 0.02
# Acero
# mallas
# Fy = 621000.0
# Es = 210000000.0
# ey = Fy/Es
# fu = 687000.0
# eult = 0.0155

p1=509.10*1000
p2=691.50*1000
p3=734.44*1000
e1=0.00248
e2=0.005
e3=0.01
pinchX=0.34
pinchY= 0.56
damage1= 0.038
damage2= 0.07
beta= 0.086

# barras
Fyb = 420000.0
Esb = 210000000.0
eyb = Fyb/Esb
fub = 630000.0
eultb = 0.1

uniaxialMaterial('Concrete01', 2, -fpc, -ec, -fcu, -ecu)
uniaxialMaterial('Concrete01', 1, -fcc, -ecc, -fucc, -eucc)
# uniaxialMaterial('Hysteretic', 5, Fy, ey, fu, eult, 0.2*Fy, 0.0156, -Fy, -ey, -fu, -eult, -0.2*Fy, -0.0156, 1.0, 1.0, 0.0, 0.0)
# uniaxialMaterial('MinMax', 3, 5, '-min', -0.0155, '-max', 0.0155)
uniaxialMaterial('Hysteretic', 5, p1, e1, p2, e2, p3, e3, -p1, -e1, -p2, -e2, -p3, -e3, pinchX, pinchY, damage1, damage2, beta)       
uniaxialMaterial('MinMax', 3, 5, '-min', -0.006, '-max', 0.0186)

uniaxialMaterial('Hysteretic', 6, Fyb, eyb, fub, eultb, 0.05*Fyb, 0.11, -Fyb, -eyb, -fub, -eultb, -0.05*Fyb, -0.11, 1.0, 1.0, 0.0, 0.0)
uniaxialMaterial('MinMax', 4, 6, '-min', -0.006, '-max', 0.05)

# material del shear
tagshear = 1000
G = Ec*0.4
uniaxialMaterial('Elastic', tagshear, G*1.5)

# %% ELEMENTOS=================================================================
muro1 = [1, 2, 6, 5]
muro2 = [2, 3, 7, 6]
muro3 = [2, 4, 8, 6]

lmm1 = lm1-0.45-0.15/2
lmm2 = lm2-0.45-0.15/2
lmm3 = lm3-0.35-0.50
t = [e, e, e, e, e, e, e, e]  # ancho de las fibras
width1 = [0.45, lmm1/6, lmm1/6, lmm1/6, lmm1/6, lmm1/6, lmm1/6, 0.15/2]
width2 = [0.15/2, lmm2/6, lmm2/6, lmm2/6, lmm2/6, lmm2/6, lmm2/6, 0.45]
width3 = [0.50-0.15, lmm3/6, lmm3/6, lmm3/6, lmm3/6, lmm3/6, lmm3/6, 0.50]


rm = 0.0025  # cuantía de las mallas
rb = 0.01  # cuantía de las barras
rho1 = [rb, rm, rm, rm, rm, rm, rm, rb]
rho2 = [rb, rm, rm, rm, rm, rm, rm, rb]
rho3 = [rb, rm, rm, rm, rm, rm, rm, rb]

concrete1 = [1, 2, 2, 2, 2, 2, 2, 1]
concrete2 = [1, 2, 2, 2, 2, 2, 2, 1]
concrete3 = [1, 2, 2, 2, 2, 2, 2, 1]

steel1 = [4, 3, 3, 3, 3, 3, 3, 4]
steel2 = [4, 3, 3, 3, 3, 3, 3, 4]
steel3 = [4, 3, 3, 3, 3, 3, 3, 4]


element('MVLEM_3D', 1, *muro1, 8, '-thick', *t, '-width', *width1, '-rho',
        *rho1, '-matConcrete', *concrete1, '-matSteel', *steel1, '-matShear', 1000)
element('MVLEM_3D', 2, *muro2, 8, '-thick', *t, '-width', *width2, '-rho',
        *rho2, '-matConcrete', *concrete2, '-matSteel', *steel2, '-matShear', 1000)
element('MVLEM_3D', 3, *muro3, 8, '-thick', *t, '-width', *width3, '-rho',
        *rho3, '-matConcrete', *concrete3, '-matSteel', *steel3, '-matShear', 1000)

opsv.plot_model(fmt_model={'color': 'green', 'linestyle': 'solid', 'linewidth': 2.0, 'marker': '.', 'markersize': 6})
plt.style.use('seaborn-colorblind')
# vfo.plot_model(setview='3D')
# %% ANALISIS

an.gravedad()
loadConst('-time', 0.0)
plt.figure()

# %%

a = nodeDisp(3)
b = nodeDisp(4)
c = nodeDisp(1)

# %% PUSHOVER

timeSeries('Linear', 2)
pattern('Plain', 2, 2)
load(6, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
dirName = 'muroT3D'
elements = [1, 2, 3]

if not os.path.exists(dirName):
    os.mkdir(dirName)
recorder('Element', '-file', dirName+'/strain.out',
         '-time', '-ele', *elements, 'Fiber_Strain')
recorder('Element', '-file', dirName+'/stress_concrete.out',
         '-time', '-ele', *elements, 'Fiber_Stress_Concrete')
recorder('Element', '-file', dirName+'/stress_steel.out',
         '-time', '-ele', *elements, 'Fiber_Stress_Steel')
recorder('Element', '-file', dirName+'/curvature.out',
         '-time', '-ele', *elements, 'Curvature')

stime = time.time()
dtecho3D, Vbasal3D = an.pushover2(0.015*h, 0.0001, 8, 1)
etime = time.time()

print('tiempo de corrida del Pushover = ', etime-stime, 's')
#%%
plt.figure()
plt.rcParams.update({'font.size': 18})
plt.rc('font', family='serif')
plt.plot(dtecho3D,Vbasal3D)
plt.xlabel('desplazamiento (m)')
plt.ylabel('Corte (kN)') 
plt.grid(linestyle='dotted')

# plt.show()

