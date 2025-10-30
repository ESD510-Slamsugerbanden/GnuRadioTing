#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: sennels
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio.fft import logpwrfft
import sip
import threading



class Transfrans(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Transfrans")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samples_pr_sym = samples_pr_sym = 3
        self.Symbol_rate = Symbol_rate = (31)*2
        self.toggle_invert = toggle_invert = (-1)
        self.toggle_amplitude = toggle_amplitude = 1
        self.sep_freq = sep_freq = 20000
        self.samp_rate = samp_rate = 500000
        self.PI = PI = 3.14159265358979323
        self.FFT_bins = FFT_bins = 256
        self.Base_samp_rate = Base_samp_rate = Symbol_rate*samples_pr_sym

        ##################################################
        # Blocks
        ##################################################

        self._toggle_invert_choices = {'Pressed': 1, 'Released': (-1)}

        _toggle_invert_toggle_button = qtgui.ToggleButton(self.set_toggle_invert, 'Invert', self._toggle_invert_choices, False, 'toggle_amplitude')
        _toggle_invert_toggle_button.setColors("default", "default", "default", "default")
        self.toggle_invert = _toggle_invert_toggle_button

        self.top_layout.addWidget(_toggle_invert_toggle_button)
        self._toggle_amplitude_choices = {'Pressed': 1, 'Released': 0}

        _toggle_amplitude_toggle_button = qtgui.ToggleButton(self.set_toggle_amplitude, 'Transmit', self._toggle_amplitude_choices, False, 'toggle_amplitude')
        _toggle_amplitude_toggle_button.setColors("default", "default", "default", "default")
        self.toggle_amplitude = _toggle_amplitude_toggle_button

        self.top_layout.addWidget(_toggle_amplitude_toggle_button)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            FFT_bins,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis((-20), 1)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_float, 1, '127.0.0.1', 5006, 0, (FFT_bins*4), False)
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
            sample_rate=samp_rate,
            fft_size=FFT_bins,
            ref_scale=1,
            frame_rate=Base_samp_rate,
            avg_alpha=1.0,
            average=False,
            shift=True)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0.1,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_float*1, FFT_bins)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, 31)
        self.blocks_vector_source_x_0 = blocks.vector_source_f((1,  1, -1, -1,  1, -1, -1, -1,  1,  1,  1, -1, -1,  1,  1, -1,  1, 1, -1,  1,  1, -1,  1, -1,  1,  1,  1, -1, -1, -1, -1), True, 31, [])
        self.blocks_vco_c_0_0 = blocks.vco_c(samp_rate, (2*PI), 1)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, (int(((samp_rate)/(Symbol_rate))*samples_pr_sym)))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_cc(toggle_amplitude)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(sep_freq)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(toggle_invert)
        self.band_pass_filter_0_0_0_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                (sep_freq-1000),
                (sep_freq+1000),
                8000,
                window.WIN_HAMMING,
                6.76))
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
        self.connect((self.band_pass_filter_0_0_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.band_pass_filter_0_0_0_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_vco_c_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.band_pass_filter_0_0_0_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_vco_c_0_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.network_udp_sink_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.band_pass_filter_0_0_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.qtgui_vector_sink_f_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "Transfrans")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samples_pr_sym(self):
        return self.samples_pr_sym

    def set_samples_pr_sym(self, samples_pr_sym):
        self.samples_pr_sym = samples_pr_sym
        self.set_Base_samp_rate(self.Symbol_rate*self.samples_pr_sym)
        self.blocks_repeat_0.set_interpolation((int(((self.samp_rate)/(self.Symbol_rate))*self.samples_pr_sym)))

    def get_Symbol_rate(self):
        return self.Symbol_rate

    def set_Symbol_rate(self, Symbol_rate):
        self.Symbol_rate = Symbol_rate
        self.set_Base_samp_rate(self.Symbol_rate*self.samples_pr_sym)
        self.blocks_repeat_0.set_interpolation((int(((self.samp_rate)/(self.Symbol_rate))*self.samples_pr_sym)))

    def get_toggle_invert(self):
        return self.toggle_invert

    def set_toggle_invert(self, toggle_invert):
        self.toggle_invert = toggle_invert
        self.blocks_multiply_const_vxx_0.set_k(self.toggle_invert)

    def get_toggle_amplitude(self):
        return self.toggle_amplitude

    def set_toggle_amplitude(self, toggle_amplitude):
        self.toggle_amplitude = toggle_amplitude
        self.blocks_multiply_const_vxx_0_1.set_k(self.toggle_amplitude)

    def get_sep_freq(self):
        return self.sep_freq

    def set_sep_freq(self, sep_freq):
        self.sep_freq = sep_freq
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.sep_freq-1000), (self.sep_freq+1000), 8000, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.sep_freq-1000), (self.sep_freq+1000), 8000, window.WIN_HAMMING, 6.76))
        self.blocks_multiply_const_vxx_0_0.set_k(self.sep_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.sep_freq-1000), (self.sep_freq+1000), 8000, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.sep_freq-1000), (self.sep_freq+1000), 8000, window.WIN_HAMMING, 6.76))
        self.blocks_repeat_0.set_interpolation((int(((self.samp_rate)/(self.Symbol_rate))*self.samples_pr_sym)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

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

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
