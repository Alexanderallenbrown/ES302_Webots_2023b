##
# @mainpage ES302 Artybot Library
# @section description_main Description
# Library for interacting with the Lafayette ES302 Artybot Robot. This library's primary class is the Artybot class, which can be set up to control either a simulation of the Artybot in Webots (requires Webots) or a real Artybot robot that is connected through a serial port (hardware or bluetooth).
#
#@section notes_main Notes
# The library depends on the pySerial library for interacting with a real robot, and it depends on Webot's Robot class for interacting with a simulated Artybot.
#
#The philosophy of the library is based on "call and response," so when the Artybot'sgiven commands, it responds with the latest sensor readings. Using the Library requires uploading the Artybot Arduino firmware to the robot before use. That firmware is included in the firmware/ folder, and includes a variant for wired communication..
#
#You can find examples for using the library in the examples/ folder.
#
#Written by Alexander Brown
#October 2022
import serial
import time


class Artybot:
    """!Artybot robot object represents either a simulated robot or a real robot. Default is a real robot; set sim=True to change"""
    def __init__(self,sim=False,port='COM5',baud=115200):
        """!initializes artybot. Servo 1 tilts artybot's arms. 90 degrees should be flat. Servo 2 is Arm 1 (middle arm). 90 degrees means arm points straight out from base (before bend). Servo 3 is Arm 2 (end effector arm). 90 degrees points straight from bent part of middle arm.
        @param sim  Whether this robot is simulated or real (default False)
        @param port port to use when connecting to a real Artybot (default 'COM5')
        @param baud baud rate too use when connecting to a real Artybot (default 115200)
        """
        ## the serial port for communicating with a real Artybot
        self.port = port
        ## the baud rate for communicating with real Artybot
        self.baud= baud

        ## the servo 1 (base tilt) command (0,180)
        self.servo_1Command = 90
        ## the servo 2 (arm 1) command (0,180)
        self.servo_2Command = 90
        ## the servo 3 (arm 2) command (0,180)
        self.servo_3Command = 90

        ## Boolean flag for whether this robot is simulated or hardware
        self.Sim = sim
        ## Boolean flag for whether the last feedback packet was properly parsed.
        self.goodReply = False
        ## raw serial (or simulated serial) text-based datastring for robot feedback
        self.datastring = ''
        if(self.Sim):
            self.__initsim__()
        else:
            self.__initSerial__()

    def __initsim__(self):
        """! initializes a simulated robot. Requires Webots's Robot() class (not for user use)"""
        from controller import Robot, Motor
        self.simartybot = Robot()
        self.timestep = self.simartybot.getBasicTimeStep()

        self.simS1 = self.simartybot.getDevice("servo_1")
        self.simS3 = self.simartybot.getDevice("servo_3")
        self.simS2 = self.simartybot.getDevice("servo_2")

    def __initSerial__(self):
        """! initializes a hardware robot using serial. Requires the pyserial library (not for user use)"""
        import serial
        self.ser = serial.Serial(self.port,baudrate=self.baud,timeout=.1)
        print("initializing")
        time.sleep(.5)
        #self.ser.open()
        time.sleep(2)
        print("done")

    def __clamp__(self,val,min,max):
        """! clamps robot commands (not for user use)"""
        assert min<max
        if(val<min):
            val=min
        elif val>max:
            val=max
        return val

    def update(self,servo_1Command=90,servo_2Command=90,servo_3Command=90):
        """! Updates the robot by sending commands to it and reading sensor values.
        @param servo_1Command    Servo 1 (tilt) command (0,180)
        @param servo_2Command    Servo 2 (middle arm) command (0,180)
        @param servo_3Command    Servo 3 (end effector) command (0,180)
        @returns    Nothing. Call this function, then access class-owned variables.

        Servo commands in Arduino are in degrees and can range from 0 to 180, although the Artybot arm kit can not necessarily reach those extremes with all servos. Be careful, because it is possible to "lock" the servos or run them into hard limits.

        Feedback from the robot is either read from the serial port (hardware robot) or from Webots (simulated robot). Simulated robot feedback is designed to mimic the hardware Robot as closely as possible.

        Assuming you instantiated a Artybot object called "robot," after calling robot.update(leftWheel,rightWheel,servo1,servo2), you should check robot.goodReply to make sure serial data was parsed correctly.

        If it was, you can then access the robot's encoder, servo, and prox sensor feedback using the class-owned feedback variables.
        robot.encRight, robot.encLeft represent wheel encoder counts
        robot.servo_1Pos, robot.servo_2Pos, and robot.servo_3Pos represent servo analog feedback in ADC counts
        robot.proxFront represents proximity sensor feedback.
        """
        #save commands to object
        self.servo_1Command = self.__clamp__(servo_1Command,0,180)
        self.servo_2Command = self.__clamp__(servo_2Command,0,180)
        self.servo_3Command = self.__clamp__(servo_3Command,0,180)

        if(self.Sim):
            self.__updateSim__()
        else:
            self.__updateHW__()

    def __updateSim__(self):
        """! updates simulation (not for user use)"""


        wb_servo_1c = (self.servo_1Command-90)*3.1415/180
        wb_servo_2c = 3.1415/180*(self.servo_2Command-90)
        wb_servo_3c = -(self.servo_3Command-90)*3.1415/180
        #now send to simulation

        self.simS1.setPosition(wb_servo_1c)
        self.simS2.setPosition(wb_servo_2c)
        self.simS3.setPosition(wb_servo_3c)
        #now get feedback from servos

        self.goodReply=True
        self.datastring = str(self.servo_1Command)+","+str(self.servo_2Command)+","+str(self.servo_3Command)+"\r\n"


    def __updateHW__(self):
        """! updates a real robot (not for user use)"""
        sendstr = "!"+format(int(self.servo_1Command),'d')+","+format(int(self.servo_2Command),'d')+","+format(int(self.servo_3Command),'d')+"\r\n"
        # print("sending:")
        # print(sendstr.encode())
        self.ser.write(sendstr.encode())
        time.sleep(0.001)
        #read reply from Serial
        reply = self.ser.readline().decode('UTF-8')
        #print(reply)
        self.datastring = reply
        reply = reply.strip()
        reply = reply.split(",")
        #print(reply)
        if(len(reply)>=6):
            try:
                self.servo_1Pos = float(reply[2])
                self.servo_2Pos = float(reply[3])
                self.servo_3Pos = float(reply[4])
                self.goodReply = True
            except:
                print("serial parsing failed")
        else:
            #print("BAD LINE")
            self.goodReply = False
