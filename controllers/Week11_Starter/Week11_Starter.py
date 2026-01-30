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
from PIL import Image, ImageOps
import numpy as np
from dijkstra import dijkstras

#create a file to write results to:
f = open('Week11_Data.txt','w')

# create the Robot instance.
#instantiating a Romi library object in simulation mode
#automatically loads proper WeBots libraries.
#the webots robot class lives inside of romi.simromi
romi = Romi(sim=True)

# get the time step of the current world.
timestep = int(romi.simromi.getBasicTimeStep())

#get the GPS sensor we added to Romi
gpsSensor = romi.simromi.getDevice("gps")
#enable the GPS
gpsSensor.enable(timestep)
#get the IMU sensor
imuSensor = romi.simromi.getDevice("imu")
imuSensor.enable(timestep)
#get the perfect distance sensor
perfectDistanceSensor = romi.simromi.getDevice("perfectDistanceSensor")
perfectDistanceSensor.enable(timestep)

T0 = Timer(1000)
T1 = Timer(1000)
FSM = exploreFSM()
proxReading = 0

oldLeftEncoder = 0#value for old left encoder (for velocity computation)
oldRightEncoder = 0 #old right encoder

#values to hold velocities
vLeft = 0
vRight = 0

#variables to hold allocentric romi estimates
Xromi = 0
Yromi = 0
#variables to hold egocentric romi estimates
U = 0
psidot = 0

simtime = 0


############### MAP STUFF ###################
#set up the map properties
map_m = 20 #20x20 map
map_d = 0.1 #10 cm grid size

#initialize a variable to say whether the map is square (it must be)
good_map = False
#load image representing map. We will resize.
im = Image.open("../Week11_Supervisor/map.png")
im = ImageOps.grayscale(im)
#resize image to our map params
im2 = im.resize((map_m,map_m))
#convert image to grayscale
im2.convert("1")
#load into a numpy array
map = np.array(im2)
#now loop through and place a crate at every occupied cell
occupied_thresh = 200 #threshold for grayscale image to consider a pixel occupied
w,h = map.shape
#convert map to BINARY occupancy grid
for i in range(0,map_m):
    for j in range(0,map_m):
        if map[i,j]>=occupied_thresh:
            map[i,j]=1
        else:
            map[i,j]=0

#set start position for Romi
start = np.array([[.1], [.1], [0]])
#set a goal position for the Romi
goal = np.array([[.3], [.3], [0]])
#now do path planning using dijkstras algorithm

method = 0

if(method == 0):
    # USAGE: dijkstras(occupancy_map, x_spacing, y_spacing, start, goal)
    path = dijkstras(map,map_d,map_d,start,goal)
else:
    planner = PathPlanner(map,True)
    init,path = planner.a_star(start,goal)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while romi.simromi.step(timestep) != -1:
    simtime += timestep/1000.0
    ### FSM block 1: inputs, timers, and counters

    #compute Romi encoder velocities in COUNTS PER SECOND
    vLeft = (romi.encLeft - oldLeftEncoder)/(timestep/1000.0)
    vRight = (romi.encRight - oldRightEncoder)/(timestep/1000.0)

    #use to get estimates of U, psidot using vLeft and vRight
    U = 0 #  TODO: implement this!
    psidot = 0 # TODO: implement this!

    #use to get estimates of current romi X, and Y in allocentric frame
    #using odometry:
    Xromi = 0 #TODO implement this!
    Yromi = 0 #TODO implement this!

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
        romi.update(100,100,120,0,110)
    elif(FSM.TURN):
        romi.update(100,-100,120,0,110)
    elif(FSM.WAIT):
        #stop
        romi.update(0,0,95,0,110)
    else:
        print("state machine broken")
        romi.update(0,0,90,90,90)
    proxReading = romi.proxFrontVal

    #print(perfectDistanceSensor.getValue())

    #now write Romi's estimates to a file. to start, let's write our X,Y estimates
    f.write(str(simtime)+","+str(Xromi)+","+str(Yromi)+"\r\n")
