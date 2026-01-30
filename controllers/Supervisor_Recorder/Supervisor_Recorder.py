from controller import Supervisor
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

simtime = 0

i = 0
while robot.step(timestep) != -1:
  #get the positions of each robot
  myromi_pos = myromi.getPosition()
  #write them to file in the specified format
  f.write(str(simtime)+","+str(myromi_pos[0])+","+str(myromi_pos[1])+"\r\n")
  #update simtime
  simtime+=timestep

f.close()
