
import numpy as np
import struct
from scipy.linalg import hadamard

import socket


class Input_stream:
    def __init__(self, host="127.0.0.1", port=5005, f_s = 5, timeout=2):

        self.num_floats = 256
        self.f_s = f_s
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.fmt = "<" + "f" * self.num_floats  # Little-endian, 256 floats      
        self.sock.bind((host, port))

    def fetch_samples(self):
        data, addr = self.sock.recvfrom(4*self.num_floats)
        #print(addr)
        floats = struct.unpack(self.fmt, data)
        return floats


GNU_fcker = Input_stream("127.0.0.1", 5006)



def generate_pattern(sps: int, pattern: list[int]):
    result: list[int] = []
    for i in pattern:
        for n in range(sps):
            result.append(i)
    return result
    
    


class RingBuffer:
    def __init__(self, size: int):
        self.size = size
        self.buffer = np.zeros(size, float)

    def put(self, sample: float):
        # Roll the buffer and assign it back
        self.buffer = np.roll(self.buffer, 1)
        self.buffer[0] = sample



#patter vi kigger efter, frekvenser over 0, frekvenser under 0
def correlate(pattern, samples_1):
    sum = 0
    for i in range(min(len(pattern),len(pattern))):
        sum += (pattern[i] * samples_1[i])
    return sum

if __name__ == "__main__":


    encodements = hadamard(8)
    print(encodements)
    print("done")

    sps = 5 #samples pr symbol
    num_syms = 8 #number of symbols allowed
    pattern_blue = generate_pattern(5, encodements[:, 4])
    pattern_red = generate_pattern(5, encodements[:, 1])

    print(pattern_red)
    print(pattern_blue)
    C_buf = RingBuffer(sps*num_syms)

    i = 0
    max_a = 0
    max_b = 0 
    while(True):
        #Får FFT værdier
        raw = GNU_fcker.fetch_samples()
        size = len(raw)

        

        #The given samples for any time

        ##frekvenser under 0
        C_1 = np.sum(np.power(10, np.divide(raw[0:int(size/2)],10)))

        ##frekvenser over 0
        C_2 = np.sum(np.power(10, np.divide(raw[int(size/2):size], 10)))

        C_buf.put(C_1 - C_2)

        
        matcha = correlate(pattern_red, C_buf.buffer)
        matchb = correlate(pattern_blue, C_buf.buffer)
        if(matcha > max_a):
            max_a = matcha
        if(matchb > max_b):
            max_b = matchb

        if (i > 200):
            print("maximums since last {:.1f} {:.1f}".format(max_a, max_b))
            max_a = 0
            max_b = 0 
            i = 0
        i += 1




