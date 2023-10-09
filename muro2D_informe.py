# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 10:33:11 2022

@author: Dirsa
"""
# hay que llamar al opensees

from openseespy.opensees import *
# hay que llamar al opsvis para poder plotear la visualización
import opsvis as opsv
# esta es una librería estándar para plotear otras cosasy poder crear figuras.
import matplotlib.pyplot as plt

import analisis as an
import math
import numpy as np

import vfo.vfo as vfo

import os as os

import time

# from analisis import *

wipe()
#
# wipe() mientras no funcione bien el script es mejor tener el wipe antes
# creación del modelo
model('basic','-ndm',2,'-ndf',3)

# %% INFORMACIÓN DE ENTRADA
h=2.7
node(1,0.0,0)
node(2,0.0,h)

# apoyos
empotrado = [1,1,1]
grado2 = [1,1,0]

# para colocarlos todos al nivel 0.0
fixY(0.0,*empotrado)
#%%  MATERIALES Y TRANSFORMACIONES
# =========================================
# #Concreto sin confinar 
# fc = 21000.0
# ec = 0.002
# E = 1000*4300*(fc/1000)**0.5
# fcu = 0.1*fc
# ecu = 0.006
# #Concreto confinado
# k=1.3
# fcc=fc*k
# ecc= 2*fcc/E
# fucc=0.2*fcc
# eucc=0.02
# # Acero 
# # mallas
# Fy=621000.0
# Es=210000000.0
# ey = Fy/Es
# fu = 687000.0
# eult = 0.0155

# # barras
# Fyb=420000.0
# Esb=210000000.0
# eyb = Fyb/Esb
# fub = 630000.0
# eultb = 0.1

# #combinación
# Fyp=(Fy+Fyb)/2
# Esp=Esb
# eyp=Fyp/Esp
# fup=(fu+fub)/2
# eultp=(eult+eultb)/2

# uniaxialMaterial('Concrete01', 2, -fc, -ec, -fcu, -ecu)
# uniaxialMaterial('Concrete01', 1, -fcc, -ecc, -fucc, -eucc)
# uniaxialMaterial('Hysteretic',5,Fy,ey,fu,eult,0.2*Fy,0.0156,-Fy,-ey,-fu,-eult,-0.2*Fy,-0.0156,1.0,1.0,0.0,0.0)
# uniaxialMaterial('MinMax', 3, 5, '-min', -0.0155, '-max', 0.0155)
# uniaxialMaterial('Hysteretic',6,Fyb,eyb,fub,eultb,0.05*Fyb,0.11,-Fyb,-eyb,-fub,-eultb,-0.05*Fyb,-0.11,1.0,1.0,0.0,0.0)
# uniaxialMaterial('MinMax', 4, 6, '-min', -0.05, '-max', 0.05)

# uniaxialMaterial('Hysteretic',7,Fyp,eyp,fup,eultp,((0.05+0.2)/2)*Fyp,((0.11+0.0155)/2),-Fyp,-eyp,-fup,-eultp,-((0.05+0.2)/2)*Fyp,-((0.11+0.0155)/2),1.0,1.0,0.0,0.0)
# uniaxialMaterial('MinMax', 8, 7, '-min', -((0.05+0.0155)/2), '-max', ((0.05+0.0155)/2))

# cMVLEM = 0.4 
# # material del shear
# tagshear = 1000
# G = E*0.4
# uniaxialMaterial('Elastic',tagshear,G*1.5)

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

#%% ELEMENTOS
e=0.15
lmm1=4.15-0.5-0.5
t = [3.9, 2.1, e, e, e, e, e, e, e, e]  # ancho de las fibras
width1 = [0.15/2,0.15/2, 0.35, lmm1/6, lmm1/6, lmm1/6, lmm1/6,lmm1/6,lmm1/6, 0.50]
# width1 = [0.15/2,0.15/2, 0.30, lmm1/8, lmm1/8, lmm1/8, lmm1/8,lmm1/8,lmm1/8,lmm1/8,lmm1/8, 0.45]
rm = 0.0025  # cuantía de las mallas
rb = 0.01  # cuantía de las barras
rho1 = [rm, rb, rb, rm, rm, rm,rm,rm, rm, rb]
concrete1 = [2, 1, 1, 2, 2, 2, 2, 2, 2, 1]
steel1 = [3, 4, 4, 3, 3, 3, 3, 3,3,3, 4]
muro1=[1,2]
matshear = [1000,1000,1000,1000,1000,1000,1000,1000,1000,1000]

element('MVLEM',1,0.0,*muro1,10,0.4,'-thick',*t,'-width',*width1,'-rho',*rho1,'-matConcrete',*concrete1,'-matSteel',*steel1,'-matShear',*matshear)

opsv.plot_model()

an.gravedad()
loadConst('-time', 0.0)
# %% PUSHOVER

timeSeries('Linear', 2)
pattern('Plain', 2, 2)
load(2, 1.0, 0.0, 0.0)
dirName = 'muroT2d_Opcion2'
elements = [1]

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
dtecho2D, Vbasal2D = an.pushover2(0.015*h, 0.0001, 2, 1)
etime = time.time()

print('tiempo de corrida del Pushover = ', etime-stime, 's')

#%%
# plt.plot(dtecho2D,Vbasal2D)
# plt.xlabel('desplazamiento (m)')
# plt.ylabel('Corte (kN)')
# plt.grid(linestyle='dotted')
# plt.show()
# plt.style.use('bmh')
plt.rcParams["font.family"] = "Calibri"
plt.rcParams['savefig.bbox'] = "tight"
fig = plt.figure(figsize=(12, 12),dpi=500)
plt.figure(figsize=(10,10))
plt.plot((dtecho3D/2.7)*100,Vbasal3D,color='forestgreen', lw= 3.0, linestyle= 'solid')
plt.plot((dtecho2D/2.7)*100,Vbasal2D,color='tab:blue', lw=3.0)
plt.xlabel('Drift ratio (%)', fontsize = 32)
plt.ylabel('Shear force (kN)', fontsize = 32)
plt.legend(['MVLEM 3D','MVLEM 2D'], fontsize = 32) 
plt.xticks(fontsize=32)
plt.yticks(fontsize=32)
# plt.xticks(precision=3)
plt.tick_params(which='both', direction='in', length=10, width=4)
# plt.tick_params(which='minor', direction='in')
plt.grid(color = 'gray', linestyle = 'dashed')
plt.xlim([0.001, 1.2])
plt.ylim([0, 5000])
plt.show()
print('tiempo de corrida del Pushover = ', etime-stime, 's')
