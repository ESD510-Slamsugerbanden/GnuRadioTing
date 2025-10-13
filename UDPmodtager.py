import socket
import struct
import time

RSSI_angles = 6
UDP_packetSize = 64


# Define the UDP IP address and port to listen on
UDP_IP = "127.0.0.1"
UDP_PORT = 2000

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
    currentAngle = 0
    RSSI_array = []
    for i in range(RSSI_angles):
        aimed_Angle = 180/RSSI_angles
        RSSI_array.append(getRSSI(UDP_packetSize))
        maltheDREJ(aimed_Angle)
        while(currentAngle!= aimed_Angle):
            currentAngle = malthe_get_angle()
            time.sleep(0.01)

    maxRSSI = 0
    for i in range(RSSI_angles):
        #parse gennem listen
        #Hvis nuværende værdi > maxRSSI
        if(RSSI_array[i] > maxRSSI):
            maxRSSI = RSSI_array[i]
            max_RSSI_index = i

    return max_RSSI_index, RSSI_array


while True:
    tx_angle, RSSI_array = find_Initial_Location()
    maltheDREJ(tx_angle)
    print(RSSI_array)
    print(f"Den godeste vinkel er {tx_angle}")


