import py4hw
from punxa_atmega328p.Memory import *


class InterruptUnit(py4hw.Logic):
    def __init__(self,parent,name:str,memory:MemoryInterface,Interrupt,Global_Interrupt_Enable,INT0,INT1,PCINT0,PCINT1,PCINT2,WDT,TIMER2_COMPA,TIMER2_COMPB,TIMER2_OVF,TIMER1_CAPT,TIMER1_COMPA,TIMER1_COMPB,TIMER1_OVF,TIMER0_COMPA,TIMER0_COMPB,TIMER0_OVF,SPI_STC,USART_RX,USART_UDRE,USART_TX,ADC,EE_READY,ANALOG_COMP,TWI,SPM_READY):
        super().__init__(parent,name)

        self.interface = self.addInterfaceSink('port',memory)

        self.JUMPto = 0

        self.I = self.addIn('I',Global_Interrupt_Enable)
        self.Interrupt = self.addOut('Interrupt',Interrupt)
        #interrutpts
        self.INT0 = self.addIn('INT0',INT0)
        self.INT1 = self.addIn('INT1',INT1)
        self.PCINT0 = self.addIn('PCINT0',PCINT0)
        self.PCINT1 = self.addIn('PCINT1',PCINT1)
        self.PCINT2 = self.addIn('PCINT2',PCINT2)
        self.WDT = self.addIn('WDT',WDT)
        self.TIMER2_COMPA = self.addIn('TIMER2_COMPA',TIMER2_COMPA)
        self.TIMER2_COMPB = self.addIn('TIMER2_COMPB',TIMER2_COMPB)
        self.TIMER2_OVF = self.addIn('TIMER2_OVF',TIMER2_OVF)
        self.TIMER1_CAPT = self.addIn('TIMER1_CAPT',TIMER1_CAPT)
        self.TIMER1_COMPA = self.addIn('TIMER1_COMPA',TIMER1_COMPA)
        self.TIMER1_COMPB = self.addIn('TIMER1_COMPB',TIMER1_COMPB)
        self.TIMER1_OVF = self.addIn('TIMER1_OVF',TIMER1_OVF)
        self.TIMER0_COMPA = self.addIn('TIMER0_COMPA',TIMER0_COMPA)
        self.TIMER0_COMPB = self.addIn('TIMER0_COMPB',TIMER0_COMPB)
        self.TIMER0_OVF = self.addIn('TIMER0_OVF',TIMER0_OVF)
        self.SPI_STC = self.addIn('SPI_STC',SPI_STC)
        self.USART_RX = self.addIn('USART_RX',USART_RX)
        self.USART_UDRE = self.addIn('USART_UDRE',USART_UDRE)
        self.USART_TX = self.addIn('USART_TX',USART_TX)
        self.ADC = self.addIn('ADC',ADC)
        self.EE_READY = self.addIn('EE_READY',EE_READY)
        self.ANALOG_COMP = self.addIn('ANALOG_COMP',ANALOG_COMP)
        self.TWI = self.addIn('TWI',TWI)
        self.SPM_READY = self.addIn('SPM_READY',SPM_READY)

    def clock(self):
        if self.I.get() == 1:

            if self.INT0.get() == 1:
                ## save the current pc position to the stack 

                ## go to the interrupt vector
                self.JUMPto = 0x002 

                self.Interrupt.preapare(1)

            elif self.INT1.get() == 1: 

                self.JUMPto = 0x004

                self.Interrupt.preapare(1)

            elif self.PCINT0.get() == 1: 

                self.JUMPto = 0x006

                self.Interrupt.preapare(1)

            elif self.PCINT1.get() == 1:

                self.JUMPto = 0x008

                self.Interrupt.preapare(1)

            elif self.PCINT2.get() == 1:

                self.JUMPto = 0x00A

                self.Interrupt.preapare(1)

            elif self.WDT.get() == 1:

                self.JUMPto = 0x00C

                self.Interrupt.preapare(1)

            elif self.TIMER2_COMPA.get() == 1:

                self.JUMPto = 0x00E

                self.Interrupt.preapare(1)

            elif self.TIMER2_COMPB.get() == 1:

                self.JUMPto = 0x010

                self.Interrupt.preapare(1)

            elif self.TIMER2_OVF.get() == 1: 

                self.JUMPto = 0x012

                self.Interrupt.preapare(1)

            elif self.TIMER1_CAPT.get() == 1:

                self.JUMPto = 0x014

                self.Interrupt.preapare(1)

            elif self.TIMER1_COMPA.get() == 1: 

                self.JUMPto = 0x016

                self.Interrupt.preapare(1)

            elif self.TIMER1_COMPB.get() == 1: 

                self.JUMPto = 0x018

                self.Interrupt.preapare(1)

            elif self.TIMER1_OVF.get() == 1: 

                self.JUMPto = 0x01A

                self.Interrupt.preapare(1)

            elif self.TIMER0_COMPA.get() == 1: 

                self.JUMPto = 0x01C

                self.Interrupt.preapare(1)

            elif self.TIMER0_COMPB.get() == 1:

                self.JUMPto = 0x01E

                self.Interrupt.preapare(1)

            elif self.TIMER0_OVF.get() == 1:

                self.JUMPto = 0x020

                self.Interrupt.preapare(1)

            elif self.SPI_STC.get() == 1:

                self.JUMPto = 0x022

                self.Interrupt.preapare(1)

            elif self.USART_RX.get() == 1:
            
                self.JUMPto = 0x24

                self.Interrupt.preapare(1)

            elif self.USART_UDRE.get() == 1:

                self.JUMPto = 0x026

                self.Interrupt.preapare(1)

            elif self.USART_TX.get() == 1:

                self.JUMPto = 0x028

                self.Interrupt.preapare(1)

            elif self.ADC.get() == 1:

                self.JUMPto = 0x2A

                self.Interrupt.preapare(1)

            elif self.EE_READY.get() == 1:

                self.JUMPto = 0x2C

                self.Interrupt.preapare(1)

            elif self.ANALOG_COMP.get() == 1:

                self.JUMPto = 0x2E

                self.Interrupt.preapare(1)

            elif self.TWI.get() == 1:

                self.JUMPto = 0x030

                self.Interrupt.preapare(1)

            elif self.SPM_READY.get() == 1: 

                self.JUMPto = 0x032
                
                self.Interrupt.preapare(1)

