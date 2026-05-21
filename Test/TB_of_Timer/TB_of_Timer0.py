import py4hw
from punxa_atmega328p.Timers import *
from punxa_atmega328p.Memory import * 
import time



def TB_of_Timer0(py4hw.Logic):
    def __init__(self,parent,name,port:MemoryInterface,Test_OC0A,Test_OC0B,Test_T0,Test_OCF0B,Test_OCF0A,Test_TOV0):
        super().__init__(parent,name)
    
        self.port0 = self.addInterfaceSink('port',port)
        self.Test_T0 = self.addIn('T0', Test_T0)
        self.Test_OC0B = self.addOut('OC0B', Test_OC0B)
        self.Test_OC0A = self.addOut('OC0A', Test_OC0A)

        self.Test_OCF0B = self.addOut('OCF0B', Test_OCF0B)
        self.Test_OCF0A = self.addOut('OCF0A', Test_OCF0A)
        self.Test_TOV0 = self.addOut('TOV0', Test_TOV0)

        self.CURRENT_TEST = 'START'

        self.INS_counter = 0

        self.TEST_RESULTS = []

#Table of test: 
# TEST1 :functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling
# TEST2 :functional incrementation test : Normal mode Compare Match Output B Clear and A Clear (writing using Ls) | No prescaling
# TEST3 :functional incrementation test : Normal mode Compare Match Output B Set and A Set (writing using Ls) | No prescaling (x3)
# TEST4 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x6.1)
# TEST5 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x6.2)
# TEST6 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x7)
# TEST7 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x8)
# TEST8 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x9)
# TEST9 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x10)
# TEST10 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x11)
# TEST11 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x12)
# TEST12 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x13)
# TEST13 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x14)
# TEST14 :functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x15)  


    def clock(self):

        match self.CURRENT_TEST:

            case 'START':
                print("Starting Test Bench of Timer0")


                self.CURRENT_TEST = 'TEST1'
            case 'TEST1':
                print("TEST1:")

                ## Loading the config values in memory
                    Timer0

                ## Testing


                ## Storing data


                self.CURRENT_TEST = 'TEST2'
            case 'TEST2':
                print("TEST2:")

                self.CURRENT_TEST = 'TEST3'
            case 'TEST3':
                print("TEST3:")

                self.CURRENT_TEST = 'TEST4'
            case 'TEST4':
                print("TEST4:")

                self.CURRENT_TEST = 'TEST5'
            case 'TEST5':
                print("TEST5:")

                self.CURRENT_TEST = 'TEST6'
            case 'TEST6':
                print("TEST6:")

                self.CURRENT_TEST = 'TEST7'
            case 'TEST7':
                print("TEST7:")

                self.CURRENT_TEST = 'TEST8'
            case 'TEST8':
                print("TEST8:")

                self.CURRENT_TEST = 'TEST9'
            case 'TEST9':
                print("TEST9:")

                self.CURRENT_TEST = 'TEST10'
            case 'TEST10':
                print("TEST10:")

                self.CURRENT_TEST = 'TEST11'
            case 'TEST11':
                print("TEST11:")

                self.CURRENT_TEST = 'TEST12'
            case 'TEST12':
                print("TEST12:")

                self.CURRENT_TEST = 'TEST13'
            case 'TEST13':
                print("TEST13:")

                self.CURRENT_TEST = 'TEST14' 
            case 'TEST14':
                print("TEST14:")

                self.CURRENT_TEST = 'FINAL'

            case 'FINAL':
                print("TEST SUMMARY:")

                self.CURRENT_TEST = 'FINAL'
"""

# Timer/Counter0 Behavioral Model Test Bench
# ATmega328P Datasheet Section 14
#
# Run from the project root directory with:
#   python -i -m Test.Timer0_test.Test_Timer0
#
# Commands:  Build_Hardware  Run_All_Tests  Run_Test(name)
#            list_commands   printState     Verbose_Test(name)

import py4hw
import os
from Source.Memory import *
from Source.Timer0 import TimerCounter0   # adjust path if needed

# ─── Globals ──────────────────────────────────────────────────────────────────

PASS_OR_FAIL_LIST = []
COMMANDS_LIST = [
    "Build_Hardware",
    "Run_All_Tests",
    "Run_Test(test_name)",
    "Verbose_Test(test_name)",
    "list_commands",
    "printState",
]

sys_hw  = None   # py4hw.HWSystem
TC0     = None   # TimerCounter0 instance
_port   = None   # MemoryInterface
_sigs   = {}     # name → py4hw.Wire


# ─── Hardware construction ─────────────────────────────────────────────────────

def Build_Hardware():
    """Instantiate a fresh Timer/Counter0 with all wires connected."""
    global sys_hw, TC0, _port, _sigs

    sys_hw = py4hw.HWSystem()

    _port = MemoryInterface(sys_hw, 'port0', 8, 16)

    _sigs['INSTYPE'] = py4hw.Wire(sys_hw, 'INSTYPE', 1)
    _sigs['OC0A']    = py4hw.Wire(sys_hw, 'OC0A',   1)
    _sigs['OC0B']    = py4hw.Wire(sys_hw, 'OC0B',   1)
    _sigs['T0']      = py4hw.Wire(sys_hw, 'T0',     1)
    _sigs['OCF0A']   = py4hw.Wire(sys_hw, 'OCF0A',  1)
    _sigs['OCF0B']   = py4hw.Wire(sys_hw, 'OCF0B',  1)
    _sigs['TOV0']    = py4hw.Wire(sys_hw, 'TOV0',   1)

    TC0 = TimerCounter0(
        sys_hw, 'TC0',
        _port,
        _sigs['INSTYPE'],
        _sigs['OC0B'],
        _sigs['OC0A'],
        _sigs['T0'],
        _sigs['OCF0B'],
        _sigs['OCF0A'],
        _sigs['TOV0'],
    )

    print("Hardware built: Timer/Counter0 ready")


# ─── Bus helpers ──────────────────────────────────────────────────────────────

def _reg_write(addr, value, ls=False):
    """Drive one register write on the memory bus."""
    _port.address.prepare(addr)
    _port.write.prepare(1)
    _port.read.prepare(0)
    _port.write_data.prepare(value & 0xFF)
    _sigs['INSTYPE'].prepare(1 if ls else 0)
    sys_hw.getSimulator().clk(1)
    _port.write.prepare(0)

def _reg_read(addr, ls=False):
    """Drive one register read and return the value."""
    _port.address.prepare(addr)
    _port.read.prepare(1)
    _port.write.prepare(0)
    _sigs['INSTYPE'].prepare(1 if ls else 0)
    sys_hw.getSimulator().clk(1)
    _port.read.prepare(0)
    return _port.read_data.get()

def _idle(n=1):
    """Advance n clock cycles with no bus activity (address 0 → no resp)."""
    _port.address.prepare(0x00)
    _port.read.prepare(0)
    _port.write.prepare(0)
    sys_hw.getSimulator().clk(n)

# ─── Register write shortcuts (IO space unless noted) ─────────────────────────

def _write_TCCR0A(v): _reg_write(0x24, v)
def _write_TCCR0B(v): _reg_write(0x25, v)
def _write_TCNT0(v):  _reg_write(0x26, v)
def _write_OCR0A(v):  _reg_write(0x27, v)
def _write_OCR0B(v):  _reg_write(0x28, v)
def _write_TIMSK0(v): _reg_write(0x6E, v, ls=True)   # TIMSK0 is LS-only

def _set_wgm_cs(wgm, cs):
    """Set WGM02:0 and CS02:0 in one step across TCCR0A/B."""
    tccr0a = (wgm & 0b11)                         # WGM01:WGM00 → TCCR0A[1:0]
    tccr0b = (((wgm >> 2) & 0b1) << 3) | (cs & 0b111)  # WGM02 → TCCR0B[3]
    _write_TCCR0A(tccr0a)
    _write_TCCR0B(tccr0b)

def _set_com0a(com):
    _write_TCCR0A((TC0.TCCR0A & 0x3F) | ((com & 0b11) << 6))

def _set_com0b(com):
    _write_TCCR0A((TC0.TCCR0A & 0xCF) | ((com & 0b11) << 4))


# ─── Result helpers ───────────────────────────────────────────────────────────

def _check(desc, condition, verbose=False):
    result = 'PASS' if condition else 'FAIL'
    entry  = (result == 'PASS', desc)
    PASS_OR_FAIL_LIST.append(entry)
    if verbose or result == 'FAIL':
        print("  [{r}] {d}".format(r=result, d=desc))
    return result == 'PASS'


# ══════════════════════════════════════════════════════════════════════════════
# Individual test functions
# Each rebuilds hardware so tests are fully independent.
# ══════════════════════════════════════════════════════════════════════════════

# ── §14.9  Register read/write ────────────────────────────────────────────────
def test_register_readwrite(verbose=False):
    Build_Hardware()
    desc = "§14.9 Register Read/Write"
    ok   = True

    _write_TCCR0A(0b10110011)
    ok &= _check("{d}: TCCR0A write/read-back".format(d=desc),
                 _reg_read(0x24) == 0b10110011, verbose)

    _write_OCR0A(0xAB)
    ok &= _check("{d}: OCR0A write/read-back".format(d=desc),
                 _reg_read(0x27) == 0xAB, verbose)

    _write_OCR0B(0xCD)
    ok &= _check("{d}: OCR0B write/read-back".format(d=desc),
                 _reg_read(0x28) == 0xCD, verbose)

    _write_TCNT0(0x55)
    ok &= _check("{d}: TCNT0 write/read-back".format(d=desc),
                 _reg_read(0x26) == 0x55, verbose)

    _write_TIMSK0(0b111)
    ok &= _check("{d}: TIMSK0 write/read-back (LS address)".format(d=desc),
                 TC0.TIMSK0 == 0b111, verbose)

    # FOC0A/B always read as 0 (§14.9.2)
    _write_TCCR0B(0b11000001)   # FOC0A | FOC0B | CS=1
    ok &= _check("{d}: FOC0A/B always read as 0".format(d=desc),
                 (_reg_read(0x25) & 0b11000000) == 0, verbose)

    return ok


# ── §14.4  CS=0 stops the timer ───────────────────────────────────────────────
def test_cs0_stops_timer(verbose=False):
    Build_Hardware()
    desc = "§14.4 CS=0 stops timer"
    _set_wgm_cs(0, 0)
    _idle(20)
    return _check(desc, TC0.TCNT0 == 0, verbose)


# ── §14.3  Prescaler ratios ───────────────────────────────────────────────────
def test_prescaler(verbose=False):
    Build_Hardware()
    desc = "§14.3 Prescaler"
    ok   = True
    for cs, factor in [(1,1),(2,8),(3,64),(4,256),(5,1024)]:
        Build_Hardware()
        _set_wgm_cs(0, cs)
        _idle(factor)
        ok &= _check("{d}: CS={c} factor={f} → TCNT0==1".format(d=desc,c=cs,f=factor),
                     TC0.TCNT0 == 1, verbose)
    return ok


# ── §14.4  External clock T0 pin (CS=6 falling, CS=7 rising) ─────────────────
def test_external_clock(verbose=False):
    Build_Hardware()
    desc = "§14.4 External clock"
    ok   = True

    # CS=6  falling edge increments
    _set_wgm_cs(0, 6)
    _sigs['T0'].prepare(1); _idle(1)   # set T0 high
    _sigs['T0'].prepare(0); _idle(1)   # falling edge
    ok &= _check("{d}: CS=6 increments on falling edge".format(d=desc),
                 TC0.TCNT0 == 1, verbose)
    _sigs['T0'].prepare(1); _idle(1)   # rising edge – must NOT count
    ok &= _check("{d}: CS=6 does NOT increment on rising edge".format(d=desc),
                 TC0.TCNT0 == 1, verbose)

    # CS=7  rising edge increments
    Build_Hardware()
    _set_wgm_cs(0, 7)
    _sigs['T0'].prepare(0); _idle(1)
    _sigs['T0'].prepare(1); _idle(1)   # rising edge
    ok &= _check("{d}: CS=7 increments on rising edge".format(d=desc),
                 TC0.TCNT0 == 1, verbose)
    _sigs['T0'].prepare(0); _idle(1)   # falling edge – must NOT count
    ok &= _check("{d}: CS=7 does NOT increment on falling edge".format(d=desc),
                 TC0.TCNT0 == 1, verbose)

    return ok


# ── §14.7.1  Normal mode ──────────────────────────────────────────────────────
def test_normal_mode(verbose=False):
    Build_Hardware()
    desc = "§14.7.1 Normal"
    ok   = True

    _set_wgm_cs(0, 1)
    _idle(5)
    ok &= _check("{d}: counts up 5 ticks".format(d=desc),
                 TC0.TCNT0 == 5, verbose)

    # Wrap 0xFF → 0x00
    _write_TCNT0(0xFE); _idle(1)
    ok &= _check("{d}: 0xFE→0xFF".format(d=desc), TC0.TCNT0 == 0xFF, verbose)
    _idle(1)
    ok &= _check("{d}: 0xFF wraps to 0x00".format(d=desc), TC0.TCNT0 == 0x00, verbose)

    # TOV0 set on overflow (§14.7.1)
    Build_Hardware()
    _set_wgm_cs(0, 1)
    _write_TIMSK0(0b001)   # TOIE0
    _write_TCNT0(0xFF)
    _idle(1)
    ok &= _check("{d}: TOV0 set on 0xFF→0x00 overflow".format(d=desc),
                 TC0.TOV0.get() == 1, verbose)

    return ok


# ── §14.7.2  CTC mode ─────────────────────────────────────────────────────────
def test_ctc_mode(verbose=False):
    Build_Hardware()
    desc = "§14.7.2 CTC"
    ok   = True

    _set_wgm_cs(2, 1)
    _write_OCR0A(4)
    _idle(4)
    ok &= _check("{d}: counts up to OCR0A=4".format(d=desc),
                 TC0.TCNT0 == 4, verbose)
    _idle(1)
    ok &= _check("{d}: clears to 0x00 on compare match".format(d=desc),
                 TC0.TCNT0 == 0x00, verbose)

    # OCF0A interrupt on match (§14.5)
    Build_Hardware()
    _set_wgm_cs(2, 1)
    _write_OCR0A(3)
    _write_TIMSK0(0b010)   # OCIE0A
    _idle(3)
    ok &= _check("{d}: OCF0A set when TCNT0==OCR0A".format(d=desc),
                 TC0.OCF0A.get() == 1, verbose)

    # TOV0 must NOT fire at the CTC clear moment (§14.7.2 last paragraph)
    # TOV0 only fires when the FREE-RUNNING counter passes MAX (0xFF→0x00)
    Build_Hardware()
    _set_wgm_cs(2, 1)
    _write_OCR0A(5)
    _write_TIMSK0(0b001)   # TOIE0
    _idle(6)   # one CTC clear cycle
    ok &= _check("{d}: TOV0 NOT set at CTC clear event".format(d=desc),
                 TC0.TOV0.get() == 0, verbose)

    # OC0A toggle in CTC (COM0A=1, §14.7.2)
    Build_Hardware()
    _set_wgm_cs(2, 1)
    _write_OCR0A(4)
    _set_com0a(1)
    prev = TC0.OC0A.get()
    _idle(4)
    ok &= _check("{d}: OC0A toggles on compare match (COM0A=1)".format(d=desc),
                 TC0.OC0A.get() != prev, verbose)

    return ok


# ── §14.7.3  Fast PWM WGM=3 (TOP=0xFF) ───────────────────────────────────────
def test_fast_pwm_wgm3(verbose=False):
    Build_Hardware()
    desc = "§14.7.3 Fast PWM WGM=3"
    ok   = True

    # Single-slope: wraps 0xFF → 0x00 (§14.7.3)
    _set_wgm_cs(3, 1)
    _write_TCNT0(0xFF)
    _idle(1)
    ok &= _check("{d}: single-slope wrap 0xFF→0x00".format(d=desc),
                 TC0.TCNT0 == 0x00, verbose)

    # TOV0 at TOP (Table 14-8)
    Build_Hardware()
    _set_wgm_cs(3, 1)
    _write_TIMSK0(0b001)
    _write_TCNT0(0xFF)
    _idle(1)
    ok &= _check("{d}: TOV0 set at TOP (0xFF)".format(d=desc),
                 TC0.TOV0.get() == 1, verbose)

    # Non-inverting COM0A=2: OC0A set at BOTTOM, cleared on match (§14.7.3)
    Build_Hardware()
    _set_wgm_cs(3, 1)
    _write_OCR0A(10)
    _set_com0a(2)
    _idle(1)   # BOTTOM → OC0A should be set
    ok &= _check("{d}: non-inv OC0A=1 at BOTTOM".format(d=desc),
                 TC0.OC0A.get() == 1, verbose)
    _idle(10)  # reach compare match → OC0A cleared
    ok &= _check("{d}: non-inv OC0A=0 after compare match".format(d=desc),
                 TC0.OC0A.get() == 0, verbose)

    # Inverting COM0A=3: OC0A cleared at BOTTOM, set on match (§14.7.3)
    Build_Hardware()
    _set_wgm_cs(3, 1)
    _write_OCR0A(10)
    _set_com0a(3)
    _idle(1)
    ok &= _check("{d}: inv OC0A=0 at BOTTOM".format(d=desc),
                 TC0.OC0A.get() == 0, verbose)
    _idle(10)
    ok &= _check("{d}: inv OC0A=1 after compare match".format(d=desc),
                 TC0.OC0A.get() == 1, verbose)

    # COM0B=1 is reserved in Fast PWM – OC0B must stay 0 (Table 14-6)
    Build_Hardware()
    _set_wgm_cs(3, 1)
    _set_com0b(1)
    _write_OCR0B(5)
    _idle(10)
    ok &= _check("{d}: COM0B=1 reserved → OC0B stays 0".format(d=desc),
                 TC0.OC0B.get() == 0, verbose)

    return ok


# ── §14.7.3  Fast PWM WGM=7 (TOP=OCR0A) ─────────────────────────────────────
def test_fast_pwm_wgm7(verbose=False):
    Build_Hardware()
    desc = "§14.7.3 Fast PWM WGM=7"
    ok   = True

    _set_wgm_cs(7, 1)
    _write_OCR0A(20)
    _idle(20)
    ok &= _check("{d}: TCNT0 reaches OCR0A=20".format(d=desc),
                 TC0.TCNT0 == 20, verbose)
    _idle(1)
    ok &= _check("{d}: TCNT0 clears to 0 at TOP=OCR0A".format(d=desc),
                 TC0.TCNT0 == 0, verbose)

    # TOV0 at TOP=OCR0A (Table 14-8)
    Build_Hardware()
    _set_wgm_cs(7, 1)
    _write_OCR0A(10)
    _write_TIMSK0(0b001)
    _write_TCNT0(10)
    _idle(1)
    ok &= _check("{d}: TOV0 set at TOP=OCR0A".format(d=desc),
                 TC0.TOV0.get() == 1, verbose)

    return ok


# ── §14.7.4  Phase-Correct PWM WGM=1 (TOP=0xFF) ──────────────────────────────
def test_phase_correct_wgm1(verbose=False):
    Build_Hardware()
    desc = "§14.7.4 Phase-Correct PWM WGM=1"
    ok   = True

    _set_wgm_cs(1, 1)

    # Count up to TOP
    _idle(0xFF)
    ok &= _check("{d}: TCNT0 reaches TOP=0xFF".format(d=desc),
                 TC0.TCNT0 == 0xFF, verbose)
    ok &= _check("{d}: direction switches to Decrement at TOP".format(d=desc),
                 TC0.direction == 'Decrement', verbose)

    # Count down to BOTTOM
    _idle(1)
    ok &= _check("{d}: begins counting down from TOP".format(d=desc),
                 TC0.TCNT0 == 0xFE, verbose)
    _idle(0xFE)
    ok &= _check("{d}: reaches BOTTOM=0x00".format(d=desc),
                 TC0.TCNT0 == 0x00, verbose)
    ok &= _check("{d}: direction switches to Increment at BOTTOM".format(d=desc),
                 TC0.direction == 'Increment', verbose)

    # TOV0 set at BOTTOM (Table 14-8)
    Build_Hardware()
    _set_wgm_cs(1, 1)
    _write_TIMSK0(0b001)
    TC0.TCNT0    = 1
    TC0.direction = 'Decrement'
    _idle(1)
    ok &= _check("{d}: TOV0 set when counter reaches BOTTOM".format(d=desc),
                 TC0.TOV0.get() == 1, verbose)

    # Non-inverting COM0A=2 (Table 14-4): clear up-count, set down-count
    Build_Hardware()
    _set_wgm_cs(1, 1)
    _write_OCR0A(50)
    _set_com0a(2)
    _idle(51)   # pass OCR0A while upcounting
    ok &= _check("{d}: non-inv OC0A cleared on up-count match".format(d=desc),
                 TC0.OC0A.get() == 0, verbose)
    _idle(0xFF - 51 + 0xFF - 50)   # reach TOP then count down through OCR0A
    ok &= _check("{d}: non-inv OC0A set on down-count match".format(d=desc),
                 TC0.OC0A.get() == 1, verbose)

    # Inverting COM0A=3 (Table 14-4): set up-count, clear down-count
    Build_Hardware()
    _set_wgm_cs(1, 1)
    _write_OCR0A(50)
    _set_com0a(3)
    _idle(51)
    ok &= _check("{d}: inv OC0A set on up-count match".format(d=desc),
                 TC0.OC0A.get() == 1, verbose)
    _idle(0xFF - 51 + 0xFF - 50)
    ok &= _check("{d}: inv OC0A cleared on down-count match".format(d=desc),
                 TC0.OC0A.get() == 0, verbose)

    return ok


# ── §14.7.4  Phase-Correct PWM WGM=5 (TOP=OCR0A) ────────────────────────────
def test_phase_correct_wgm5(verbose=False):
    Build_Hardware()
    desc = "§14.7.4 Phase-Correct PWM WGM=5"
    ok   = True

    _set_wgm_cs(5, 1)
    _write_OCR0A(30)
    _idle(30)
    ok &= _check("{d}: TCNT0 reaches TOP=OCR0A=30".format(d=desc),
                 TC0.TCNT0 == 30, verbose)
    ok &= _check("{d}: direction = Decrement at TOP".format(d=desc),
                 TC0.direction == 'Decrement', verbose)
    _idle(30)
    ok &= _check("{d}: TCNT0 returns to BOTTOM=0".format(d=desc),
                 TC0.TCNT0 == 0, verbose)

    return ok


# ── §14.9.1  WGM bits decoded correctly for all 8 modes ──────────────────────
def test_wgm_decoding(verbose=False):
    desc = "§14.9.1 WGM decoding"
    ok   = True
    for mode in range(8):
        Build_Hardware()
        tccr0a = (mode & 0b11)
        tccr0b = (((mode >> 2) & 0b1) << 3)
        _write_TCCR0A(tccr0a)
        _write_TCCR0B(tccr0b)
        _idle(1)   # let parse run
        ok &= _check("{d}: WGM={m} parsed from TCCR0A/B".format(d=desc, m=mode),
                     TC0.WGM == mode, verbose)
    return ok


# ── §14.9.1  COM0A/B bits decoded correctly ───────────────────────────────────
def test_com_decoding(verbose=False):
    desc = "§14.9.1 COM decoding"
    ok   = True
    for com in range(4):
        Build_Hardware()
        _write_TCCR0A((com << 6) | (com << 4))
        _idle(1)
        ok &= _check("{d}: COM0A={c}".format(d=desc, c=com), TC0.COM0A == com, verbose)
        ok &= _check("{d}: COM0B={c}".format(d=desc, c=com), TC0.COM0B == com, verbose)
    return ok


# ── §14.5.1  Force Output Compare (FOC0A/B) non-PWM only ─────────────────────
def test_foc(verbose=False):
    Build_Hardware()
    desc = "§14.5.1 FOC"
    ok   = True

    _set_wgm_cs(0, 1)   # Normal (non-PWM)
    _set_com0a(1)        # toggle on match
    prev = TC0.OC0A.get()
    # Write FOC0A (bit7) to TCCR0B with CS=1 still set
    _reg_write(0x25, 0b10000001)   # FOC0A | CS=1
    ok &= _check("{d}: FOC0A toggles OC0A immediately in normal mode".format(d=desc),
                 TC0.OC0A.get() != prev, verbose)

    # FOC must NOT generate an interrupt (§14.9.2)
    Build_Hardware()
    _set_wgm_cs(0, 1)
    _set_com0a(1)
    _write_TIMSK0(0b010)   # OCIE0A enabled
    _reg_write(0x25, 0b10000001)
    ok &= _check("{d}: FOC0A does NOT set OCF0A interrupt flag".format(d=desc),
                 TC0.OCF0A.get() == 0, verbose)

    return ok


# ── §14.5.2  TCNT0 write blocks next compare match ───────────────────────────
def test_tcnt0_write_blocks_match(verbose=False):
    Build_Hardware()
    desc = "§14.5.2 TCNT0 write blocks match"
    ok   = True

    _set_wgm_cs(0, 1)
    _write_OCR0A(10)
    _write_TIMSK0(0b010)   # OCIE0A
    _write_TCNT0(10)       # write TCNT0 == OCR0A → match on THIS cycle suppressed
    # The cycle immediately after the write must NOT trigger OCF0A
    _idle(1)
    ok &= _check("{d}: match suppressed on cycle after TCNT0 write".format(d=desc),
                 TC0.OCF0A.get() == 0, verbose)
    # The FOLLOWING cycle the match fires normally
    _idle(1)
    ok &= _check("{d}: match fires on next cycle after blocked cycle".format(d=desc),
                 TC0.OCF0A.get() == 1, verbose)

    return ok


# ══════════════════════════════════════════════════════════════════════════════
# BUG CHECKS  – each deliberately verifies a known model deviation from
# the datasheet.  A FAIL here means the bug is still present.
# ══════════════════════════════════════════════════════════════════════════════

def test_known_bugs(verbose=False):
    desc_prefix = "[BUG]"
    ok_all = True

    # BUG-1 §14.7.4: Phase-Correct decrement block unreachable.
    # The `elif direction=='Decrement'` is nested inside
    # `if direction=='Increment'` so it can never execute.
    Build_Hardware()
    _set_wgm_cs(1, 1)
    TC0.TCNT0     = 0xFF
    TC0.direction = 'Decrement'
    _idle(1)
    ok = _check(
        "{p} BUG-1 §14.7.4: TCNT0 decrements when direction=Decrement".format(p=desc_prefix),
        TC0.TCNT0 == 0xFE, verbose)
    ok_all &= ok

    # BUG-2 §14.5/Normal: OCF0A set unconditionally after COM0A match block,
    # firing even when COM0A=0 (OC0A disconnected).
    Build_Hardware()
    _set_wgm_cs(0, 1)
    _write_OCR0A(5)
    _write_TCCR0A(0x00)   # COM0A=0 (disconnected)
    _write_TIMSK0(0b010)
    _idle(5)
    ok = _check(
        "{p} BUG-2 §14.5: OCF0A must NOT fire when COM0A=0 (OC0A disconnected)".format(p=desc_prefix),
        TC0.OCF0A.get() == 0, verbose)
    ok_all &= ok

    # BUG-3 §14.9.7: OCF0A/OCF0B written as plain int attributes,
    # not through the signal's .prepare() path → .get() returns stale value.
    Build_Hardware()
    _set_wgm_cs(0, 1)
    _write_OCR0A(3)
    _set_com0a(1)
    _write_TIMSK0(0b010)
    _idle(3)
    ok = _check(
        "{p} BUG-3 §14.9.7: OCF0A readable via signal .get() after match".format(p=desc_prefix),
        TC0.OCF0A.get() == 1, verbose)
    ok_all &= ok

    # BUG-4 §14.9.2: FOC0A never parsed. Model writes `self.FOC0B` twice;
    # `self.FOC0A` is left from __init__ (always 0).
    Build_Hardware()
    _reg_write(0x25, 0b11000001)   # FOC0A | FOC0B | CS=1
    _idle(1)
    ok = _check(
        "{p} BUG-4 §14.9.2: FOC0A parsed from TCCR0B bit7 (typo overwrites with FOC0B)".format(p=desc_prefix),
        TC0.FOC0A == 1, verbose)
    ok_all &= ok

    # BUG-5 §14.7.2: CTC uses `> self.TOP` instead of `>= self.TOP`.
    # Counter overshoots to TOP+1 before clearing.
    Build_Hardware()
    _set_wgm_cs(2, 1)
    _write_OCR0A(5)
    _idle(5)   # at TCNT0==OCR0A the model should clear, not at 6
    ok = _check(
        "{p} BUG-5 §14.7.2: CTC clears when TCNT0==OCR0A, not OCR0A+1".format(p=desc_prefix),
        TC0.TCNT0 == 0, verbose)
    ok_all &= ok

    # BUG-6 §14.9.7: OCF0B interrupt uses `self.OCFOB` (lowercase o) typo
    # so the OCF0B Wire signal is never driven.
    Build_Hardware()
    _set_wgm_cs(0, 1)
    _write_OCR0B(5)
    _set_com0b(1)   # toggle on match
    _write_TIMSK0(0b100)   # OCIE0B
    _idle(5)
    ok = _check(
        "{p} BUG-6 §14.9.7: OCF0B signal fires at compare match (OCFOB typo)".format(p=desc_prefix),
        TC0.OCF0B.get() == 1, verbose)
    ok_all &= ok

    return ok_all


# ══════════════════════════════════════════════════════════════════════════════
# Top-level runners
# ══════════════════════════════════════════════════════════════════════════════

_ALL_TESTS = {
    "register_readwrite"    : test_register_readwrite,
    "cs0_stops_timer"       : test_cs0_stops_timer,
    "prescaler"             : test_prescaler,
    "external_clock"        : test_external_clock,
    "normal_mode"           : test_normal_mode,
    "ctc_mode"              : test_ctc_mode,
    "fast_pwm_wgm3"         : test_fast_pwm_wgm3,
    "fast_pwm_wgm7"         : test_fast_pwm_wgm7,
    "phase_correct_wgm1"    : test_phase_correct_wgm1,
    "phase_correct_wgm5"    : test_phase_correct_wgm5,
    "wgm_decoding"          : test_wgm_decoding,
    "com_decoding"          : test_com_decoding,
    "foc"                   : test_foc,
    "tcnt0_write_blocks"    : test_tcnt0_write_blocks_match,
    "known_bugs"            : test_known_bugs,
}

def Run_All_Tests(verbose=False):
    """Run every test, write results to Test_Timer0_Results.txt."""
    global PASS_OR_FAIL_LIST
    PASS_OR_FAIL_LIST = []

    if os.path.exists("Test/Timer0_test/Test_Timer0_Results.txt"):
        os.remove("Test/Timer0_test/Test_Timer0_Results.txt")

    results = open("Test/Timer0_test/Test_Timer0_Results.txt", "a")

    print("=" * 60)
    print("Timer/Counter0 Verification  (ATmega328P §14)")
    print("=" * 60)

    for name, fn in _ALL_TESTS.items():
        ok = fn(verbose=verbose)
        tag = 'PASS' if ok else 'FAIL'
        line = "test:{name:<26} {tag}\n".format(name=name, tag=tag)
        results.write(line)
        if verbose or not ok:
            print("[{tag}] {name}".format(tag=tag, name=name))

    results.close()

    total  = len(PASS_OR_FAIL_LIST)
    passed = sum(1 for ok, _ in PASS_OR_FAIL_LIST if ok)
    failed = total - passed

    print("=" * 60)
    print("Results: {p} passed,  {f} failed  ({t} checks total)".format(
          p=passed, f=failed, t=total))
    print("=" * 60)
    print("Full report: Test/Timer0_test/Test_Timer0_Results.txt")

def Run_Test(test_name, verbose=True):
    """Run a single named test with verbose output."""
    global PASS_OR_FAIL_LIST
    PASS_OR_FAIL_LIST = []
    if test_name not in _ALL_TESTS:
        print("Unknown test '{t}'. Available: {a}".format(
              t=test_name, a=list(_ALL_TESTS.keys())))
        return
    ok = _ALL_TESTS[test_name](verbose=verbose)
    print("\n[{tag}] {name}".format(tag='PASS' if ok else 'FAIL', name=test_name))

def Verbose_Test(test_name):
    Run_Test(test_name, verbose=True)

def printState():
    if TC0 is None:
        print("Hardware not built. Call Build_Hardware() first.")
        return
    print("─" * 40)
    print("TCNT0 : {v}  (0x{v:02X})".format(v=TC0.TCNT0))
    print("OCR0A : {v}  OCR0B : {w}".format(v=TC0.OCR0A, w=TC0.OCR0B))
    print("WGM   : {v}  CS    : {w}  opMode: {m}".format(
          v=TC0.WGM, w=TC0.CS, m=TC0.opMode))
    print("COM0A : {a}  COM0B : {b}".format(a=TC0.COM0A, b=TC0.COM0B))
    print("OC0A  : {a}  OC0B  : {b}".format(
          a=TC0.OC0A.get(), b=TC0.OC0B.get()))
    print("OCF0A : {a}  OCF0B : {b}  TOV0 : {t}".format(
          a=TC0.OCF0A.get(), b=TC0.OCF0B.get(), t=TC0.TOV0.get()))
    print("direction: {d}  prescalerCounter: {p}".format(
          d=TC0.direction, p=TC0.prescalerCounter))
    print("TCCR0A: 0b{a:08b}  TCCR0B: 0b{b:08b}".format(
          a=TC0.TCCR0A, b=TC0.TCCR0B))
    print("TIMSK0: 0b{v:08b}  TIFR0 : 0b{w:08b}".format(
          v=TC0.TIMSK0, w=TC0.TIFR0))
    print("─" * 40)

def list_commands():
    for cmd in COMMANDS_LIST:
        print(cmd)