#andres bibs
import numpy as np
import matplotlib.pyplot as plt
import time

from angle_corr import get_rssi ##Simulated RSSI response



class lp_server:


    def __init__(self, w_n, T_s_back):
        import threading
        self.filter = piss_filters.Lowpass(w_n, T_s_back)
        self.T_s = T_s_back
        self.tarm = ez_comm("/dev/ttyUSB0")
        self.thread_handle = threading.Thread(target=self._internal_runner)
        self.pos = self.tarm.get_pos()[0]
        self.start_el = -30

    def start(self):
        self.thread_handle.start()

    def setpos(self, azimuth: float):
        self.pos = azimuth
        
        
    def _internal_runner(self):
        while True:
            flt = self.filter.filter(self.pos)
            self.tarm.set_pos(flt,  self.start_el )
            time.sleep(self.T_s)


    def getpos(self):
        return self.tarm.get_pos()

#vores biblioteker
from Rotax import ez_comm #Uart controller for the motor
from beacon_serde import Beacon_decoder
import switch as sw
import piss_filters


def get_correlation(samples, lookup):
    """Gets the index for max correlation between the two bitches"""
    max_score = -np.inf
    max_i = 0
    corr_scores = [0]*len(lookup)
    for i in range(len(lookup)):
        res = lookup[i]* samples
        corr_scores[i] = np.sum(res)
        if(corr_scores[i] > max_score):
            max_i = i
            max_score = corr_scores[i]
         
    return max_i, corr_scores


if __name__ == "__main__":

    scanwidth = np.deg2rad(40)
    n = 10
    sim_results = [[float,float,float,float]]*n
    theta_array = np.linspace(-scanwidth, scanwidth, n)
    for i in range(n):
        sim_results[i] = np.abs(get_rssi(theta_array[i]))
        sim_results[i] = np.divide(sim_results[i], np.sqrt(np.sum(np.square(sim_results[i]))))#np.divide(sim_results[i], np.sum(sim_results[i]))
        #sim_results[i] = sim_results[i] - np.arange(4)*np.mean(sim_results[i]) 
    ##Calulates fixed possible simulated results
    #tarm_serv = lp_server(6.28, 0.05)
    
    #tarm = ez_comm("/dev/ttyUSB0")
    #azimuth = tarm.get_pos()[0]
    azimuth = 0 
    rssi_calibration = [np.float64(5.135578199722128), np.float64(8.464705345695965), np.float64(6.794669667876534), np.float64(7.907608195544618)]
    rssi_calibration = np.divide(1, rssi_calibration)
    rssi_calibration = np.divide(rssi_calibration, np.max(rssi_calibration))
    

    beacon_decoder = Beacon_decoder(my_id=1) #Sets up a decoder looking for the given ID
    beacon_decoder.start() #starts the decoder in the background
    plt.ion()
    beam_offsets = [48, 15, -15, -48]
    fig = plt.figure()
    regnbue = ['r', 'g', 'b', 'm']
    ax = fig.add_subplot()
    line = ax.plot([], [])
    line2 = ax.plot([], [])
    line3 = ax.plot([], [])
    ax.set_ylim(-40,40)
    ax.set_xlim(min(beam_offsets)-10, max(beam_offsets)+10)

    w_n = 1*2*np.pi
    T_s = 1/4
    filters = [piss_filters.Lowpass(w_n, T_s), piss_filters.Lowpass(w_n, T_s), piss_filters.Lowpass(w_n, T_s), piss_filters.Lowpass(w_n, T_s)]


    #print(line)
    T_s = 256/8 * 1/4
    k_i = 0.8
    rssi = [0]*4
    rssi_flt  =[0] * 4
    i = 0
    while(True):
        sw.set_switch(i)
        beacon_decoder.flush()
        while(beacon_decoder.avaliable() == False):
            pass
            plt.pause(0.01)
        beacon_decoder.flush()
        while(beacon_decoder.avaliable() == False):
            pass
            plt.pause(0.01)


        rssi_temp, corr = beacon_decoder.get_lastest()
        rssi_flt[i] = rssi_temp * rssi_calibration[i] #filters[i].filter(rssi_temp)
        #rssi_offset = rssi_flt - np.arange(len(beam_offsets))*np.mean(rssi_flt)
        i_theta, scores = get_correlation(rssi_flt, sim_results)
        azimuth -= T_s * k_i * theta_array[i_theta]
        #tarm.set_pos(azimuth, 0)

        if(i==0):
            #print(azimuth)
            line[0].set_data(beam_offsets, rssi_flt)
            line2[0].set_data(beam_offsets, sim_results[i_theta]*10)
            line3[0].set_data(np.linspace(-np.rad2deg(scanwidth), np.rad2deg(scanwidth), len(scores)), np.multiply(scores, 1))
            pass
            #print(rssi_flt)
            #print(np.rad2deg(theta_array[i_theta]))
        i = (i+1) % 4
        #ax.relim()
        #ax.autoscale_view()

