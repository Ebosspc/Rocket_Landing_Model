# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 17:41:46 2021
2
@author: Ethan Francolla
"""


'''
SECTION 1-Vertical Takeoff-
    
Introducary Remarks:
This model is designed to show a rocket's trajectory, from takeoff to landing.
It describes the trajectory as vertical position with repect to time.
This model is only tracking vertical position in time because the other
assuptions made make it easier to assume a 2d plane for modeling and
a seperate set of equations to model drag, and jsut output
it into the 2d plane. Even if it were trackign in a 3d plane, those beneifts
would not matter due to the other assumptions and sources of error contained
within the model


Important Notes:
The y-axis can be seen as the altitude, or distance above ground (in meters)
The x-axis can be seen as the time passed(in seconds)
The sequence of events necessary to land the rocket will start the
second that the rocket is at its apex, and has 0 upwards velocity
At that point systems will  orient the rocket properly as it descends,
freefalling for a while beforedoing a rentry burn. 
Then, right before it hits the ground, the rocket will do a landing burn
to bring its velocity from the terminal velocity it was falling with to a 
stop, rigt as it touches the ground, landing verically.

Assumptions: 
The rocket launches from the ground starting at a velocity of zero
The postiiton of the rocket accross the bounds of the model is one-dimentional
Therefore, it goes straight up and then straight down
As the engine is burning it pushes the rocket with constant acceleration
Engine cutoff is instantaneous and immidiately sets the acceleration to 0
Obviously, gravity will still be acting on the rocket, during engine cutoff.
The rocket launches from the ground starting at a velocity of zero
The postiiton of the rocket accross the bounds of the model is one-dimentional
Therefore, it goes straight up and then straight down
As the engine is burning it pushes the rocket with constant acceleration
Engine cutoff is instantaneous and immidiately sets the acceleration to 0
Gravity remains constant thoughout the model
Air resistance is negligable
Thrust generated by orientation systems is negligable
After the rentry burn is complete the rocket will be 
at termial velocity, which is stored as its own variable throughout different
sections of the code
'''

import math #Library for mathematical functions
import matplotlib #Library for plotting functions
import matplotlib.pyplot as plt #Library for plotting functions

#Setting variables
dt = 1 # 1 second incrememnt
cutoff = 120 #How long engines will burn before stopping
g= 9.81 # acceleration due to gravity in m/s^2
#acc = 35
theta = 45 #angle from horizontal
y = [0] #creating a blank array as we will want to store y throughout model
vy=[0] #creating a blank array as we will want to store vy throughout model
t = [0] #Create empty array t to store differnt time values
time= 0
vyi = 0
yi = 0
F = 3000000 #Force (Newtons) generated by 1 raptor engine
dm = 300000 #Dry mass (kg) of the rocket
wm = 3000000 #Wet Mass of the rocket at liftoff
A = 630 # cross section area of bellyflop
Cd = 1.18 #bellyflop drag coefficient
drag=[] #Setting the value of drag to an array
accy= (30*F)/(wm) #acceleration produced by 30 raptor engines



#For Loop describing engine accelerating and then cutting off at time t=8
for i in range(1,600):
    if i==cutoff: #sets acceleration to 0 during engine cutoff
        accy =0
    vyf= vyi + (accy-g)*dt
    yf = yi + vyf*dt + (1/2)*(accy-g)*dt**2
    y.append(yf)
    vy.append(vyf)
    time = time+1
    t.append(time) #typo????? there is no array t
    vyi = vyf
    yi = yf   
    if vyf<0: #Break loop if velocity goes below 0
        break






'''
SECTION 2- Reentry-

Assumptions:
Reentry is started when the rocket has reached has reached its maximum height
and its vertical velocity is zero.

Important Notes:
The reentry calculations and modelling or air resisitance
is split up into 3 different sections, each representing different parts
of the atomosphere, with varyign air densiites, resulting in different effects
on the rocket's velocity.
'''

vyin = vyi
yin = yi
#vt= math.sqrt((2*dm*g)/(ro*A*Cd)) #Terminal Velocity
p0 = 101325 #pressure at sea level (Pa)
T0 = 220 #temperature at sea level (K)
L = 0 #temperature lapse rate (K/m)
R = 8.31446 #ideal gas constant J/(mol*K)
M = 0.0289652 #molar mass of dry air (kg/mol)

for i in range(10000):
    #three conditions below for calculating the drag acceleration 
    #depends on height. The first condition is for the troposphere (<10km)
    #the second condition is for the tropopause (constant temp, 10km to 20km)
    #the third condition is above the stratosphere. We're simplifying out assumptions to say no drag above that point
    if yin<10000: #if condition set to go off if the heigh is less than 10000
        L=0.0065
        T0=288.15
        const = (p0*M)/(R*T0)
        exp = ((g*M)/(R*L))-1
        arg = 1-(L*yin/T0)
        ro = const*(arg**exp)
        dragy = (0.5)*ro*(vyin**2)*Cd*A/dm
    elif 10000<=yin<=20000: #if condition if the height is between 10000-20000
        p = p0*math.exp(-g*M*yin/(R*T0))
        ro = (p*M)/(R*T0)
        dragy = (0.5)*ro*(vyin**2)*Cd*A/dm
    elif yin>20000: #if condition 
        dragy=0
    vyf= vyin + (dragy-g)*dt
    yf = yin + vyf*dt + (1/2)*(dragy-g)*dt**2
    y.append(yf)
    vy.append(vyf)
    time = time+1
    t.append(time)
    drag.append(dragy)
    vyin = vyf
    yin = yf
    if yf< 436:
        break
    i=i+1 #After every increment, increase i by 1 in for loop

'''
SECTION 3-LANDING PROCEDURE:
    
The rocket is very close to sea level when performing the final landing burn.
Therefore, varibles relating to the environament aroudn the rocket will stay
constant.
Due to the fact that the change in mass of the rocket will be minimal, as
little fuel will be used, the mass of the rocket throughout the model will
remain constant.
3 Engines will perform the landing burn at the same, constant thrust.
It will be timed so that the velocity of the rocket reaches 0 right
as the rocket hits the ground.
The acceleration due to graivty will not be used, considering the assumption
that the rocket will not exceed terminal velocity.
'''

g= 9.81 # acceleration due to gravity in m/s^2
F = 800679 #Force (Newtons) generated by 1 raptor engine
dm = 300000 #Dry mass of the rocket
dt = 1 # 1 second incrememnt
yi = yf #For initial height (m) set to yf from previous loop
accy= (3*F)/(dm)

for i in range(1000):
    vf =vyin + accy*dt
    yf = yi + vyin*dt + 0.5*accy*dt
    vyin =vf
    yi = yf
    y.append(yf)
    vy.append(vf)
    time = time+1
    t.append(time)
    if yf<0 :
        break
    if vf>0 :
        break
#####plot height with respect to time#####
plt.plot(t, y)
plt.show()

####plot velocity with respect to time####
plt.plot(t, vy)
plt.show()

####plot velocity with repsect to height###
plt.plot (y,vy)
plt.show()