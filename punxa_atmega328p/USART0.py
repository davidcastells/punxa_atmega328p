import py4hw
from punxa_atmega328p.Memory import *




class USART(py4hw.Logic):
    def __init__(self,parent,name:str,memory:MemoryInterface,RXD,TXD,RXC_INT,TXC_INT,UDRE_INT):
        super().__init__(parent, name)

        self.interface = self.addInterfaceSink('port',memory)

        #Physical Pins
        self.RXB = self.addIn('RXD',RXD)
        self.TXB = self.addOut('TXD',TXD)

        #Interrupts
        self.RXC_INT = self.addOut('RXC_INIT',RXC_INT)
        self.TXC_INT = self.addOut('TXC_INT', TXC_INT)
        self.UDRE_INT = self.addOut('UDRE_INT', UDRE_INT)

        self.UCSR0A = 0x20 # Bit5: UDRE0 is 1 by default (Buffer Empty)
        self.UCSR0A_addr_LS = 0xC0

        self.UCSR0B = 0
        self.UCSR0B_addr_LS = 0xC1

        self.USCR0C = 0 # Default: Async, No parity, 1 stop bit, 8 data bits
        self.USCR0C_addr_LS = 0xC2

        self.UBRR0L = 0
        self.UBRR0L_addr_LS = 0xC4

        self.UBRR0H = 0
        self.UBRR0H_addr_LS = 0xC5

        self.UDR0 = 0
        self.UDR0_addr_LS = 0xC6

        #Internal Data Buffers
        self.RXB = 0
        self.TXB = 0

        #Control & Status Bits
        #UCSR0A
        self.RXC0 = 0 
        self.TXC0 = 0
        self.UDRE0 = 1  
        self.FE0 = 0
        self.DOR0 = 0
        self.UPE0 = 0
        self.U2X0 = 0
        self.MPCM0 = 0

        #UCSR0B
        self.RXCIE0 = 0
        self.TXCIE0 = 0
        self.UDRIE0 = 0
        self.RXEN0 = 0
        self.TXEN0 = 0
        self.UCSZ02 = 0
        self.RXB80 = 0
        self.TXB80 = 0

        #UCSR0C
        self.UMSEL01 = 0
        self.UMSEL00 = 0
        self.UPM01 = 0
        self.UPM00 = 0
        self.USBS0 = 0
        self.UCSZ01 = 0
        self.UCSZ00 = 0
        self.UCPOL0 =0

        # Interrupt Enables
        self.RXCIE0 = 0
        self.TXCIE0 = 0
    

        self.opp_mode = 'Asynchronous'

        # Transmit/Receive State Machines
        self.baud_counter = 0
        self.tx_state = 'IDLE'
        self.tx_shift_reg = 0
        self.tx_bits = 0
        
        self.rx_state = 'IDLE'
        self.rx_shift_reg = 0
        self.rx_bits = 0

        self.prescaler = 0 
        self.CLKcounter = 0 


    def clock(self):
        ADDR = self.interface.address.get()
        read_opp = (self.interface.read.get() == 1) and (self.interface.write.get() == 0)
        write_opp = (self.interface.read.get() == 0) and (self.interface.write.get() == 1)
        valid_ins = self.interface.instype.get() == 1 

        if valid_ins:
            if ADDR == self.UCSR0A_addr_LS:
                if read_opp:
                    self.interface.read_data.prepare(self.UCSR0A)
                    self.interface.resp.prepare(1)
                elif write_opp:
                    self.UCSR0A = self.interface.write_data.get()
                    self.interface.resp.prepare(1)
                else:
                    self.interface.resp.prepare(0)
            elif ADDR == self.UCSR0B_addr_LS:
                if read_opp:
                    self.interface.read_data.preapre(self.UCSR0B)
                    self.interface.resp.prepare(1)
                elif write_opp:
                    self.UCSR0B = self.interface.write_data.get()
                    self.interface.resp.prepare(1)
                else:
                    self.interface.resp.prepare(0)
            elif ADDR == self.USCR0C_addr_LS:
                if read_opp:
                    self.interface.read_data.prepare(self.USCR0C)
                    self.interface.resp.prepare(1)
                elif write_opp:
                    self.USCR0C = self.interface.write_data.get()
                    self.interface.resp.prepare(1)
                else:
                    self.interface.resp.prepare(0)
            elif ADDR == self.UBRR0L_addr_LS:
                if read_opp:
                    self.interface.read_data.prepare(self.UBRR0L)
                    self.interface.resp.prepare(1)
                elif write_opp:
                    self.UBRR0L = self.interface.write_data.get()
                    self.interface.resp.prepare(1)
                else:
                    self.interface.resp.prepare(0)
            elif ADDR == self.UBRR0H_addr_LS:
                if read_opp:
                    self.interface.read_data.prepare(self.UBRR0H)
                    self.interface.resp.prepare(1)
                elif write_opp:
                    self.UBRR0H = self.interface.write_data.get()
                    self.interface.resp.prepare(1)
                else:
                    self.interface.resp.prepare(0)
            elif ADDR == self.UDR0_addr_LS:
                if read_opp:
                    self.interface.read_data.prepare(self.UDR0)
                    self.interface.resp.prepare(1)
                elif write_opp:
                    self.UDR0 = self.interface.write_data.get()
                    self.interface.resp.prepare(1)
                else:
                    self.interface.resp.prepare(0)
            else:
                self.interface.resp.prepare(0)


        #Control & Status Bits
        #UCSR0A
        self.RXC0 = (self.UCSR0A>>7)&1
        self.TXC0 = (self.UCSR0A>>6)&1
        self.UDRE0 = (self.UCSR0A>>5)&1  
        self.FE0 = (self.UCSR0A>>4)&1
        self.DOR0 = (self.UCSR0A>>3)&1
        self.UPE0 = (self.UCSR0A>>2)&1
        self.U2X0 = (self.UCSR0A>>1)&1
        self.MPCM0 = (self.UCSR0A>>0)&1

        #UCSR0B
        self.RXCIE0 = (self.UCSR0B>>7)&1
        self.TXCIE0 = (self.UCSR0B>>6)&1
        self.UDRIE0 = (self.UCSR0B>>5)&1
        self.RXEN0 = (self.UCSR0B>>4)&1
        self.TXEN0 = (self.UCSR0B>>3)&1
        self.UCSZ02 = (self.UCSR0B>>2)&1
        self.RXB80 = (self.UCSR0B>>1)&1
        self.TXB80 = (self.UCSR0B>>0)&1

        #USCR0C
        self.UMSEL01 = (self.USCR0C>>7)&1
        self.UMSEL00 = (self.USCR0C>>6)&1
        self.UPM01 = (self.USCR0C>>5)&1
        self.UPM00 = (self.USCR0C>>4)&1
        self.USBS0 = (self.USCR0C>>3)&1
        self.UCSZ01 = (self.USCR0C>>2)&1
        self.UCSZ00 = (self.USCR0C>>1)&1
        self.UCPOL0 = (self.USCR0C>>0)&1

        #UMSEL0 Bits Settings
        if (self.UMSEL01 == 0) and (self.UMSEL00 ==0):
            self.opp_mode = 'Asynchronous'
        elif (self.UMSEL01 == 0) and (self.UMSEL00 ==1):
            self.opp_mode = 'Synchronous'
        elif (self.UMSEL01 == 1) and (self.UMSEL00 ==0):
            self.opp_mode = 'Master SPI'
        else:
            self.opp_mode = '(Reserved)'

        UBRR = (self.UBRR0H << 8) | self.UBRR0L
        baud_limit = UBRR if UBRR > 0 else 1

        self.baud_counter += 1
        baud_tick = False
        if self.baud_counter >= baud_limit:
            self.baud_counter = 0 
            baud_tick = True

        #TX logic
        if self.TXEN0 == 1:
            if baud_tick:
                match self.tx_state:
                    case 'IDLE':
                        if self.UDRE0 == 0: #Data in bufer ready to send 
                            self.tx_shift_reg = self.TXB
                            self.UDRE0 = 1 #Buffer is now empty again
                            self.tx_state = 'START_BIT'
                            self.TXD.prepare(0) #Drive Start Bit (LOW)
                        else:
                            self.TXD.prepare(1) #Drive Idle (HIGH)
                        
                    case 'START_BIT':
                        self.tx_bits = 0
                        self.tx_state = 'DATA_BITS'
                        self.TXD.prepare(self.tx_shift_reg&1)

                    case 'DATA_BITS':
                        self.tx_shift_reg>>= 1 
                        self.tx_bits += 1 
                        if self.tx_bits < 7:
                            self.TXD.prepare(self.tx_shift_reg & 1)
                        else:
                            self.tx_state = 'STOP_BIT'
                            self.TXD.prepare(1) #Drive STOP Bit (HIGH)

                    case 'STOP_BIT':
                        self.TXC0 = 1 #Transmission Complete Flag
                        self.tx_state = 'IDLE'
                        self.TXD.prepare(1) #Back to Idle

        else:
            self.TXD.prepare(1) # default high when disabled


        #RX logic 

        if self.RXEN0 == 1:

            rx_pin = self.RXD.get()


            if baud_tick:
                match self.rx_state:
                    case 'IDLE':
                        if rx_pin == 0: # Start Bit Detected
                            self.rx_state = 'DATA_BITS'
                            self.rx_bits = 0 
                            self.rx_shift_reg = 0

                    case 'DATA_BITS':
                        self.rx_shift_reg = (self.rx_shift_reg >> 1) | (rx_pin<< 7)
                        self.rx_bits += 1
                        if self.rx_bits >= 8:
                            self.rx_state = 'STOP_BIT'

                    case 'STOP_BIT':
                        if rx_pin == 1: #Valid Stop Bit
                            self.RXB = self.rx_shift_reg
                            self.RXC0 = 1 #Receive Complete
                        self.rx_state = 'IDLE'

        # Interrupts
        self.RXC_INT.prepare(1 if(self.RXCIE0 and self.RXC0)else 0)
        self.TXC_INT.prepare(1 if(self.TXCIE0 and self.TXC0)else 0)
        self.UDRE_INT.prepare(1 if(self.UDRIE0 and self.UDRE0)else 0)                            


            