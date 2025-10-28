
import numpy as np
import struct
from scipy.linalg import hadamard
import threading
import socket
import logging
import gold_codes 
import time 
import plotly.express as px

class Beacon_decoder:


    class RingBuffer:
        def __init__(self, size: int):
            self.size = size
            self.buffer = np.zeros(size, float)

        def put(self, sample: float):
            # Roll the buffer and assign it back
            self.buffer = np.roll(self.buffer, 1)
            self.buffer[0] = sample

    def __init__(self, my_id = 0, n = 5, samples_pr_symbol=2, port=5006):
        self.sps = samples_pr_symbol #samples pr symbol
        self.num_syms = 2**n-1 #number of symbols allowed
        logging.info("Initializing decoder")
        #Gets the codes for the hadamard.


        # Example: n = 5 (length = 31)
        # Preferred polynomials for n=5 are often [5,2] and [5,4,3,2]

        poly1 = [5, 2]          # x^5 + x^2 + 1
        poly2 = [5, 4, 3, 2]    # x^5 + x^4 + x^3 + x^2 + 1
        seed = np.array([1, 0, 0, 0, 1])

        self.code_table = gold_codes.gold_codes(n, poly1, poly2, seed)
        self.code_table = self.code_table*2 -1
        
        self.code_vector = np.repeat(self.code_table[my_id], self.sps)
        self.code_vector = np.flip(self.code_vector)
        print("looking for this bitch")
        print(self.code_table[my_id])
        #self.code_table = hadamard(self.num_syms)
        logging.info(f"Generated codes: {self.code_table}")
        #Readys the ringbuffer for later.
        self.code_buf = self.RingBuffer(self.sps*self.num_syms)
        self.RSSI_buf = self.RingBuffer(self.sps*self.num_syms)
        logging.info(f"Mounting socket, port={port}")
        #Sets up the input stream fo later use.
        
        self.input_stream = self.Input_stream(host="127.0.0.1", port=port)
        

        #Sets the code for the decoder itself.

        ##Starter forberedelser til at køre en thread.
        self.thread_handle = threading.Thread(target=self._internal_runner)
        self.last_corr = None
        self.last_rssi = None
        self.lastest = False
        self.loopback_counter = 0

    def loopback(self):
        sample = self.code_vector[self.loopback_counter]
        self.loopback_counter = (self.loopback_counter-1) % len(self.code_vector)
        return sample

    def _internal_runner(self):

        sample_counter = 0
        chip_period = self.sps* self.num_syms

        x_corr_max = 0
        rssi_max = 0
        i_max = 0
        i = 0
        K_p = 0.005  # small gain for stability
        K_i = 0.00
        i_term = 1
        res = []
        adjust_values = []
        temp_corr = []
        phase_error= 0
        i_modifier = 0
        while(True):
            #Gets the FFT samples

            fft_samples = self.input_stream.fetch_samples()
            
            size = len(fft_samples)

            ##frekvenser under 0 bliver gemt som et 0
            C_1 = np.sum(fft_samples[0:int(size/2)])
            ##frekvenser over 0 blive gemt som et 1
            C_2 = np.sum(fft_samples[int(size/2):size])


            #Puts them in the buffer
            self.code_buf.put(C_1-C_2)
            self.RSSI_buf.put(C_1+C_2)

            #print("rssi: {:.3f}\t , corr: {:.3f}".format(C_1 + C_2,C_1 - C_2))
            xcorr_score = Beacon_decoder.correlate(self.code_buf.buffer,self.code_vector)
            temp_corr.append(xcorr_score)
            if(np.abs(xcorr_score) > np.abs(x_corr_max)):
                rssi_max = np.average(self.RSSI_buf.buffer)
                x_corr_max = xcorr_score
                i_max = i
                #Gives a little PLL functionality
            
            
            if (i >= (chip_period*(1-i_modifier))):
                self.lastest = True
                self.last_corr = x_corr_max 
                self.last_rssi = rssi_max
                #fig = px.line(x=range(len(temp_corr)), y=[temp_corr])
                #fig.show()
                temp_corr = []
                phase_error = (chip_period/2 - i_max)
                i_term = phase_error * K_i
                i_modifier = phase_error*K_p + i_term
                i = 0
                #print("rssi: {:.4f}\t , corr: {:.4f}, \t i_max:= {:.0f}, new i={:.0f}".format(self.last_rssi, self.last_corr, i_max, i))
                print("most likely: {:.2f}".format(x_corr_max))
                x_corr_max = 0
                rssi_max = 0
            i = i + 1
        



    def start(self):
        self.thread_handle.start()

    def stop(self):
        logging.warning("Stopper not implemented")
        print("Not implemnted: SUCKS TO SUCK")

    def avaliable():
        pass

    def get_lastest():
        pass

    class Input_stream:
        def __init__(self, host: str="127.0.0.1", port:int=5005, f_s:int=5):

            self.num_floats = 32
            self.f_s = f_s
            self.host = host
            self.port = port
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Set receive buffer size (SO_RCVBUF)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)  # 4 KB

            self.sock.setblocking(True)  # ensures it's blocking
            self.fmt = "<" + "f" * self.num_floats  # Little-endian, 256 floats      
            self.sock.bind((host, self.port))


        def fetch_samples(self):
            data, addr = self.sock.recvfrom(4*self.num_floats)
            floats = struct.unpack(self.fmt, data)
            return floats


    def generate_pattern(sps: int, pattern: list[int]):
        result: list[int] = []
        for i in pattern:
            for n in range(sps):
                result.append(i)
        return result


    #kigger på pattern matchet
    def correlate(pattern: np.ndarray, samples_1: np.ndarray):
        sum = np.multiply(pattern, samples_1)
        sum = np.sum(sum)
        return sum





if __name__ == "__main__":
    beacon = Beacon_decoder()
    beacon.start()
