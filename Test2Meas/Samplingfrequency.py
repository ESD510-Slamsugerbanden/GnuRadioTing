import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if __name__== "__main__":

    data = [0,0,0]
    data[0] = pd.read_csv("12rpm1.csv")
    data[1] = pd.read_csv("12rpm2.csv")
    data[2] = pd.read_csv("12rpm3.csv")


    beams = np.array([-48, -15, 15, 48])

    timestamps = [0,0,0]
    angle_est = [0,0,0]
    start_t = 8
    delta_t  = [0, -9, 2.5]
    beam_select = [0,0,0]



    for i in range(3):
        timestamps[i] = data[i]["Times"] - data[i]["Times"][0] + delta_t[i] - start_t
        angle_est[i] = np.rad2deg(data[i]["Angles"])

        compare_matrix = np.outer(np.ones(len(angle_est[i])),beams)
        

        temp = np.outer(angle_est[i], np.transpose([1,1,1,1]))
        error = np.abs(compare_matrix -temp)

        idx = error.argmin(axis=1)
        
        
        beam_select[i] = beams[idx]



    plt.plot(timestamps[0], beam_select[0], linewidth=2, label="Beam selected 1")
    plt.plot(timestamps[1], beam_select[1], linewidth=2, label="Beam selected 2")
    plt.plot(timestamps[2], beam_select[2], linewidth=2, label="Beam selected 3")

    plt.scatter(timestamps[0], angle_est[0], s=4, label="Source estimate 1")
    plt.scatter(timestamps[1], angle_est[1], s=4, label="Source estimate 2")
    plt.scatter(timestamps[2], angle_est[2], s=4, label="Source estimate 3")
    plt.ylabel("Angle estimation [°]")
    
    plt.xlabel("time [s]")
    plt.tight_layout()
    plt.xlim([0,30])
    plt.legend()
    plt.grid(True)
    plt.show()