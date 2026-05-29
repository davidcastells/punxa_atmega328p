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
        self.SPR = 0 

        self.CLKcounter = 0
        self.lastCLK = 0
        self.currentCLk = 0

        #state machines
        self.stateMachineRX = 'START' #'DATA' 'STOP'
        self.stateMAchineTx = 'START' #'DATA' 'STOP'
        self.lastSPR=17

    def Memory_access(self):
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
                self.SPSR = self.interface.write_data.get()& 0b00000001
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

    def Parse_control_registers(self):
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

    def update_prescaler(self):
        #prescaler set up 

        match self.SPR:
            case 0: self.prescaler = 4
            case 1: self.prescaler = 16
            case 2: self.prescaler = 64
            case 3: self.prescaler = 128
            case 4: self.prescaler = 2
            case 5: self.prescaler = 8
            case 6: self.prescaler = 32
            case 7: self.prescaler = 64

        if self.lastSPR != self.SPR:
            self.CLKcounter = 0 
            self.lastSPR = self.SPR



    def clock(self):
        self.Memory_access()
        self.Parse_control_registers()
        self.update_prescaler()


        if self.SPIF == 1 and self.SPIE == 1:
            self.SPI_STC.prepare(1)
        else:
            self.SPI_STC.prepare(0)

        if self.SPE == 1: # TO enable the SPI
            # SS pin logic 
            if self.MSTR == 1 and self.SS.get() == 0:

                self.SPCR = self.SPCR & 0xEF 
                self.MSTR = 0
                self.SPSR = self.SPSR | 0x80
                self.SPIF = 1 

            if self.MSTR == 0 and self.SS.get() == 1:
                self.bit_counter = 8 
                return
            
            self.CLKcounter += 1 

            #Divide prescaler by2 because a full cycle requires TWO toggles
            toggle_threshold = max(1,self.prescaler>>1)

            if self.CLKcounter >=  toggle_threshold:
                self.CLKcounter = 0 

                current_clk_val = self.CLK.get()

                if self.MSTR == 1:
                    next_clk_val = 0 if current_clk_val == 1 else 1 
                    self.CLK.prepare(next_clk_val)
                    current_clk_val = next_clk_val
                else:
                    pass 

                leading_edge = (self.lastCLK == self.CPOL) and (current_clk_val != self.CPOL)
                trailing_edge = (self.lastCLK != self.CPOL) and (current_clk_val == self.CPOL)

                sample_edge = leading_edge if self.CPHA == 0 else trailing_edge
                setup_edge =  trailing_edge if self.CPHA == 0 else leading_edge


                if self.bit_counter < 8:

                    if setup_edge:

                        if self.DORD == 1:
                            bit_out = self.SPDR & 1
                        else:
                            bin_out = (self.SPDR >> 7) & 1

                        self.MOSI.prepare(bin_out)

                    elif sample_edge:

                        incoming_bit = self.MISO.get() & 1

                        if self.DORD == 1:
                            self.SPDR = (self.SPDR >> 1 ) | (incoming_bit << 7)
                        else:
                            self.SPDR = ((self.SPDR << 1)& 0xFF) | incoming_bit

                        self.bit_counter += 1

                        if self.bit_counter == 8:
                            self.SPSR = self.SPSR | 0x80
                            self.SPIF = 1 

                self.lastCLK = current_clk_val
            idle_state = 1 if self.CPOL == 1 else 0
            self.CLK.prepare(idle_state)
            self.lastCLK = idle_state
            self.bit_counter = 8

    