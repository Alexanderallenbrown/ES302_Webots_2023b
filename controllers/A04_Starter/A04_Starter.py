"""ES302 Assignment 04 Starter Code."""
#import the sys library so we can get path above
import sys
#add ES302 directory to path because Romi.py is there
sys.path.append("../ES302_Romi")
#now import the Romi library
from Romi import Romi

# create the Robot instance.
#instantiating a Romi library object in simulation mode
#automatically loads proper WeBots libraries.
#the webots robot class lives inside of romi.simromi
romi = Romi(sim=True)

# get the time step of the current world.
timestep = int(romi.simromi.getBasicTimeStep())

#this Romi has light sensors. Let's get them!
lightSensorL = romi.simromi.getDevice("lightSensorLeft")
lightSensorR = romi.simromi.getDevice("lightSensorRight")
#sensors have to be enabled before use
lightSensorR.enable(timestep)
lightSensorL.enable(timestep)
#values to hold the sensor info we need
proxFrontVal = 0
lightLeft = 0
lightRight = 0


# Main loop:
# - perform simulation steps until Webots is stopping the controller
while romi.simromi.step(timestep) != -1:
    ###### YOUR FSM CODE GOES here

    ####### END YOUR FSM CODE.

    #update the Romi with commands
    #motor left (-400,400), motor right (-400,400), servo 1 (0,180), servo 2 (0,180), servo 3 (0,180)
    romi.update(0,0,90,90,90)
    #read the prox sensors we added
    proxReading = romi.proxFrontVal
    lightLeft = lightSensorL.getValue()
    lightRight = lightSensorR.getValue()
    print("Prox: "+str(proxReading)+", lightLeft: "+str(lightLeft)+", lightRight: "+str(lightRight))
