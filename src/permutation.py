import numpy as np
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import piss_filters as flt
#from get_rssi import get_rssi



class permutation_controller:
    def __init__(self, T_s, start_theta):
        self.w_n = 0.8*np.pi
        self.highpass = flt.Highpass(self.w_n, T_s)
        self.lowpass = flt.Lowpass(self.w_n, T_s)
        self.hp_theta = flt.Highpass(self.w_n, T_s)
        self.lp_theta  = flt.Lowpass(self.w_n*8, T_s)
        self.T_s = T_s
        self.permu_A = np.deg2rad(8) #How big should the permutation be in radians
        self.ki = 4
        self.ki2 = 0
        self.w_per = 1*np.pi
        self.probe_counter = 0
        self.theta_i = start_theta
        self.theta_i2 = 0
        self.permutation = 0
        self.i_log = []
        self.hp_log = []
        self.last = 0
        pass

    def compute(self, rssi, true_theta):
        d_theta = self.hp_theta.filter(true_theta)
        d_theta = self.lp_theta.filter(d_theta)
        est_perm = np.sin(self.probe_counter * self.T_s * self.w_per - np.deg2rad(20))
        print(d_theta)
        hp_res = self.highpass.filter(rssi)
        temp = self.lowpass.filter(self.T_s * d_theta   * hp_res * self.ki) 
        self.theta_i += temp
        self.theta_i2 += self.theta_i / self.ki
        self.permutation = self.permu_A * np.sin(self.probe_counter * self.T_s * self.w_per)
        self.probe_counter += 1
        return self.permutation + self.theta_i + self.theta_i2 * self.ki2


#andres bibs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#vores biblioteker
from Rotax import ez_comm #Uart controller for the motor
from beacon_serde import Beacon_decoder
import switch as sw


if __name__ == "__main__":
    tarm = ez_comm("/dev/ttyUSB0") #controller for the arm
    beacon_decoder = Beacon_decoder(my_id=1) #Sets up a decoder looking for the given ID
    beacon_decoder.start() #starts the decoder in the background
    tarm.set_pos(0, 20)
    T_s = 8/(128)
    sw.set_switch(1)
    ctrl = permutation_controller(T_s, np.deg2rad(0))

    while(True):
        if(beacon_decoder.avaliable()):
            rssi, corr = beacon_decoder.get_lastest()   
            azi, _ = tarm.get_pos()
            theta = np.rad2deg(ctrl.compute(rssi, np.deg2rad(azi)))
            theta = min(theta, 90)
            theta = max(theta, -90)
            if theta != float('nan'):
                tarm.set_pos(theta, 0)
            print("RSSI {:.2f},\t Theta: {:.2f}\t DIR:{:.2f} \n".format(rssi, theta, ctrl.theta_i))
