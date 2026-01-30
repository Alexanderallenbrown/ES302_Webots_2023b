import numpy as np
import matplotlib.pyplot as plt


#load supervisor_data. numpy can automatically unpack columns
#to know what columns there are, see the data file. We skip first row, which has headers.
time,robot_x,robot_y = np.loadtxt('supervisor_data.txt',delimiter=',',skiprows=1,unpack=True)

#convert time to seconds
time = time/1000.0

#plot x and y vs time
plt.figure()
plt.subplot(121)
plt.plot(time,robot_x,'k')
plt.ylabel('Robot X (m)')
plt.subplot(122)
plt.plot(time,robot_y,'k')
plt.xlabel('Time (s)')
plt.ylabel('Robot Y (m)')


#now plot the XY plane view of robot motion
plt.figure()
plt.plot(robot_x,robot_y,'k.')
plt.xlabel('Robot X (m)')
plt.ylabel('Robot Y (m)')
plt.axis('equal')

plt.show()
