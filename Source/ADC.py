import py4hw 
from .Memory import *

class ADCBehavioral(py4hw.Logic):

    def __init__(self,parent,name,port:MemoryInterface,INSTYPE,ADC0,ADC1,ADC2,ADC3,ADC4,ADC5,ADC6,ADC7): ## how to assign each function to each pin
        super().__init__(parent,name)

        self.port0 =  self.addInterfaceSink('port',port)

        self.INSTYPE = self.addIn('INSTYPE',INSTYPE)

        self.ADC0 = self.addIn('ADC0',ADC0)
        self.ADC1 = self.addIn('ADC1',ADC1)
        self.ADC2 = self.addIn('ADC2',ADC2)
        self.ADC3 = self.addIn('ADC3',ADC3)
        self.ADC4 = self.addIn('ADC4',ADC4)
        self.ADC5 = self.addIn('ADC5',ADC5)
        self.ADC6 = self.addIn('ADC6',ADC6)
        self.ADC7 = self.addIn('ADC7',ADC7)

        self.ADCIN = 0

        self.ADMUX = 0
        self.ADMUX_addr_LS = 0x7C

        self.ADCSRA = 0
        self.ADCSRA_addr_LS = 0x7A 

        self.ADCH = 0
        self.ADCH_addr_LS = 0x79 
        self.ADCL = 0
        self.ADCL_addr_LS = 0x78

        self.ADCSRB = 0
        self.ADCSRB_addr_LS = 0x7B

        self.DIDR0 = 0
        self.DIDR0_addr_LS = 0x7E

        self.MUX = 0
        self.RREFS = 0
        self.ADLAR = 0

        self.ADPS2 = 0
        self.ADIE = 0

        self.ADTS = 0
        self.ACME = 0

    def clock(self):
        #Address decoder
        self.ADDR = self.port0.address.get()
        if ((self.ADDR == self.ADMUX_addr_LS) and self.INSTYPE.get() == 1):
            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):  #read
                self.port0.read_data.prepare(self.ADMUX)
                self.port0.resp.prepare(1)
            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1): #write
                self.ADMUX = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)
        elif ((self.ADDR == self.ADCSRA_addr_LS)and self.INSTYPE.get() == 1):
            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):  #read
                self.port0.read_data.prepare(self.ADCSRA)
                self.port0.resp.prepare(1)
            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1): #write
                self.ADCSRA = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)
        elif ((self.ADDR == self.ADCH_addr_LS)and self.INSTYPE.get() == 1):
            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):  #read
                self.port0.read_data.prepare(self.ADCH)
                self.port0.resp.prepare(1)
            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1): #write
                self.ADCH = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)
        elif ((self.ADDR == self.ADCL_addr_LS)and self.INSTYPE.get() == 1):
            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):  #read
                self.port0.read_data.prepare(self.ADCL)
                self.port0.resp.prepare(1)
            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1): #write
                self.ADCL = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)
        elif ((self.ADDR == self.ADCSRB_addr_LS)and self.INSTYPE.get() == 1):
            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):  #read
                self.port0.read_data.prepare(self.ADCSRB)
                self.port0.resp.prepare(1)
            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1): #write
                self.ADCSRB = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)
        elif ((self.ADDR == self.DIDR0_addr_LS)and self.INSTYPE.get() == 1):
            if (self.port0.read.get() == 1) and (self.port0.write.get() == 0):  #read
                self.port0.read_data.prepare(self.DIDR0)
                self.port0.resp.prepare(1)
            elif (self.port0.read.get() == 0) and (self.port0.write.get() == 1): #write
                self.DIDR0 = self.port0.write_data.get()
                self.port0.resp.prepare(1)
            else:
                self.port0.resp.prepare(0)
        else:
            self.port0.resp.prepare(0)
        
        #Parameter Decoding
        self.MUX = self.ADMUX&0b1111
        self.ADLAR = (self.ADMUX>>5)&0b1
        self.REFS =  (self.ADMUX>>6)&0b11

        self.ADPS2 = (self.ADCSRA&0b111)
        self.ADIE = (self.ADCSRA>>3)&0b1
        self.ADIF = (self.ADCSRA>>4)&0b1
        self.ADATE = (self.ADCSRA>>5)&0b1
        self.ADSC = (self.ADCSRA>>6)&0b1
        self.ADEN = (self.ADCSRA>>7)&0b1

        self.ADTS = self.ADCSRB&0b111
        self.ACME = (self.ADCSRB>>6)&0b1

        match self.MUX:

            case 0:
                self.ADCIN = self.ADC0.get()

            case 1:
                self.ADCIN = self.ADC1.get()

            case 2:
                self.ADCIN = self.ADC2.get()

            case 3:
                self.ADCIN = self.ADC3.get()

            case 4:
                self.ADCIN = self.ADC4.get()

            case 5:
                self.ADCIN = self.ADC5.get()

            case 6:
                self.ADCIN = self.ADC6.get()

            case 7:
                self.ADCIN = self.ADC7.get()
        



        print("ADC")