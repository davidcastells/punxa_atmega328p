import py4hw
from punxa_atmega328p.Timers import *
from punxa_atmega328p.Memory import * 
import time
import math



def TestBench_of_Timer1():

    sys = py4hw.HWSystem()

    SIGNALS1 = []

    OCF1B = py4hw.Wire(sys,'OCF1B',1)
    SIGNALS1.append(OCF1B)
    OCF1A = py4hw.Wire(sys,'OCF1A',1)
    SIGNALS1.append(OCF1A)
    TOV1 = py4hw.Wire(sys,'TOV1',1)
    SIGNALS1.append(TOV1)

    OC1A = py4hw.Wire(sys,'OC1A',1)
    SIGNALS1.append(OC1A)
    OC1B = py4hw.Wire(sys,'OC1B',1)
    SIGNALS1.append(OC1B)
    T1 = py4hw.Wire(sys,'T1',1)
    SIGNALS1.append(T1)
    ICF1 = py4hw.Wire(sys,'ICF1',1)
    SIGNALS1.append(ICF1)

    interface1 = MemoryInterface(sys,'interface1',8,16)

    TIMER1 = TimerCounter1(sys,'TIMER1',interface1,OC1B,OC1A,T1,OCF1B,OCF1A,TOV1,ICF1)

    SIGNALS1.append(interface1.write)
    SIGNALS1.append(interface1.read)
    SIGNALS1.append(interface1.address)
    SIGNALS1.append(interface1.write_data)
    SIGNALS1.append(interface1.read_data)
    SIGNALS1.append(interface1.resp)

    CURRENT_TEST = 'START'

    wvf = py4hw.Waveform(sys,'wvf',SIGNALS1)

    #sch = py4hw.Schematic(sys)
    #sch.draw()

    #sys.getSimulator().clk(len(TIMER0_WRITE_DATA_TEST))

    Testing = True
    with open("Test/TB_of_Timer/Test_Results.txt",'w+') as results:
        while Testing:
            match CURRENT_TEST:
                case 'START':
                    results.write("Starting Test Bench of Timer1")
                    CURRENT_TEST = 'TEST0'
                case 'TEST0':# TEST0 :Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
                    results.write("TEST0\n")
                    #Setup
                    ## Loading the config values in memory
                    TIMER1.TCCR1A = 0x00
                    TIMER1.TCCR1B = 0x01
                    TIMER1.TCCR1C = 0x00

                    TIMER1.OCR1BH = 0
                    TIMER1.OCR1BL = 0
                    TIMER1.OCR1AH = 0
                    TIMER1.OCR1AL = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.TCNT1H = 0
                    TIMER1.TCNT1L = 0

                    ## Testing
                    for i in range(65536):
                        # counter test 

                        if TIMER1.TCNT1 != i%65536:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,i%65536))

                        #Output A
                        if OC1A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}".format(1,0))

                        #Output B 
                        if OC1B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER1.TCNT1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}| iteration = {}".format(0,1,i))

                        #Interrupt B 
                        if (TIMER1.TCNT1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}| iteration = {}".format(0,1,i))

                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFFFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys.getSimulator().clk(1)
                        

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)

                    
                    CURRENT_TEST = 'TEST1'
                case 'TEST1':# TEST1 :Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls to load data) | No prescaling (X2)
                    results.write("TEST1\n")
                    #Setup
                    ## Loading the config values in memory
                    TIMER1.TCCR1A = 0x50
                    TIMER1.TCCR1B = 0x01
                    TIMER1.TCCR1C = 0x00

                    TIMER1.OCR1BH = 0b00010011
                    TIMER1.OCR1BL = 0b10001000
                    TIMER1.OCR1AH = 0b00100111
                    TIMER1.OCR1AL = 0b00010000

                    TIMER1.TCNT1H = 0
                    TIMER1.TCNT1L = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1A_val = 0
                    TIMER1.OC1B_val = 0

                    last_OC1A = 0
                    last_OC1B = 0

                    ## Testing
                    for i in range(65536):
                        # counter test 

                        if TIMER1.TCNT1 != i%65536:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,i%65536))

                        #Output A 
                        if TIMER1.TCNT1 >= TIMER1.OCR1A:
                            if OC1A.get() == last_OC1A:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}| Iteration = {}".format(last_OC1A,(1-last_OC1A),i))
                        else:
                            last_OC1A = OC1A.get()

                        #Output B 
                        if TIMER1.TCNT1 >= TIMER1.OCR1B:
                            if OC1B.get() == last_OC1B:# error val
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}| Iteration = {}".format(last_OC1B,(1-last_OC1B),i))
                        else:
                            last_OC1B = OC1B.get()

                        #Interrupt A
                        if (TIMER1.TCNT1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}| Iteration = {}".format(0,1,i))

                        #Interrupt B 
                        if (TIMER1.TCNT1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}| Iteration = {}".format(0,1,i))

                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFFFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}| Iteration = {}".format(0,1,i))

                        sys.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)

                    break
                    ## Storing data
                    CURRENT_TEST = 'TEST2'
                case 'TEST2':# TEST2 :Normal mode Compare Match Output B Clear and A Clear (writing using Ls to load data) | No prescaling (X3)
                    results.write("TEST2\n")
                    #Setup
                    TIMER1.TCCR1A = 0xA0
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1A_val = 1
                    TIMER1.OC1B_val = 1
                

                ## Testing
                    for i in range(255):
                        # counter test 

                        if TIMER1.TCNT1 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,i%255))

                        #Output A 
                        if TIMER1.TCNT1 >= TIMER1.OCR1A:
                            if OC1A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}| Iteration = {}".format(0,1,i))
                        else:
                            if OC1A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}| Iteration = {}".format(1,0,i))
        
                        #Output B 
                        if TIMER1.TCNT1 >= TIMER1.OCR1B:
                            if OC1B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}| Iteration = {}".format(0,1,i))
                        else:
                            if OC1B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}| Iteration = {}".format(1,0,i))

                        #Interrupt A
                        if (TIMER1.TCNT1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}| Iteration = {}".format(0,1,i))

                        #Interrupt B 
                        if (TIMER1.TCNT1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}| Iteration = {}".format(0,1,i))

                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}| Iteration = {}".format(0,1,i))

                        sys.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)


                    CURRENT_TEST = 'TEST3'
                case 'TEST3':# TEST3 :Normal mode Compare Match Output B Set and A Set (writing using Ls to load data) | No prescaling (X4)
                    results.write("TEST3\n")
                    #Setup
                    TIMER1.TCCR1A = 0xF0
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1A_val = 0
                    TIMER1.OC1B_val = 0

                ## Testing
                    for i in range(255):
                        # counter test 

                        if TIMER1.TCNT1 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,i%255))

                        #Output A 
                        if TIMER1.TCNT1 >= TIMER1.OCR1A:
                            if OC1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}| Iteration = {}".format(0,1,i))
                        else:
                            if OC1A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}| Iteration = {}".format(1,0,i))
        
                        #Output B 
                        if TIMER1.TCNT1 >= TIMER1.OCR1B:
                            if OC1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}| Iteration = {}".format(0,1,i))
                        else:
                            if OC1B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}| Iteration = {}".format(1,0,i))

                        #Interrupt A
                        if (TIMER1.TCNT1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}".format(0,1))
                        #else:
                        #    if OCF0A.get() == 1:
                        #        TEST = False
                        #        ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER1.TCNT1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}".format(0,1))
                        #else:
                        #    if OCF0A.get() == 1:
                        #        TEST = False
                        #        ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)

                    CURRENT_TEST = 'TEST4'
                case 'TEST4': # TEST4 :Fast PWM Mode mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X5)
                    results.write("TEST4\n")
                    #Setup
                    TIMER1.TCCR1A = 0x03
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1A_val = 0
                    TIMER1.OC1B_val = 0

                    sys.getSimulator().clk(1)

                    TIMER1.TCNT1 = 0

                ## Testing
                    for i in range(255):
                        # counter test 
                        if TIMER1.TCNT1 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}| iteration = ".format(TIMER1.TCNT1,i%255))


                        #Output A
                        if OC1A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}| iteration = {}".format(1,0,i))


                        #Output B 
                        if OC1B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1B = {} expected {}| iteration = {}".format(1,0,i))


                        #Interrupt A
                        if (TIMER1.TCNT1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}| iteration = {}".format(0,1,i))


                        #Interrupt B 
                        if (TIMER1.TCNT1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}| iteration = {}".format(0,1,i))

                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)

                    CURRENT_TEST = 'TEST5'
                case 'TEST5':# TEST5 :Fast PWM Mode mode Compare Match Output B disconnected and A (Normal port operation, OC0A disconnected) (writing using Ls to load data) | No prescaling (X6.1)
                    results.write("TEST5\n")
                    #Setup
                    TIMER1.TCCR1A = 0x53
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1A_val = 0
                    TIMER1.OC1B_val = 0

                    last_OC1A = 0
                    last_OC1B = 0

                ## Testing
                    for i in range(255):
                        # counter test 
                        if TIMER1.TCNT1 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,i%255))

                        #Output A
                        if OC1A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}".format(1,0))

                        #Output B 
                        if OC1B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1B = {} expected {}".format(1,0))


                        #Interrupt A
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}| Iteration = {}".format(0,1,i))


                        #Interrupt B 
                        if TIMER1.TCNT1-1 == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}| Iteration = {}".format(0,1,i))


                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}| Iteration = {}".format(0,1,i))

                        sys.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)

                    CURRENT_TEST = 'TEST6'
                case 'TEST6':# TEST6 :Fast PWM Mode mode Compare Match Output B disconnected and A (Toggle OC0A on compare match.) (writing using Ls to load data) | No prescaling (X6.2)
                    results.write("TEST6\n")
                    #Setup
                    TIMER1.TCCR1A = 0x53
                    TIMER1.TCCR1B = 0x09

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                ## Testing
                    for i in range(255):
                        # counter test 
                        if TIMER1.TCNT1 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT2 = {} expected {}".format(TIMER1.TCNT1,i%255))

                        #Output A 
                        if TIMER1.TCNT1 >= TIMER1.OCR1A:
                            if OC1A.get() == last_OC1A:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}| Iteration = {}".format(last_OC1A,(1-last_OC1A),i))
                        else:
                            last_OC1A = OC1A.get()


                        if OC1B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1B = {} expected {}| Iteration = {}".format(1,0,i))


                        #Interrupt A
                        if (TIMER1.TCNT1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}| Iteration = {}".format(0,1,i))


                        #Interrupt B 
                        if TIMER1.TCNT1 == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}| Iteration = {}".format(0,1,i))


                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}| Iteration = {}".format(0,1,i))

                        sys.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)

                    CURRENT_TEST = 'TEST7'
                case 'TEST7':# TEST7 :Fast PWM Mode mode Compare Match Output B (Clear OC0B on compare match, set OC0B at BOTTOM,(non-inverting mode)) and A (Clear OC0A on compare match, set OC0A at BOTTOM,(non-inverting mode).) (writing using Ls to load data) | No prescaling (X7)
                    results.write("TEST7\n")
                    #Setup
                    TIMER1.TCCR1A = 0xA3
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1B_val = 1
                    TIMER1.OC1A_val = 1

                    sys.getSimulator().clk(1)

                    TIMER1.TCNT1 = 0

                ## Testing
                    for i in range(255):
                        # counter test 
                        if TIMER1.TCNT1 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,i%255))

                        #Output A 
                        if TIMER1.TCNT1 >= TIMER1.OCR1A:
                            if OC1A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}| Iteration = {}".format(1,0,i))
                        else:
                            if OC1A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}| Iteration = {}".format(0,1,i))
        
                        #Output B 
                        if TIMER1.TCNT1 >= TIMER1.OCR1B:
                            if OC1B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}| Iteration = {}".format(1,0,i))
                        else:
                            if OC1B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}| Iteration = {}".format(0,1,i))

                        #Interrupt A
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}| Iteration = {}".format(0,1,i))

                        #Interrupt B 
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}| Iteration = {}".format(0,1,i))
                                
                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}| Iteration = {}".format(0,1,i))

                        sys.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)


                    CURRENT_TEST = 'TEST8'
                case 'TEST8':# TEST8 :Fast PWM Mode mode Compare Match Output B (Set OC0B on compare match, clear OC0B at BOTTOM,(inverting mode)) and A (Set OC0A on compare match, clear OC0A at BOTTOM,(inverting mode).) (writing using Ls to load data) | No prescaling (X8)
                    results.write("TEST8\n")
                    #Setup
                    TIMER1.TCCR1A = 0xF3
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1B_val = 0
                    TIMER1.OC1A_val = 0

                    sys.getSimulator().clk(1)
                    TIMER1.TCNT1 = 0

                ## Testing
                    for i in range(255):
                        # counter test 
                        if TIMER1.TCNT1 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,i))

                        #Output A 
                        if TIMER1.TCNT1 >= TIMER1.OCR1A:
                            if OC1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}|Iteration {}".format(0,1,i))
                        else:
                            if OC1A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}|Iteration {}".format(1,0,i))
        
                        #Output B 
                        if TIMER1.TCNT1 >= TIMER1.OCR1B:
                            if OC1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}|Iteration {}".format(0,1,i))
                        else:
                            if OC1B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}|Iteration {}".format(1,0,i))

                        #Interrupt A
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}|Iteration {}".format(0,1,i))

                        #Interrupt B 
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}|Iteration {}".format(0,1,i))
                                
                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}|Iteration {}".format(0,1,i))

                        sys.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)


                    CURRENT_TEST = 'TEST9'
                case 'TEST9':# TEST9 :Phase Correct PWM mode Compare Match Output B disconnected and A disconnected (writing using Ls) | No prescaling (X9)
                    results.write("TEST9\n")
                    #Setup
                    TIMER1.TCCR1A = 0x01
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1B_val = 0
                    TIMER1.OC1A_val = 0

                    sys.getSimulator().clk(1)
                    TIMER1.TCNT1 = 0

                ## Testing
                    for i in range(255*2):
                        # counter test 

                        if i <= 255 :
                            if TIMER1.TCNT1 != i:
                                TEST = False
                                ERROR_LIST.append("TCNT2 = {} expected {}".format(TIMER1.TCNT1,i))
                        else: 
                            if TIMER1.TCNT1 != (255 - (i - 255)):
                                TEST = False
                                ERROR_LIST.append("TCNT2 = {} expected {}".format(TIMER1.TCNT1,255-(i-255))) 


                        #Output A 
                        if ((TIMER1.TCNT1 >= TIMER1.OCR1A) and i<= 255) or ((TIMER1.TCNT1 <= TIMER1.OCR1A) and  i >= 255 ):
                            if OC1A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}|Iteration {}".format(0,1,i))
        

                        #Output B 
                        if ((TIMER1.TCNT1 >= TIMER1.OCR1B) and (i<= 255)) or ((TIMER1.TCNT1 <= TIMER1.OCR1A) and (i >= 255)):
                            if OC1B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}|Iteration {}".format(0,1,i))


                        #Interrupt A
#                        if (TIMER2.TCNT0-1) == TIMER2.OCR0A:
#                            if OCF0A.get() == 0:# error val
#                                TEST = False
#                                ERROR_LIST.append("OCF0A = {} expected {}|Iteration {}".format(0,1,i))
#                        else:
#                            if OCF0A.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OCF0A = {} expected {}|Iteration {}".format(1,0,i))


                        #Interrupt B 
#                        if (TIMER2.TCNT0-1) == TIMER2.OCR0B:
#                            if OCF0B.get() == 0:# error val
#                                TEST = False
#                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
#                        else:
#                            if OCF0B.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                

                        #Interrupt OVF
#                        if (TIMER2.TCNT0) == 0xFF:
#                            if TOV0.get() == 0:# error val
#                                TEST = False
#                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))


                        sys.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)


                    CURRENT_TEST = 'TEST10'
                case 'TEST10':# TEST10 :Phase Correct PWM mode Compare Match Output B disconnected and A (Normal port operation, OC0A disconnected.) (writing using Ls) | No prescaling (X10.1)
                    results.write("TEST10\n")
                    #Setup
                    TIMER1.TCCR1A = 0xA3
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128


                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts


                    TIMER1.OC1B_val = 0
                    TIMER1.OC1A_val = 0
                    sys.getSimulator().clk(1)

                    TIMER1.TCNT1 = 0

                ## Testing
                    for i in range(255):
                        # counter test 
                        if TIMER1.TCNT1 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,i%255))


                        #Output A 
                        if OC1A.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1A = {} expected {}|Iteration {}".format(0,1,i))
        

                        #Output B 
                        if OC1B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1B = {} expected {}|Iteration {}".format(0,1,i))


                        #Interrupt A
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}|Iteration {}".format(0,1,i))
#                        else:
#                            if OCF0A.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OCF0A = {} expected {}|Iteration {}".format(1,0,i))


                        #Interrupt B 
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}|Iteration {}".format(0,1,i))
#                        else:
#                            if OCF0B.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OCF0B = {} expected {}|Iteration {}".format(1,0,i))
                                

                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}|Iteration {}".format(0,1,i))


                        sys.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)


                    CURRENT_TEST = 'TEST11'
                case 'TEST11':# TEST11 :Phase Correct PWM mode Compare Match Output B disconnected and A (Toggle OC0A on compare match.) (writing using Ls) | No prescaling (X10.2)
                    results.write("TEST11\n")
                    #Setup
                    TIMER1.TCCR1A = 0xA3
                    TIMER1.TCCR1B = 0x09

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1A_val = 0
                    TIMER1.OC1B_val = 0

                    sys.getSimulator().clk(1)

                    last_OCR1A = OC1A.get()
                    TIMER1.TCNT1 = 0

                ## Testing
                    for i in range(255):
                        # counter test 
                        if TIMER1.TCNT1 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT2 = {} expected {}".format(TIMER1.TCNT1,i%255))

                        #Output A 
                        if ((TIMER1.TCNT1 == TIMER1.OCR1A) and i <= 255) or ((TIMER1.TCNT1 == TIMER1.OCR1A) and i>=255):
                            if OC1A.get() == last_OCR1A:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}|Iteration {}".format(0,1,i))
                        else:
                            last_OCR1A


                        #Interrupt A
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}|Iteration {}".format(0,1,i))
#                        else:
#                            if OCF0A.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OCF0A = {} expected {}|Iteration".format(1,0,i))

                        #Interrupt B 
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}|Iteration".format(0,1,i))
#                        else:
#                            if OCF0B.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OCF0B = {} expected {}|Iteration".format(1,0,i))
                                
                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}|Iteration".format(0,1,i))


                        sys.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)


                    CURRENT_TEST = 'TEST12'
                case 'TEST12':# TEST12 :Phase Correct PWM mode Compare Match Output B (Clear OC0B on compare match when up-counting. Set OC0B on compare match when down-counting.) and A (Clear OC0A on compare match when up-counting. Set OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X11)
                    results.write("TEST12\n")
                    #Setup
                    TIMER1.TCCR1A = 0xA1
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1A_val = 1
                    TIMER1.OC1B_val = 1

                    sys.getSimulator().clk(1)

                    last_OCR1A = OC1A.get()
                    TIMER1.TCNT1 = 0

                    counter = 0
                ## Testing
                    for i in range(511):
                        # counter test 
                        if i < 255:
                            if TIMER1.TCNT1 != i:
                                TEST = False
                                ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,i))
                        elif i>=255:
                            if TIMER1.TCNT1 != 255-counter:
                                TEST = False
                                ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,255-counter))
                            counter += 1

                        #Output A 
                        if  64<=i<=445:   #((TIMER2.TCNT0 >= TIMER2.OCR0A) and (i < 255)) or ((TIMER2.TCNT0 <= TIMER2.OCR0A) and (i>=255)):
                            if OC1A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}|Iteration {}".format(1,0,i))
                        else:
                            if OC1A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}|Iteration {}".format(0,1,i))
        
                        #Output B 
                        if  128<=i<=381:# (TIMER2.TCNT0 >= TIMER2.OCR0B) and i <= 255) or ((TIMER2.TCNT0 <= TIMER2.OCR0B) and i>=255):
                            if OC1B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}|Iteration {}".format(1,0,i))
                        else:
                            if OC1B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OC1B = {} expected {}|Iteration {}".format(0,1,i))

                        #Interrupt A
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}|Iteration {}".format(0,1,i))
#                        else:
#                            if OCF0A.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER1.TCNT1-1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}|Iteration {}".format(0,1,i))
#                        else:
#                            if OCF0B.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
#                        if (TIMER2.TCNT0) == 0xFF:
#                            if TOV0.get() == 0:# error val
#                                TEST = False
#                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)


                    CURRENT_TEST = 'TEST14'
                case 'TEST14':# TEST14 :CTC Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X13)
                    results.write("TEST14\n")
                    #Setup
                    ## Loading the config values in memory
                    TIMER1.TCCR1A = 0x02
                    TIMER1.TCCR1B = 0x01

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    last_OC1A = 0
                    last_OC1B = 0

                    TIMER1.OC1A_val = 0
                    TIMER1.OC1B_val = 0

                    sys.getSimulator().clk(1)

                    TIMER1.TCNT1 = 0

                    counter = 0
                    ## Testing
                    for i in range(128):
                        # counter test 

                        if (TIMER1.TCNT1) <= TIMER1.OCR1A:
                                if TIMER1.TCNT1 != counter%64:
                                    TEST = False
                                    ERROR_LIST.append("TCNT1 = {} expected {}|Iteration {}".format(TIMER1.TCNT1,counter%64,i))
                        
                        #Output A
                        if OC1A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}".format(1,0))


                        #Output B 
                        if OC1B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1B = {} expected {}".format(1,0))


                        #Interrupt A
                        if (TIMER1.TCNT1) == TIMER1.OCR1A:
                            counter = 0
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}| iteration = {}".format(0,1,i))


                        #Interrupt B 
                        if (TIMER1.TCNT1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}| iteration = {}".format(0,1,i))

                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys.getSimulator().clk(1)
                        counter+=1

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)

                    CURRENT_TEST = 'TEST15'
                case 'TEST15':# TEST15 :Normal mode Compare Match Output B disconected and A disconected (writing using Ls) | External clock source on T0 pin. Clock on falling edge. (X14)
                    results.write("TEST15\n")
                    #Setup
                    TIMER1.TCCR1A = 0x00
                    TIMER1.TCCR1B = 0x07

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1A_val = 0
                    TIMER1.OC1B_val = 0

                    last_T1 = 0
                    T1.prepare(0)

                    sys.getSimulator().clk(1)

                    TIMER1.TCNT1 = 0

                    counter = 0
                    clockCounter = 0
                ## Testing
                    while 1:

                        # counter test 
                        if TIMER1.TCNT1 != math.floor(counter/2): # 2 transitions
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}".format(TIMER1.TCNT1,math.floor(counter/2)))


                        #Output A
                        if OC1A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC1A = {} expected {}".format(1,0))


                        #Output B 
                        if OC1B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1B = {} expected {}".format(1,0))


                        #Interrupt A
                        if (TIMER1.TCNT1) == TIMER1.OCR1A:
                            if OCF1A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1A = {} expected {}| iteration = {}".format(0,1,i))


                        #Interrupt B 
                        if (TIMER1.TCNT1) == TIMER1.OCR1B:
                            if OCF1B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF1B = {} expected {}| iteration = {}".format(0,1,i))

                        #Interrupt OVF
                        if (TIMER1.TCNT1) == 0xFF:
                            if TOV1.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys.getSimulator().clk(1)
                        clockCounter+=1
                        if clockCounter >= 2:
                            counter += 1 
                        last_T1 = T1.get()
                        T1.prepare(1-last_T1)
                        if counter >= 255:
                            break
                        


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)

                    CURRENT_TEST = 'TEST16'
                case 'TEST16':# TEST16 :Normal mode Compare Match Output B disconected and A disconected (writing using Ls) | /8 prescaler (X15)
                    results.write("TEST16\n")
                    #Setup
                    TIMER1.TCCR1A = 0x00
                    TIMER1.TCCR1B = 0x02

                    TIMER1.OCR1A = 64
                    TIMER1.OCR1B = 128

                    TIMER1.TCNT1 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER1.TIMSK1 = 0b111
                    TIMER1.TIFR1 = 0 # clear interrupts

                    TIMER1.OC1A_val = 0
                    TIMER1.OC1B_val = 0

                    sys.getSimulator().clk(1)

                    TIMER1.TCNT1 = 0
                    counter = 0
                    clockCounter = 1
                ## Testing
                    for i in range(4080):

                        # counter test 
                        if TIMER1.TCNT1 != counter%256:
                            TEST = False
                            ERROR_LIST.append("TCNT1 = {} expected {}|Iteration {}".format(TIMER1.TCNT1,counter%256,i))


                        #Output A 
                        if OC1A.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1A = {} expected {}|Iteration {}".format(0,1,i))

        

                        #Output B 
                        if OC1B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC1B = {} expected {}|Iteration {}".format(0,1,i))


                        #Interrupt A
#                        if (TIMER2.TCNT0-1) == TIMER2.OCR0A:
#                            if OCF0A.get() == 0:# error val
#                                TEST = False
#                                ERROR_LIST.append("OC0A = {} expected {}|Iteration {}".format(0,1,i))
#                        else:
#                            if OCF0A.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OC0A = {} expected {}|Iteration {}".format(1,0,i))

                        #Interrupt B 
#                        if (TIMER2.TCNT0-1) == TIMER2.OCR0B:
#                            if OCF0B.get() == 0:# error val
#                                TEST = False
#                                ERROR_LIST.append("OC0B = {} expected {}|Iteration {}".format(0,1,i))
#                        else:
#                            if OCF0B.get() == 1:
#                                TEST = False
#                                ERROR_LIST.append("OC0B = {} expected {}|Iteration {}".format(1,0,i))
                                
                        #Interrupt OVF
#                        if (TIMER2.TCNT0) == 0xFF:
#                            if TOV0.get() == 0:# error val
#                                TEST = False
#                                ERROR_LIST.append("OVF = {} expected {}|Iteration {}".format(0,1,i))

                        sys.getSimulator().clk(1)
                        clockCounter += 1
                        if clockCounter >= 8:
                            clockCounter = 0
                            counter += 1 


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)


                    CURRENT_TEST = 'FINAL'
                case 'FINAL':
                    results.write("TEST Finished")
                    
                    
                    results.close()

                    
                    wvf.gui()
                    Testing = False
                    CURRENT_TEST = 'FINAL'



if __name__ == '__main__':
    TestBench_of_Timer1()