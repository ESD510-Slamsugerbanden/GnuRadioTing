"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr




######################################################
# RØV LANG OG TRÆLS KODE FOR AT LAVE NOGLE GOLDCODES # 
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

    def __init__(self, burst_period=1000,bursts = 4, gold_code=1, sps=3, minislot_delay=50):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Jydesnak BEACONIZER',   # will show up in GRC
            out_sig=[np.float32],
            in_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.gold_code_index = gold_code
        self.sps = sps
        self.bursts = bursts
        self.global_sample_index = 0
        self.i_code = 0
        self.transmitting = False
        self.transmit_index = 0
        self.mycode = np.subtract(np.repeat(auto_generate(gold_code), self.sps) * 2 , 1)
        self.vectorlength = len(self.mycode)
        
        ##How big a minislot should be
        self.minislot = int(self.vectorlength/4)
        self.burst_period = burst_period*self.minislot
        self.minislot_delay = minislot_delay
        self.mycode = np.concatenate([self.mycode, np.zeros(self.minislot*minislot_delay)]) ##Genererer vores SCHLONG vektor der kan bruges med minislot spacing
        self.vectorlength_w_padding = len(self.mycode)



        print(f"vectorlength (samples): {self.vectorlength}")
        print(f"[Beaconizer]: minislot: {self.minislot}, \t burst period: {self.burst_period}")

    def work(self, input_items, output_items):
        out = output_items[0]
        n = len(out)

        for i_sample in range(n):
            pos_in_period = (self.global_sample_index + i_sample) % self.burst_period

            if pos_in_period < self.vectorlength_w_padding * self.bursts:
                if(pos_in_period < self.vectorlength_w_padding *2):
                    out[i_sample] = self.mycode[pos_in_period % self.vectorlength_w_padding] # vector at start
                else:
                    out[i_sample] = self.mycode[pos_in_period % self.vectorlength_w_padding] * -1  # vector at start
            else:
                out[i_sample] = 0  # zero padding until end of period

        self.global_sample_index = (self.global_sample_index + n) % self.burst_period
        return n


