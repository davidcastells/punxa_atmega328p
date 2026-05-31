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
