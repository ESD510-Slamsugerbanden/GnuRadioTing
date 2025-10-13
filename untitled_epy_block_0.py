"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, vectorSize=2048):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[(np.float32, vectorSize)],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        sum = 0.0
        for i in range(220, 224):
            sum +=  10**(input_items[0][:,i]/20)
        output_items[0][:] = 20*np.log10(sum/4)
        return len(output_items[0])




