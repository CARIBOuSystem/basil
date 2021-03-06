#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#

import unittest
import os
from basil.dut import Dut
from basil.utils.sim.utils import cocotb_compile_and_run, cocotb_compile_clean

cnfg_yaml = """
transfer_layer:
  - name  : intf
    type  : SiSim
    init:
        host : localhost
        port  : 12345

hw_drivers:
  - name      : PULSE_GEN
    type      : pulse_gen
    interface : intf
    base_addr : 0x0000

  - name      : SEQ_GEN
    type      : seq_gen
    interface : intf
    mem_size  : 8192
    base_addr : 0x1000

  - name      : SEQ_REC
    type      : seq_rec
    interface : intf
    mem_size  : 8192
    base_addr : 0x3000

registers:
  - name        : SEQ
    type        : TrackRegister
    hw_driver   : SEQ_GEN
    seq_width   : 8
    seq_size    : 8192
    tracks  :
      - name     : S0
        position : 0
      - name     : S1
        position : 1
      - name     : S2
        position : 2
      - name     : S3
        position : 3
      - name     : S4
        position : 4
      - name     : S5
        position : 5
      - name     : S6
        position : 6
      - name     : S7
        position : 7
"""


class TestSimSeq(unittest.TestCase):
    def setUp(self):
        cocotb_compile_and_run([os.getcwd() + '/test_SimSeq.v'])

        self.chip = Dut(cnfg_yaml)
        self.chip.init()

    def test_io(self):
        self.assertEqual(self.chip['SEQ_GEN'].get_mem_size(), 8 * 1024)

        self.chip['SEQ']['S0'][0] = 1
        self.chip['SEQ']['S1'][1] = 1
        self.chip['SEQ']['S2'][2] = 1
        self.chip['SEQ']['S3'][3] = 1

        self.chip['SEQ']['S4'][12] = 1
        self.chip['SEQ']['S5'][13] = 1
        self.chip['SEQ']['S6'][14] = 1
        self.chip['SEQ']['S7'][15] = 1

        pattern = [0x01, 0x02, 0x04, 0x08, 0, 0, 0, 0, 0, 0, 0, 0, 0x10, 0x20, 0x40, 0x80]

        self.chip['SEQ'].write(16)

        ret = self.chip['SEQ'].get_data(size=16)
        self.assertEqual(ret.tolist(), pattern)

        rec_size = 16 * 4 + 8
        self.chip['SEQ_REC'].set_en_ext_start(True)
        self.chip['SEQ_REC'].set_size(rec_size)

        self.chip['PULSE_GEN'].set_delay(1)
        self.chip['PULSE_GEN'].set_width(1)

        self.assertEqual(self.chip['PULSE_GEN'].get_delay(), 1)
        self.assertEqual(self.chip['PULSE_GEN'].get_width(), 1)

        self.chip['SEQ'].set_repeat(4)
        self.chip['SEQ'].set_en_ext_start(True)
        self.chip['SEQ'].set_size(16)
        # self.chip['SEQ'].start()

        self.chip['PULSE_GEN'].start()

        while(not self.chip['SEQ'].is_done()):
            pass

        ret = self.chip['SEQ_REC'].get_data(size=rec_size)
        self.assertEqual(ret.tolist(), [0x0] * 2 + pattern * 4 + [0x80] * 6)  # 2 clk delay + pattern x4 + 6 x last pattern

        #
        self.chip['SEQ'].set_repeat_start(12)
        self.chip['PULSE_GEN'].start()

        while(not self.chip['SEQ'].is_done()):
            pass

        ret = self.chip['SEQ_REC'].get_data(size=rec_size)
        self.assertEqual(ret.tolist(), [0x80] * 2 + pattern + pattern[12:] * 3 + [0x80] * 3 * 12 + [0x80] * 6)  # 2 clk delay 0x80 > from last pattern + ...

        self.chip['SEQ'].set_wait(4)
        self.chip['PULSE_GEN'].start()

        while(not self.chip['SEQ'].is_done()):
            pass

        ret = self.chip['SEQ_REC'].get_data(size=rec_size)
        lpat = pattern[12:] + [0x80] * 4
        self.assertEqual(ret.tolist(), [0x80] * 2 + pattern + [0x80] * 4 + lpat * 3 + [0x80] * (3 * 12 - 4 * 4) + [0x80] * 6)

        #
        rec_size = rec_size * 3
        self.chip['SEQ_REC'].set_size(rec_size)
        self.chip['SEQ'].set_clk_divide(3)
        self.chip['SEQ'].set_wait(3)
        self.chip['PULSE_GEN'].start()

        while(not self.chip['SEQ'].is_done()):
            pass

        ret = self.chip['SEQ_REC'].get_data(size=rec_size)
        lpat = pattern[12:] + [0x80] * 3
        mu_pat = pattern + [0x80] * 3 + lpat * 3
        fm = []
        for i in mu_pat:
            fm += [i, i, i]
        self.assertEqual(ret.tolist(), [0x80] * 2 + fm + [0x80] * 94)

        #
        self.chip['SEQ'].set_wait(0)
        self.chip['PULSE_GEN'].start()

        while(not self.chip['SEQ'].is_done()):
            pass

        ret = self.chip['SEQ_REC'].get_data(size=rec_size)
        lpat = pattern[12:]
        mu_pat = pattern + lpat * 3
        fm = []
        for i in mu_pat:
            fm += [i, i, i]
        self.assertEqual(ret.tolist(), [0x80] * 2 + fm + [0x80] * (94 + 4 * 3 * 3))

        # nested loop test
        pattern = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.chip['SEQ'].set_data(pattern)
        self.chip['SEQ'].set_repeat(4)
        self.chip['SEQ'].set_repeat_start(2)
        self.chip['SEQ'].set_nested_start(8)
        self.chip['SEQ'].set_nested_stop(12)
        self.chip['SEQ'].set_nested_repeat(3)
        self.chip['SEQ'].set_clk_divide(1)
        self.chip['PULSE_GEN'].start()

        while(not self.chip['SEQ'].is_done()):
            pass

        exp_pattern = [0x10, 0x10]
        exp_pattern += pattern[0:2]
        rep = pattern[2:8]
        rep += pattern[8:12] * 3
        rep += pattern[12:16]
        exp_pattern += rep * 4
        exp_pattern += [16] * 124

        ret = self.chip['SEQ_REC'].get_data(size=rec_size)
        self.assertEqual(ret.tolist(), exp_pattern)

    def tearDown(self):
        self.chip.close()  # let it close connection and stop simulator
        cocotb_compile_clean()

if __name__ == '__main__':
    unittest.main()
