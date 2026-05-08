import py4hw
import os
from Lib.SingleCycle.runCycle import *
from Lib.Memory import *
from Lib.Instruction_Decoder import *
import ast

PASS_OR_FAIL_LIST =[]
INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES = []

#INSTRUCTION_SET_TEST_EXPECTED_MEMORY_VALUES = [] # {address} {Value} 

#  +-----+    +-----+     +-----+
#  | CPU |--C-| bus |--B--| mem |
#  +-----+    |     |     +-----+
#             |     |     +------+
#             |     |--U--| uart |
#             |     |     +------+
#             |     |     +-----+
#             |     |--S--| SPI |
#             |     |     +-----+
#             |     |     +-----+
#             |     |--A--| ADC |
#             |     |     +-----+
#             |     |     +------+
#             |     |--G--| GPIO |
#             |     |     +------+
#             |     |      +-----------+
#             |     |--T0--| 8bitTimer0|
#             |     |      +-----------+
#             |     |      +------------+
#             |     |--T1--| 16bitTimer1|
#             |     |      +------------+
#             |     |      +-----------+
#             |     |--T2--| 8bitTimer2|
#             |     |      +-----------+
#             +-----+
#  | start               | stop                | device        |
#  | 0080 0000 0000 0000 | 0080 0000 FFFF FFFF | memory (2GB)  |
#  | 0000 00FF F0C2 C000 | 0000 00FF F0C2 CFFF | UART          |
#  | 0000 0000 0200 0000 | 0000 0000 0202 FFFF | CLINT         |
#  | 0000 0000 0C00 0000 | 0000 0000 0C0F FFFF | PLIC          |
#  | 0000 0000 0C00 0000 | 0000 0000 0C0F FFFF | GPIO          |



# Pinout:
# PIN1 PD3 (INT1/OC2B/PCINT19)
# PIN2 PD4 (T0/XCK/PCINT20)
# PIN3 GND 
# PIN4 VCC
# PIN5 GND
# PIN6 VCC
# PIN7 PB6 (TOSC1/XTAL1/PCINT6)
# PIN8 PB7 (TOSC2/XTAL2/PCINT7)
# PIN9 PD5 (T1/OC0B/PCINT21)
# PIN10 PD6 (AIN0/OC0A/PCINT22)
# PIN11 PD7 (AIN1/PCINT23)
# PIN12 PB0 (ICP1/CLOKO/PCINT0)
# PIN13 PB1 (OC1A/PCINT1)
# PIN14 PB2 (OC1B/!SS/PCINT2)
# PIN15 PB3 (MOSI/OC2A/PCINT3)
# PIN16 PB4 (MISO/PCINT4)
# PIN17 PB5 (SCK/PCINT5)
# PIN18 AVCC
# PIN19 ADC6
# PIN20 AREF
# PIN21 GND
# PIN22 ADC7
# PIN23 PC0 (ADC0/PCINT8)
# PIN24 PC1 (ADC1/PCINT9)
# PIN25 PC2 (ADC2/PCINT10)
# PIN26 PC3 (ADC3/PCINT11)
# PIN27 PC4 (ADC4/SDA/PCINT12)
# PIN28 PC5 (ADC5/SCL/PCINT13)
# PIN29 PC6 (!RESET/PCINT14)
# PIN30 PD0 (RXD/PCINT16)
# PIN31 PD1 (TXD/PCINT17)
# PIN32 PD2 (INT0/PCINT18)




#Parameters for the test bench 

Verbose = False
#while Verbose == 7:
#    print("Verbose? Y/N")
#    responce = input()
#    if (responce == 'Y') or (responce == 'y'):
#        Verbose = True 
#    elif (responce == 'N') or (responce == 'n'):
#        Verbose = False 

Show_Schematic = True
#while Show_Schematic == 7:
#    print("Show Schematic? Y/N")
#    responce = input()
#    if (responce == 'Y') or (responce == 'y'):
#        Show_Schematic = True 
#    elif (responce == 'N') or (responce == 'n'):
#        Show_Schematic = False 

#Loades Custom instructions in flash to test each instruction 
Instruction_test = True
#while Instruction_test == 7:
#    print("Instruction Test? Y/N")
#    responce = input()
#    if (responce == 'Y') or (responce == 'y'):
#        Instruction_test = True 
#    elif (responce == 'N') or (responce == 'n'):
#        Instruction_test = False 

#Loads the hex file and executes the code 
Arduino_Code_Test = False
#while Arduino_Code_Test == 7:
#    print("Arduino Code Test? Y/N")
#    responce = input()
#    if (responce == 'Y') or (responce == 'y'):
#        Arduino_Code_Test = True 
#    elif (responce == 'N') or (responce == 'n'):
#        Arduino_Code_Test = False 

Line_by_Line = False
#if (Instruction_test == True) or (Arduino_Code_Test == True): 
#    while Line_by_Line == 7:
#        print("Execute line By line ? Y/N")
#        responce = input()
#        if (responce == 'Y') or (responce == 'y'):
#            Line_by_Line = True 
#        elif (responce == 'N') or (responce == 'n'):
#            Line_by_Line = False 

#if Arduino_Code_Test == True:
#    print_periferal_registers = 7
#    while print_periferal_registers == 7:
#        print("Execute line By line ? Y/N")
#        responce = input()
#        if (responce == 'Y') or (responce == 'y'):
#            print_periferal_registers = True 
#        elif (responce == 'N') or (responce == 'n'):
#            print_periferal_registers = False 


sys = py4hw.HWSystem()

mem = MemoryInterface(sys,'port0',8,16)




#port_C = MemoryInterface(sys,'port_C',8,16)
#port_B = MemoryInterface(sys,'port_B',8,16)
#port_U = MemoryInterface(sys,'port_U',8,16)
#port_S = MemoryInterface(sys,'port_S',8,16)
#port_A = MemoryInterface(sys,'port_A',8,16)
#port_G = MemoryInterface(sys,'port_G',8,16)
#port_T0= MemoryInterface(sys,'prot_T0',8,16)
#port_T1= MemoryInterface(sys,'prot_T1',8,16)
#port_T2= MemoryInterface(sys,'prot_T2',8,16)


#SIGNALS = []

#INT0 = py4hw.Wire(sys,'INT0',1)
#INT1 = py4hw.Wire(sys,'INT1',1)
#PCINT0 = py4hw.Wire(sys,'PCINT0',1)
#PCINT1 = py4hw.Wire(sys,'PCINT1',1)
#PCINT2 = py4hw.Wire(sys,'PCINT2',1)
#WDT = py4hw.Wire(sys,'WDT',1)
#TIMER2_COMPA = py4hw.Wire(sys,'TIMER2_COMPA',1)
#TIMER2_COMPB = py4hw.Wire(sys,'TIMER2_COMPB',1)
#TIMER2_OVF = py4hw.Wire(sys,'TIMER2_OVF',1)
#TIMER1_CAPT = py4hw.Wire(sys,'TIMER1_CAPT',1)
#TIMER1_COMPA = py4hw.Wire(sys,'TIMER1_COMPA',1)
#TIMER1_COMPB = py4hw.Wire(sys,'TIMER1_COMPB',1)
#TIMER1_OVF = py4hw.Wire(sys,'TIMER1_OVF',1)
#TIMER0_COMPA = py4hw.Wire(sys,'TIMER0_COMPA',1)
#TIMER0_COMPB = py4hw.Wire(sys,'TIMER0_COMPB',1)
#TIMER0_OVF = py4hw.Wire(sys,'TIMER0_OVF',1)
#SPI_STC = py4hw.Wire(sys,'SPI_STC',1)
#USART_RX = py4hw.Wire(sys,'USART_RX',1)
#USART_UDRE = py4hw.Wire(sys,'USART_UDRE',1)
#USART_TX = py4hw.Wire(sys,'USART_TX',1)
#ADC = py4hw.Wire(sys,'ADC',1)
#EE_READY = py4hw.Wire(sys,'EE_READY',1)
#ANALOG_COMP = py4hw.Wire(sys,'ANALOG_COMP',1)
#TWI = py4hw.Wire(sys,'TWI',1)
#SPM_READY = py4hw.Wire(sys,'SPM_READY',1)


#SIGNALS.append(INT0)
#SIGNALS.append(INT1)
#SIGNALS.append(PCINT0)
#SIGNALS.append(PCINT1)
#SIGNALS.append(PCINT2)
#SIGNALS.append(WDT)
#SIGNALS.append(TIMER2_COMPA)
#SIGNALS.append(TIMER2_COMPB)
#SIGNALS.append(TIMER2_OVF)
#SIGNALS.append(TIMER1_CAPT)
#SIGNALS.append(TIMER1_COMPA)
#SIGNALS.append(TIMER1_COMPB)
#SIGNALS.append(TIMER1_OVF)
#SIGNALS.append(TIMER0_COMPA)
#SIGNALS.append(TIMER0_COMPB)
#SIGNALS.append(TIMER0_OVF)
#SIGNALS.append(SPI_STC)
#SIGNALS.append(USART_RX)
#SIGNALS.append(USART_UDRE)
#SIGNALS.append(USART_TX)
#SIGNALS.append(ADC)
#SIGNALS.append(EE_READY)
#SIGNALS.append(ANALOG_COMP)
#SIGNALS.append(TWI)
#SIGNALS.append(SPM_READY)

def verify_instruction_value (instruction_counter_val):
    everything_ok = True
    error_Message = 'NULL'

    #test registers
    for i in range(32):
        if CPU.reg[i] != INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][i]:
            error_Message = "reg-{v} wrong value {C}".format(v=i,C=INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][i])
            everything_ok = False
    
    #test of SREG
    if CPU.SREG != INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][31]:
        error_Message = "SREG wrong value expected: {C}".format(v=i,C=INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][31])
        everything_ok = False

    #test of pc
    if CPU.pc != INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][32]:
        error_Message = "PC wrong value expected: {C}".format(v=i,C=INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][32])
        everything_ok = False

    #test of sp 
    SP = ((CPU.SPH<<8) | (CPU.SPL))
    if SP != INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][33]:
        error_Message = "SP wrong value expected: {C}".format(v=i,C=INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][33])
        everything_ok = False


    return everything_ok, error_Message


CPU = SingleCycleATmega328P(sys,'CPU',mem)#INT0,INT1,PCINT0,PCINT1,PCINT2,WDT,TIMER2_COMPA,TIMER2_COMPB,TIMER2_OVF,TIMER1_CAPT,TIMER1_COMPA,TIMER1_COMPB,TIMER1_OVF,TIMER0_COMPA,TIMER0_COMPB,TIMER0_OVF,SPI_STC,USART_RX,USART_UDRE,USART_TX,ADC,EE_READY,ANALOG_COMP,TWI,SPM_READY)
RAM = Memory(sys,'mem',8,16,mem)


#wvf = py4hw.Waveform(sys,'wvf',SIGNALS)


#if Show_Schematic == True:
#    sch = py4hw.Schematic(sys)
#    sch.draw()
 

instruction_counter = 0
everything_ok = True

#load instruction test to memory 
if Instruction_test == True:

    with open('Code_Test/EXPECTED_REGISTER_VALUES.txt','r') as file:
        for line in file:
            data_list = ast.literal_eval(line.strip())
            clean_list = [int(item) for item in data_list]
            INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES.append(clean_list)
    #print(INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES)
    #loading the test code
    memory_position = 0
    with open('./Code_Test/INSTRUCTION_TEST.hex','rb') as f:
        while 1 :
            start_Code = f.read(1)
            if not start_Code:
                break
            start_Code = str(start_Code,'utf-8')
            if Verbose == True :
                print("start_code:",start_Code)
            nbbytes = str(f.read(2),'utf-8')
            if Verbose == True :
                print("nbbytes:",nbbytes)
            starting_address =  str(f.read(4),'utf-8')
            if Verbose == True :
                print("starting_address:",starting_address)
            record_type = str(f.read(2),'utf-8')
            if Verbose == True :
                print("record_type:",record_type)
            if record_type == "00": # To write only "Data Record"
                memory_position = int(starting_address,16)//2

                for i in range(int(nbbytes,16)//2): 
                    byteLSB = str(f.read(2),'utf-8')  #there may be a problem between word adressis and byte adressis but I am willing to let it slide
                    byteMSB = str(f.read(2),'utf-8')
                    byte = byteMSB + byteLSB
                    CPU.flash[memory_position] = int(byte,16)  #little or big 
                    if Verbose == True :
                        print("Flash:{flash} Mem_pos:{mem_pos} Index:{index} Val:{val}".format(flash=hex(CPU.flash[memory_position]),mem_pos=memory_position,index = i ,val = byte))   
                    memory_position+=1

                checksum = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("checksum:",checksum)
                end_of_line_caracters = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("end_of_line_caracters:",end_of_line_caracters)

            elif record_type == '01': #"End of Record."

                memory_position = int(starting_address,16)//2
                byte = str(f.read(4),'utf-8')
                if Verbose == True :
                    print("Index:{index} Val:{val}".format(index = i ,val = byte)) 
                #CPU.flash[memory_position] = int(byte,16)  #little or big 
                checksum = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("checksum:",checksum)
                end_of_line_caracters = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("end_of_line_caracters:",end_of_line_caracters)
                
            elif record_type == '02':  #"Extended Segment Address Record"
                if Verbose == True :
                    print("Record type 02 not implemented")

            elif record_type == '03':  #"Start Segment Address Record"
                if Verbose == True :
                    print("Record type 03 not implemented")

            elif record_type == '04':  #"Extended Linear Address Record"
                byte = str(f.read(4),'utf-8')
                if Verbose == True :
                    print("Val:{val}".format( val = byte)) 
                memory_position = 0
                checksum = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("checksum:",checksum)
                end_of_line_caracters = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("end_of_line_caracters",end_of_line_caracters)

            elif record_type == '05':  #"Extended Linear Address Record"
                if Verbose == True :
                    print("Record type 05 not implemented")
                
        f.close()
        CPU.pc = 0

        if  Line_by_Line == True:
            print("Hello \n n : next instruction \n r: ram memory dump \n f: flash memory dump \n e: exit ")
                
            print("Register State")
            #print register state 
            print("Next instruction:{instruction}".format(instruction =  ins_to_str(CPU.flash[CPU.pc])))
            for i in range(32):
                print("R{index} : {value}".format(index = i, value = CPU.reg[i]),end=" ")
            print("Pc:{value}".format(value = CPU.pc))
            print("Ps:{value}".format(value = (CPU.SPH<<8) | (CPU.SPL&0xF)))
            print("opp:{value1} ins:{value2} Rr:{value3} Rd:{value4} K:{value5} A:{value6}".format(value1 = CPU.opp,value2 = bin(CPU.ins), value3 = CPU.Rr, value4 = CPU.Rd,value5 = CPU.K, value6 = hex(CPU.A)))
            #print("I:{I} T:{T} H:{H} S:{S} V:{V} N:{N} Z:{Z} C{C}".format(I = CPU.I))
            print("SREG:{0:>08b}".format(CPU.SREG))
            print("---------------------------------------------------------------")            
            #sys.getSimulator().clk(8) 
            main_loop = True
            while main_loop == True:


                user_command = input()
                if user_command ==  'f':
                    if os.path.exists("FlashMemoryDump.txt"):
                        os.remove("FlashMemoryDump.txt")

                    ## CPU Flash memory dump  
                    dump = open("FlashMemoryDump.txt", "a")
                    #dump with instrucions decoded. #CALL and JUMP are 32bits 
                    for i in range(0,len(CPU.flash)):
                        ins = CPU.flash[i] 
                        if CPU.pc == (i-1): 
                            dump.write(">{0:>016b} : {instr} \n".format(ins,instr = ins_to_str(ins)))
                        else:
                            dump.write("{0:>016b} : {instr} \n".format(ins,instr = ins_to_str(ins)))

                    dump.close()

                elif user_command == 'r':
                    if os.path.exists("RamMemoryDump.txt"):
                        os.remove("RamMemoryDump.txt")

                    ## CPU Flash memory dump  
                    dump = open("RamMemoryDump.txt", "a")
                    #dump with instrucions decoded. #CALL and JUMP are 32bits 
                    for i in range(0,len(RAM.values)):
                        val = RAM.values[i]
                        dump.write("{0:>08b} : {val1} \n".format(val,val1 = val))

                    dump.close()
                    
                elif user_command == 'n':        
                    sys.getSimulator().clk(1)
                    print("Next instruction:{instruction}".format(instruction =  ins_to_str(CPU.flash[CPU.pc])))
                    for i in range(32):
                        print("R{index}:{value}".format(index = i, value = CPU.reg[i]),end=" ")
                    print("Pc:{value}".format(value = CPU.pc))
                    print("Ps:{value}".format(value = (CPU.SPH<<8) | (CPU.SPL&0xFF)))
                    print("opp:{value1} ins:{value2} Rr:{value3} Rd:{value4} K:{value5} A:{value6}".format( value1 = CPU.opp , value2 = bin(CPU.ins) , value3 = CPU.Rr , value4 = CPU.Rd ,value5 = CPU.K, value6 = hex(CPU.A)))
                    print("SREG:{0:>08b}".format(CPU.SREG))

                    #testing if the output is correct
                    #everything_ok = verify_instruction_value(instruction_counter)
                    #instruction_counter+=1
                    #if everything_ok == True:
                    #    PASS_OR_FAIL_LIST.append("PASS")
                    #else:
                    #    PASS_OR_FAIL_LIST.append("FAIL")
                    

                    print("---------------------------------------------------------------")
                
                elif user_command == 'e':#to exit
                    main_loop = False
                    #for i in range(len(PASS_OR_FAIL_LIST)):
                    #    print(PASS_OR_FAIL_LIST[i])
        else:
            instruction_counter = 0
            for i in range(len(INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES)):
                sys.getSimulator().clk(1)
                #testing if the output is correct
                everything_ok,error_Message = verify_instruction_value(instruction_counter)
                instruction_counter+=1
                appds = (everything_ok,error_Message) 
                PASS_OR_FAIL_LIST.append(appds)


            print(PASS_OR_FAIL_LIST)

if Arduino_Code_Test == True: 
    ## loading hex file of arduino test code to memory 
    memory_position = 0
    with open('./Code_Test/ARDUINO_TEST_PROGRAM.hex','rb') as f:
        while 1 :
            start_Code = f.read(1)
            if not start_Code:
                break
            start_Code = str(start_Code,'utf-8')
            if Verbose == True :
                print("start_code:",start_Code)
            nbbytes = str(f.read(2),'utf-8')
            if Verbose == True :
                print("nbbytes:",nbbytes)
            starting_address =  str(f.read(4),'utf-8')
            if Verbose == True :
                print("starting_address:",starting_address)
            record_type = str(f.read(2),'utf-8')
            if Verbose == True :
                print("record_type:",record_type)
            if record_type == "00": # To write only "Data Record"
                memory_position = int(starting_address,16)//2

                for i in range(int(nbbytes,16)//2): 
                    byteLSB = str(f.read(2),'utf-8')  #there may be a problem between word adressis and byte adressis but I am willing to let it slide
                    byteMSB = str(f.read(2),'utf-8')
                    byte = byteMSB + byteLSB
                    CPU.flash[memory_position] = int(byte,16)  #little or big 
                    if Verbose == True :
                        print("Flash:{flash} Mem_pos:{mem_pos} Index:{index} Val:{val}".format(flash=hex(CPU.flash[memory_position]),mem_pos=memory_position,index = i ,val = byte))   
                    memory_position+=1

                checksum = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("checksum:",checksum)
                end_of_line_caracters = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("end_of_line_caracters:",end_of_line_caracters)

            elif record_type == '01': #"End of Record."

                memory_position = int(starting_address,16)//2
                byte = str(f.read(4),'utf-8')
                if Verbose == True :
                    print("Index:{index} Val:{val}".format(index = i ,val = byte)) 
                #CPU.flash[memory_position] = int(byte,16)  #little or big 
                checksum = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("checksum:",checksum)
                end_of_line_caracters = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("end_of_line_caracters:",end_of_line_caracters)
                
            elif record_type == '02':  #"Extended Segment Address Record"
                if Verbose == True :
                    print("Record type 02 not implemented")

            elif record_type == '03':  #"Start Segment Address Record"
                if Verbose == True :
                    print("Record type 03 not implemented")

            elif record_type == '04':  #"Extended Linear Address Record"
                byte = str(f.read(4),'utf-8')
                if Verbose == True :
                    print("Val:{val}".format( val = byte)) 
                memory_position = 0
                checksum = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("checksum:",checksum)
                end_of_line_caracters = str(f.read(2),'utf-8')
                if Verbose == True :
                    print("end_of_line_caracters",end_of_line_caracters)

            elif record_type == '05':  #"Extended Linear Address Record"
                if Verbose == True :
                    print("Record type 05 not implemented")
                
        f.close()


    if Line_by_Line == True:
        print("Hello \n n : next instruction \n r: ram memory dump \n f: flash memory dump \n e: exit ")
            
        print("Register State")
        #print register state 
        print("Next instruction:{instruction}".format(instruction =  ins_to_str(CPU.flash[CPU.pc])))
        for i in range(32):
            print("R{index} : {value}".format(index = i, value = CPU.reg[i]),end=" ")
        print("Pc:{value}".format(value = CPU.pc))
        print("Ps:{value}".format(value = (CPU.SPH<<8) | (CPU.SPL&0xF)))
        print("opp:{value1} ins:{value2} Rr:{value3} Rd:{value4} K:{value5} A:{value6}".format(value1 = CPU.opp,value2 = bin(CPU.ins), value3 = CPU.Rr, value4 = CPU.Rd,value5 = CPU.K, value6 = hex(CPU.A)))
        #print("I:{I} T:{T} H:{H} S:{S} V:{V} N:{N} Z:{Z} C{C}".format(I = CPU.I))
        print("SREG:{0:>08b}".format(CPU.SREG))
        print("---------------------------------------------------------------")
        main_loop = True
        while main_loop == True:


            user_command = input()
            if user_command ==  'f':
                if os.path.exists("FlashMemoryDump.txt"):
                    os.remove("FlashMemoryDump.txt")

                ## CPU Flash memory dump  
                dump = open("FlashMemoryDump.txt", "a")
                #dump with instrucions decoded. #CALL and JUMP are 32bits 
                for i in range(0,len(CPU.flash)):
                    ins = CPU.flash[i] 
                    if CPU.pc == (i-1): 
                        dump.write(">{0:>016b} : {instr} \n".format(ins,instr = ins_to_str(ins)))
                    else:
                        dump.write("{0:>016b} : {instr} \n".format(ins,instr = ins_to_str(ins)))

                dump.close()

            elif user_command == 'r':
                if os.path.exists("RamMemoryDump.txt"):
                    os.remove("RamMemoryDump.txt")

                ## CPU Flash memory dump  
                dump = open("RamMemoryDump.txt", "a")
                #dump with instrucions decoded. #CALL and JUMP are 32bits 
                for i in range(0,len(RAM.values)):
                    val = RAM.values[i]
                    dump.write("{0:>08b} : {val1} \n".format(val,val1 = val))

                dump.close()
                
            elif user_command == 'n':        
                sys.getSimulator().clk(1)
                print("Next instruction:{instruction}".format(instruction =  ins_to_str(CPU.flash[CPU.pc])))
                for i in range(32):
                    print("R{index}:{value}".format(index = i, value = CPU.reg[i]),end=" ")
                print("Pc:{value}".format(value = CPU.pc))
                print("Ps:{value}".format(value = (CPU.SPH<<8) | (CPU.SPL&0xFF)))
                print("opp:{value1} ins:{value2} Rr:{value3} Rd:{value4} K:{value5} A:{value6}".format( value1 = CPU.opp , value2 = bin(CPU.ins) , value3 = CPU.Rr , value4 = CPU.Rd ,value5 = CPU.K, value6 = hex(CPU.A)))
                print("SREG:{0:>08b}".format(CPU.SREG))
                print("---------------------------------------------------------------")
            
            elif user_command == 'e':#to exit
                main_loop = False




