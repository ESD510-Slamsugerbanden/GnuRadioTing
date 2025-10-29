import socket
import struct
import time
import rotte
import matplotlib.pyplot as plt
import numpy as np
import variables
import Walsh.decoder as decoder
import threading
import RPi.GPIO as GPIO

Pin1 = 17
Pin2 = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(Pin1, GPIO.OUT)
GPIO.setup(Pin2, GPIO.OUT)
GPIO.output(Pin1, GPIO.LOW)
GPIO.output(Pin2, GPIO.LOW)

t2 = threading.Thread(target=decoder.decodeServer)
t2.start()

RSSI_angles = 100
UDP_packetSize = 64
AZ_counts = 368
ele = 0

# Define the UDP IP address and port to listen on
UDP_IP = "127.0.0.1"
UDP_PORT = 24944 

#TARM
TARM = rotte.UdpProtocolClient("192.168.4.1", 8700)

'''
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, UDP_packetSize)
sock.bind((UDP_IP, UDP_PORT))
'''

print(f"Listening for UDP packets on {UDP_IP} :{UDP_PORT}")

def getRSSI(bytes):
    '''
    valNow = 0
    runningSum = 0
    data, addr = sock.recvfrom(bytes)
    #print(f"Received packet from {addr}:")
    
    #Unpack 
    for i in range((bytes//4)-1):
        valNow = struct.unpack('f', data[(i*4):(i*4+4)])
        #print(valNow)
        runningSum += valNow[0]
    '''
    return variables.corrScore, variables.globalRSSI



def find_Initial_Location():
    RSSI_array = []
    RSSI_array2 = []
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
        RSSI_array.append(getRSSI(UDP_packetSize)[0])
        RSSI_array2.append(getRSSI(UDP_packetSize)[1])
        print(f"Vinkel:{currentPos}, RSSI:{RSSI_array[i]}")
        


    maxRSSI = -1000
    max_RSSI_index = 0
    for i in range(RSSI_angles):
        if(RSSI_array[i] > maxRSSI):
            maxRSSI = RSSI_array[i]
            max_RSSI_index = i

    angle_out = angle_Array[max_RSSI_index]

    return angle_out, RSSI_array, angle_Array, RSSI_array2





def radialPlot(CORR, RSSI, angle_Array):

    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection="polar", label="CORR")
    ax2 = fig.add_subplot(111, projection="polar", label="RSSI", frame_on=False)

    # Plotting the data
    ax1.plot(angle_Array, CORR, color='b', label="Correlation Score")
    ax2.plot(angle_Array, RSSI, color='r', label="RSSI")

    # Hide radial ticks, grid, and labels on ax2 to avoid overlap
    ax2.set_yticklabels([])     # Hide radial labels
    ax2.set_yticks([])          # Hide radial ticks
    ax2.grid(False)             # Hide grid lines

    # Add legends
    ax1.legend(loc='upper right')
    ax2.legend(loc='upper left')

    plt.show()


def findRSSIavg(inputArray):
    runningSum = 0
    for i in range(len(inputArray)):
        runningSum += inputArray[i]

    return runningSum/len(inputArray)


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
        

def switchTest(sw):
    match sw:
        case 1:
            GPIO.output(Pin1, GPIO.LOW)
            GPIO.output(Pin2, GPIO.LOW)
        
        case 2:
            GPIO.output(Pin1, GPIO.HIGH)
            GPIO.output(Pin2, GPIO.LOW)
        
        case 3:
            GPIO.output(Pin1, GPIO.LOW)
            GPIO.output(Pin2, GPIO.HIGH)
        

        case 4:
            GPIO.output(Pin1, GPIO.HIGH)
            GPIO.output(Pin2, GPIO.HIGH)
            print("Det var fire")





#MAIN
def RSSIplot():
    getRSSI(UDP_packetSize)

    #Find bedste vinkel og lav emission plot

    tx_angle, RSSI_array, angle_Array, RSSI_array2 = find_Initial_Location()
    TARM.set_pos(np.rad2deg(tx_angle), ele)
    print(RSSI_array)
    print(f"Den godeste vinkel er {np.rad2deg(tx_angle)}")
    radialPlot(RSSI_array, RSSI_array2, angle_Array)

    #mechanicalTrack(np.rad2deg(tx_angle))

if(__name__ == "__main__"):
    RSSIplot()
    #mechanicalTrack(0)
    while(True):
        for i in range(4):
            switchTest(i+1)
            getRSSI(UDP_packetSize)