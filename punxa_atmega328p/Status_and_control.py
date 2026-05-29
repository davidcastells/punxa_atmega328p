import py4hw
from Source.Memory import * 


## *_IO = IN and OUT instruction address
## *_LS =  LD LDS ST STS instruction address
class Status_and_control(py4hw.Logic):
    
    def __init__(self,parent,name,port:MemoryInterface):
        super().__init__(parent,name)

        self.port0 = self.addInterfaceSink('port',port)
    

        self.SREG = 0
        self.SREG_addr_IO = 0x3F
        self.SREG_addr_LS = 0x5F

        self.SPH = 0
        self.SPH_addr_IO = 0x3E
        self.SPH_addr_LS = 0x5E

        self.SPL = 0 
        self.SPL_addr_IO = 0x3D
        self.SPL_addr_LS = 0x5D

        self.GPIOR2 = 0
        self.GPIOR2_addr_IO = 0x39
        self.GPIOR2_addr_LS = 0x59

        self.GPIOR1 = 0
        self.GPIOR1_addr_IO = 0x38
        self.GPIOR1_addr_LS = 0x58

        self.GPIOR0 = 0  
        self.GPIOR0_addr_IO = 0x1E 
        self.GPIOR0_addr_LS = 0x3E

        self.SPMCSR = 0
        self.SPMCSR_addr_IO = 0x37
        self.SPMCSR_addr_LS = 0x57

        self.MCUCR = 0
        self.MCUCR_addr_IO = 0x35
        self.MCUCR_addr_LS = 0x55

        self.MCUSR = 0
        self.MCUSR_addr_IO = 0x34
        self.MCUSR_addr_LS = 0x54

        self.SMCR = 0
        self.SMCR_addr_IO = 0x33
        self.SMCR_addr_LS = 0x53


        self.OSCCAL = 0
        self.OSCCAL_addr_LS = 0x66
        
        self.PRR = 0
        self.PRR_addr_LS = 0x64

        self.CLKPR = 0
        self.CLKPR_addr_LS = 0x61

    def clock(self):
        self.ADDR = self.interface.address.get()
        if ((self.ADDR == self.SREG_addr_IO) and self.port0.instype.get() == 0) or ((self.ADDR == self.SREG_addr_LS) and self.INSTYPE.get() == 1):
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0):  #read
                self.interface.read_data.prepare(self.GPIOR2)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1): #write
                self.GPIOR2 = self.interface.write_data.get()
                self.interface.resp.prepare(0)
            else:
                self.interface.resp.prepare(1)
        elif ((self.ADDR == self.SPH_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.SPH_addr_LS)and self.INSTYPE.get() == 1):
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0):  #read
                self.interface.read_data.prepare(self.GPIOR1)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1): #write
                self.GPIOR1 = self.interface.write_data.get()
                self.interface.resp.prepare(0)
            else:
                self.interface.resp.prepare(1)
        elif ((self.ADDR == self.SPL_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.SPL_addr_LS) and self.INSTYPE.get() == 1):
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0):
                self.interface.read_data.prepare(self.GPIOR0)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1):
                self.GPIOR0 = self.interface.write_data.get()
            else:
                self.interface.resp.prepare(1)   
        elif ((self.ADDR == self.SPL_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.PORTB_addr_LS) and self.INSTYPE.get() == 1): #PORTB
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0):  #read
                self.interface.read_data.prepare(self.PORTB)
                self.interface.resp.prepare(0)

            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1): #write
                self.PORTB = self.interface.write_data.get()
                self.interface.resp.prepare(0)
            else:
                self.interface.resp.prepare(1)
        elif ((self.ADDR == self.GPIOR2_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.DDRB_addr_LS) and self.INSTYPE.get() == 1):
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0):  #read
                self.interface.read_data.prepare(self.DDRB)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1):  #write
                self.DDRB = self.interface.write_data.get()
                self.interface.resp.prepare(0)
            else:
                self.interface.resp.prepare(1)
        elif ((self.ADDR == self.PINB_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.PINB_addr_LS) and self.INSTYPE.get() == 1):
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0): #read
                self.interface.read_data.prepare(self.PINB)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1): #write
                self.PINB = self.interface.write_data.get()
            else:
                self.interface.resp.prepare(1)  
        elif ((self.ADDR == self.PORTC_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.PORTC_addr_LS) and self.INSTYPE.get() == 1): #PORTC
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0):  #read
                self.interface.read_data.prepare(self.PORTC)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1): #write
                self.PORTC = self.interface.write_data.get()
            else:
                self.interface.resp.prepare(1)
        elif ((self.ADDR == self.DDRC_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.DDRC_addr_LS) and self.INSTYPE.get() == 1):
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0):  #read
                self.interface.read_data.prepare(self.DDRC)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1):  #write
                self.DDRC = self.interface.write_data.get()
            else:
                self.interface.resp.prepare(1)
        elif ((self.ADDR == self.PINC_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.PINC_addr_LS) and self.INSTYPE.get() == 1):   #PORTD
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0): #read
                self.interface.read_data.prepare(self.PINC)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1): #write
                self.PINC = self.interface.write_data.get()
            else:
                self.interface.resp.prepare(1)        
        elif ((self.ADDR == self.PORTD_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.PORTD_addr_LS) and self.INSTYPE.get() == 1): 
            print("test1")
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0):  #read
                self.interface.read_data.prepare(self.PORTD)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1): #write
                self.PORTD = self.interface.write_data.get()
            else:
                self.interface.resp.prepare(1)
        elif ((self.ADDR == self.DDRD_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.DDRD_addr_LS) and self.INSTYPE.get() == 1):
            print("test2")
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0):  #read
                self.interface.read_data.prepare(self.DDRD)
                self.interface.resp.prepare(0)
            elif ((self.interface.read.get() == 0) and self.INSTYPE == 0) and ((self.interface.write.get() == 1) and self.INSTYPE == 1):  #write
                self.DDRD = self.interface.write_data.get()
            else:
                self.interface.resp.prepare(1)
        elif ((self.ADDR == self.PIND_addr_IO) and self.INSTYPE.get() == 0) or ((self.ADDR == self.PIND_addr_LS) and self.INSTYPE.get() == 1):
            if (self.interface.read.get() == 1) and (self.interface.write.get() == 0): #read
                self.interface.read_data.prepare(self.PIND)
                self.interface.resp.prepare(0)
            elif (self.interface.read.get() == 0) and (self.interface.write.get() == 1): #write
                self.PIND = self.interface.write_data.get()
            else:
                self.interface.resp.prepare(1)
        else:

