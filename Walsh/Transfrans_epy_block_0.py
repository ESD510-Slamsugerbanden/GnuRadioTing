import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    """Takes a scalar input and outputs a scaled vector."""

    def __init__(self, chip_vector=[-1, -1, -1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1]):

        self.chip_vector = np.array(chip_vector, dtype=np.float32)

        gr.sync_block.__init__(
            self,
            name='Scalar to Vector Block',
            in_sig=[np.float32],                     # Single float input per item
            out_sig=[(np.float32, len(chip_vector))] # Vector output per item
        )

    def work(self, input_items, output_items):
        x = input_items[0]           # shape: (ninput_items,)
        out = output_items[0]        # shape: (ninput_items, len(chip_vector))
        out[:] = x[:, np.newaxis] * self.chip_vector
        return len(out)
