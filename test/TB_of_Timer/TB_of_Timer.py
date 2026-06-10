import py4hw
from punxa_atmega328p.Timers import *
from punxa_atmega328p.Memory import * 


#Parameters for the test bench 
Verbose = False 
#while Verbose == 7:
#    print("Verbose? Y/N")
#    responce = input()
#    if (responce == 'Y') or (responce == 'y'):
#        Verbose = True 
#    elif (responce == 'N') or (responce == 'n'):
#        Verbose = False 


def TestBench_of_Timer0():

    sys0 = py4hw.HWSystem()

    SIGNALS0 = []

    OCF0B = py4hw.Wire( sys0,'OCF0B',1)
    SIGNALS0.append(OCF0B)
    OCF0A = py4hw.Wire( sys0,'OCF0A',1)
    SIGNALS0.append(OCF0A)
    TOV0 = py4hw.Wire( sys0,'TOV0',1)
    SIGNALS0.append(TOV0)

    OC0A = py4hw.Wire(sys0,'OC0A',1)
    SIGNALS0.append(OC0A)
    OC0B = py4hw.Wire(sys0,'OC0B',1)
    SIGNALS0.append(OC0B)
    T0 = py4hw.Wire(sys0,'T0',1)
    SIGNALS0.append(T0)

    interface0 = MemoryInterface(sys0,'interface0',8,16)

    TIMER0 = TimerCounter0(sys0,'TIMER0',interface0,OC0B,OC0A,T0,OCF0B,OCF0A,TOV0)



    SIGNALS0.append(interface0.write)
    SIGNALS0.append(interface0.read)
    SIGNALS0.append(interface0.address)
    SIGNALS0.append(interface0.write_data)
    SIGNALS0.append(interface0.read_data)
    SIGNALS0.append(interface0.resp)

    CURRENT_TEST = 'START'
    CURRENT_STEP = 'SETUP'

    wvf = py4hw.Waveform(sys0,'wvf',SIGNALS0)


    #sch = py4hw.Schematic(sys)
    #sch.draw()


    #sys.getSimulator().clk(len(TIMER0_WRITE_DATA_TEST))


    INS_counter = 0

    TEST_RESULTS = []

    Testing = True
    with open("Test/TB_of_Timer/Test_Results.txt",'w+') as results:
        while Testing:

            
            match CURRENT_TEST:

                case 'START':
                    print("Starting Test Bench of Timer0")



                    CURRENT_TEST = 'TEST0'
                case 'TEST0':# TEST0 :Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
                    results.write("TEST0\n")
                    #Setup
                    ## Loading the config values in memory
                    TIMER0.TCCR0A = 0x00
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                    last_OC0A = 0
                    last_OC0B = 0

                    ## Testing
                    for i in range(256):
                        # counter test 

                        if TIMER0.TCNT0 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i%255))


                        #Output A
                        if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OC0A = {} expected {}".format(1,0))

                        #Output B 
                        if OC0B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OC0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}| iteration = {}".format(0,1,i))

                        #Interrupt B 
                        if (TIMER0.TCNT0) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}| iteration = {}".format(0,1,i))


                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)

                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST1'
                case 'TEST1':# TEST1 :Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls to load data) | No prescaling (X2)
                    results.write("TEST1\n")
                    #Setup
                    ## Loading the config values in memory
                    TIMER0.TCCR0A = 0x00
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                    last_OC0A = 0
                    last_OC0B = 0

                    ## Testing
                    for i in range(256):
                        # counter test 

                        if TIMER0.TCNT0 != i%255:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i%255))

                        #Output A 
                        if TIMER0.TCNT0 > TIMER0.OCR0A:
                            if OC0A.get() == last_OC0A:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(last_OC0A,(1-last_OC0A)))
                        else:
                            last_OC0A = OC0A.get()

        
                        #Output B 
                        if TIMER0.TCNT0 > TIMER0.OCR0B:
                            if OC0B.get() == last_OC0B:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(last_OC0B,(1-last_OC0B)))
                        else:
                            last_OC0B = OC0B.get()


                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))


                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))


                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    ## Storing data
                    CURRENT_TEST = 'TEST2'
                case 'TEST2':# TEST2 :Normal mode Compare Match Output B Set and A Set (writing using Ls to load data) | No prescaling (X4)
                    results.write("TEST2\n")
                    #Setup
                    TIMER0.TCCR0A = 0x50
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(250):
                        # counter test 

                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST3'
                case 'TEST3':# TEST3 :Normal mode Compare Match Output B Clear and A Clear (writing using Ls to load data) | No prescaling (X3)
                    results.write("TEST3\n")
                    #Setup
                    TIMER0.TCCR0A = 0xA0
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 

                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST4'
                case 'TEST4': # TEST4 :Fast PWM Mode mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X5)
                    results.write("TEST4\n")
                    #Setup
                    TIMER0.TCCR0A = 0x03
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST5'
                case 'TEST5':# TEST5 :Fast PWM Mode mode Compare Match Output B disconnected and A (Normal port operation, OC0A disconnected) (writing using Ls to load data) | No prescaling (X6.1)
                    results.write("TEST5\n")
                    #Setup
                    TIMER0.TCCR0A = 0x53
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST6'
                case 'TEST6':# TEST6 :Fast PWM Mode mode Compare Match Output B disconnected and A (Toggle OC0A on compare match.) (writing using Ls to load data) | No prescaling (X6.2)
                    results.write("TEST6\n")
                    #Setup
                    TIMER0.TCCR0A = 0x53
                    TIMER0.TCCR0B = 0x09

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)

                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST7'
                case 'TEST7':# TEST7 :Fast PWM Mode mode Compare Match Output B (Clear OC0B on compare match, set OC0B at BOTTOM,(non-inverting mode)) and A (Clear OC0A on compare match, set OC0A at BOTTOM,(non-inverting mode).) (writing using Ls to load data) | No prescaling (X7)
                    results.write("TEST7\n")
                    #Setup
                    TIMER0.TCCR0A = 0xA3
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST8'
                case 'TEST8':# TEST8 :Fast PWM Mode mode Compare Match Output B (Set OC0B on compare match, clear OC0B at BOTTOM,(inverting mode)) and A (Set OC0A on compare match, clear OC0A at BOTTOM,(inverting mode).) (writing using Ls to load data) | No prescaling (X8)
                    results.write("TEST8\n")
                    #Setup
                    TIMER0.TCCR0A = 0xF3
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST9'
                case 'TEST9':# TEST9 :Phase Correct PWM mode Compare Match Output B disconnected and A disconnected (writing using Ls) | No prescaling (X9)
                    results.write("TEST9\n")
                    #Setup
                    TIMER0.TCCR0A = 0x01
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST10'
                case 'TEST10':# TEST10 :Phase Correct PWM mode Compare Match Output B disconnected and A (Normal port operation, OC0A disconnected.) (writing using Ls) | No prescaling (X10.1)
                    results.write("TEST10\n")
                    #Setup
                    TIMER0.TCCR0A = 0xA3
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST11'
                case 'TEST11':# TEST11 :Phase Correct PWM mode Compare Match Output B disconnected and A (Toggle OC0A on compare match.) (writing using Ls) | No prescaling (X10.2)
                    results.write("TEST11\n")
                    #Setup
                    TIMER0.TCCR0A = 0xA3
                    TIMER0.TCCR0B = 0x09

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST12'
                case 'TEST12':# TEST12 :Phase Correct PWM mode Compare Match Output B (Clear OC0B on compare match when up-counting. Set OC0B on compare match when down-counting.) and A (Clear OC0A on compare match when up-counting. Set OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X11)
                    results.write("TEST12\n")
                    #Setup
                    TIMER0.TCCR0A = 0xA1
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST13'
                case 'TEST13':# TEST13 :Phase Correct PWM mode Compare Match Output B (Set OC0B on compare match when up-counting. Clear OC0B on compare match when down-counting.) and A (Set OC0A on compare match when up-counting. Clear OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X12)
                    results.write("TEST13\n")
                    #Setup
                    TIMER0.TCCR0A = 0xF3
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST14' 
                case 'TEST14':# TEST14 :Phase Correct PWM mode Compare Match Output B (Set OC0B on compare match when up-counting. Clear OC0B on compare match when down-counting.) and A (Set OC0A on compare match when up-counting. Clear OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X13)
                    results.write("TEST14\n")
                    #Setup
                    TIMER0.TCCR0A = 0xF3
                    TIMER0.TCCR0B = 0x01

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST15'
                case 'TEST15':# TEST15 :Normal mode Compare Match Output B disconected and A disconected (writing using Ls) | External clock source on T0 pin. Clock on falling edge. (X14)
                    results.write("TEST15\n")
                    #Setup
                    TIMER0.TCCR0A = 0x00
                    TIMER0.TCCR0B = 0x07

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts

                ## Testing
                    for i in range(256):
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,i))

                        #Output A 
                        if TIMER0.TCNT0 >= TIMER0.OCR0A:
                            if OC0A.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OC0A.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))
        
                        #Output B 
                        if TIMER0.TCNT0 >= TIMER0.OCR0B:
                            if OC0B.get() == 1:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OC0B.get() == 0:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))

                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'TEST16'
                case 'TEST16':# TEST16 :Normal mode Compare Match Output B disconected and A disconected (writing using Ls) | /8 prescaler (X15)
                    results.write("TEST16\n")
                    #Setup
                    TIMER0.TCCR0A = 0x00
                    TIMER0.TCCR0B = 0x02

                    TIMER0.OCR0A = 64
                    TIMER0.OCR0B = 128

                    TIMER0.TCNT0 = 0

                    ERROR_LIST = []
                    TEST = True 

                    TIMER0.TIMSK0 = 0b111
                    TIMER0.TIFR0 = 0 # clear interrupts
                    tick = 0 

                ## Testing
                    for i in range((256*8)*2):

                        if (i//16) == 0 :
                            tick += 1 
                        # counter test 
                        if TIMER0.TCNT0 != i:
                            TEST = False
                            ERROR_LIST.append("TCNT0 = {} expected {}".format(TIMER0.TCNT0,tick))

                        #Output A 

                        if OC0A.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))

        
                        #Output B 
                        if OC0B.get() == 1:# error val
                            TEST = False
                            ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))


                        #Interrupt A
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0A:
                            if OCF0A.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(0,1))
                        else:
                            if OCF0A.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0A = {} expected {}".format(1,0))

                        #Interrupt B 
                        if (TIMER0.TCNT0-1) == TIMER0.OCR0B:
                            if OCF0B.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(0,1))
                        else:
                            if OCF0B.get() == 1:
                                TEST = False
                                ERROR_LIST.append("OCF0B = {} expected {}".format(1,0))
                                
                        #Interrupt OVF
                        if (TIMER0.TCNT0) == 0xFF:
                            if TOV0.get() == 0:# error val
                                TEST = False
                                ERROR_LIST.append("OVF = {} expected {}".format(0,1))

                        sys0.getSimulator().clk(1)


                    ## Storing data
                    ITEM = []
                    ITEM.append(TEST)
                    ITEM.append(ERROR_LIST)
                    results.write('%s\n' %ITEM)
                    while len(ITEM) > 0:
                        print("")

                    CURRENT_TEST = 'FINAL'
                case 'FINAL':
                    print("TEST SUMMARY:")

                    
                    results.close()

                    wvf.gui()
                    Testing = False
                    CURRENT_TEST = 'FINAL'
    

#Timer 0 
TIMER0_READ_TEST = [
    #read Write test for IO
    0,0,0,1,1,#TCCR0A
    0,0,0,1,1,#TCCR0B

    0,0,0,1,1,#TCNT0
    0,0,0,1,1,#OCR0A
    0,0,0,1,1,#OCR0B

    0,0,0,1,1,#TIFR0

    #read Write test for LS
    0,0,0,1,1,#TCCR0A
    0,0,0,1,1,#TCCR0B

    0,0,0,1,1,#TCNT0
    0,0,0,1,1,#OCR0A
    0,0,0,1,1,#OCR0B

    0,0,0,1,1,#TIMSK0
    0,0,0,1,1,#TIFR0

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling


    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Clear and A Clear (writing using Ls) | No prescaling


    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Normal mode Compare Match Output B Set and A Set (writing using Ls) | No prescaling (x3)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

    #functional incrementation test : PWM phase correct mode Compare Match Output B disconnected and A disconnected (writing using Ls) | No prescaling (x4)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x5)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x6.1)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x6.2)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x7)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x8)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x9)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2
#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x10)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x11)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2
#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x12)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x13)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x14)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    #16
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x15)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1

    0,0,0,1,1,#TCNT0 SET1

    #32
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2
]
TIMER0_WRITE_TEST = [
    #read Write test for IO
    1,1,0,0,0,#TCCR0A
    1,1,0,0,0,#TCCR0B

    1,1,0,0,0,#TCNT0
    1,1,0,0,0,#OCR0A
    1,1,0,0,0,#OCR0B

    1,1,0,0,0,#TIFR0

    #read Write test for LS
    1,1,0,0,0,#TCCR0A
    1,1,0,0,0,#TCCR0B

    1,1,0,0,0,#TCNT0
    1,1,0,0,0,#OCR0A
    1,1,0,0,0,#OCR0B

    1,1,0,0,0,#TIMSK0
    1,1,0,0,0,#TIFR0


    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)


    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    1,1,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1


    0,0,0,0,0,#TCNT0 END1

]
TIMER0_WRITE_DATA_TEST = [
    #read Write test for IO
    3,3,3,3,3,#TCCR0A
    1,1,1,1,1,#TCCR0B

    7,7,7,7,7,#TCNT0
    6,6,6,6,6,#OCR0A
    9,9,9,9,9,#OCR0B

    2,2,2,2,2,#TIFR0

    #read Write test for LS
    8,8,8,8,8,#TCCR0A
    0,0,0,0,0,#TCCR0B

    3,3,3,3,3,#TCNT0
    8,8,8,8,8,#OCR0A
    2,2,2,2,2,#OCR0B

    6,6,6,6,6,#TIMSK0
    1,1,1,1,1,#TIFR0

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)


    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET1
    0x00,0x00,0x00,0x00,0x00, #TCCR0A SET1

    64,64,64,64,64, #OCR0A SET1
    128,128,128,128,128, #OCR0B SET1 

    0,0,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Clear and A Clear (writing using Ls) | No prescaling (X2)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0x50,0x50,0x50,0x50,0x50, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional test : Normal mode Compare Match Output B Clear and A Clear (writing using Ls to load data) | No prescaling (X3)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0xA0,0xA0,0xA0,0xA0,0xA0, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional test : Normal mode Compare Match Output B Set and A Set (writing using Ls to load data) | No prescaling (X4)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0xF0,0xF0,0xF0,0xF0,0xF0, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional test : Fast PWM Mode mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X5)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0x03,0x03,0x03,0x03,0x03, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

   #functional test : Fast PWM Mode mode Compare Match Output B disconnected and A (Normal port operation, OC0A disconnected) (writing using Ls to load data) | No prescaling (X6.1)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0x53,0x53,0x53,0x53,0x53, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional test : Fast PWM Mode mode Compare Match Output B disconnected and A (Toggle OC0A on compare match.) (writing using Ls to load data) | No prescaling (X6.2)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0xA3,0xA3,0xA3,0xA3,0xA3, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional test : Fast PWM Mode mode Compare Match Output B (Clear OC0B on compare match, set OC0B at BOTTOM,(non-inverting mode)) and A (Clear OC0A on compare match, set OC0A at BOTTOM,(non-inverting mode).) (writing using Ls to load data) | No prescaling (X7)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0xF3,0xF3,0xF3,0xF3,0xF3, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional test : Fast PWM Mode mode Compare Match Output B (Set OC0B on compare match, clear OC0B at BOTTOM,(inverting mode)) and A (Set OC0A on compare match, clear OC0A at BOTTOM,(inverting mode).) (writing using Ls to load data) | No prescaling (X8)
    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0xF1,0xF1,0xF1,0xF1,0xF1, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B disconnected and A disconnected (writing using Ls) | No prescaling (X9)


    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0x01,0x01,0x01,0x01,0x01, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B disconnected and A (Normal port operation, OC0A disconnected.) (writing using Ls) | No prescaling (X10.1)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0x51,0x51,0x51,0x51,0x51, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B disconnected and A (Toggle OC0A on compare match.) (writing using Ls) | No prescaling (X10.2)

    0x09,0x09,0x09,0x09,0x09, #TCCR0B SET2
    0x51,0x51,0x51,0x51,0x51, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B (Clear OC0B on compare match when up-counting. Set OC0B on compare match when down-counting.) and A (Clear OC0A on compare match when up-counting. Set OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X11)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0xF1,0xF1,0xF1,0xF1,0xF1, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B (Set OC0B on compare match when up-counting. Clear OC0B on compare match when down-counting.) and A (Set OC0A on compare match when up-counting. Clear OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X12)

    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0xF0,0xF0,0xF0,0xF0,0xF0, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B (Set OC0B on compare match when up-counting. Clear OC0B on compare match when down-counting.) and A (Set OC0A on compare match when up-counting. Clear OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X13)


    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0xF0,0xF0,0xF0,0xF0,0xF0, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Normal mode Compare Match Output B disconected and A disconected (writing using Ls) | External clock source on T0 pin. Clock on falling edge. (X14)


    0x01,0x01,0x01,0x01,0x01, #TCCR0B SET2
    0xF0,0xF0,0xF0,0xF0,0xF0, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Normal mode Compare Match Output B disconected and A disconected (writing using Ls) | /8 prescaler (X15)

    0x02,0x02,0x02,0x02,0x02, #TCCR0B SET2
    0x00,0x00,0x00,0x00,0x00, #TCCR0A SET2

    64,64,64,64,64, #OCR0A SET2
    128,128,128,128,128, #OCR0B SET2

    0,0,0,0,0,#TCNT0 SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

]
TIMER0_ADDRESS_TEST_FULL = [
    #read Write test for IO
    0x24,0x24,0x24,0x24,0x24, #TCCR0A
    0x25,0x25,0x25,0x25,0x25, #TCCR0B

    0x26,0x26,0x26,0x26,0x26, #TCNT0
    0x27,0x27,0x27,0x27,0x27, #OCR0A
    0x28,0x28,0x28,0x28,0x28, #OCR0B

    0x15,0x15,0x15,0x15,0x15, #TIFR0

    #read Write test for LS
    0x44,0x44,0x44,0x44,0x44, #TCCR0A
    0x45,0x45,0x45,0x45,0x45, #TCCR0B

    0x46,0x46,0x46,0x46,0x46, #TCNT0
    0x47,0x47,0x47,0x47,0x47, #OCR0A
    0x48,0x48,0x48,0x48,0x48, #OCR0B

    0x6E,0x6E,0x6E,0x6E,0x6E, #TIMSK0
    0x35,0x35,0x35,0x35,0x35, #TIFR0

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)


    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1


    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls to load data) | No prescaling (X2)


    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

     0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional test : Normal mode Compare Match Output B Clear and A Clear (writing using Ls to load data) | No prescaling (X3)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional test : Normal mode Compare Match Output B Set and A Set (writing using Ls to load data) | No prescaling (X4)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional test : Fast PWM Mode mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X5)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional test : Fast PWM Mode mode Compare Match Output B disconnected and A (Normal port operation, OC0A disconnected) (writing using Ls to load data) | No prescaling (X6.1)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional test : Fast PWM Mode mode Compare Match Output B disconnected and A (Toggle OC0A on compare match.) (writing using Ls to load data) | No prescaling (X6.2)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional test : Fast PWM Mode mode Compare Match Output B (Clear OC0B on compare match, set OC0B at BOTTOM,(non-inverting mode)) and A (Clear OC0A on compare match, set OC0A at BOTTOM,(non-inverting mode).) (writing using Ls to load data) | No prescaling (X7)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional test : Fast PWM Mode mode Compare Match Output B (Set OC0B on compare match, clear OC0B at BOTTOM,(inverting mode)) and A (Set OC0A on compare match, clear OC0A at BOTTOM,(inverting mode).) (writing using Ls to load data) | No prescaling (X8)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B disconnected and A disconnected (writing using Ls) | No prescaling (X9)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B disconnected and A (Normal port operation, OC0A disconnected.) (writing using Ls) | No prescaling (X10.1)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B disconnected and A (Toggle OC0A on compare match.) (writing using Ls) | No prescaling (X10.2)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B (Clear OC0B on compare match when up-counting. Set OC0B on compare match when down-counting.) and A (Clear OC0A on compare match when up-counting. Set OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X11)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B (Set OC0B on compare match when up-counting. Clear OC0B on compare match when down-counting.) and A (Set OC0A on compare match when up-counting. Clear OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X12)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional incrementation test : Phase Correct PWM mode Compare Match Output B (Set OC0B on compare match when up-counting. Clear OC0B on compare match when down-counting.) and A (Set OC0A on compare match when up-counting. Clear OC0A on compare match when down-counting.) (writing using Ls) | No prescaling (X13)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional incrementation test : Normal mode Compare Match Output B disconected and A disconected (writing using Ls) | External clock source on T0 pin. Clock on falling edge. (X14)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    #functional incrementation test : Normal mode Compare Match Output B disconected and A disconected (writing using Ls) | /8 prescaler (X15)

    0x45,0x45,0x45,0x45,0x45, #TCCR0B SET1
    0x44,0x44,0x44,0x44,0x44, #TCCR0A SET1

    0x47,0x47,0x47,0x47,0x47, #OCR0A SET1
    0x48,0x48,0x48,0x48,0x48, #OCR0B SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1
    0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

    0x46,0x46,0x46,0x46,0x46, #TCNT0 SET1

]
TIMER0_DATA_TEST = []
TIMER0_READ_DATA_CORRECT = []
TIMER0_INSTYPE = [
    #read Write test for IO
    0,0,0,0,0,#TCCR0A
    0,0,0,0,0,#TCCR0B

    0,0,0,0,0,#TCNT0
    0,0,0,0,0,#OCR0A
    0,0,0,0,0,#OCR0B

    0,0,0,0,0,#TIFR0

    #read Write test for LS
    1,1,1,1,1,#TCCR0A
    1,1,1,1,1,#TCCR0B

    1,1,1,1,1,#TCNT0
    1,1,1,1,1,#OCR0A
    1,1,1,1,1,#OCR0B

    1,1,1,1,1,#TIMSK0
    1,1,1,1,1,#TIFR0

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 


    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1


    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

] #0 for i in range(len(TIMER0_ADDRESS_TEST_IO)),1 for j in range(len(TIMER0_ADDRESS_TEST_LS))
TIMER0_T0_TEST = [
    #read Write test for IO
    0,0,0,0,0,#TCCR0A
    0,0,0,0,0,#TCCR0B

    0,0,0,0,0,#TCNT0
    0,0,0,0,0,#OCR0A
    0,0,0,0,0,#OCR0B

    0,0,0,0,0,#TIFR0

    #read Write test for LS
    0,0,0,0,0,#TCCR0A
    0,0,0,0,0,#TCCR0B

    0,0,0,0,0,#TCNT0
    0,0,0,0,0,#OCR0A
    0,0,0,0,0,#OCR0B

    0,0,0,0,0,#TIMSK0
    0,0,0,0,0,#TIFR0

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1 

    0,0,0,0,0,#TCNT0 SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X2)
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2

    #xx
    0,0,0,0,0, #TCNT0 SET2

    0,0,0,0,0, #TCCR0B SET2
    0,0,0,0,0, #TCCR0A SET2

    0,0,0,0,0, #OCR0A SET2
    0,0,0,0,0, #OCR0B SET2

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END2
]
TIMER0_SIGNALS = []

if Verbose == True:
    length_of_test = 0
    print("=============TIMER0_TEST=============")
    length_of_test = TIMER0_READ_TEST
    print("Lenght of READ_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER0_READ_TEST),match = (length_of_test == len(TIMER0_READ_TEST))))
    print("Lenght of WRITE_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER0_WRITE_TEST),match = (length_of_test == len(TIMER0_WRITE_TEST))))
    print("Lenght of DATA_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER0_DATA_TEST),match = (length_of_test == len(TIMER0_DATA_TEST))))
    print("Lenght of WRITE_DATA_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER0_WRITE_DATA_TEST),match = (length_of_test == len(TIMER0_WRITE_DATA_TEST))))
    print("Lenght of READ_DATA_CORRECT: {length} clk | Equal to others: {match}".format(length = len(TIMER0_READ_DATA_CORRECT),match = (length_of_test == len(TIMER0_READ_DATA_CORRECT))))
    print("Lenght of ADDRESS_TEST_FULL: {length} clk | Equal to others: {match}".format(length = len(TIMER0_ADDRESS_TEST_FULL),match = (length_of_test == len(TIMER0_ADDRESS_TEST_FULL))))
    print("Lenght of TIMER0_T0_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER0_T0_TEST),match = (length_of_test == len(TIMER0_T0_TEST))))

#Timer 1 
TIMER1_READ_TEST = []
TIMER1_WRITE_TEST = []
TIMER1_DATA_TEST = []
TIMER1_WRITE_DATA_TEST = []
TIMER1_READ_DATA_CORRECT = []
TIMER1_ADDRESS_TEST_FULL  =[
    #read Write test IO   
    0x16,0x16,0x16,0x16,0x16, #TIFR1
    0x15,0x15,0x15,0x15,0x15, #TIFR0

    #read Write test LS
    0x8B,0x8B,0x8B,0x8B,0x8B, #OCR1BH
    0x8A,0x8A,0x8A,0x8A,0x8A, #OCR1BL

    0x89,0x89,0x89,0x89,0x89, #OCR1AH
    0x88,0x88,0x88,0x88,0x88, #OCR1AL

    0x87,0x87,0x87,0x87,0x87, #ICR1H
    0x86,0x86,0x86,0x86,0x86, #ICR1L

    0x85,0x85,0x85,0x85,0x85, #TCNT1H
    0x84,0x84,0x84,0x84,0x84, #TCNT1L

    0x82,0x82,0x82,0x82,0x82, #TCCR1C
    0x81,0x81,0x81,0x81,0x81, #TCCR1B

    0x80,0x80,0x80,0x80,0x80, #TCCR1A

    0x6F,0x6F,0x6F,0x6F,0x6F, #TIMSK1
    0x36,0x36,0x36,0x36,0x36, #TIFR1

]
TIMER1_INSTYPE = []
TIMER1_T1_TEST = []
TIMER1_SIGNALS = []

if Verbose == True:
    length_of_test = 0
    print("=============TIMER1_TEST=============")
    length_of_test = TIMER1_READ_TEST
    print("Lenght of READ_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER1_READ_TEST),match = (length_of_test == len(TIMER1_READ_TEST))))
    print("Lenght of WRITE_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER1_WRITE_TEST),match = (length_of_test == len(TIMER1_WRITE_TEST))))
    print("Lenght of DATA_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER1_DATA_TEST),match = (length_of_test == len(TIMER1_DATA_TEST))))
    print("Lenght of WRITE_DATA_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER1_WRITE_DATA_TEST),match = (length_of_test == len(TIMER1_WRITE_DATA_TEST))))
    print("Lenght of READ_DATA_CORRECT: {length} clk | Equal to others: {match}".format(length = len(TIMER1_READ_DATA_CORRECT),match = (length_of_test == len(TIMER1_READ_DATA_CORRECT))))
    print("Lenght of ADDRESS_TEST_FULL: {length} clk | Equal to others: {match}".format(length = len(TIMER1_ADDRESS_TEST_FULL),match = (length_of_test == len(TIMER1_ADDRESS_TEST_FULL))))
    print("Lenght of TIMER0_T0_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER1_T1_TEST),match = (length_of_test == len(TIMER1_T1_TEST))))

# Timer 2
TIMER2_READ_TEST = [
    #read Write test for IO
    0,0,0,1,1,#TCCR0A
    0,0,0,1,1,#TCCR0B

    0,0,0,1,1,#TCNT0
    0,0,0,1,1,#OCR0A
    0,0,0,1,1,#OCR0B

    0,0,0,1,1,#TIFR0

    #read Write test for LS
    0,0,0,1,1,#TCCR0A
    0,0,0,1,1,#TCCR0B

    0,0,0,1,1,#TCNT0
    0,0,0,1,1,#OCR0A
    0,0,0,1,1,#OCR0B

    0,0,0,1,1,#TIMSK0
    0,0,0,1,1,#TIFR0

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling
    0,0,0,1,1,#TCNT0 SET1

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Clear and A Clear (writing using Ls) | No prescaling
    0,0,0,1,1,#TCNT0 SET1

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

    #functional incrementation test : Normal mode Compare Match Output B Set and A Set (writing using Ls) | No prescaling (x3)
    0,0,0,1,1,#TCNT0 SET1

    0,0,0,0,0, #TCCR0B SET1
    0,0,0,0,0, #TCCR0A SET1

    0,0,0,0,0, #OCR0A SET1
    0,0,0,0,0, #OCR0B SET1


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

    #functional incrementation test : PWM phase correct mode Compare Match Output B disconnected and A disconnected (writing using Ls) | No prescaling (x4)
    0,0,0,1,1,#TCNT0 SET4

    0,0,0,0,0, #TCCR0B SET4
    0,0,0,0,0, #TCCR0A SET4

    0,0,0,0,0, #OCR0A SET4
    0,0,0,0,0, #OCR0B SET4


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x5)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x6.1)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x6.2)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x7)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x8)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x9)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2
#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x10)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x11)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2
#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x12)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x13)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x14)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5

    #16
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2

#functional incrementation test : PWM phase correct mode Compare Match Output B CLEAR and A CLEAR (writing using Ls) | No prescaling (x15)
    0,0,0,1,1,#TCNT0 SET5

    0,0,0,0,0, #TCCR0B SET5
    0,0,0,0,0, #TCCR0A SET5

    0,0,0,0,0, #OCR0A SET5
    0,0,0,0,0, #OCR0B SET5

    #32
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,0,0,0,0,#TCNT0 END2
]
TIMER2_WRITE_TEST = [
    #read Write test for IO
    1,1,0,0,0,#TCCR0A
    1,1,0,0,0,#TCCR0B

    1,1,0,0,0,#TCNT0
    1,1,0,0,0,#OCR0A
    1,1,0,0,0,#OCR0B

    1,1,0,0,0,#TIFR0

    #read Write test for LS
    1,1,0,0,0,#TCCR0A
    1,1,0,0,0,#TCCR0B

    1,1,0,0,0,#TCNT0
    1,1,0,0,0,#OCR0A
    1,1,0,0,0,#OCR0B

    1,1,0,0,0,#TIMSK0
    1,1,0,0,0,#TIFR0


    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

     0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1

    0,0,0,0,0,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling (X1)
    1,1,0,0,0,#TCNT0 SET1

    1,1,1,1,1, #TCCR0B SET1
    1,1,1,1,1, #TCCR0A SET1

    1,1,1,1,1, #OCR0A SET1
    1,1,1,1,1, #OCR0B SET1

    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, #TCNT0 SEE1


    0,0,0,0,0,#TCNT0 END1
]
TIMER2_DATA_TEST = []
TIMER2_WRITE_DATA_TEST = []
TIMER2_READ_DATA_CORRECT = []
TIMER2_ADDRESS_TEST_FULL = [
    
    #read Write test IO
    0x37,0x37,0x37,0x37,0x37, #TIFR2

    #read Write test LS
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A 
    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2
    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B

    0x70,0x70,0x70,0x70,0x70, #TIMSK2
    0x37,0x37,0x37,0x37,0x37, #TIFR2

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1


    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

    #functional test : Normal mode Compare Match Output B disconnected and A disconnected (writing using Ls to load data) | No prescaling (X1)
    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SET1

    0xB1,0xB1,0xB1,0xB1,0xB1, #TCCR2B SET1
    0xB0,0xB0,0xB0,0xB0,0xB0, #TCCR2A SET1

    0xB3,0xB3,0xB3,0xB3,0xB3, #OCR2A SET1
    0xB4,0xB4,0xB4,0xB4,0xB4, #OCR2B SET1

    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1
    0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 SEE1

    0xB2,0xB2,0xB2,0xB2,0xB2, #TCNT2 END1

]
TIMER2_INSTYPE = [
    #read Write test for IO
    0,0,0,0,0,#TCCR0A
    0,0,0,0,0,#TCCR0B

    0,0,0,0,0,#TCNT0
    0,0,0,0,0,#OCR0A
    0,0,0,0,0,#OCR0B

    0,0,0,0,0,#TIFR0

    #read Write test for LS
    1,1,1,1,1,#TCCR0A
    1,1,1,1,1,#TCCR0B

    1,1,1,1,1,#TCNT0
    1,1,1,1,1,#OCR0A
    1,1,1,1,1,#OCR0B

    1,1,1,1,1,#TIMSK0
    1,1,1,1,1,#TIFR0

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1


    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1


    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1

    #functional incrementation test : Normal mode Compare Match Output B Toggle and A Toggle (writing using Ls) | No prescaling 
    1,1,1,1,1,#TCNT0 SET1

    1,1,1,1,1,#TCCR0A SET1
    1,1,1,1,1,#TCCR0B SET1

    1,1,1,1,1,#OCR0A SET1
    1,1,1,1,1,#OCR0B SET1

    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1
    1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1, #TCNT0 SEE1

    1,1,1,1,1,#TCNT0 END1
]
TIMER2_ADDRESS_TEST_FULL = []
TIMER2_T2_TEST = []
TIMER2_SIGNALS = []

if Verbose == True:
    length_of_test = 0
    print("=============TIMER2_TEST=============")
    length_of_test = TIMER2_READ_TEST
    print("Lenght of READ_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER2_READ_TEST),match = (length_of_test == len(TIMER2_READ_TEST))))
    print("Lenght of WRITE_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER2_WRITE_TEST),match = (length_of_test == len(TIMER2_WRITE_TEST))))
    print("Lenght of DATA_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER2_DATA_TEST),match = (length_of_test == len(TIMER2_DATA_TEST))))
    print("Lenght of WRITE_DATA_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER2_WRITE_DATA_TEST),match = (length_of_test == len(TIMER2_WRITE_DATA_TEST))))
    print("Lenght of READ_DATA_CORRECT: {length} clk | Equal to others: {match}".format(length = len(TIMER2_READ_DATA_CORRECT),match = (length_of_test == len(TIMER2_READ_DATA_CORRECT))))
    print("Lenght of ADDRESS_TEST_FULL: {length} clk | Equal to others: {match}".format(length = len(TIMER2_ADDRESS_TEST_FULL),match = (length_of_test == len(TIMER2_ADDRESS_TEST_FULL))))
    print("Lenght of TIMER0_T0_TEST: {length} clk | Equal to others: {match}".format(length = len(TIMER2_T2_TEST),match = (length_of_test == len(TIMER2_T2_TEST))))

#SIGNALS = []

#sys = py4hw.HWSystem()


#interface1 = MemoryInterface(sys,'interface1',8,16)
#interface2 = MemoryInterface(sys,'interface2',8,16)


#TIMER0
#interface0 = MemoryInterface(sys,'interface0',8,16)

#OCF0B = py4hw.Wire( sys,'OCF0B',1)
#OCF0A = py4hw.Wire( sys,'OCF0A',1)
#TOV0 = py4hw.Wire( sys,'TOV0',1)
#SIGNALS.append(OCF0B)
#SIGNALS.append(OCF0A)
#SIGNALS.append(TOV0)

#SIGNALS.append(interface0.write)
#SIGNALS.append(interface0.read)
#SIGNALS.append(interface0.address)
#SIGNALS.append(interface0.write_data)
#SIGNALS.append(interface0.read_data)
#SIGNALS.append(interface0.resp)

#TIMER1
#TIMER1_SIGNALS.append(interface1.write)
#TIMER1_SIGNALS.append(interface1.read)
#TIMER1_SIGNALS.append(interface1.address)
#TIMER1_SIGNALS.append(interface1.write_data)
#TIMER1_SIGNALS.append(interface1.read_data)
#TIMER1_SIGNALS.append(interface1.resp)

#TIMER2
#TIMER2_SIGNALS.append(interface2.write)
#TIMER2_SIGNALS.append(interface2.read)
#TIMER2_SIGNALS.append(interface2.address)
#TIMER2_SIGNALS.append(interface2.write_data)
#TIMER2_SIGNALS.append(interface2.read_data)
#TIMER2_SIGNALS.appedn(interface2.resp)

#INSTYPE0 = py4hw.Wire(sys,'INSTYPE0',1)
#INSTYPE1 = py4hw.Wire(sys,'INSTYPE1',1)
#INSTYPE2 = py4hw.Wire(sys,'INSTYPE2',1)

#OC0A = py4hw.Wire(sys,'OC0A',1)
#OC0B = py4hw.Wire(sys,'OC0B',1)
#OC1A = py4hw.Wire(sys,'OC1A',1)
#OC1B = py4hw.Wire(sys,'OC1B',1)
#OC2A = py4hw.Wire(sys,'OC2A',1)
#OC2B = py4hw.Wire(sys,'OC2B',1)

#T0 = py4hw.Wire(sys,'T0',1)
#T1 = py4hw.Wire(sys,'T1',1)
#T2 = py4hw.Wire(sys,'T2',1)

#SIGNALS.append(INSTYPE0)
#SIGNALS.append(OC0A)
#SIGNALS.append(OC0B)
#SIGNALS.append(T0)

#SIGNALS.append(INSTYPE1)
#SIGNALS.append(OC1A)
#SIGNALS.append(OC1B)
#SIGNALS.append(T1)

#SIGNALS.append(INSTYPE2)
#SIGNALS.append(OC2A)
#SIGNALS.append(OC2B)
#SIGNALS.append(T2)


#TIMER0 = TimerCounter0(sys,'TIMER0',interface0,INSTYPE0,OC0B,OC0A,T0,OCF0B,OCF0A,TOV0)
#TIMER1 = TimerCounter1(sys,'TIMER1',interface0,INSTYPE1,OC1B,OC1A,T1)
#TIMER2 = TimerCounter2(sys,'TIMER2',interface0,INSTYPE2,OC2B,OC2A,T2)

#Timer 0
#py4hw.Sequence(sys,'TIMER0_INSTYPE_TEST',TIMER0_INSTYPE,INSTYPE0)
#py4hw.Sequence(sys,'TIMER0_READ_TEST',TIMER0_READ_TEST,interface0.read)
#py4hw.Sequence(sys,'TIMER0_ADDRESS_TEST',TIMER0_ADDRESS_TEST_FULL,interface0.address)
#py4hw.Sequence(sys,'TIMER0_WRITE_TEST',TIMER0_WRITE_TEST,interface0.write)
#py4hw.Sequence(sys,'TIMER0_WRITE_DATA_TEST',TIMER0_WRITE_DATA_TEST,interface0.write_data)
#py4hw.Sequence(sys,'TIMER0_T0_TEST',TIMER0_T0_TEST,T0)


#Timer 1
#py4hw.Sequence(sys,'TIMER1_INSTYPE_TEST',TIMER1_INSTYPE,INSTYPE1)
#py4hw.Sequence(sys,'TIMER1_READ_TEST',TIMER1_READ_TEST,interface1.read)
#py4hw.Sequence(sys,'TIMER1_ADDRESS_TEST',TIMER1_ADDRESS_TEST_FULL,interface1.address)
#py4hw.Sequence(sys,'TIMER1_WRITE_TEST',TIMER1_WRITE_TEST,interface1.write)
#py4hw.Sequence(sys,'TIMER1_WRITE_DATA_TEST',TIMER1_WRITE_DATA_TEST,interface1.write_data)
#py4hw.Sequence(sys,'TIMER1_T1_TEST',TIMER1_T1_TEST,T1)

#Timer 2
#py4hw.Sequence(sys,'TIMER2_INSTYPE_TEST',TIMER2_INSTYPE,INSTYPE2)
#py4hw.Sequence(sys,'TIMER2_READ_TEST',TIMER2_READ_TEST,interface2.read)
#py4hw.Sequence(sys,'TIMER2_ADDRESS_TEST',TIMER2_ADDRESS_TEST_FULL,interface2.address)
#py4hw.Sequence(sys,'TIMER2_WRITE_TEST',TIMER2_WRITE_TEST,interface2.write)
#py4hw.Sequence(sys,'TIMER2_WRITE_DATA_TEST',TIMER2_WRITE_DATA_TEST,interface2.write_data)
#py4hw.Sequence(sys,'TIMER2_T2_TEST',TIMER2_T2_TEST,T2)


#wvf = py4hw.Waveform(sys,'wvf',SIGNALS)


#sch = py4hw.Schematic(sys)
#sch.draw()


#sys.getSimulator().clk(len(TIMER0_WRITE_DATA_TEST))
#wvf.gui()


if __name__ == "__main__":
    TestBench_of_Timer0()
