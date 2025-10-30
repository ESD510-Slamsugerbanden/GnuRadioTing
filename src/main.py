import time


from Rotax import ez_comm #Uart controller for the motor
from beacon_serde import Beacon_decoder








if __name__ == "__main__":
    tarm = ez_comm("/dev/ttyUSB0") #controller for the arm
    beacon_decoder = Beacon_decoder(my_id=1) #Sets up a decoder looking for the given ID

    beacon_decoder.start() #starts the decoder in the background
    
    
    while(True):
        time.sleep(0.5)
        
        print("Angle: {:.1f}, RSSI & CORR: {:.1f}".format(tarm.get_pos()[1], ))
        

