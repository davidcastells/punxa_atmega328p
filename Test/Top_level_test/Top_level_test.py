
# To use this file use the command python -i -m Test.Top_level_test.Top_level_test in the top directory of the project



import py4hw
import os
from punxa_atmega328p.SingleCycle.runCycle import *
from punxa_atmega328p.Memory import *
from punxa_atmega328p.Instruction_Decoder import *
import ast

PASS_OR_FAIL_LIST =[]
INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES = []
INSTRUCTION_SET_TEST_EXPECTED_MEMORY_VALUES = []
#INSTRUCTION_SET_TEST_EXPECTED_MEMORY_VALUES = [] # {address} {Value} 
COMMANDS_LIST= ["Build_Hardware","Instruction_test","Arduino_Code_Test","list_commands","printState","runCycles","Load_program_to_memory","Flash_Memory_Dump"]
#             +-----+     +---------------------+
#             | bus |--R--| GlobalConfRegisters |
#             |     |     +---------------------+
#  +-----+    |     |     +-----+
#  | CPU |--C-|     |--B--| mem |
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
#             |     |      +-----------+
#             |     |--E---|   EEPROM  |
#             |     |      +-----------+
#             |     |      +-----------+
#             |     |--I---| Interrupt |
#             |     |      +-----------+
#             +-----+
#
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


def Build_Hardware():
    global CPU
    global RAM
    global sys
    
    sys = py4hw.HWSystem()

    mem = MemoryInterface(sys,'port0',8,16)

    CPU = SingleCycleATmega328P(sys,'CPU',mem)#INT0,INT1,PCINT0,PCINT1,PCINT2,WDT,TIMER2_COMPA,TIMER2_COMPB,TIMER2_OVF,TIMER1_CAPT,TIMER1_COMPA,TIMER1_COMPB,TIMER1_OVF,TIMER0_COMPA,TIMER0_COMPB,TIMER0_OVF,SPI_STC,USART_RX,USART_UDRE,USART_TX,ADC,EE_READY,ANALOG_COMP,TWI,SPM_READY)
    RAM = Ram_Memory(sys,'mem',8,16,mem)

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
    error_Message = ''


    #test registers
    for i in range(31):
        if CPU.reg[i] != INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][i]:
            error_Message = error_Message +"reg-{v} {E} expected: {C}".format(v=i,C=INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][i],E=CPU.reg[i])
            everything_ok = False
    
    #test of SREG
    if CPU.SREG != INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][31]:
        error_Message = error_Message + "SREG {E} expected: {C}".format(v=i,C=INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][31],E=CPU.SREG)
        everything_ok = False

    #test of pc
    if CPU.pc != INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][32]:
        error_Message =  error_Message + "PC {E} expected: {C}".format(v=i,C=INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][32],E=CPU.pc)
        everything_ok = False

    #test of sp 
    SP = ((CPU.SPH<<8) | (CPU.SPL))
    if SP != INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][33]:
        error_Message =  error_Message + "SP {E} expected: {C}".format(v=i,C=INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES[instruction_counter_val][33],E = SP)
        everything_ok = False

    #verifing ram 

    for address,val in INSTRUCTION_SET_TEST_EXPECTED_MEMORY_VALUES[instruction_counter_val].items():
        #print(type(val),val)
        #print(type(address),address)
        if (address >= 0x100) and (address <= 0x8FF):
            address_int = address -0x0100 -1
            #print(len(RAM.values),address_int)
            if RAM.values[address_int] != int(val):
                error_Message = error_Message + "Address {address1} {val1} expected: {val2}".format(address1 = address , val1= RAM.values[address_int], val2=val)
                everything_ok = False

    #test of memory

    return everything_ok, error_Message
def Load_program_to_memory(Test_File,Verbose=False):
    file_path = ''

    match Test_File:

        case 'INSTRUCTION_TEST' :
            file_path = 'Test/Code_Test/INSTRUCTION_TEST.hex'
            CPU.pc = 0
        
        case 'INSTRUCTION_TESTV2' :
            file_path = 'Test/Code_Test/INSTRUCTION_TESTV2.hex'
            CPU.pc = 0

        case 'ARDUINO_TEST_PROGRAM' :
            file_path = 'Test/Code_Test/ARDUINO_TEST_PROGRAM.hex'
            CPU.pc = 0x3F00
        

    with open(file_path,'rb') as f:
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

def runCycles(nbCycle):
    sys.getSimulator().clk(nbCycle)
def Flash_Memory_Dump():
    if os.path.exists("Test/Top_level_test/FlashMemoryDump.txt"):
        os.remove("Test/Top_level_test/FlashMemoryDump.txt")

        ## CPU Flash memory dump  
        dump = open("Test/Top_level_test/FlashMemoryDump.txt", "a")
        #dump with instrucions decoded. #CALL and JUMP are 32bits 
        for i in range(0,len(CPU.flash)):
            ins = CPU.flash[i] 
            if CPU.pc == (i-1): 
                dump.write(">{0:>016b} : {instr} \n".format(ins,instr = ins_to_str(ins)))
            else:
                dump.write("{0:>016b} : {instr} \n".format(ins,instr = ins_to_str(ins)))

        dump.close()
def Ram_Memory_Dump():
    if os.path.exists("Test/Top_level_test/RamMemoryDump.txt"):
        os.remove("Test/Top_level_test/RamMemoryDump.txt")

    ## CPU Ram memory dump  
    dump = open("Test/Top_level_test/RamMemoryDump.txt", "a")
    #dump with instrucions decoded. #CALL and JUMP are 32bits 
    for i in range(0,len(RAM.values)):
        val = RAM.values[i]
        dump.write("{0:>08b} : {val1} \n".format(val,val1 = val))

    dump.close()
def printState():
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


#wvf = py4hw.Waveform(sys,'wvf',SIGNALS)


#if Show_Schematic == True:
#    sch = py4hw.Schematic(sys)
#    sch.draw()
 

#load instruction test to memory 
def Instruction_test(Line_by_line=False,Verbose=False,breakPoint=0): 
    instruction_counter = 0
    everything_ok = True

    with open('Test/Code_Test/EXPECTED_REGISTER_VALUESV2.txt','r') as file:
        for line in file:
            data_list = ast.literal_eval(line.strip())
            clean_list = [int(item) for item in data_list[0]]
            #print(type(data_list[2]))
            clean_dict = {int(key):int(val) for key,val in data_list[2].items()}
            INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES.append(clean_list)
            INSTRUCTION_SET_TEST_EXPECTED_MEMORY_VALUES.append(clean_dict)

    #print(INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES)
    
    #loading the test code
    memory_position = 0

    with open('Test/Code_Test/INSTRUCTION_TESTV2.hex','rb') as f:
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

        if  Line_by_line == True:
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
            
            #sys.getSimulator().clk(366) # memeory test part of the program 

            main_loop = True
            while main_loop == True:

            #if user_command == 'r':
                if os.path.exists("Test/Top_level_test/RamMemoryDump.txt"):
                    os.remove("Test/Top_level_test/RamMemoryDump.txt")

                ## CPU Flash memory dump  
                dump = open("Test/Top_level_test/RamMemoryDump.txt", "a")
                #dump with instrucions decoded. #CALL and JUMP are 32bits 
                val = 0xFF 
                for i in range(0,len(RAM.values)):
                    val = RAM.values[i]
                    if val != 0:
                        dump.write("{address} >{0:>08b} : {val1} \n".format(val,val1 = val,address = (i+0x100)))
                    else: 
                        dump.write("{address} {0:>08b} : {val1} \n".format(val,val1 = val,address = (i+0x100)))

                dump.close()

                user_command = input()
                if user_command ==  'f':
                    if os.path.exists("Test/Top_level_test/FlashMemoryDump.txt"):
                        os.remove("Test/Top_level_test/FlashMemoryDump.txt")

                    ## CPU Flash memory dump  
                    dump = open("Test/Top_level_test/FlashMemoryDump.txt", "a")
                    #dump with instrucions decoded. #CALL and JUMP are 32bits 
                    for i in range(0,len(CPU.flash)):
                        ins = CPU.flash[i] 
                        if CPU.pc == (i-1): 
                            dump.write(">{0:>016b} : {instr} \n".format(ins,instr = ins_to_str(ins)))
                        else:
                            dump.write("{0:>016b} : {instr} \n".format(ins,instr = ins_to_str(ins)))

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
            if os.path.exists("Test/Top_level_test/Test_resuslts.txt"):
                os.remove("Test/Top_level_test/Test_resuslts.txt")
            results = open("Test/Top_level_test/Test_resuslts.txt","a")
            instruction_counter = 0
            for i in range(len(INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES)):
                past_pc = CPU.pc
                while past_pc == CPU.pc:
                    sys.getSimulator().clk(1)
                    #print("CPU.pc:=",CPU.pc)
                    #print("instruction",ins_to_str(CPU.flash[instruction_counter]))
                    if breakPoint != 0:
                        if CPU.pc == breakPoint:
                            print("Next instruction:{instruction}".format(instruction =  ins_to_str(CPU.flash[CPU.pc])))
                            for i in range(32):
                                print("R{index}:{value}".format(index = i, value = CPU.reg[i]),end=" ")
                            print("Pc:{value}".format(value = CPU.pc))
                            print("Ps:{value}".format(value = (CPU.SPH<<8) | (CPU.SPL&0xFF)))
                            print("opp:{value1} ins:{value2} Rr:{value3} Rd:{value4} K:{value5} A:{value6}".format( value1 = CPU.opp , value2 = bin(CPU.ins) , value3 = CPU.Rr , value4 = CPU.Rd ,value5 = CPU.K, value6 = hex(CPU.A)))
                            print("SREG:{0:>08b}".format(CPU.SREG))
                        


                #testing if the output is correct
                #print("instruction",ins_to_str(CPU.flash[past_pc]),end='')
                

                everything_ok,error_Message = verify_instruction_value(instruction_counter)
                appds = (everything_ok,error_Message) 
                #print(appds)
                results.write("instruction:{ins} {res} \n".format(ins = ins_to_str(CPU.flash[past_pc]), res = appds ))
                PASS_OR_FAIL_LIST.append(appds)
                instruction_counter+=1
            results.close()


            if os.path.exists("Test/Top_level_test/RamMemoryDump.txt"):
                os.remove("Test/Top_level_test/RamMemoryDump.txt")


            dump = open("Test/Top_level_test/RamMemoryDump.txt", "a")
            #dump with instrucions decoded. #CALL and JUMP are 32bits 
            for i in range(0,len(RAM.values)):
                val = RAM.values[i]
                dump.write("{0:>08b} : {val1} \n".format(val,val1 = val))

            dump.close()

            if os.path.exists("Test/Top_level_test/FlashMemoryDump.txt"):
                os.remove("Test/Top_level_test/FlashMemoryDump.txt")

            ## CPU ram memory dump  
            dump = open("Test/Top_level_test/FlashMemoryDump.txt", "a")
            #dump with instrucions decoded. #CALL and JUMP are 32bits 
            for i in range(0,len(CPU.flash)):
                ins = CPU.flash[i] 
                if CPU.pc == (i-1): 
                    dump.write("{addr} >{A:>016b} : {instr} \n".format(A=ins,addr = i,instr = ins_to_str(ins)))
                else:
                    dump.write("{addr} {A:>016b} : {instr} \n".format(A=ins,addr = i,instr = ins_to_str(ins)))

            dump.close()
def Arduino_Code_Test(Line_by_line=False,Verbose=False): 
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


    if Line_by_line == True:


        print("Hello \n n : next instruction \n r: ram memory dump \n f: flash memory dump \n e: exit ")
            
        print("Register State")
        #print register state 
        print("Next instruction:{instruction}".format(instruction = ins_to_str(CPU.flash[CPU.pc])))
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

                ## CPU Ram memory dump  
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
def list_commands():
    for item in COMMANDS_LIST:
        print(item)