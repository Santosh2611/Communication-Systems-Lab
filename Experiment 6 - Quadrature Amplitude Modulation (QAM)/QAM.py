#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QAM
# Author: Santosh
# Copyright: 2022
# GNU Radio version: 3.10.4.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



from gnuradio import qtgui

class QAM(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "QAM", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("QAM")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "QAM")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 500000

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_1_0 = qtgui.sink_f(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'm2(t)', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1_0.set_update_time(1.0/10)
        self._qtgui_sink_x_1_0_win = sip.wrapinstance(self.qtgui_sink_x_1_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_1_0_win)
        self.qtgui_sink_x_1 = qtgui.sink_f(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'm1(t)', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_1.set_update_time(1.0/10)
        self._qtgui_sink_x_1_win = sip.wrapinstance(self.qtgui_sink_x_1.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_1.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_1_win)
        self.qtgui_sink_x_0 = qtgui.sink_f(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            's(t)', #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                70000,
                100,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                70000,
                100,
                window.WIN_HAMMING,
                6.76))
        self.blocks_vector_to_streams_0 = blocks.vector_to_streams(gr.sizeof_int*1, 2)
        self.blocks_streams_to_vector_0 = blocks.streams_to_vector(gr.sizeof_int*1, 2)
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_int*1, 100)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_int*1, 100)
        self.blocks_multiply_xx_0_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_int_to_float_0_0 = blocks.int_to_float(1, 1)
        self.blocks_int_to_float_0 = blocks.int_to_float(1, 1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_sig_source_x_0_1_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 140000, 2, 0, 0)
        self.analog_sig_source_x_0_1_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, 140000, 2, 0, 0)
        self.analog_sig_source_x_0_1_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, 140000, 1, 0, 0)
        self.analog_sig_source_x_0_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 140000, 1, 0, 0)
        self.analog_random_source_x_0_0 = blocks.vector_source_i(list(map(int, numpy.random.randint((-2), 2, 1000))), True)
        self.analog_random_source_x_0 = blocks.vector_source_i(list(map(int, numpy.random.randint((-2), 2, 1000))), True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.analog_random_source_x_0_0, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_1_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_0_1_0_0, 0), (self.blocks_multiply_xx_0_0_0_0, 0))
        self.connect((self.analog_sig_source_x_0_1_1, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_0_0_0_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_int_to_float_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_int_to_float_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_streams_to_vector_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_streams_to_vector_0, 1))
        self.connect((self.blocks_streams_to_vector_0, 0), (self.blocks_vector_to_streams_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 0), (self.blocks_int_to_float_0, 0))
        self.connect((self.blocks_vector_to_streams_0, 1), (self.blocks_int_to_float_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_1, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_sink_x_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "QAM")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1_1.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 70000, 100, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 70000, 100, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_1_0.set_frequency_range(0, self.samp_rate)




def main(top_block_cls=QAM, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

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
