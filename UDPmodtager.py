import socket
import struct
import time
import rotte
import matplotlib.pyplot as plt
import numpy as np


RSSI_angles = 100
UDP_packetSize = 64
AZ_counts = 368
ele = -45

# Define the UDP IP address and port to listen on
UDP_IP = "127.0.0.1"
UDP_PORT = 24944

#TARM
TARM = rotte.UdpProtocolClient("192.168.4.1", 8700)


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, UDP_packetSize)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets on {UDP_IP} :{UDP_PORT}")

def getRSSI(bytes):
    valNow = 0
    runningSum = 0
    data, addr = sock.recvfrom(bytes)
    #print(f"Received packet from {addr}:")
    
    #Unpack 
    for i in range((bytes//4)-1):
        valNow = struct.unpack('f', data[(i*4):(i*4+4)])
        #print(valNow)
        runningSum += valNow[0]

    return runningSum/(bytes/4)



def find_Initial_Location():
    RSSI_array = []
    angle_Array = []
    TARM.set_pos(0,ele)
    time.sleep(2)
    for i in range(RSSI_angles):
        aimed_Angle = int((AZ_counts/RSSI_angles)*i)
        currentPos, _ = TARM.get_pos()
        TARM.set_pos(aimed_Angle, ele)

        while(abs(aimed_Angle - currentPos) > 5):
            time.sleep(0.01)
            currentPos, _ = TARM.get_pos()

        angle_Array.append(np.deg2rad(currentPos))
        getRSSI(UDP_packetSize)
        getRSSI(UDP_packetSize)
        RSSI_array.append(getRSSI(UDP_packetSize))
        print(f"Vinkel:{currentPos}, RSSI:{RSSI_array[i]}")
        


    maxRSSI = -1000
    max_RSSI_index = 0
    for i in range(RSSI_angles):
        if(RSSI_array[i] > maxRSSI):
            maxRSSI = RSSI_array[i]
            max_RSSI_index = i

    angle_out = angle_Array[max_RSSI_index]

    return angle_out, RSSI_array, angle_Array




def radialPlot(amp_Array, angle_Array):
    
    plt.polar(angle_Array, amp_Array)
    plt.show()


def findRSSIavg(inputArray):
    runningSum = 0
    for i in range(len(inputArray)):
        runningSum += inputArray[i]

    return runningSum/len(inputArray)


def mechanicalTrack(initialAngle):

    samples_4_avg = 25
    mech_RSSI_array = [0] * samples_4_avg
    aimingAngle = initialAngle
    local_max_RSSI = 0
    deviation_RSSI = 3
    direction = "left"


    counter = 0
    while(True):
        if(counter == samples_4_avg):
            counter = 0

        mech_RSSI_array[counter] = getRSSI(UDP_packetSize)
        counter += 1

        now_RSSI = findRSSIavg(mech_RSSI_array)
        if(local_max_RSSI < now_RSSI):
            local_max_RSSI = now_RSSI

        if(now_RSSI < local_max_RSSI - deviation_RSSI):
            if(direction == "left"):
                direction = "right"
                local_max_RSSI = 0

            elif(direction == "right"):
                direction = "left"
                local_max_RSSI = 0
                
        if(direction == "left"):
            TARM.set_pos(int(aimingAngle - 1), ele)
            print(f"moveleft , RSSI: {now_RSSI}")
            aimingAngle -= 2
            time.sleep(0.03)
        elif(direction == "right"):
            TARM.set_pos(int(aimingAngle + 1), ele)
            print(f"moveright , RSSI: {now_RSSI}")
            aimingAngle += 2
            time.sleep(0.03)
        else:
            print("Du har lavet den fejl din dum")
        


        





#MAIN

getRSSI(UDP_packetSize)

#Find bedste vinkel og lav emission plot

tx_angle, RSSI_array, angle_Array = find_Initial_Location()
TARM.set_pos(np.rad2deg(tx_angle), ele)
print(RSSI_array)
print(f"Den godeste vinkel er {np.rad2deg(tx_angle)}")
radialPlot(RSSI_array, angle_Array)

#mechanicalTrack(np.rad2deg(tx_angle))