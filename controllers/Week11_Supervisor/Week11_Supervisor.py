from controller import Supervisor
from PIL import Image, ImageOps
import numpy as np

robot = Supervisor()  # create Supervisor instance
#open a file
f = open("supervisor_data.txt",'w')
#write a format line to the top
f.write("time, robot_x, robot_y\r\n")

# get access to our two robots in the world
myromi = robot.getFromDef('Romi')
#get the timestep from one of them
timestep = int(robot.getBasicTimeStep())
print("supervisor timestep: "+str(timestep))

root_node = robot.getRoot()
#get access to the children of the root note (environment)
children_field = root_node.getField('children')

simtime = 0
i = 0

#set up the map properties
map_m = 20 #20x20 map
map_d = 0.1 #10 cm grid size

#initialize a variable to say whether the map is square (it must be)
good_map = False
#load image representing map. We will resize.
im = Image.open("map.png")
im = ImageOps.grayscale(im)
#resize image to our map params
im2 = im.resize((map_m,map_m))
#convert image to true black and white
im2.convert("1")
# im.show("map")
#load into a numpy array
map = np.array(im2)
#now loop through and place a crate at every occupied cell
occupied_thresh = 200 #threshold for grayscale image to consider a pixel occupied
w,h = map.shape
#convert map to BINARY occupancy grid
for i in range(0,h):
    for j in range(0,w):
        if map[i,j]>=occupied_thresh:
            map[i,j]=1
        else:
            map[i,j]=0



for i in range(0,h):
    for j in range(0,w):
        if map[i,j]==1:
            #we have now found an occupied cell. Place a box here.
            #print("found object at i="+str(i)+",j="+str(j))
            children_field.importMFNodeFromString(-1, "WoodenBox {translation "+str(map_d/2+j*map_d)+" "+str(map_m*map_d - (map_d/2+i*map_d))+" 0.05  size 0.1 0.1 0.1 }")

while robot.step(timestep) != -1:
  #get the positions of each robot
  myromi_pos = myromi.getPosition()
  #write them to file in the specified format
  f.write(str(simtime)+","+str(myromi_pos[0])+","+str(myromi_pos[1])+"\r\n")
  #update simtime
  simtime+=timestep

f.close()
