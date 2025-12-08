import numpy as np
import pandas as pd
from beacon_serde_vs import Beacon_decoder
from Rotax import ez_comm
import time

from static_scanner import get_sim_vectors


rssi_values = []
corr_values = []
timestamp_values = []
theta_values = []



if __name__ == "__main__":
    
    beacon_decoder = Beacon_decoder()
    beacon_decoder.begin()

    tarm = ez_comm("/dev/ttyUSB0") #controller for the arm

    minmax = (-90,90)
    n = 100
    Angles = np.linspace(minmax[0], minmax[1],n)

    for theta in Angles:
        tarm.set_pos(theta, 10) 
        while(np.abs(tarm.get_pos()[0] - theta) > 2):
            pass
        time.sleep(0.01)
        for i in range(32):
            print(f"meas theta={theta}, i={i}")
            beacon_decoder.flush()
            while(beacon_decoder.avaliable() == False):
                pass
            rssi_sample, corr_sample = beacon_decoder.get_values()

            rssi_values.append(rssi_sample)
            corr_values.append(corr_sample)
            timestamp_values.append(time.time())
            theta_values.append(tarm.get_pos()[0])


    raw_rssi = pd.DataFrame()

    raw_rssi["rssi"] = rssi_values
    raw_rssi["corr"] = corr_values
    raw_rssi["theta"] = theta_values
    raw_rssi["timestamp"] = timestamp_values
    
    raw_rssi.to_csv("RAW angular measurements.csv")

    