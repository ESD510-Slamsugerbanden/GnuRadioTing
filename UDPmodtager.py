import socket
import struct


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

def initialLocation():
    #1. Sweep Butler & put RSSI i array
    #2. Roter 30 grader vertikalt x2
    #3 Roter 30 grader Azimuth
    #Repeat 1-3 til tilbage ved start
    






    return True


while True:
    initialLocation()

    print(getRSSI(64))


