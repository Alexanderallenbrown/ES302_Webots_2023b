"""Week 09 Starter controller.
The task for this controller is to make the Romi go to a desired
location in allocentric coords with a particular yaw angle psi.

To do this, we will use inverse differential kinematics! Textbook section 3.4
"""
#import the sys library so we can get path above
import sys
#add ES302 directory to path because Romi.py is there
sys.path.append("../ES302_Romi")
#now import the Romi library
from Romi import Romi
from numpy import *

# create the Robot instance.
#instantiating a Romi library object in simulation mode
#automatically loads proper WeBots libraries.
#the webots robot class lives inside of romi.simromi
romi = Romi(sim=True)

#goal forward speed and yaw rate of Romi
goalU = .1
goalPsidot = 1

# get the time step of the current world.
timestep = int(romi.simromi.getBasicTimeStep())

#values for getting joint velocities
oldLeftEncoder = 0#value for old left encoder (for velocity computation)
oldRightEncoder = 0 #old right encoder

#values to hold velocities
omega_left = 0
omega_right = 0

#variables to hold allocentric romi estimates
Xromi = 0
Yromi = 0
#variables to hold egocentric romi estimates
U = 0
psidot = 0
psi = 0
simtime = 0

# romi parameters
r_romi = .07438
r_wheel = .035

#update velocity esimates
def updateQdots():
    global oldRightEncoder,oldLeftEncoder,omega_right,omega_left
    pass

#update romi-local velocities
def updateVelocities():
    global omega_left,omega_right,r_romi,psidot,U
    pass

def updateOdometry():
    global Xromi,Yromi,psi,psidot,timestep,U
    pass

def calcJac():
    global r_wheel,r_romi
    #TODO fill in!
    return np.array([[0,0],[0,0],[0,0]])

def pseudoInv(J):
    return J #TODO fill in!!

def computeMotorCommands(Jplus,e):
    #TODO fill in!!
    return 0,0


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while romi.simromi.step(timestep) != -1:
    simtime += timestep/1000.0

    #update estimates of romi wheel velocities
    updateQdots()
    #update estimates of Romi local updateVelocities
    updateVelocities()
    #update estimates of Romi Position
    updateOdometry()
    #now compute the current Jacobian for forward differential kinematics
    J = calcJac()
    #now compute the pseudo-inverse of Ja
    Jplus = pseudoInv(J)
    #now compute the desired omegas
    mLeft,mRight = computeMotorCommands(Jplus,np.array([[goalU],[0],[goalPsidot]]))
    print(e)
    print(Xromi,Yromi,psi)
    romi.update(mLeft,mRight,90,90,90)
