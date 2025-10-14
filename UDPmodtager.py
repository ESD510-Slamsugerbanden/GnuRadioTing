import socket
import struct
import time
import rotte
import matplotlib.pyplot as plt
import numpy as np


RSSI_angles = 20
UDP_packetSize = 64
AZ_counts = 360

# Define the UDP IP address and port to listen on
UDP_IP = "127.0.0.1"
UDP_PORT = 2000

#TARM
TARM = rotte.UdpProtocolClient("192.168.4.1", 8700)
ele = 90

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
    for i in range(RSSI_angles):
        aimed_Angle = int(AZ_counts/RSSI_angles)*i
        runningSum = getRSSI(UDP_packetSize)
        runningSum += getRSSI(UDP_packetSize)
        runningSum += getRSSI(UDP_packetSize)
        runningSum += getRSSI(UDP_packetSize)
        RSSI_array.append(runningSum)

       # RSSI_array.append(getRSSI(UDP_packetSize))
        print(runningSum)
        TARM.set_pos(aimed_Angle, ele)
        time.sleep(1)

    maxRSSI = -1000
    max_RSSI_index = 0
    for i in range(RSSI_angles):
        if(RSSI_array[i] > maxRSSI):
            maxRSSI = RSSI_array[i]
            max_RSSI_index = i

    angle_out = int(max_RSSI_index*AZ_counts/RSSI_angles)

    return angle_out, RSSI_array




def radialPlot(Arrray_in):
    thetas = []

    for i in range(RSSI_angles):
        thetas.append(((2*np.pi/RSSI_angles)*i))

    
    plt.polar(thetas[0:RSSI_angles], Arrray_in[0:RSSI_angles])
    plt.show()



#MAIN


tx_angle, RSSI_array = find_Initial_Location()
TARM.set_pos(tx_angle, ele)
print(RSSI_array)
print(f"Den godeste vinkel er {tx_angle}")
radialPlot(RSSI_array)

