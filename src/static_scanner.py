#andres bibs
import numpy as np
import matplotlib.pyplot as plt
import time


#vores biblioteker
from Rotax import ez_comm #Uart controller for the motor
from beacon_serde import Beacon_decoder
import switch as sw
import piss_filters

if __name__ == "__main__":
    beacon_decoder = Beacon_decoder(my_id=1) #Sets up a decoder looking for the given ID
    beacon_decoder.start() #starts the decoder in the background
    plt.ion()
    fig = plt.figure()
    regnbue = ['r', 'g', 'b', 'm']
    ax = fig.add_subplot(111, projection="polar", label="0")
    line = ax.plot([], [])
    ax.set_ylim(0,6)

    w_n = 1
    T_s = 1/4
    filters = [piss_filters.Lowpass(w_n, T_s), piss_filters.Lowpass(w_n, T_s), piss_filters.Lowpass(w_n, T_s), piss_filters.Lowpass(w_n, T_s)]


    print(line)
    angles = [np.deg2rad(45), np.deg2rad(15), np.deg2rad(-15), np.deg2rad(-45)]
    rssi = [0]*4
    rssi_flt  =[0] * 4
    i = 0
    while(True):
        sw.set_switch(i)
        beacon_decoder.flush()
        while(beacon_decoder.avaliable() == False):
            plt.pause(0.001)
        rssi[i], corr = beacon_decoder.get_lastest()
        rssi_flt[i] = filters[i].filter(rssi[i])
        
        line[0].set_data(angles, rssi_flt)
        i += 1
        if (i > 3):
            i = 0
            
            #plt.draw()
            print(f"{rssi}")

        #ax.relim()
        #ax.autoscale_view()

