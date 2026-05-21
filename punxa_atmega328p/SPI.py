import py4hw
from punxa_atmega328p.Memory import *

class SPI(py4hw.Logic):
    def __init__(self,parent,name:str,memory:MemoryInterface,SS,MISO,MOSI,STC,CLK):
        super().__init__(parent, name)

        self.interface = self.addInterfaceSink('port',memory)

        #Physical Pins
        self.SS = self.addIn('!SS',SS)
        self.MISO = self.addIn('MISO',MISO)
        self.MOSI = self.addOut('MOSI',MOSI)
        self.CLK = self.addOut('CLK',CLK)

        #Interrupts
        self.SPI_STC = self.addOut('STC',STC)

        self.SPCR = 0
        self.SPCR_addr_LS = 0x2C
        self.SPCR_addr_IO = 0x4C

        self.SPSR = 0
        self.SPSR_addr_LS = 0x2D
        self.SPSR_addr_IO = 0x4D

        self.SPDR = 0
        self.SPDR_addr_LS = 0x2E
        self.SPDR_addr_IO = 0x4E

        #Bits
        #SPCR
        self.SPIE = 0
        self.SPE = 0
        self.DORD = 0
        self.MSTR = 0
        self.CPOL = 0
        self.CPHA = 0
        self.SPR1 = 0
        self.SPR0 = 0 


        #SPSR 
        self.SPIF = 0
        self.WCOL = 0 
        self.SPI2X = 0

        self.CLKcounter = 0

        self.lastCLK = 0
        self.currentCLk = 0

        #state machines
        self.stateMachineRX = 'START' #'DATA' 'STOP'
        self.stateMAchineTx = 'START' #'DATA' 'STOP'
        self.lastSPR=17

    
    def clock(self):
        ADDR = self.interface.address.get()
        read_opp = (self.interface.read.get() == 1) and (self.interface.write.get() == 0)
        write_opp = (self.interface.read.get() == 0) and (self.interface.write.get() == 1)
           

        if ((ADDR == self.SPCR_addr_IO) and (self.interface.instype.get() == 0)) or ((ADDR == self.SPCR_addr_LS) and (self.interface.instype.get() == 1)):
            if read_opp:
                self.interface.read_data.prepare(self.SPCR)
                self.interface.resp.prepare(1)
            elif write_opp:
                self.SPCR = self.interface.write_data.get()
                self.interface.resp.prepare(1)
            else:
                self.interface.resp.prepare(0)
        elif ((ADDR == self.SPSR_addr_IO) and (self.interface.instype.get() == 0)) or ((ADDR == self.SPSR_addr_LS) and (self.interface.instype.get() == 1)):
            if read_opp:
                self.interface.read_data.prepare(self.SPSR)
                self.interface.resp.prepare(1)
            elif write_opp:
                self.SPSR = self.interface.write_data.get()
                self.interface.resp.prepare(1)
            else:
                self.interface.resp.prepare(0)
        elif ((ADDR == self.SPDR_addr_IO) and (self.interface.instype.get() == 0)) or ((ADDR == self.SPDR_addr_LS) and (self.interface.instype.get() == 1)):
            if read_opp:
                self.interface.read_data.prepare(self.SPDR)
                self.interface.resp.prepare(1)
            elif write_opp:
                self.SPDR = self.interface.write_data.get()
                self.interface.resp.prepare(1)
            else:
                self.interface.resp.prepare(0)
        else:
            self.interface.resp.prepare(0)

        self.SPIE = (self.SPCR>>7)&1
        self.SPE = (self.SPCR>>6)&1
        self.DORD = (self.SPCR>>5)&1
        self.MSTR = (self.SPCR>>4)&1
        self.CPOL = (self.SPCR>>3)&1
        self.CPHA = (self.SPCR>>2)&1
        self.SPR1 = (self.SPCR>>1)&1
        self.SPR0 = (self.SPCR>>0)&1 

        #SPSR 
        self.SPIF = (self.SPSR>>7)&1
        self.WCOL = (self.SPSR>>6)&1
        self.SPI2X = (self.SPSR>>0)&1
        self.SPR =  (self.SPI2X<<2)|(self.SPR1<<1)|(self.SPR)

        #prescaler set up 
        if (self.SPR == 0): # clk/4
            self.prescaler = 4
            if self.lastSPR != 0:
                self.CLKcounter = 0
                self.lastSPR=0
        elif (self.SPR == 1): # clk/16
            self.prescaler = 16
            if self.lastSPR != 0:
                self.CLKcounter = 0
                self.lastSPR=1
        elif (self.SPR == 2): # clk/64
            self.prescaler = 64
            if self.lastSPR != 0:
                self.CLKcounter = 0
                self.lastSPR=2
        elif (self.SPR == 3): # clk/128
            self.prescaler = 128 
            if self.lastSPR != 0:
                self.CLKcounter = 0 
                self.lastSPR=3
        elif (self.SPR == 4): # clk/2
            self.prescaler = 2
            if self.lastSPR != 0:
                self.CLKcounter = 0
                self.lastSPR=4
        elif (self.SPR == 5): # clk/8
            self.prescaler = 8
            if self.lastSPR != 0:
                self.CLKcounter = 0
                self.lastSPR=5
        elif (self.SPR == 6): # clk/32
            self.prescaler = 32
            if self.lastSPR != 0:
                self.CLKcounter = 0
                self.lastSPR=6
        elif (self.SPR == 7): # clk/64
            self.prescaler = 64
            if self.lastSPR != 0:
                self.CLKcounter = 0
                self.lastSPR=7

        if self.SPIF == 1:
            self.SPI_STC.prepare(1)
        else:
            self.SPI_STC.prepare(0)

        if self.SPE == 1: # TO enable the SPI
            self.CLKcounter += 1

            if self.MSTR == 1 :  # Master Mode

            elif self.MSTR == 0: # Slave Mode

            


            if self.CLKcounter >= self.prescaler:
                self.CLKcounter = 0

                #CLK output
                if self.CLK.get() == 1:
                    self.lastCLK = 0
                    self.CLK.prepare(0)
                else: 
                    self.lastCLK = 1
                    self.CLK.prepare(1)


                ## send information
                if (self.SPDR != 0) and (self.DORD == 1) : #LSB first
                    # to output to the terminal
                    print(self.SPDR&1)
                    self.MOSI.prepare(self.SPDR&1)
                    self.SPDR = self.SPDR>>1
                elif (self.SPDR != 0) and (self.DORD == 0): # MSB first
                    # to output to the terminal
                    print((self.SPDR>>7)&1)
                    self.MOSI.prepare((self.SPDR>>7)&1)
                    self.SPDR = self.SPDR<<1
                else:


                if ((self.lastCLK == 0) and (self.CLK.get() == 1) and self.CPOL == 1):## read on falling edge
                    if (self.DORD == 1 ):
                        # to get imput form the terminal 
                        #self.SPDR = (self.SPDR<<1) | int(input(),2)
                        self.SPDR =  (self.SPDR<<1) | self.MISO.get()
                    else:
                        # to get imput form the terminal 
                        #self.SPDR = (self.SPDR>>1) | (int(input(),2)<<7)
                        self.SPDR = (self.SPDR>>1) | (self.MISO.get()<<7)

                elif((self.lastCLK == 1) and (self.CLK.get() == 0) and (self.CPOL ==0)): ## read on rising edge 
                    if (self.DORD == 1 ):
                        self.SPDR =  (self.SPDR<<1) | self.MISO.get()
                    else:
                        self.SPDR = (self.SPDR>>1) | (self.MISO.get()<<7)
        
        


        else:
            if self.CPOL == 1:
                self.CLK.prepare(1)
            else:
                self.CLK.prepare(0) 