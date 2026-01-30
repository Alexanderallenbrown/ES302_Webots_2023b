"""artybot_demo controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor
from math import sin
import sys
#add ES302 directory to path because Artybot.py is there
sys.path.append("../ES302_Artybot")
from Artybot import Artybot

arty = Artybot(sim=True)
artyHW = Artybot(port='/dev/cu.usbmodem101')#replace with your port!

# get the time step of the current world.
timestep = int(arty.simartybot.getBasicTimeStep())

# sim time for servo positions
simtime = 0.0

while arty.simartybot.step(timestep) != -1:
    #update sim time
    simtime+=timestep/1000.0

    #compute servo commands to send to Arty
    s1pos = 90
    s2pos = 20*sin(simtime+2)+90
    s3pos = 20*sin(simtime)+30

    #update Arty
    arty.update(s1pos,s2pos,s3pos)
    artyHW.update(s1pos,s2pos,s3pos)
    pass

# Enter here exit cleanup code.
