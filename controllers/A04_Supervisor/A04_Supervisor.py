from controller import Supervisor
robot = Supervisor()  # create Supervisor instance
#open a file
f = open("A04_data.txt",'w')
#write a format line to the top
f.write("time, leader_x, leader_y, follower_x, follower_y\r\n")

# get access to our two robots in the world
leader = robot.getFromDef('Romi_Leader')
follower = robot.getFromDef('Romi_Follower')
#get the timestep from one of them
timestep = int(robot.getBasicTimeStep())
print("supervisor timestep: "+str(timestep))

root_node = robot.getRoot()

simtime = 0

i = 0
while robot.step(timestep) != -1:
  #get the positions of each robot
  follower_pos = follower.getPosition()
  leader_pos = leader.getPosition()
  #write them to file in the specified format
  f.write(str(simtime)+","+str(leader_pos[0])+","+str(leader_pos[1])+","+str(follower_pos[0])+","+str(follower_pos[1])+"\r\n")
  #update simtime
  simtime+=timestep

f.close()
