"""
Práctica 0: Mecánica pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Jahzeel Abisai Tapia Gracia
Número de control: 22210798
Correo institucional: l22210798@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np 
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h =0,0,10,1E-3,6,3
N=round((tend-t0)/dt)+1
t=np.linspace(t0,tend,N)
u1=np.ones(N)# escalon unitario
u2=np.zeros(N);u2[round(1/dt):round(2/dt)]=1 #Impulse
u3=(np.linspace(0,tend,N))/tend #ramp pendiente 1/10
u4=np.sin(m.pi/2*t) #funcion sinusoidal 250mHz

u=np.stack((u1,u2,u3,u4),axis=1)
signal=['Escalon','Impulso','Ramp','Sin']

# Componentes del circuito RLC y función de transferencia
R=1.5E3
L=390E-6
C=10E-6

num=[C*L*R, C*R**2+L, R]
den=[3*C*L*R, 5*C*R**2+L, 2*R]
sys=ctrl.tf(num,den)
print(sys)

# Componentes del controlador
Rr = 22E3
Re = 8E3
Cr = 1e-6
kP = 2.8
kI = 125
Re = 1/(kI*Cr); print('Re =  ',Re)
Rr = (kP*Re); print('Re =  ',Rr)
numPI = [Rr*Cr,1]
denPI = [Re*Cr,0]
PI = ctrl.tf(numPI,denPI)
print(PI)
    
# Sistema de control en lazo cerrado
X=ctrl.series(PI,sys)      
sysPI=ctrl.feedback(X,1,sign=-1)              
print(sysPI)

#Colores
morado = [.6,.2,.5]
rojo= [1,0,0]
amarillo=[1,.7,0]
azul= [.1,.5,.7]

# Respuesta del sistema en lazo abierto y en lazo cerrado
fig1=plt.figure();
plt.plot(t,u1, '-', color = azul, label = 'Ve(t)')
_,Pa=ctrl.forced_response(sys,t,u1,x0)
plt.plot(t,Pa, '-', color = rojo, label = 'Vs(t)')
_,VPI=ctrl.forced_response(sysPI,t,u1,x0)

plt.plot(t,VPI, ':',linewidth=3, color = morado, label = 'VPI(t)')
plt.xlim(-0.25,10);plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.1);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3, fontsize=8,frameon=False)
plt.show()
fig1.savefig('ESCALE.pdf',bbox_inches='tight')

fig2=plt.figure();
plt.plot(t,u2, '-', color = azul, label = 'Ve(t)')
_,Pa=ctrl.forced_response(sys,t,u2,x0)
plt.plot(t,Pa, '-', color = rojo, label = 'Vs(t)')
_,VPI=ctrl.forced_response(sysPI,t,u2,x0)

plt.plot(t,VPI, ':',linewidth=3, color = morado, label = 'VPI(t)')
plt.xlim(-0.25,10);plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.1);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3, fontsize=8,frameon=False)
fig2.savefig('IMPULSE.pdf',bbox_inches='tight')
plt.show()

fig3=plt.figure();
plt.plot(t,u3, '-', color = azul, label = 'Ve(t)')
_,Pa=ctrl.forced_response(sys,t,u3,x0)
plt.plot(t,Pa, '-', color = rojo, label = 'Vs(t)')
_,VPI=ctrl.forced_response(sysPI,t,u3,x0)

plt.plot(t,VPI, ':',linewidth=3, color = morado, label = 'VPI(t)')
plt.xlim(-0.25,10);plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.1);plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize=11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3, fontsize=8,frameon=False)
fig3.savefig('RAMP.pdf',bbox_inches='tight')
plt.show()

fig4 = plt.figure();

plt.plot(t,u4,"-",color = azul, label = "Va(t)")
ts,PA = ctrl.forced_response(sys,t,u4,x0)

plt.plot(t,PA,"-",color = rojo, label = "Vs(t)")
_,VPID = ctrl.forced_response(sysPI,t,u4,x0)

plt.plot(t,VPID,":",linewidth=3, color = morado, label = "VPID(t)")
plt.xlim(-0.25,10);plt.xticks(np.arange(0,11,1.0))
plt.ylim(-1,1.2); plt.yticks(np.arange(-1.1,1.2,0.2))
plt.xlabel("t[s]",fontsize=11)
plt.ylabel("V_i(t)",fontsize=11)
plt.legend(bbox_to_anchor=(0.5,-0.3),loc="center",ncol=3,fontsize=8,frameon=False)

plt.show()
