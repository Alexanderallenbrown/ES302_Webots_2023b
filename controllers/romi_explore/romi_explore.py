"""romi_test controller."""
#import the sys library so we can get path above
import sys
#add ES302 directory to path because Romi.py is there
sys.path.append("../ES302_Romi")
#now import the Romi library
from Romi import Romi
#import sine function to use
from exploreFSM import exploreFSM,Timer
import random


# create the Robot instance.
#instantiating a Romi library object in simulation mode
#automatically loads proper WeBots libraries.
#the webots robot class lives inside of romi.simromi
romi = Romi(sim=True)

# get the time step of the current world.
timestep = int(romi.simromi.getBasicTimeStep())

T0 = Timer(1000)
T1 = Timer(1000)
FSM = exploreFSM()
proxReading = 0

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while romi.simromi.step(timestep) != -1:
    #update the timers: FSM block 1
    #timer 0 should run when in wait
    T0.update(FSM.WAIT,timestep)
    #if we are in wait, choose a random duration for the turn timer.
    if(FSM.WAIT):
        T1.preset = random.randrange(1000,4000)
    #T1 should run if we are in the turn state
    T1.update(FSM.TURN,timestep)

    #Now update the FSM itself.
    FSM.update((proxReading>700),T0.state,T1.state)
    #now block 4: do what needs to be done in each state
    if(FSM.FWD):
        romi.update(100,100,95,0,110)
    elif(FSM.TURN):
        romi.update(100,-100,95,0,110)
    elif(FSM.WAIT):
        #stop
        romi.update(0,0,95,0,110)
    else:
        print("state machine broken")
        romi.update(0,0,90,90,90)
    proxReading = romi.proxFrontVal
    #print("Prox: "+str(proxReading))
