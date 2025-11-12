#andres bibs
import time
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

    pik =0 
    rssi = [[], [], [], []]
    angles = [[], [], [], []]
    print("Starter svinet")
    tarm.set_zero()
    time.sleep(1)
    while(np.abs(tarm.get_pos()[0])  > 2 ):
        pass
    theta_start = -45
    theta_stop = 135
    for i in range(4):
        sw.set_switch(i)
        tarm.set_pos(theta_start, 10)
        time.sleep(0.2) 
        for a in np.linspace(theta_start, theta_stop, 180):
            tarm.set_pos(a, 10) 
            while(np.abs(tarm.get_pos()[0] - a) > 2):
                pass
            time.sleep(0.01)
            beacon_decoder.flush()
            while(beacon_decoder.avaliable() == False):
                pass
            rssi_sample, corr_sample = beacon_decoder.get_lastest()
            rssi[i].append(rssi_sample)
            angles[i].append(tarm.get_pos()[0] / 180 *np.pi)

    df = pd.DataFrame()
    for i in range(4):
        df[f"rssi{i}"] = rssi[i]
        df[f"theta{i}"] = angles[i]

    df.to_csv("walla.csv", index=False)
    fig = plt.figure()
    ax = []
    regnbue = ['r', 'g', 'b', 'm']
    ax.append(fig.add_subplot(111, projection="polar", label="0"))
    for i in range(1, 4):
        ax.append(fig.add_subplot(111, projection="polar", label=f"{i}", frame_on=False))
        ax[i].set_yticklabels([])     # Hide radial labels
        ax[i].set_yticks([])          # Hide radial ticks
        ax[i].grid(False)             # Hide grid lines

    
    # Plotting the data

    for i in range(4):
        ax[i].plot(angles[i], rssi[i], label=f"SW={i}", color=regnbue[i])


        
    fig.legend()
    plt.show()

