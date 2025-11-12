#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: sennels
# GNU Radio version: 3.10.12.0

from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import uhd
import time
from gnuradio.fft import logpwrfft
import threading




class Transfrans(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samples_pr_sym = samples_pr_sym = 3
        self.Symbol_rate = Symbol_rate = 256
        self.sep_freq = sep_freq = 20000
        self.samp_rate = samp_rate = 500000
        self.PI = PI = 3.14159265358979323
        self.FFT_bins = FFT_bins = 256
        self.Base_samp_rate = Base_samp_rate = Symbol_rate*samples_pr_sym

        ##################################################
        # Blocks
        ##################################################

        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(2490000000, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(20, 0)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_float, 1, '127.0.0.1', 5006, 0, (FFT_bins*4), False)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=FFT_bins,
            ref_scale=1,
            frame_rate=Base_samp_rate,
            avg_alpha=1.0,
            average=False,
            shift=True)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_float*1, FFT_bins)
        self.band_pass_filter_0_0_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                (sep_freq-1000),
                (sep_freq+1000),
                8000,
                window.WIN_HAMMING,
                6.76))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.band_pass_filter_0_0_0, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.network_udp_sink_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.band_pass_filter_0_0_0, 0))


    def get_samples_pr_sym(self):
        return self.samples_pr_sym

    def set_samples_pr_sym(self, samples_pr_sym):
        self.samples_pr_sym = samples_pr_sym
        self.set_Base_samp_rate(self.Symbol_rate*self.samples_pr_sym)

    def get_Symbol_rate(self):
        return self.Symbol_rate

    def set_Symbol_rate(self, Symbol_rate):
        self.Symbol_rate = Symbol_rate
        self.set_Base_samp_rate(self.Symbol_rate*self.samples_pr_sym)

    def get_sep_freq(self):
        return self.sep_freq

    def set_sep_freq(self, sep_freq):
        self.sep_freq = sep_freq
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.sep_freq-1000), (self.sep_freq+1000), 8000, window.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.sep_freq-1000), (self.sep_freq+1000), 8000, window.WIN_HAMMING, 6.76))
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_PI(self):
        return self.PI

    def set_PI(self, PI):
        self.PI = PI

    def get_FFT_bins(self):
        return self.FFT_bins

    def set_FFT_bins(self, FFT_bins):
        self.FFT_bins = FFT_bins

    def get_Base_samp_rate(self):
        return self.Base_samp_rate

    def set_Base_samp_rate(self, Base_samp_rate):
        self.Base_samp_rate = Base_samp_rate




def main(top_block_cls=Transfrans, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.flowgraph_started.set()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
