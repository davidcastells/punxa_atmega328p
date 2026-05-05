import py4hw
import os
from Lib.SingleCycle.runCycle import *
from Lib.Memory import *
from Lib.Instruction_Decoder import *

INSTRUCTION_SET_TEST_PROGRAM = [
    0b1110 0000 0001 1111, #LDI 16,16
    0b1110 0000 0010 1111, #LDI 17,16
    0b0000 1111 0001 0010, #ADD 16,17
]
INSTRUCTION_SET_TEST_EXPECTED_REGISTER_VALUES = [ #{R0 to R31} {STREG} {PROGRAM COUNTER} {STACK POINTER} 
    #R:0|R:1|R:2|R:3|R:4|R:5|R:6|R:7|R:8|R:9|R:10|R:11|R:12|R:13|R:14|R:15|R:16|R:17|R:18|R:19|R:20|R:21|R:22|R:23|R:24|R:25|R:26|R:27|R:28|R:29|R:30|SREG      |PC|SP
    [0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0    ,0  ,0b00000000,0,0]
    [0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0   ,0   ,0   ,0   ,0   ,0   ,16  ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0    ,0  ,0b00000000,1,0]#LDI 16,16
    [0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0   ,0   ,0   ,0   ,0   ,0   ,16  ,16  ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0    ,0  ,0b00000000,2,0]#LDI 17,16
    [0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0   ,0   ,0   ,0   ,0   ,0   ,32  ,16  ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0    ,0  ,0b00000000,3,0]#ADD 16,17

]

INSTRUCTION_SET_TEST_EXPECTED_MEMORY_VALUES = [] # {address} {Value} 

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

#Parameters for the test bench 
Verbose = 7
while Verbose == 7:
    print("Verbose? Y/N")
    responce = input()
    if (responce == 'Y') or (responce == 'y'):
        Verbose = True 
    elif (responce == 'N') or (responce == 'n'):
        Verbose = False 

Show_Schematic = 7
while Show_Schematic == 7:
    print("Show Schematic? Y/N")
    responce = input()
    if (responce == 'Y') or (responce == 'y'):
        Show_Schematic = True 
    elif (responce == 'N') or (responce == 'n'):
        Show_Schematic = False 

#Loades Custom instructions in flash to test each instruction 
Instruction_test = 7
while Instruction_test == 7:
    print("Instruction Test? Y/N")
    responce = input()
    if (responce == 'Y') or (responce == 'y'):
        Instruction_test = True 
    elif (responce == 'N') or (responce == 'n'):
        Instruction_test = False 

#Loads the hex file and executes the code 
Arduino_Code_Test = 7
while Arduino_Code_Test == 7:
    print("Arduino Code Test? Y/N")
    responce = input()
    if (responce == 'Y') or (responce == 'y'):
        Arduino_Code_Test = True 
    elif (responce == 'N') or (responce == 'n'):
        Arduino_Code_Test = False 

if (Instruction_test == True) or (Arduino_Code_Test == True): 
    Line_by_Line = 7
    while Line_by_Line == 7:
        print("Execute line By line ? Y/N")
        responce = input()
        if (responce == 'Y') or (responce == 'y'):
            Line_by_Line = True 
        elif (responce == 'N') or (responce == 'n'):
            Line_by_Line = False 

if Arduino_Code_Test == True:
    print_periferal_registers = 7
    while print_periferal_registers == 7:
        print("Execute line By line ? Y/N")
        responce = input()
        if (responce == 'Y') or (responce == 'y'):
            print_periferal_registers = True 
        elif (responce == 'N') or (responce == 'n'):
            print_periferal_registers = False 

sys = py4hw.HWSystem()

mem = MemoryInterface(sys,'port0',8,16)

CPU = SingleCycleATmega328P(sys,'CPU',mem)
RAM = Memory(sys,'mem',8,16,mem)


port_C = MemoryInterface(sys,'port_C',8,16)
port_B = MemoryInterface(sys,'port_B',8,16)
port_U = MemoryInterface(sys,'port_U',8,16)
port_S = MemoryInterface(sys,'port_S',8,16)
port_A = MemoryInterface(sys,'port_A',8,16)
port_G = MemoryInterface(sys,'port_G',8,16)
port_T0= MemoryInterface(sys,'prot_T0',8,16)
port_T1= MemoryInterface(sys,'prot_T1',8,16)
port_T2= MemoryInterface(sys,'prot_T2',8,16)




if Show_Schematic == True:
    sch = py4hw.Schematic(sys)
    sch.draw()
 

#load instruction test to memory 
if Instruction_test == True:
    for memory_position in range(len(INSTRUCTION_SET_TEST_PROGRAM)):
        CPU.flash[memory_position] = INSTRUCTION_SET_TEST_PROGRAM[memory_position]



if Arduino_Code_Test == True: 
    ## loading hex file of arduino test code to memory 
    memory_position = 0
    with open('./Code_Test/main.hex','rb') as f:
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




