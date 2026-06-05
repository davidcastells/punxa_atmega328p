import py4hw
import punxa_atmega328p as punxa
from punxa_atmega328p.instruction_decode import ins_to_str
from punxa_atmega328p.instruction_decode import MEMORY_INSTRUCTIONS

from punxa_atmega328p.csr import *
from deprecated import deprecated

## *_IO = IN and OUT instruction address
## *_LS =  LD LDS ST STS instruction address

#0x0000 to 0x3FFF flash memory range 

#Start of Sram : 0x0100 | End of Sram : 0x08FF
#pointer registers
# R26 X-register Low Byte 
# R27 X-register High Byte
# R28 Y-register Low Byte
# R29 Y-register High Byte
# R30 Z-register Low Byte 
# R31 Z-register High Byte
 
# interupt wires to add: INT0, INT1, PCINT0, PCINT1, PCINT2, WDT, TIMER2 COMPA, TIMER2 COMPB, TIMER2 OVF, TIMER1 CAPT, TIMER1 COMPA, TIMER1 COMPB, TIMER1 OVF, TIMER0 COMPA, TIMER0 COMPB, TIMER0 OVF, SPI/STC , USART/RX , USART/UDRE , USART/TX , ADC , EE READY , ANALOG COMP, TWI, SPM READY.

SPL_REG =   0x5D 
SPH_REG =   0x5E
SREG_REG =  0x5F


class SingleCycleATmega328P(py4hw.Logic):
    def __init__(self,parent, name:str , ins_mem:MemoryInterface, memory:MemoryInterface, reset_address):
        #INT0,INT1,PCINT0,PCINT1,PCINT2,WDT,TIMER2_COMPA,TIMER2_COMPB,TIMER2_OVF,TIMER1_CAPT,TIMER1_COMPA,TIMER1_COMPB,TIMER1_OVF,TIMER0_COMPA,TIMER0_COMPB,TIMER0_OVF,SPI_STC,USART_RX,USART_UDRE,USART_TX,ADC,EE_READY,ANALOG_COMP,TWI,SPM_READY):
        super().__init__(parent,name)

        assert(ins_mem.read_data.getWidth() == 16)
        assert(memory.read_data.getWidth() == 8)
        
        self.ins_mem = self.addInterfaceSource('ins', ins_mem)
        self.mem = self.addInterfaceSource('data', memory)
        
        self.pc = reset_address # Reset address is a property of the processor. In Atmega328p it is stored in non-volatile memory and can be configured by JTAG
        
        #  0x3F00 ##bootloarder
        
        
        #self.reg = [0]*32  # REGS are stored in memory
        # self.ram = [0]*2048
        
        
        #self.stack_pointer  = 0x08FF ## value sould be known by using a register, I need to verify that it doesent go in to the negatives  
        self.next_cycle = False #varible to indicate that data is ready to read from ram/memeory
        self.ins = 0
        self.opp = 'NOP'
        self.FirstBoot = True #is this actuatly odable ?
        self.BOOTRST = 1
        self.databyteNb = 0
        
        # Registers
        self.SP = 0
        
        # Status flags
        self.Z = 0
        self.N = 0
        self.C = 0
        self.V = 0
        self.S = 0
        self.H = 0
        self.T = 0
        self.I = 0
        
        self.MCUCR = 0
        self.MCUCR_addr_IO = 0x35
        self.MCUCR_addr_LS = 0x55

        #Stack Pointer
        


        self.MCUSR = 0x02 # Power-on Reset  or it can be 0x02 External Reset
        self.MCUSR_addr_IO = 0x34
        self.MCUSR_addr_LS = 0x54

        #Warchdog Timer Configruation
        self.WDTCSR = 0
        self.WDTCSR_addr_LS = 0x60

        #SPMCSR - Store Program Memory Control and Status Register
        self.SPMCSR = 0 
        self.SPMCSR_addr_IO = 0x37
        self.SPMCSR_addr_LS = 0x57



        self.gotToGoFast = False

        self.insFiniteStateMachine = 'START'

        self.PAGE_SIZE_WORDS = 64
        
        self.temp_page_buffer = [0xFFFF] * self.PAGE_SIZE_WORDS     
        
        self.csr = {}
        self.csr[CSR_INSTRET] = 0
        self.csr[CSR_CYCLE] = 0
        
        
        self.co = self.run()

    
    def clock(self):
        next(self.co)
        
        self.csr[CSR_CYCLE] += 1
        
    def run(self):
        yield
        
        while (True):
            yield from self.fetchIns()
            # if (ins_to_str(self.ins) not in MEMORY_INSTRUCTIONS) and (self.gotToGoFast == 1):
            #     self.mem.read.prepare(0)
            #     self.mem.write.prepare(0)
    
            yield from self.execute()
        
            self.csr[CSR_INSTRET] += 1
            yield


    def getCSR(self, csr):
        # only assuming insret is implemented
        return self.csr[csr] 
        
    
    def writeByte(self, add, value):
        self.mem.write.prepare(1)
        self.mem.read.prepare(0) 
        self.mem.address.prepare(add)
        self.mem.write_data.prepare(value)
        yield
        self.mem.write.prepare(0) 
        
        while (self.mem.resp.get() == 0):
            # wait until response
            yield
            
        yield
    
    def readByte(self, add):
        self.mem.write.prepare(0)
        self.mem.read.prepare(1) 
        self.mem.address.prepare(add)
        yield
        self.mem.read.prepare(0) 
        
        while (self.mem.resp.get() == 0):
            # wait until response
            yield
            
        return self.mem.read_data.get()


    def readInsWord(self):
        self.ins_mem.address.prepare(self.pc)
        self.ins_mem.read.prepare(1)
        self.ins_mem.write.prepare(0)
        yield
        self.ins_mem.read.prepare(0)
        self.ins_mem.write.prepare(0)
        yield
        self.pc += 1
        return self.ins_mem.read_data.get()
        
        
        
    def fetchIns(self):
        print(f'{self.pc:04X} - ', end='')
        self.ins = yield from self.readInsWord()
        
        #print(f'FETCH INS: {self.pc:04X} -  {self.ins:04X}')
        

    def getFlagString(self):
        sZ = 'Z' if (self.Z) else ' '
        sC = 'C' if (self.C) else ' '
        sN = 'N' if (self.N) else ' '
        sV = 'V' if (self.V) else ' '
        sH = 'H' if (self.H) else ' '
        sS = 'S' if (self.S) else ' '
        
        return f'{sZ}{sC}{sN}{sV}{sH}{sS}'
        

    def execute(self):
        self.opp =  ins_to_str(self.ins)
        
        b3 = self.ins & 0b111
        
        Rd4 = ((self.ins>>4) & 0xF)
        Rd5 = ((self.ins>>4) & 0x1F)

        Rr5 = (((self.ins>>9) & 1) << 4) | (self.ins & 0xF)
        
        K7 = (self.ins>>3) & 0b1111111 
        K8 = ((self.ins>>8) & 0xF) << 4 | (self.ins & 0xF)
        
        A6 = ((((self.ins)>>9) & 0b11)<<4) | ((self.ins) & 0xF)  
        
        #print(f'{self.pc:02X} - {self.ins:04X}', self.opp)

        match self.opp: 
            case 'ADD':
                # ADD Rd, Rr -> 0000 11rd dddd rrrr
                Rr = Rr5
                Rd = Rd5
                
                vRr = yield from self.readByte(Rr)
                vRd = yield from self.readByte(Rd)
                
                res = vRd + vRr
                
                self.Z = 1 if (res == 0) else 0
                self.N = (res >> 7) 
                self.C = 1 if (res > 0xFF) else 0                
                self.H =  1 if (((vRd & 0x0F) + (vRr & 0x0F)) > 0x0F) else 0
                rd_sign = (vRd >> 7) & 1      # Bit 7 of Rd
                rr_sign = (vRr >> 7) & 1      # Bit 7 of Rr
                res_sign = (res >> 7) & 1     # Bit 7 of result
                self.V = 1 if ((rd_sign == rr_sign) and (rd_sign != res_sign)) else 0
                self.S = self.N ^ self.V
                
                yield from self.writeByte(Rd, res)
                
                print(f'ADD R{Rd}, R{Rr}\t\tR{Rd}={res:02X}\t{self.getFlagString()}')
                
                
            case 'ADC': # there may be a problem with this but I don't know what is the problem
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>4) & 0x1F)
                Rd7 = (self.reg[self.Rd]>>7)&0b1
                Rr7 = (self.reg[self.Rr]>>7)&0b1

                self.res =  (self.reg[self.Rd] + self.reg[self.Rr] + (self.SREG & 0b1)) &0xFF
                Rd3 = (self.reg[self.Rd]>>3)&0b1
                Rr3 = (self.reg[self.Rr]>>3)&0b1

                R7  = (self.res>>7)&0b1
                R3  = (self.res>>3)&0b1

                #H
                if ((Rd3 & Rr3)|(Rr3 & (1 - R3))|(Rd3 & (1 - R3))):
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)
                
                #self.SREG &= ~(1<<5) # This is a bipas 

                #C
                if (Rd7 & Rr7 )|( Rr7 & (not R7))|((not R7) & Rd7):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)

                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)

                #V
                V = ((Rd7 & Rr7 & (not R7)) | ((not Rd7) & (not Rr7) & R7))&0b1

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)

                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                self.reg[self.Rd] = self.res & 0xFF

                self.pc += 1
            case 'ADIW':
                raise Exception('not reviewed')
                self.K = (((self.ins>>6)&0b11)<<4)|(self.ins & 0xF)
                self.Rd = 24 + (((self.ins >> 4) & 0b11) * 2)
                self.res =  (self.reg[self.Rd+1]<<8|self.reg[self.Rd])  +  self.K

                Rdh7 = ((self.reg[self.Rd+1]>>7)&0b1)
                R15 = ((self.res>>15)&0b1)

                #C
                if (not R15) & Rdh7:
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)
                #Z
                N = (self.res == 0)
                if N == 1:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R15 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V
                V = (not Rdh7) & R15
                if V == 1 :
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if (N)^(V):
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                self.reg[self.Rd] =  self.res & 0xFF
                self.reg[self.Rd+1] =  (self.res>>8) & 0xFF

                self.pc += 1
            case 'SUB':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.res =  (self.reg[self.Rd] - self.reg[self.Rr]) & 0xFF


                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                Rr7= ((self.reg[self.Rr]&0xFF)>>7)&0b1
                R7 = ((self.res&0xFF)>>7)&0b1

                #C
                if ((not Rd7) & Rr7 )|( Rr7 & R7)|( R7 & (not Rd7)):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)
                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V
                V = ((Rd7 & (not Rr7) & (not R7)) | ((not Rd7) & Rr7 & R7))&0b1

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                #H
                Rd3= ((self.reg[self.Rd]&0xFF)>>3)&0b1
                Rr3= ((self.reg[self.Rr]&0xFF)>>3)&0b1
                R3 = ((self.res&0xFF)>>3)&0b1

                if ((not Rd3) & Rr3)|(Rr3 & R3)|(R3 & (not Rd3)):
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)

                self.reg[self.Rd] =  self.res & 0xFF

                self.pc += 1
            case 'SUBI':
                raise Exception('not reviewed')
                self.K =  ((self.ins>>4)&0xF0)|(self.ins&0xF)
                self.Rd = 16 + ((self.ins >> 4) & 0xF)
                self.res = self.reg[self.Rd] - self.K

                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                K7= ((self.K&0xFF)>>7)&0b1
                R7 = ((self.res&0xFF)>>7)&0b1

                #C
                if ((not Rd7) & K7 )|( K7 & R7)|( R7 & (not Rd7)):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)
                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V
                V = ((Rd7 & (not K7) & (not R7)) | ((not Rd7) & K7 & R7))&0b1

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                #H
                Rd3= ((self.reg[self.Rd]&0xFF)>>3)&0b1
                K3= ((self.K&0xFF)>>3)&0b1
                R3 = ((self.res&0xFF)>>3)&0b1

                if ((not Rd3) & K3)|(K3 & R3)|(R3 & (not Rd3)):
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)



                self.reg[self.Rd] =  self.res & 0xFF

                self.pc += 1
            case 'SBC':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.res =  self.reg[self.Rd] - self.reg[self.Rr] - (self.SREG & 0b1)

                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                Rr7= ((self.reg[self.Rr]&0xFF)>>7)&0b1
                R7 = ((self.res&0xFF)>>7)&0b1

                #C
                if ((not Rd7) & Rr7 )|( Rr7 & R7)|( R7 & (not Rd7)):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)
                #Z 
                current_Z = (self.SREG >> 1) & 0b1
                if (self.res&0xFF == 0) and current_Z == 1:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V
                V = ((Rd7 & (not Rr7) & (not R7)) | ((not Rd7) & Rr7 & R7))&0b1

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                #H
                Rd3= ((self.reg[self.Rd]&0xFF)>>3)&0b1
                Rr3= ((self.reg[self.Rr]&0xFF)>>3)&0b1
                R3 = ((self.res&0xFF)>>3)&0b1

                if ((not Rd3) & Rr3)|(Rr3 & R3)|(R3 & (not Rd3)):
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)

                self.reg[self.Rd] =  self.res & 0xFF
                self.pc += 1
            case 'SBCI':
                raise Exception('not reviewed')
                self.K =  ((self.ins>>4)&0xF0)|(self.ins&0xF)
                self.Rd = ((self.ins>>4) & 0xF) + 16
                self.res =  self.reg[self.Rd] - self.K - (self.SREG & 0b1)

                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                K7= ((self.K&0xFF)>>7)&0b1
                R7 = ((self.res&0xFF)>>7)&0b1

                #C
                if ((not Rd7) & K7 )|( K7 & R7)|( R7 & (not Rd7)):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)
                #Z 
                current_Z = (self.SREG >> 1) & 0b1
                if (self.res&0xFF == 0) and current_Z == 1:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V
                V = ((Rd7 & (not K7) & (not R7)) | ((not Rd7) & K7 & R7))&0b1

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                #H
                Rd3= ((self.reg[self.Rd]&0xFF)>>3)&0b1
                K3= ((self.K&0xFF)>>3)&0b1
                R3 = ((self.res&0xFF)>>3)&0b1

                if ((not Rd3) & K3)|(K3 & R3)|(R3 & (not Rd3)):
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)

                self.reg[self.Rd] =  self.res & 0xFF
                self.pc += 1
            case 'SBIW':
                raise Exception('not reviewed')
                self.K = (((self.ins>>6)&0b11)<<4)|(self.ins & 0xF)
                self.Rd = 24 + (((self.ins>>4)&0b11) * 2)
                self.res =  (self.reg[self.Rd+1]<<8|self.reg[self.Rd]) -  self.K

                Rdh7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                R15 = ((self.res&0xFF)>>7)&0b1

                #C
                if R15 & (not Rdh7):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)
                #Z 
                if (self.res&0xFF == 0):
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R15 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V

                V = (not R15) & Rdh7 
                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R15:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)


                self.reg[self.Rd] =  self.res&0xFF
                self.reg[self.Rd+1] = (self.res>>8)&0xFF 

                self.pc += 1
            case 'AND':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.res =  self.reg[self.Rd] & self.reg[self.Rr]


                R7 =  ((self.res&0xFF)>>7)&0b1
                #Z
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                N = (R7 == 1)
                if N == 1 : 
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)

                self.SREG &= ~(1<<3) #flag V to 0

                #S 
                if N == 1:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)  

                self.reg[self.Rd] =  self.res

                self.pc += 1
            case 'ANDI':
                raise Exception('not reviewed')
                self.K =  ((self.ins>>4)&0xF0)|(self.ins&0xF)
                self.Rd = ((self.ins>>4) & 0xF) + 16
                self.res =  self.reg[self.Rd] & self.K 

                R7 =  ((self.res&0xFF)>>7)&0b1
                #Z
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                N = (R7 == 1)
                if N == 1 : 
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)

                self.SREG &= ~(1<<3) #flag V to 0

                #S 
                if N == 1:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)  


                self.reg[self.Rd] =  self.res
                self.pc += 1
            case 'OR':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.res =  self.reg[self.Rd] | self.reg[self.Rr]

                R7 =  ((self.res&0xFF)>>7)&0b1
                #Z
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                N = (R7 == 1)
                if N == 1 : 
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)

                self.SREG &= ~(1<<3) #flag V to 0

                #S 
                if N == 1:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)  



                self.reg[self.Rd] =  self.res

                self.pc += 1
            case 'ORI':
                raise Exception('not reviewed')
                self.K =  ((self.ins>>4)&0xF0)|(self.ins&0xF)
                self.Rd = ((self.ins>>4) & 0xF) + 16
                self.res =  self.reg[self.Rd] | self.K 

                R7 =  ((self.res&0xFF)>>7)&0b1
                #Z
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                N = (R7 == 1)
                if N == 1 : 
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)

                self.SREG &= ~(1<<3) #flag V to 0

                #S 
                if N == 1:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)  

                self.reg[self.Rd] =  self.res
                self.pc += 1
            case 'EOR':
                Rr = ((self.ins>>8) & 0b1) <<4 | (self.ins & 0xF)
                Rd = ((self.ins>>9) & 0b1) <<4 | ((self.ins>>4) & 0xF)
                vRr = yield from self.readByte(Rr)
                vRd = yield from self.readByte(Rd)
                
                res =  vRd ^ vRr

                self.Z = 1 if (res == 0) else 0
                self.N = (res >> 7) 
                self.C = 0
                self.V = 0
                self.S = self.N
                self.H = 0
                
                yield from self.writeByte(Rd, res)
                
                print(f'EOR R{Rd}, R{Rr}\t\tR{Rd} = {res:02X}\t{self.getFlagString()}')
                
            case 'COM':
                raise Exception('not reviewed')
                self.Rd = ((self.ins>>4) & 0x1F)
                self.res = 0xFF - self.reg[self.Rd] 

                R7 =  ((self.res&0xFF)>>7)&0b1
                self.SREG |= (1<<0) #flag C to 1
                #Z
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                N = (R7 == 1)
                if N == 1 : 
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)

                self.SREG &= ~(1<<3) #flag V to 0

                #S 
                if N == 1:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)  

                self.reg[self.Rd] =  self.res

                self.pc += 1
            case 'NEG':
                raise Exception('not reviewed')
                self.Rd = ((self.ins>>4) & 0x1F)
                self.res = (0x00 - self.reg[self.Rd]) & 0xFF 

                R7 = ((self.res&0xFF)>>7)&0b1
                #C
                if self.res != 0:
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)
                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                
                #V
                V = (self.res == 0x80)
                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                #H
                Rd3= ((self.reg[self.Rd])>>3)&0b1
                R3 = (self.res>>3)&0b1
                if (1- Rd3) | R3 :
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)

                self.reg[self.Rd] =  self.res
                self.pc += 1
            case 'SBR':
                raise Exception('not reviewed')
                self.K =  ((self.ins>>4)&0xF0)|(self.ins&0xF)
                self.Rd = ((self.ins>>4) & 0xF) + 16
                self.res =  self.reg[self.Rd] | self.K 

                R7 =  ((self.res&0xFF)>>7)&0b1
                #Z
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                N = (R7 == 1)
                if N == 1 : 
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)

                self.SREG &= ~(1<<3) #flag V to 0

                #S 
                if N == 1:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)  

                self.reg[self.Rd] =  self.res
                self.pc += 1
                self.pc += 1
                
            case 'CBR':
                raise Exception('not reviewed')
                self.K =  ((self.ins>>4)&0xF0)|(self.ins&0xF)
                self.Rd = ((self.ins>>4) & 0xF)
                self.res =  self.reg[self.Rd] & self.K 

                self.testZ(self.res)
                self.testN(self.res)
#                self.SREG &= ~(1<<V) # flag V to 0
                self.testS()     

                self.reg[self.Rd] =  self.res 
                self.pc += 1
                
            case 'INC':
                # INC Rd --> 1001 010d dddd 0011.
                Rd = Rd5
                vRd = yield from self.readByte(Rd)
                
                res = vRd + 1
                
                self.Z = 1 if (res == 0) else 0
                self.N = (res >> 7) 
                self.V = 1 if vRd == 0x7F else 0
                self.S = self.N ^ self.V
                
                yield from self.writeByte(Rd, res & 0xFF)

                print(f'INC\t\t\t\t{self.getFlagString()}')
                
            case 'DEC':
                raise Exception('not reviewed')
                self.Rd = ((self.ins>>4) & 0x1F)
                self.res = (self.reg[self.Rd] - 1) & 0xFF

                R7 =  ((self.res&0xFF)>>7)&0b1
                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                
                #V
                V = (self.Rd == 0x80)
                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)

                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                self.reg[self.Rd] =  self.res
                self.pc += 1
            case 'SER':
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0b1111 + 16
                self.reg[self.Rd] = 0xFF
        

                self.pc +=1 
            case 'MUL':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.res =  self.reg[self.Rd] * self.reg[self.Rr]

                R15 = (self.res>>15) & 0b1

                if R15 == 1:
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0) 

                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                self.reg[1] = (self.res>>8) &0xFF
                self.reg[0] = self.res & 0xFF

                self.pc += 1
            case 'MULS': 
                raise Exception('not reviewed')
                self.Rr = (self.ins & 0xF) + 16
                self.Rd = ((self.ins>>4) & 0xF) + 16

                val_Rd = self.reg[self.Rd] & 0xFF
                val_Rr = self.reg[self.Rr] & 0xFF

                if val_Rd >= 128:
                    val_Rd -=256
                if val_Rr >= 128:
                    val_Rr -=256

                self.res =  (val_Rd * val_Rr) & 0xFFFF

                R15 = (self.res>>15) & 0b1

                if R15 == 1:
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0) 

                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                self.reg[1]= (self.res>>8) & 0xFF
                self.reg[0]= self.res & 0xFF

                self.pc += 1
            case 'MULSU':
                raise Exception('not reviewed')
                self.Rr = (self.ins & 0b111) + 16
                self.Rd = ((self.ins>>4) & 0b111) + 16

                val_Rd = self.reg[self.Rd] & 0xFF
                val_Rr = self.reg[self.Rr] & 0xFF

                if val_Rd >= 128:
                    val_Rd -=256
                if val_Rr >= 128:
                    val_Rr -=256

                self.res =  (val_Rd * val_Rr) & 0xFFFF

                R15 = (self.res>>15) & 0b1

                if R15 == 1:
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0) 

                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                self.reg[1]= self.res>>8 & 0xFF
                self.reg[0]= self.res & 0xFF

                self.pc += 1
            case 'FMUL':
                raise Exception('not reviewed')
                self.Rr = (self.ins & 0b111) + 16
                self.Rd = ((self.ins>>4) & 0b111) + 16
                self.res =  (self.reg[self.Rd]&0xFF) * (self.reg[self.Rr]&0xFF)

                R15 = (self.res>>15) & 0b1

                if R15 == 1:
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0) 

                self.res = (self.res <<1) &0xFFFF

                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                self.reg[1]= self.res>>8 & 0xFF
                self.reg[0]= self.res & 0xFF

                self.pc += 1
            case 'FMULS': 
                raise Exception('not reviewed')
                self.Rr = (self.ins & 0b111) + 16
                self.Rd = ((self.ins>>4) & 0b111) + 16
                val_Rd = self.reg[self.Rd] & 0xFF
                val_Rr = self.reg[self.Rr] & 0xFF

                if val_Rd >= 128:
                    val_Rd -=256
                if val_Rr >= 128:
                    val_Rr -=256

                self.res =  (val_Rd * val_Rr) & 0xFFFF

                R15 = (self.res>>15) & 0b1

                if R15 == 1:
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0) 

                self.res = (self.res <<1) &0xFFFF

                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                self.reg[1]= (self.res>>8) & 0xFF
                self.reg[0]= self.res & 0xFF

                self.pc += 1
            case 'FMULSU':
                raise Exception('not reviewed')
                self.Rr = (self.ins & 0b111) + 16 
                self.Rd = ((self.ins>>4) & 0b111) + 16

                val_Rd = self.reg[self.Rd] & 0xFF
                val_Rr = self.reg[self.Rr] & 0xFF

                if val_Rd >= 128:
                    val_Rd -=256
                if val_Rr >= 128:
                    val_Rr -=256

                self.res =  (val_Rd * val_Rr) & 0xFFFF

                R15 = (self.res>>15) & 0b1

                if R15 == 1:
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0) 

                self.res = (self.res <<1) &0xFFFF

                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                self.reg[1]= (self.res>>8) & 0xFF
                self.reg[0]= self.res & 0xFF

                self.pc += 1
            case 'RJMP':
                off = self.ins & 0xFFF
                soff = py4hw.IntegerHelper.c2_to_signed(off, 12)
                self.pc += soff
                print(f'RJMP {soff}')
                
            case 'IJMP':
                raise Exception('not reviewed')
                self.pc  = + (self.reg[30] | self.reg[31]<<8)
            case 'JMP':
                raise Exception('not reviewed')
                self.K = (((self.ins>>4)&0x1F)<<17)|(self.ins&0b1<<16)|self.flash[self.pc+1] 
                self.pc = self.K
            case 'RCALL':
                K = py4hw.IntegerHelper.c2_to_signed(self.ins & 0xFFF, 12)
                
                ra = self.pc
                
                self.SP -= 1
                yield from self.writeByte(self.SP, ra >> 8)
                self.SP -= 1
                yield from self.writeByte(self.SP, ra & 0xFF)
                
                self.pc += K                    
                
                print(f'RCALL {K:03X}\t\t[{self.SP+1:04X}]={ra>>8:02X} [{self.SP:04X}]={ra & 0xFF}')
                    
            case 'ICALL':
                raise Exception('not reviewed')
                self.A = (self.reg[30]&0xFF) | ((self.reg[31]&0xFF)<<8) 
                SP = ((self.SPH&0xFF)<<8) | (self.SPL&0xFF)


                PC_to_store = (self.pc+2)&0xFFFF


                PClwo = PC_to_store&0xFF
                PChigh = (PC_to_store>>8)&0xFF


                match self.insFiniteStateMachine:

                    case 'START':
                        self.mem.write.prepare(1)
                        self.mem.read.prepare(0)

                        self.mem.address.prepare(SP)
                        self.mem.write_data.prepare(PClwo)

                        if(self.mem.resp.get() == 1):
                            self.insFiniteStateMachine = 'STEP1'

                    case 'STEP1':

                        self.mem.write.prepare(0)
                        self.mem.read.prepare(0)
                    
                        self.insFiniteStateMachine = 'STEP2'

                    case 'STEP2':

                        self.mem.write.prepare(1)
                        self.mem.read.prepare(0)
                    
                        self.mem.address.prepare(SP-1)
                        self.mem.write_data.prepare(PChigh)

                        if(self.mem.resp.get() == 1):
                            self.insFiniteStateMachine = 'STEP3'

                    case 'STEP3':

                        self.mem.write.prepare(0)
                        self.mem.read.prepare(0)
                            
                        self.insFiniteStateMachine = 'START'

                        SP = SP - 2
                        self.SPH = (SP>>8)&0xFF
                        self.SPL = SP&0xFF

                        self.pc = self.A  
            case 'CALL':
                raise Exception('not reviewed')
                self.K = (((self.ins>>4)&0x1F)<<17)|((self.ins&0b1)<<16)|self.flash[self.pc+1] 
                SP = ((self.SPH&0xFF)<<8) | (self.SPL&0xFF)


                PC_to_store = (self.pc+2)&0xFFFF


                PClwo = PC_to_store&0xFF
                PChigh = (PC_to_store>>8)&0xFF


                match self.insFiniteStateMachine:

                    case 'START':
                        self.mem.write.prepare(1)
                        self.mem.read.prepare(0)

                        self.mem.address.prepare(SP)
                        self.mem.write_data.prepare(PClwo)

                        if(self.mem.resp.get() == 1):
                            self.insFiniteStateMachine = 'STEP1'

                    case 'STEP1':

                        self.mem.write.prepare(0)
                        self.mem.read.prepare(0)
                    
                        self.insFiniteStateMachine = 'STEP2'

                    case 'STEP2':

                        self.mem.write.prepare(1)
                        self.mem.read.prepare(0)
                    
                        self.mem.address.prepare(SP-1)
                        self.mem.write_data.prepare(PChigh)

                        if(self.mem.resp.get() == 1):
                            self.insFiniteStateMachine = 'STEP3'

                    case 'STEP3':

                        self.mem.write.prepare(0)
                        self.mem.read.prepare(0)
                            
                        self.insFiniteStateMachine = 'START'

                        SP = SP - 2
                        self.SPH = (SP>>8)&0xFF
                        self.SPL = SP&0xFF

                        self.pc = self.K
                        
            case 'RET':
                retl = yield from self.readByte(self.SP)
                self.SP += 1
                reth = yield from self.readByte(self.SP)
                self.SP += 1
                
                self.pc = (reth << 8) | retl
                print(f'RET\t\t\t\t[{SPH_REG:04X}]={(self.SP>>8):02X} [{SPL_REG:04X}]={(self.SP & 0xFF):02X}')
                
            case 'RETI':## return from interrupt 
                raise Exception('not reviewed')
                match self.insFiniteStateMachine:
                    
                    case 'START':
                        SP = (((self.SPH&0xFF)<<8) | (self.SPL&0xFF))+1

                        self.mem.address.prepare(SP)
                        self.mem.write.prepare(0)
                        self.mem.read.prepare(1)

                        if self.mem.read.get() == 1:
                            self.insFiniteStateMachine = 'STEP1'
                            
                    case 'STEP1':
                        self.high = self.mem.read_data.get()
                        self.mem.write.prepare(0)
                        self.mem.read.prepare(0)
                        self.insFiniteStateMachine = 'STEP2'

                    case 'STEP2':
                        SP = (((self.SPH&0xFF)<<8) | (self.SPL&0xFF))+2
                        self.mem.address.prepare(SP)
                        self.mem.write.prepare(0)
                        self.mem.read.prepare(1)


                        if self.mem.read.get() == 1 :
                            self.insFiniteStateMachine = 'STEP3'

                    case 'STEP3': 
                        self.low = self.mem.read_data.get()
                        SP = (((self.SPH&0xFF)<<8) | (self.SPL&0xFF))+2

                        self.SPH = (SP>>8)&0x00FF
                        self.SPL = SP&0x00FF
                        self.pc  = ((self.high&0xFF)<<8) | (self.low&0xFF)
                        self.insFiniteStateMachine = 'START'

            case 'CPSE':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>8)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>9)&0b1)<<4|((self.ins>>4) & 0xF)


                if self.reg[self.Rr] == self.reg[self.Rd]:
                    next_ins = ins_to_str(self.flash[self.pc])
                    if(next_ins == 'CALL' or next_ins == 'JMP' or next_ins == 'STS' or next_ins == 'LDS'):
                        self.pc += 3 ##skip 2 word instruction
                    else:
                        self.pc += 2## skip 1 word instruction 
                else:
                    self.pc += 1
            case 'CP':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.res =  self.reg[self.Rd] - self.reg[self.Rr] 

                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                Rr7= ((self.reg[self.Rr]&0xFF)>>7)&0b1
                R7 = ((self.res&0xFF)>>7)&0b1
                #C
                if ((not Rd7) & Rr7 )|( Rr7 & R7)|(R7 & (not Rd7)):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)

                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)

                #V
                V = ((Rd7 & (not Rr7) & (not R7)) | ((not Rd7) & Rr7 & R7))&0b1

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)

                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                #H
                Rd3= ((self.reg[self.Rd]&0xFF)>>3)&0b1
                Rr3= ((self.reg[self.Rr]&0xFF)>>3)&0b1
                R3 = ((self.res&0xFF)>>3)&0b1
                if ((not Rd3) & Rr3)|(Rr3 & (not R3))|(R3 & (not Rd3)):
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)

                self.pc += 1
            case 'CPC':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.res =  (self.reg[self.Rd] - self.reg[self.Rr] - (self.SREG & 0b1)) & 0xFF

                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                Rr7= ((self.reg[self.Rr]&0xFF)>>7)&0b1
                R7 = ((self.res&0xFF)>>7)&0b1
                #C
                if ((not Rd7) & Rr7 )|( Rr7 & R7)|(R7 & (not Rd7)):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)

                #Z 
                if (self.res == 0) or (((self.SREG>>1)&0b1)) :
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)

                #V
                V = ((Rd7 & (not Rr7) & (not R7)) | ((not Rd7) & Rr7 & R7))&0b1

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)

                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                #H
                Rd3= ((self.reg[self.Rd]&0xFF)>>3)&0b1
                Rr3= ((self.reg[self.Rr]&0xFF)>>3)&0b1
                R3 = ((self.res&0xFF)>>3)&0b1
                if ((not Rd3) & Rr3)|(Rr3 & R3 )|(R3 & (not Rd3)):
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)

                self.pc += 1
            
            case 'CPI':
                # Compare with immediate
                K = (self.ins&0xF) | (((self.ins>>8)&0xF)<<4)
                Rd = (self.ins>>4) & 0xF + 16
                
                vRd = yield from self.readByte(Rd)
                
                res = (vRd - K) 

                self.Z = 1 if (res == 0) else 0
                self.N = (res & 0x80) >> 7
                self.C = 1 if (res >= 0) else 0
                self.H =  1 if ((vRd & 0x0F) - (K & 0x0F)) < 0 else 0
                rd_sign = (vRd >> 7) & 1      # Bit 7 of Rd
                rr_sign = (K >> 7) & 1      # Bit 7 of Rr
                res_sign = (res >> 7) & 1     # Bit 7 of result
                self.V = 1 if ((rd_sign == rr_sign) and (rd_sign != res_sign)) else 0
                self.S = self.N ^ self.V
                
                print(f'CPI R{Rd}, {K:02X}\t\t{self.getFlagString()}')
                
            case 'SBRC':
                raise Exception('not reviewed')
                b = self.ins&0b111
                self.A = (self.ins>>4)&0b11111
                if (self.reg[self.A]>>b)&1 == 0:
                    next_ins = ins_to_str(self.flash[self.pc])
                    if(next_ins == 'CALL' or next_ins == 'JMP' or next_ins == 'STS' or next_ins == 'LDS'):
                        self.pc += 3 ##skip 2 word instruction
                    else:
                        self.pc += 2## skip 1 word instruction 
                else:
                    self.pc += 1
            case 'SBRS':
                # SBRS Rd, b -> 1111 111r rrrr 0bbb
                b = b3      # bit position
                R = Rd5     # Register
                
                v = yield from self.readByte(R)
                cond = (((v >> b) & 1) == 1)
                if cond:
                    self.pc += 1
                
                print(f'SBRS R{R}, {b}\t\t{v:08b} & {1 << b:08b} = {cond}')
                
            case 'SBIC':
                raise Exception('not reviewed')
                b = self.ins&0b111
                A = (self.ins>>3)&0b11111
                ## implement I/O read to test if 0

                self.pc += 1
            case 'SBIS':
                raise Exception('not reviewed')
                b = self.ins&0b111
                A = (self.ins>>3)&0b11111
                ## implement I/O read to test if 1

                self.pc += 1
            case 'BRBS':
                raise Exception('not reviewed')
                self.K =  (self.ins>>3)&0b1111111 
                S =  self.ins&0b111

                if (self.K & 0x40):
                    self.K = self.K - 128
                
                if(self.SREG>>S)&1 == 1:
                    self.pc += + self.K +1
                else:
                    self.pc += 1 
            case 'BRBC':
                # BRBC s, k -> 1111 01kk kkkk ksss
                K = K7
                S = b3

                if (K & 0x40):
                    K = K - 128

                SREG = (self.I << 7) | (self.T<<6) | (self.H<<5) | (self.S<<4) | (self.V<<3) | (self.N<<2) | (self.Z<<1) | self.C 
                sSREG = 'ITHSVNZC'[::-1]
                
                cond = ((SREG >> S) == 0)
                
                if (cond):
                    self.pc += K 
                
                print(f'BRBC {S}, {K:02X}\t\t{sSREG[S]}={cond}')
                    
            case 'SBI': ## implement write in io 
                raise Exception('not reviewed')
                b = (n3 & 0b111)
                add = ((n >>3) & 0x1F) + 0x20

                v = yield from self.readByte(add)
                v = v | (1 << b)
                yield from self.writeByte(add, v)
                
                print(f'SBI R{Rd}, {K}\t\tR{Rd}={K:02X}')
                
                self.pc += 1
            case 'CBI': ## implement write in io 
                raise Exception('not reviewed')

                self.pc += 1

            case 'LSL': 
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.res = (self.reg[self.Rd] + self.reg[self.Rr]) &0xFF

                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                Rr7= ((self.reg[self.Rr]&0xFF)>>7)&0b1
                R7 = ((self.res&0xFF)>>7)&0b1
                #C
                if (Rd7 & Rr7 )|( Rr7 & (not R7))|((not R7) & Rd7):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)
                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V
                V = ((Rd7 & Rr7 & (not R7)) | ((not Rd7) & (not Rr7) & R7))&0b1

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                #H
                Rd3= ((self.reg[self.Rd]&0xFF)>>3)&0b1
                Rr3= ((self.reg[self.Rr]&0xFF)>>3)&0b1
                R3 = ((self.res&0xFF)>>3)&0b1
                if (Rd3 & Rr3)|(Rr3 & (not R3))|((not R3) & Rd3):
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)

                
                self.reg[self.Rd] =  self.res

                self.pc += 1
            case 'LSR':
                raise Exception('not reviewed')
                self.Rd =  (self.ins>>4)&0x1F
                
                #C 
                C = self.reg[self.Rd] & 0b1

                if C == 1:
                    self.SREG |= (1 << 0)
                else:
                    self.SREG &= ~(1 << 0)

                self.res = (self.reg[self.Rd]>>1)&0xFF
                
                #Z
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)

                self.SREG &= ~(1<<2) # N is set to 0

                #V
                V = ((self.SREG&0b1)^0)
                if V == 1 :
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                
                #S
                if V == 1:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)


                self.reg[self.Rd] = self.res
                self.pc += 1
            case 'ROL':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.res =  (self.reg[self.Rd] + self.reg[self.Rr] + (self.SREG & 0b1)) &0xFF

                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                Rr7= ((self.reg[self.Rr]&0xFF)>>7)&0b1
                R7 = ((self.res&0xFF)>>7)&0b1
                #C
                if (Rd7 & Rr7 )|( Rr7 & (not R7))|((not R7) & Rd7):
                    self.SREG |= (1<<0)
                else:
                    self.SREG &= ~(1<<0)
                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V
                V = ((Rd7 & Rr7 & (not R7)) | ((not Rd7) & (not Rr7) & R7))&0b1

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                #H
                Rd3= ((self.reg[self.Rd]&0xFF)>>3)&0b1
                Rr3= ((self.reg[self.Rr]&0xFF)>>3)&0b1
                R3 = ((self.res&0xFF)>>3)&0b1
                if (Rd3 & Rr3)|(Rr3 & (not R3))|((not R3) & Rd3):
                    self.SREG |= (1<<5)
                else:
                    self.SREG &= ~(1<<5)

                self.reg[self.Rd] =  self.res

                self.pc += 1
            case 'ROR':
                raise Exception('not reviewed')
                self.Rd =  (self.ins>>4)&0x1F

                #C 
                C = self.reg[self.Rd] & 0b1

                self.res = (self.reg[self.Rd]>>1 & 0xFF) | (self.SREG&0b1)<<7

                if C == 1:
                    self.SREG |= (1 << 0)
                else:
                    self.SREG &= ~(1 << 0)

                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                R7 = ((self.res&0xFF)>>7)&0b1

                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V
                V = R7^C

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                self.reg[self.Rd] = self.res & 0xFF

                self.pc += 1
            case 'ASR':
                raise Exception('not reviewed')
                self.Rd =  (self.ins>>4)&0x1F

                #C 
                C = self.reg[self.Rd] & 0b1
                if C == 1:
                    self.SREG |= (1 << 0)
                else:
                    self.SREG &= ~(1 << 0)

                Rd7= ((self.reg[self.Rd]&0xFF)>>7)&0b1
                
                self.res = (self.reg[self.Rd]>>1 & 0xFF) | (Rd7)<<7

                R7 = ((self.res&0xFF)>>7)&0b1
                #Z 
                if self.res == 0:
                    self.SREG |= (1<<1)
                else:
                    self.SREG &= ~(1<<1)
                #N
                if R7 == 1:
                    self.SREG |= (1<<2)
                else:
                    self.SREG &= ~(1<<2)
                #V
                V = R7^C

                if V == 1:
                    self.SREG |= (1<<3)
                else:
                    self.SREG &= ~(1<<3)
                #S
                if V^R7:
                    self.SREG |= (1<<4)
                else:
                    self.SREG &= ~(1<<4)

                self.reg[self.Rd] = self.res & 0xFF

                self.pc += 1
            case 'SWAP':
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.reg[self.Rd]= ((self.reg[self.Rd]&0xF)<<4) | ((self.reg[self.Rd]&0xF0)>>4)

                self.pc += 1
            case 'BSET':
                raise Exception('not reviewed')
                s = (self.ins>>4)&0b111
                self.SREG |=(1<<s) 

                self.pc += 1
            case 'BCLR':
                raise Exception('not reviewed')
                s = (self.ins>>4)&0b111
                self.SREG &= ~(1<<s) 

                self.pc += 1
            case 'BST':
                raise Exception('not reviewed')
                b = self.ins&0b111
                self.Rd = (self.ins>>4)&0x1F
                bit = (self.reg[self.Rd]>>b)&1

                if bit:
                    self.SREG |= (1<<6)
                else:
                    self.SREG &= ~(1<<6)
 
                self.pc += 1
            case 'BLD':
                raise Exception('not reviewed')
                b = self.ins&0b111
                self.Rd = (self.ins>>4)&0x1F
                self.reg[self.Rd] &= ~(0b1<<b)
                self.reg[self.Rd] |= ((self.SREG>>6)&1)<<b

                self.pc += 1


            case 'MOV':
                raise Exception('not reviewed')
                self.Rr = ((self.ins>>9)&0b1)<<4|(self.ins & 0xF)
                self.Rd = ((self.ins>>8)&0b1)<<4|((self.ins>>4) & 0xF)
                self.reg[self.Rd] =  self.reg[self.Rr]

                self.pc += 1
            case 'MOVW':
                raise Exception('not reviewed')
                self.Rr = (self.ins & 0xF) << 1
                self.Rd = ((self.ins>>4) & 0xF) << 1

                self.reg[self.Rd+1] = self.reg[self.Rr+1]
                self.reg[self.Rd] =  self.reg[self.Rr]

                self.pc += 1
            case 'LDI':
                # LDI Rd, K -> 1110 KKKK dddd KKKK
                Rd = Rd4+16                      
                K = K8
                yield from self.writeByte(Rd, K)
                
                print(f'LDI R{Rd}, {K:02X}\t\tR{Rd}={K:02X}')
                
            case 'LDX': #X
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.A  = (self.reg[27]<<8)|(self.reg[26]&0xFF) #X address

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1
                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.instype.prepare(0)

                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0) 

                    self.pc += 1
                    self.databyteNb = 0
            case 'LDX+': #X+
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.A = self.reg[26]|(self.reg[27]<<8)

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1

                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0) 
                    self.A += 1 ##incrementing X
                    self.reg[26] = self.A&0xFF 
                    self.reg[27] = (self.A>>8)&0xFF

                    self.mem.instype.prepare(0)

                    self.pc += 1
                    self.databyteNb = 0
            case 'LD-X': #-X
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.A = (self.reg[27]<<8)|(self.reg[26]&0xFF)

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.A -= 1 ##decrementing X
                    self.reg[26] = self.A&0xFF 
                    self.reg[27] = (self.A>>8)&0xFF

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1

                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.instype.prepare(0)

                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0) 

                    self.pc += 1
                    self.databyteNb = 0
            case 'LDY': #Y
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0b11111
                self.A = self.reg[28]|(self.reg[29]<<8)

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1
                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.instype.prepare(0)

                    self.pc += 1
                    self.databyteNb = 0
            case 'LDY+': #Y+
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0b11111
                self.A = (self.reg[28]&0xFF)|(self.reg[29]<<8)

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1

                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0) 

                    self.mem.instype.prepare(0)

                    self.A = (self.A + 1) & 0xFFFF ##incrementing Y
                    self.reg[28] = self.A&0xFF 
                    self.reg[29] = (self.A>>8)&0xFF

                    self.pc += 1
                    self.databyteNb = 0
            case 'LD-Y': #-Y
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.A = (self.reg[29]<<8)|self.reg[28]

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.A -= 1 ##decrementing Y
                    self.reg[28] = self.A&0xFF 
                    self.reg[29] = (self.A>>8)&0xFF

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1
                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.instype.prepare(0)

                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0) 

                    self.pc += 1
                    self.databyteNb = 0
            case 'LDDY':#Y+q
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.q = (self.ins&0b111)|(((self.ins>>10)&0b11)<<3)|(((self.ins>>13)&0b1)<<5)
                self.A = (((self.reg[28]&0xFF)|((self.reg[29]&0xFF)<<8))+self.q) & 0xFFFF # Y address
                
                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1

                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.instype.prepare(0)

                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0) 

                    self.pc += 1
                    self.databyteNb = 0
            case 'LDZ':#Z
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.A = (self.reg[30]&0xFF)|(self.reg[31]<<8) # A but it is a Z memory address

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1
                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.instype.prepare(0)

                    self.pc += 1
                    self.databyteNb = 0
            case 'LDZ+':#Z+
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.A = self.reg[30]|(self.reg[31]<<8)

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1
                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0) 
                    self.A += 1 ##incrementing Y
                    self.reg[30] = self.A&0xFF 
                    self.reg[31] = (self.A>>8)&0xFF

                    self.mem.instype.prepare(0)

                    self.pc += 1
                    self.databyteNb = 0
            case 'LD-Z':#–Z
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.A = (self.reg[30]&0xFF)|(self.reg[31]<<8)

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.A -= 1 ##decrementing Y
                    self.reg[30] = self.A&0xFF 
                    self.reg[31] = (self.A>>8)&0xFF

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1
                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.instype.prepare(0)

                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0) 

                    self.pc += 1
                    self.databyteNb = 0
            case 'LDDZ':#Z+q  verify this implementation
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0b11111
                self.q = (self.ins&0b111)|(((self.ins>>10)&0b11)<<3)|(((self.ins>>13)&0b1)<<5)
                self.A = ((self.reg[30]&0xFF)|((self.reg[31]&0xFF)<<8))+self.q # Y address
                

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1
                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.instype.prepare(0)

                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0)

                    self.pc += 1
                    self.databyteNb = 0
            case 'LDS':
                # Load direct from sram
                Rd = (self.ins>>4) & 0x1F
                add = yield from self.readInsWord()

                v = yield from self.readByte(add)
                yield from self.writeByte(Rd, v)
                
                print(f'LDS R{Rd}, {add:04X}\tR{Rd}={v:02X}')
                
            case 'STX':#X
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.A = (self.reg[26]&0xFF)|((self.reg[27]&0xFF)<<8) #X adress

                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])

                    self.databyteNb = 1
                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.mem.instype.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0
            case 'STX+':#X+
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.A = self.reg[26]|(self.reg[27]<<8) #X addres 

                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])
                    
                    self.databyteNb = 1
                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.mem.instype.prepare(0)

                    self.A += 1 ##incrementing X
                    self.reg[26] = self.A&0xFF 
                    self.reg[27] = (self.A>>8)&0xFF

                    self.pc += 1 
                    self.databyteNb = 0
            case 'ST-X':#–X
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.A = self.reg[26]|(self.reg[27]<<8) #X address


                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.A -= 1 ##decrementing X
                    self.reg[26] = self.A&0xFF 
                    self.reg[27] = (self.A>>8)&0xFF

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])
                    
                    self.databyteNb = 1
                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.mem.instype.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0
            case 'STY':#Y
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.A = self.reg[28]|(self.reg[29]<<8) #Y address


                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])
                    
                    self.databyteNb = 1
                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.mem.instype.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0
            case 'STY+':#Y+
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.A = self.reg[28]|(self.reg[29]<<8) #Y address

                if self.mem.resp.get() == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])

                    self.databyteNb = 1
                    
                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.mem.instype.prepare(0)

                    self.A += 1 ##incrementing Y
                    self.reg[28] = self.A&0xFF 
                    self.reg[29] = (self.A>>8)&0xFF

                    self.pc += 1 
                    self.databyteNb = 0
            case 'ST-Y':#–Y
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.A = self.reg[28]|(self.reg[29]<<8) #Y address

                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.A -= 1 ##decrementing Y
                    self.reg[28] = self.A&0xFF 
                    self.reg[29] = (self.A>>8)&0xFF

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])
                    
                    self.databyteNb = 1

                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.mem.instype.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0
            case 'STDY':#Y+q or STY
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.q = (self.ins&0b111)|(((self.ins>>10)&0b11)<<3)|(((self.ins>>13)&0b1)<<5)
                self.A = ((self.reg[28]&0xFF)|(self.reg[29]<<8))+self.q # Y address
                
                
                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])

                    self.mem.instype.prepare(1)

                    self.databyteNb = 1

                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.mem.instype.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0
            case 'STZ':#Z
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.A = self.reg[30]|(self.reg[31]<<8) # Z

                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.mem.instype.prepare(1)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])

                    self.databyteNb = 1
                    
                else:

                    self.mem.instype.prepare(0)

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0
            case 'STZ+':#Z+
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.A = self.reg[30]|(self.reg[31]<<8)

                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])

                    self.mem.instype.prepare(1)

                    self.databyteNb = 1
                    
                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.A += 1 ##incrementing Z
                    self.reg[30] = self.A&0xFF 
                    self.reg[31] = (self.A>>8)&0xFF

                    self.mem.instype.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0
            case 'ST-Z':#–Z
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0b11111
                Z = self.reg[30]&0xFF|(self.reg[31]<<8) # Z address

                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.A -= 1 ##decrementing Z
                    self.reg[30] = self.A&0xFF 
                    self.reg[31] = (self.A>>8)&0xFF

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rd])

                    self.mem.instype.prepare(1)

                    self.databyteNb = 1

                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.mem.instype.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0
            case 'STDZ':#Z+q or STZ
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.q = (self.ins&0b111) | (((self.ins>>10)&0b11)<<3) | (((self.ins>>13)&0b11)<<3)
                self.A = self.reg[30]|(self.reg[31]<<8) #named A but it is a Z address

                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.mem.address.prepare(self.A+self.q)
                    self.mem.write_data.prepare(self.reg[self.Rd])

                    self.mem.instype.prepare(1)

                    self.databyteNb = 1

                else:

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.mem.instype.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0
            
            case 'STS':
                Rr = (self.ins>>4) & 0x1F
                add = yield from self.readInsWord()
                
                v = yield from self.readByte(Rr)
                yield from self.writeByte(add, v)
                
                print(f'STS {add:04X}, R{Rr}\t[{add:04X}]={v:02X}')

            case 'LPM': #R0 implied
                raise Exception('not reviewed')
                self.A = (self.reg[30]&0xFF)|((self.reg[31]&0xFF)<<8)

                if(self.A&0b1 == 1 ):##high byte
                    self.reg[1] = (self.flash[(self.A>>1)] & 0xFF00)>>8
                else: ## low byte 
                    self.reg[0] = (self.flash[(self.A>>1)]&0xFF)

                self.pc += 1 
            case 'LPMZ': #Z
                raise Exception('not reviewed')
                self.Rd = ((self.ins>>4)&0x1F)
                self.A = (self.reg[30]&0xFF)|((self.reg[31]&0xFF)<<8)


                if(self.A&0b1 == 1 ):##high byte
                    self.reg[self.Rd] = (self.flash[(self.A>>1)] & 0xFF00)>>8
                else: ## low byte 
                    self.reg[self.Rd] = (self.flash[(self.A>>1)]&0xFF)


                self.pc += 1
            case 'LPMZ+': #Z+
                raise Exception('not reviewed')
                self.Rd = ((self.ins>>4)&0x1F) 
                self.A = (self.reg[30]&0xFF)|((self.reg[31]&0xFF)<<8)

                original_address = self.A

                if(self.A&0b1 == 1 ):##high byte
                    self.reg[self.Rd+1] = (self.flash[(self.A>>1)] & 0xFF00)>>8
                else: ## low byte 
                    self.reg[self.Rd] = (self.flash[(self.A>>1)]&0xFF)

                original_address += 1 ##decrementing Z
                self.reg[30] = original_address&0xFF 
                self.reg[31] = (original_address>>8)&0xFF

                self.pc+=1
            case 'SPM':
                raise Exception('not reviewed')
                # must use SPMCSR
                SELFPRGEN = self.SPMCSR & 0b1
                PGERS = (self.SPMCSR >> 1) & 0b1
                PGWRT = (self.SPMCSR >> 2) & 0b1
                BLBSET = (self.SPMCSR >> 3) & 0b1
                RWWSRE = (self.SPMCSR >> 4) & 0b1
                RES = (self.SPMCSR >> 5) & 0b1
                SPMIE = (self.SPMCSR >> 7) & 0b1

                self.Z = (self.reg[30] & 0xFF) | ((self.reg[31] & 0xFF) << 8)

                word_addr = self.Z >> 1

                page_offset = word_addr % self.PAGE_SIZE_WORDS
                page_base_addr = word_addr - page_offset

                if SELFPRGEN == 1: # SPM operation is enabled

                    # --- 1. PAGE ERASE ---
                    if (PGERS == 1) and (PGWRT == 0): 
                        # Wipe the entire page in actual flash memory
                        for i in range(self.PAGE_SIZE_WORDS):
                            if (page_base_addr + i) < len(self.flash):
                                self.flash[page_base_addr + i] = 0xFFFF
                        
                    # --- 2. PAGE WRITE ---
                    elif (PGERS == 0) and (PGWRT == 1): 
                        # Commit the temporary buffer to the flash memory page
                        for i in range(self.PAGE_SIZE_WORDS):
                            if (page_base_addr + i) < len(self.flash):
                                # Flash can only change bits from 1 to 0. 
                                # A bitwise AND correctly simulates writing over existing data.
                                self.flash[page_base_addr + i] &= self.temp_page_buffer[i]
                        
                        # Hardware auto-erases the temporary buffer after a Page Write
                        self.temp_page_buffer = [0xFFFF] * self.PAGE_SIZE_WORDS

                    # --- 3. FILL TEMPORARY BUFFER ---
                    elif (PGERS == 0) and (PGWRT == 0) and (BLBSET == 0):
                        # Load the data word from R1:R0 (R0 is LSB, R1 is MSB)
                        data_word = (self.reg[0] & 0xFF) | ((self.reg[1] & 0xFF) << 8)
                        
                        # Write into the temporary buffer at the specified offset
                        self.temp_page_buffer[page_offset] = data_word

                    # Hardware auto-clears the SPM enable bit after execution
                    self.SPMCSR &= ~0b1

                    # Trigger interrupt if enabled
                    if SPMIE == 1:
                        print("SPM Interrupt Triggered")

                self.pc += 1

            case 'IN':
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0b11111
                self.A = ((self.ins)&0xF) | ((((self.ins)>>9)&0b11)<<4) #don't know what is the port

                #verify if the address is valid
                #Minimum Address: 0x00
                #Maximum Address: 0x3F
                if (self.A >= 0x00) and (self.A <=0x3F):
                    #internal addresses
                    if (self.A == self.SREG_addr_IO):
                        self.reg[self.Rd] = self.SREG #status register
                        print("Register:SREG")
                        self.pc += 1
                    elif (self.A == self.MCUSR_addr_IO):
                        self.reg[self.Rd] = self.MCUSR
                        print("Register:MCUSR = {val}".format(val = self.MCUSR))  
                        self.pc += 1 
        
                    if self.databyteNb == 0 :
                        self.mem.write.prepare(0)
                        self.mem.read.prepare(1) 

                        self.mem.address.prepare(self.A)
                        self.databyteNb = 1
                    elif self.mem.resp.get() == 1:
                        self.reg[self.Rd] = self.mem.read_data.get()

                        self.pc += 1
                        self.databyteNb = 0
                else:
                    # increment by one if the address is invalid    
                    self.pc+=1
            case 'OUT':
                # -> 1011 1AAr rrrr AAAA
                Rr = Rd5
                add = A6 + 0x20
                
                v = yield from self.readByte(Rr)
                
                if (add == SPH_REG):
                    self.SP = (v << 8) | self.SP & 0x00FF
                elif (add == SPL_REG):
                    self.SP = v | self.SP & 0xFF00
                elif (add == SREG_REG):
                    self.I = (v >> 7) & 1
                    self.T = (v >> 6) & 1
                    self.H = (v >> 5) & 1
                    self.S = (v >> 4) & 1
                    self.V = (v >> 3) & 1
                    self.N = (v >> 2) & 1
                    self.Z = (v >> 1) & 1
                    self.C = (v & 1)
                else:
                    yield from self.writeByte(add + 0x20, v)
                
                print(f'OUT {add:04X}, R{Rr}\t[{add:04X}]={v:02X}')

            case 'PUSH':
                raise Exception('not reviewed')
                self.Rr = (self.ins>>4)&0x1F
                self.A = (self.SPH<<8) | (self.SPL&0xFF)

                if self.databyteNb == 0:
                    self.mem.write.prepare(1)
                    self.mem.read.prepare(0)

                    self.mem.address.prepare(self.A)
                    self.mem.write_data.prepare(self.reg[self.Rr])

                    self.databyteNb = 1

                else:
                    self.A -= 1 ##decrementing SP
                    self.SPL = self.A&0xFF 
                    self.SPH = (self.A>>8)&0xFF

                    self.mem.write.prepare(0)
                    self.mem.write.prepare(0)

                    self.pc += 1 
                    self.databyteNb = 0            
            case 'POP':
                raise Exception('not reviewed')
                self.Rd = (self.ins>>4)&0x1F
                self.A = ((self.SPH&0xFF)<<8) | (self.SPL&0xFF)

                if self.databyteNb == 0 :
                    self.mem.write.prepare(0)
                    self.mem.read.prepare(1) 

                    self.A = (self.A + 1 ) & 0xFFFF ##incrementing SP

                    self.SPL = self.A&0xFF 
                    self.SPH = (self.A>>8)&0xFF

                    self.mem.address.prepare(self.A)
                    self.databyteNb = 1

                elif self.mem.resp.get() == 1:
                    self.reg[self.Rd] = self.mem.read_data.get()

                    self.mem.write.prepare(0)
                    self.mem.read.prepare(0)

                    self.pc += 1
                    self.databyteNb = 0
            case 'NOP':
                raise Exception('not validated')
                self.pc += 1 
            case 'SLEEP':
                ##activation of SLEEP MODE
                raise Exception('not validated')
                self.pc += 1
            case 'WDR' :
                ## Watchdog Reset
                raise Exception('not validated')
                self.pc +=1
            case 'BREAK' : 
                ## Sould enter debug mode
                raise Exception('not validated')
                self.pc += 1
            case 'invalid': #basicaly a nop
                raise Exception(f'invalid opocode: {self.ins:04X}')
                self.pc += 1
                
        yield