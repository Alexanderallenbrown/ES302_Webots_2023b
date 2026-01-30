class Timer:
    def __init__(self,preset):
        #current "state" of the timer
        self.state = False
        #current elapsed time
        self.elapsed = 0
        #timer will go true if it has counted for more than 1 second
        self.preset = preset
    def update(self,ENABLE,dt):
        #dt is the timestep by which we should count up. make sure its units match your preset!
        #don't set the preset in seconds and increment the elapsed time in milliseconds, for example!
        #ENABLE is a boolean. When it is true, we run up the timer. When it is not, the time resets and we stop counting.
        if(ENABLE):
            #increment time by dt
            self.elapsed+=dt
            self.state=self.elapsed>=self.preset
        else:
            self.elapsed=0
            self.state=False

class exploreFSM:
    def __init__(self):
        #initialize FSM to start in wait
        self.WAIT = True
        self.TURN = False
        self.FWD = False


    def update(self,prox,T0,T1):
        #latch on wait, waits for T0 to expire
        t1 = self.WAIT and not T0
        #transition from wait to FWD. timer up and forward clear
        t2 = self.WAIT and T0 and not(prox)
        #transition from wait to turn
        t3 = self.WAIT and T0 and prox
        #latch on Turn
        t4 = self.TURN and not T1
        #transition from turn to wait
        t5 = self.TURN and T1
        #latch on forwards
        t6 = self.FWD and not prox
        #transition from fowards to wait
        t7 = self.FWD and prox

        #block 3: set States
        self.WAIT = t1 or t7 or t5
        self.TURN = t3 or t4
        self.FWD = t6 or t2
