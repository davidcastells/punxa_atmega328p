import py4hw
from py4hw.logic import *
from py4hw.logic.storage import *
from py4hw.simulation import Simulator
import py4hw.debug
import mmap

#2048 bytes of ram
#32256 of rom 

class MemoryInterface(Interface):

    def __init__(self, parent:Logic, name:str, data_width:int, address_width:int):
        super().__init__(parent,name)

        self.read = self.addSourceToSink("read",1)
        self.write = self.addSourceToSink("write",1) # These are to enable read an wirte 

        self.write_data = self.addSourceToSink("writedata",data_width) 
        self.read_data = self.addSinkToSource("readdata",data_width)

        self.address = self.addSourceToSink("address",address_width)
        self.instype = self.addSourceToSink("instype",1)

        if((data_width % 8) != 0):
            raise Exception('data_width must be multiple of byte,{} not supported').format(data_width)
        
        #self.be = self.addSourceToSink('be', data_width // 8) #nb of bytes does not make sense because the registers of the mcu are 8 bit8 
        self.resp = self.addSinkToSource('resp',1)# 0 = normal state, 1 = Operation Performed


class Ram_Memory(Logic):
    def __init__(self, parent:Logic, name:str, data_width:int, address_width:int, port:MemoryInterface):
        super().__init__(parent, name)

        self.port0 = self.addInterfaceSink('port',port)
        self.startAddress = 0x0100
        self.stopAddress = 0x08FF
        self.values = [0]*(self.stopAddress-self.startAddress+1)

    def clock(self):
        address = self.port0.address.get()
        #print("Address:",address)

        if (address >= self.startAddress) and (address <= self.stopAddress):
            address = address -0x0100
            
            print("opperation")
            #print((self.port0.read.get() == 1) and (self.port0.write.get() == 0))
            #print((self.port0.read.get() == 1) and (self.port0.write.get() == 1))

            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):
                self.port0.read_data.prepare(self.values[address])
                self.port0.resp.prepare(1)
                #print('reading address ', address, '=', self.values[address])


            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1):
                self.values[address] = self.port0.write_data.get()
                self.port0.resp.prepare(1)
                #print('writing address ', address, '=', self.values[address])
                

            else:
                self.port0.resp.prepare(0)
        else:
            self.port0.resp.prepare(0)


class EEPROM_Memory(Logic):
    def __init__(self, parent:Logic, name:str, data_width:int, address_width:int, port:MemoryInterface,EERI):
        super().__init__(parent,name)
        
        self.port0 = self.addInterfaceSink('port',port)
        self.startAddress = 0x000
        self.stopAddress = 0x3FF
        self.values = [0]*(self.stopAddress-self.startAddress)

        self.EERI = py4hw.addOut('EERI',EERI)


        self.EEARH = 0
        self.EEARH_addr_IO = 0x22
        self.EEARH_addr_LS = 0x42


        self.EEARL = 0
        self.EEARL_addr_IO = 0x21 
        self.EEARL_addr_LS = 0x41


        self.EEDR = 0
        self.EEDR_addr_IO = 0x20
        self.EEDR_addr_LS = 0x40


        self.EECR = 0
        self.EECR_addr_IO = 0x1F
        self.EECR_addr_LS = 0x3F

        self.ADDR = 0



    def clock(self):

        self.ADDR = self.port0.address.get()
        if ((self.ADDR == self.EEARH_addr_IO) and self.port0.instype.get() == 0) or ((self.ADDR == self.EEARH_addr_LS) and self.port0.instype.get() == 1):
            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):  #read
                self.port0.read_data.prepare(self.EEARH)
                self.port0.resp.prepare(1)
            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1): #write
                self.EEARH = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)
        elif ((self.ADDR == self.EEARL_addr_IO) and self.port0.instype.get() == 0) or ((self.ADDR == self.EEARL_addr_LS)and self.port0.instype.get() == 1):
            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):  #read
                self.port0.read_data.prepare(self.EEARL)
                self.port0.resp.prepare(1)
            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1): #write
                self.EEARL = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)
        elif ((self.ADDR == self.EEDR_addr_IO) and self.port0.instype.get() == 0) or ((self.ADDR == self.EECR_addr_LS)and self.port0.instype.get() == 1):
            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):  #read
                self.port0.read_data.prepare(self.EEDR)
                self.port0.resp.prepare(1)
            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1): #write
                self.EEDR = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)

        address = ((self.EEARH<<8)&0b1)|(self.EEARL)

        #EEPROM Control Register

        EEPM = ((self.EECR>>4) & 3)
        EERIE =  ((self.EECR>>3) & 1)
        EEMPE = ((self.EECR>>2) & 1 )
        EEPE = ((self.EECR>>1) & 1)
        EERE = (self.EECR & 1)

        if (address >= self.startAddress) and (address <= self.stopAddress):

            
            
            print("opperation")
            #print((self.port0.read.get() == 1) and (self.port0.write.get() == 0))
            #print((self.port0.read.get() == 1) and (self.port0.write.get() == 1))

            if EEPM == 1:
                self.port0.read_data.prepare(self.values[address])
                self.port0.resp.prepare(1)
                #print('reading address ', address, '=', self.values[address])


            elif EEPM == 2:
                self.values[address] = self.port0.write_data.get()
                self.port0.resp.prepare(1)
                #print('writing address ', address, '=', self.values[address])
                
            elif EEPM == 0:
                self.port0.read_data.preapre(self.values[address])
                self.values[address] = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)
        else:
            self.port0.resp.prepare(0)
            





class ProgramMemory(py4hw.Logic):
    def __init__(self,parent,name,ADRESS,DATA_IN,DATA_OUT, Write_Enable): #RW = 0 then R else W
        super().__init__(parent, name)

        self.ADRESS = self.addIn('ADRESS', ADRESS)
        self.memory = [0]*32256 #address_width data_width
        self.DATA_OUT = self.addOut('DATA_OUT', DATA_OUT)
        self.DATA_IN = self.addIn('DATA_IN',DATA_IN)
        self.Write_Enable = self.addIn('Write_Enable',Write_Enable)

    def clock(self):
        if self.Write_Enable.get() == 1:
            self.DATA_OUT.prepare(self.memory[self.ADRESS.get()])
        else: 
            self.memory[self.ADRESS.get()] = self.DATA_IN


