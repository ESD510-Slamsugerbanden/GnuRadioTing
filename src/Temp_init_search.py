from switch import *
from Rotax import ez_comm
from beacon_serde import Beacon_decoder
import numpy as np
import time 
import matplotlib.pyplot as plt



tarm = ez_comm("/dev/ttyUSB0") #controller for the arm
beacon_decoder = Beacon_decoder(my_id=1) #Sets up a decoder looking for the given ID
beacon_decoder.start() #starts the decoder in the background
Max_elevation = 50
Min_elevation = 10


def DnC_search(Vinkel1=30, Vinkel2=60, step=4, max_elevation=0, min_elevation=0, angle=0):
            """Simple step-search (divide-and-conquer flavor):
            1) mål RSSI ved Vinkel1 og Vinkel2
            2) vælg den bedst og step i den retning (op hvis Vinkel2 var bedst, ned hvis Vinkel1 var bedst)
            3) stop når RSSI ikke forbedres eller når vi rammer grænser
            Returnerer (best_elevation, best_rssi).
            """         
            tarm.set_pos(angle, Vinkel1)  
            r1 = beacon_decoder.get_lastest()
            tarm.set_pos(angle, Vinkel2)
            r2 = beacon_decoder.get_lastest()

            if r2 > r1:
                start = Vinkel2
                direction = 1
                best_rssi = r2
            else:
                start = Vinkel1
                direction = -1
                best_rssi = r1

            best_elev = start
            current_elev = start + direction * step
            while min_elevation <= current_elev <= max_elevation:
                r = beacon_decoder.get_lastest()
                if r > best_rssi:
                    best_rssi = r
                    best_elev = current_elev
                    current_elev = current_elev + direction * step
                else:
                    break

            return best_elev, best_rssi



def search_initial_location():
    beam_offsets = [48, 15, -15, -48]
    RSSI_array = []
    angle_array = []
    tarm.set_pos(0,10) #Antager at vi kun kan elevation 0-90 grader så vi starter lige på 30 grader og +30 efter
    
    
    time.sleep(0.2)
    for angle in np.linspace(0,180,5): #Deler 360 grader op i 4 dele så vi kan gætte os hurtigere frem til den bedste vinkel
        tarm.set_pos(angle,10)
        while((tarm.get_pos()[0]- angle)>5):
            time.sleep(0.01)

        for i in range(4):
            set_switch(i)
            beacon_decoder.flush()
            while(beacon_decoder.avaliable()==False):
                time.sleep(0.001)
            beacon_decoder.flush()            
            while(beacon_decoder.avaliable()==False):
                time.sleep(0.001)
            
            RSSI_array.append(beacon_decoder.get_lastest()[0])
            angle_array.append(tarm.get_pos()[0] + beam_offsets[i])
    
    max_rssi = max(RSSI_array)
    max_index = RSSI_array.index(max_rssi)
    max_angle = angle_array[max_index]


    tarm.set_pos(max_angle - beam_offsets[1],30) #Sætter antennen til den bedste vinkel fundet vi er kun interesseret i azimuth her
    set_switch(1) #Sætter switchen til den bedste beam fundet

    
    plt.scatter(angle_array, RSSI_array)
    plt.show()
    time.sleep(1)


    best_elevation, best_rssi = DnC_search(Vinkel1= 20, Vinkel2= 40, step=2, max_elevation=Max_elevation, min_elevation=Min_elevation, angle=angle_array[index[0]])
    
    
    
    tarm.set_pos(angle_array[index[0]], best_elevation)
        
    switch_pos = index[1]
    angle_pos = angle_array[index[0]]
    
    return angle_pos, switch_pos, best_elevation
    
 

search_initial_location()

