from beacon_serde import Beacon_decoder
import beacon_serde
import Rotax



class mech_tracker():
    
    def __init__(self, starting_angle: tuple[float, float] ,decoder: beacon_serde.Beacon_decoder, platform: Rotax.ez_comm):
        self.current_angle = starting_angle
        self.beacon = decoder
        self.platform = platform
        platform.set_pos(starting_angle)
        pass
    

    def track_iteration(self):
        
        




def mechanicalTrack(initialAngle):

    samples_4_avg = 1
    mech_RSSI_array = [-1000] * samples_4_avg
    aimingAngle = initialAngle
    local_max_RSSI = -1000
    deviation_RSSI = 2
    direction = "left"


    counter = 0
    while(True):
        if(counter == samples_4_avg):
            counter = 0

        mech_RSSI_array[counter] = getRSSI(UDP_packetSize)[1]
        counter += 1

        now_RSSI = 20*np.log10(mech_RSSI_array[0])
        if(local_max_RSSI < now_RSSI):
            local_max_RSSI = now_RSSI

        if(now_RSSI < (local_max_RSSI - deviation_RSSI)):
            if(direction == "left"):
                direction = "right"
                local_max_RSSI = -1000

            elif(direction == "right"):
                direction = "left"
                local_max_RSSI = -1000
                
        if(direction == "left"):
            TARM.set_pos(int(aimingAngle - 2), ele)
            print(f"moveleft , RSSI: {now_RSSI}")
            aimingAngle -= 2
            time.sleep(0.1)
        elif(direction == "right"):
            TARM.set_pos(int(aimingAngle + 2), ele)
            print(f"moveright , RSSI: {now_RSSI}")
            aimingAngle += 2
            time.sleep(0.1)
        else:
            print("Du har lavet den fejl din dum")





if __name__ == "__main__":
    beacon = Beacon_decoder()
    beacon.start()

