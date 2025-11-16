"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
from enum import Enum





######################################################
# RØV LANG OG TRÆLS KODE FOR AT LAVE NOGLE GOLDCODES # xoxo Malther
######################################################


def lfsr_sequence(poly, seed, n):
    """Generate an m-sequence using given feedback polynomial (as taps)."""
    state = seed.copy()
    seq = np.zeros(2**n - 1, dtype=int)
    for i in range(len(seq)):
        seq[i] = state[-1]
        feedback = np.mod(np.sum(state[np.array(poly) - 1]), 2)
        state[1:] = state[:-1]
        state[0] = feedback
    return seq

def gold_codes(n, poly1, poly2, seed):
    """Generate Gold code family for degree n LFSRs with given feedback taps."""
    s1 = lfsr_sequence(poly1, seed.copy(), n)
    s2 = lfsr_sequence(poly2, seed.copy(), n)
    N = len(s1)
    codes = []

    for shift in range(N):
        s2_shift = np.roll(s2, shift)
        codes.append(np.bitwise_xor(s1, s2_shift))
    # Add original sequences too
    codes.append(s1)
    codes.append(s2)
    return np.array(codes)


def auto_generate(my_id):
    """Generate codes using predefined settings"""
    n = 5
    poly1 = [5, 2]          # x^5 + x^2 + 1
    poly2 = [5, 4, 3, 2]    # x^5 + x^4 + x^3 + x^2 + 1
    seed = np.array([1, 0, 0, 0, 1])

    codes = gold_codes(n, poly1, poly2, seed)
    return np.float32(codes[my_id])









class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, burst_period=100,bursts = 4, gold_code=1, sps=3):  # only default arguments here
        """Jydesnak DE-beaconizer"""
        gr.sync_block.__init__(
            self,
            name='Jydesnak DE-BEACONIZER',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32],
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.burst_period = burst_period
        self.bursts = bursts
        self.sps= sps
        self.mycode = np.subtract(np.repeat(auto_generate(gold_code), self.sps) * 2 , 1)##Genererer vores SCHLONG vektor der kan bruges
        self.mycode = np.flip(self.mycode)
        self.vectorlength = len(self.mycode)
        self.buffer = np.zeros(self.vectorlength)
        self.corr_thres = 0.6
        self.maxcorr = 0
        self.i_maxcorr = 0
        ###STUFF for locking onto our target in time
        self.minislot = int(self.vectorlength/4)
        self.set_max_output_buffer(0, self.minislot)
        self.T_search = int(self.minislot*6) 
        self.switch_number = 0
        self.Locked = False
        self.peakflag = False
        self.t = 0

        self.sleep = 0
        self.t_minislot = 0
        print(f"[DE-beaconizer]: minislot: {self.minislot}, \t burst period: {self.burst_period}")


    def work(self, input_items, output_items):
        """example: multiply with constant"""
        input = input_items[0]
        N = len(input)
        
        
        for i in range(N):
            self.buffer = np.roll(self.buffer, 1)
            self.buffer[0] = input[i]
            corr = np.dot(self.buffer, self.mycode) *  1/self.vectorlength##FLyver lige igennem en kryscorr og bobber ham ned engang
            candidate = np.abs(corr)
            if(candidate> self.corr_thres):
                self.maxcorr = corr
                self.i_maxcorr = i
                self.peakflag = True

            output_items[0][i] = corr 


        
        if(self.peakflag):
            key = pmt.intern("suspekt")          # the tag name
            value = pmt.from_long(int(self.maxcorr*100))           # the tag value
            self.add_item_tag(0, self.nitems_written(0)+int(self.i_maxcorr), key, value)
            self.peakflag = False

        """


        
        t_maxcorr = self.t + self.i_maxcorr 

        self.t = (self.t + N)
        self.t_minislot += 1


        if (self.t_minislot >= 0):
            
            e_minislots = (t_maxcorr - self.minislot*5) / self.minislot ##Our error in minslots
            if(self.maxcorr != 0): #Something to lock on
                self.Locked = True
                self.t_minislot = -self.burst_period #+ int(e_minislots+0.5)

                
            if(self.Locked == False):
                self.switch_number = (self.switch_number+ 1) % 4
                key = pmt.intern("SWITCH")          # the tag name
                value = pmt.from_long(self.switch_number)           # the tag value
                self.add_item_tag(0, self.nitems_written(0), key, value)
            else:
                key = pmt.intern("EVAL")          # the tag name
                value = pmt.from_long(int(e_minislots))           # the tag value
                self.add_item_tag(0, self.nitems_written(0)+N, key, value)


        if(self.t > self.T_search):
            self.t = self.t % self.T_search
            self.maxcorr = 0

        """

        return N
