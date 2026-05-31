import py4hw
import serial 
import os 


class VirtualPort_to_USART(py4hw.Logic):
    def __init__(self, parent, name: str, RXD, TXD, USART_CLK):
        super().__init__(parent, name)

        # Physical Pins
        self.RXD = self.addIn('RXD', RXD)
        self.TXD = self.addOut('TXD', TXD)
        self.USART_CLK = self.addIn('USART_CLK', USART_CLK)

        v_port = "/dev/ttyV1"
        v_baud = 115200

        # Virtual Serial Port Configuration
        self.v_serial = None
        if v_port:
            try:
                # timeout=0 makes reads non-blocking so it doesn't freeze the simulation clock
                self.v_serial = serial.Serial(v_port, v_baud, timeout=0)
            except Exception as e:
                print(f"Warning: Could not open virtual serial port {v_port}: {e}")

        self._v_tx_byte = 0

        self.TXD_val = 1
        self.RXC_INT_val = 0
        self.TXC_INT_val = 0
        self.USART_CLK_val = 0
        self.UDRE_INT_val = 0

        self.UCSR0A = 0x20  # Bit5: UDRE0 is 1 by default (Buffer Empty)
        self.UCSR0B = 0x18  # Enable RXEN0 (Bit 4) and TXEN0 (Bit 3) by default for bridge mode
        self.USCR0C = 0x06  # Default: Async, No parity, 1 stop bit, 8 data bits
        self.UBRR0L = 0
        self.UBRR0H = 0

        # Internal Data Buffers
        self.RXB_buffer = 0
        self.readBuffer = 0
        self.TXB_buffer = 0
        self.TXB_full = False

        # Control & Status Bits
        # UCSR0A
        self.RXC0 = 0 
        self.TXC0 = 0
        self.UDRE0 = 1  
        self.FE0 = 0
        self.DOR0 = 0
        self.UPE0 = 0
        self.U2X0 = 0
        self.MPCM0 = 0

        # UCSR0B
        self.RXCIE0 = 0
        self.TXCIE0 = 0
        self.UDRIE0 = 0
        self.RXEN0 = 1
        self.TXEN0 = 1
        self.UCSZ02 = 0
        self.RXB80 = 0
        self.TXB80 = 0

        # UCSR0C
        self.UMSEL01 = 0
        self.UMSEL00 = 0
        self.UPM01 = 0
        self.UPM00 = 0
        self.USBS0 = 0
        self.UCSZ01 = 1
        self.UCSZ00 = 1
        self.UCPOL0 = 0

        self.opp_mode = 'Asynchronous'
        self.nbBits = 8
        self.nbStopBits = 1
        self.ParityMode = 'Disabled'

        # Transmit/Receive State Machines
        self.baud_counter = 0
        self.tx_state = 'IDLE'  
        self.tx_shift_reg = 0
        self.tx_bits_left = 0
        self.tx_stop_cnt = 0
        self.tx_parity = 0
        self.tx_tick_cnt = 0
        
        self.rx_state = 'IDLE'  
        self.rx_shift_reg = 0
        self.rx_bits_rcvd = 0
        self.rx_stop_cnt = 0
        self.rx_tick_cnt = 0
        self.rx_parity = 0 
        self.rx_fe = 0
        self.rx_upe = 0
        
        self.rx_shift_reg_full = False
        self.baud_Tick = False
        self.tickCounter = 0

    def Parse_control_registers(self):
        # UCSR0A
        self.RXC0 = (self.UCSR0A >> 7) & 1
        self.TXC0 = (self.UCSR0A >> 6) & 1
        self.UDRE0 = (self.UCSR0A >> 5) & 1  
        self.FE0 = (self.UCSR0A >> 4) & 1
        self.DDR0 = (self.UCSR0A >> 3) & 1
        self.UPE0 = (self.UCSR0A >> 2) & 1
        self.U2X0 = (self.UCSR0A >> 1) & 1
        self.MPCM0 = (self.UCSR0A >> 0) & 1

        # UCSR0B
        self.RXCIE0 = (self.UCSR0B >> 7) & 1
        self.TXCIE0 = (self.UCSR0B >> 6) & 1
        self.UDRIE0 = (self.UCSR0B >> 5) & 1
        self.RXEN0 = (self.UCSR0B >> 4) & 1
        self.TXEN0 = (self.UCSR0B >> 3) & 1
        self.UCSZ02 = (self.UCSR0B >> 2) & 1
        self.RXB80 = (self.UCSR0B >> 1) & 1
        self.TXB80 = (self.UCSR0B >> 0) & 1

        # USCR0C
        self.UMSEL01 = (self.USCR0C >> 7) & 1
        self.UMSEL00 = (self.USCR0C >> 6) & 1
        self.UPM01 = (self.USCR0C >> 5) & 1
        self.UPM00 = (self.USCR0C >> 4) & 1
        self.USBS0 = (self.USCR0C >> 3) & 1
        self.UCSZ01 = (self.USCR0C >> 2) & 1
        self.UCSZ00 = (self.USCR0C >> 1) & 1
        self.UCPOL0 = (self.USCR0C >> 0) & 1

        # Composed fields
        self.UBRR0 = ((self.UBRR0H & 0xF) << 8) | self.UBRR0L
        self.UCSZ = (self.UCSZ02 << 2) | (self.UCSZ01 << 1) | (self.UCSZ00 << 0) 
        self.UMSEL = (self.UMSEL01 << 1) | self.UMSEL00
        self.UPM = (self.UPM01 << 1) | self.UPM00

    def update_UCSR0A(self):
        self.UCSR0A = (
            (self.RXC0 << 7 ) |
            (self.TXC0 << 6 ) |
            (self.UDRE0 << 5) |
            (self.FE0 << 4  ) |
            (self.DDR0 << 3 ) |
            (self.UPE0 << 2 ) |
            (self.U2X0 << 1 ) |
            (self.MPCM0 << 0)
        )

    def setSettings(self): 
        match self.UCSZ:
            case 0: self.nbBits = 5
            case 1: self.nbBits = 6
            case 2: self.nbBits = 7
            case 3: self.nbBits = 8
            case 7: self.nbBits = 9
            case _: self.nbBits = 8   

        self.nbStopBits = 2 if self.USBS0 else 1

        match self.UMSEL:
            case 0: self.opp_mode = 'Asynchronous'
            case 1: self.opp_mode = 'Synchronous'
            case 2: self.opp_mode = 'Master SPI'
            case _: self.opp_mode = '(Reserved)'

        match self.UPM:
            case 0: self.ParityMode = 'Disabled'
            case 2: self.ParityMode = 'even'
            case 3: self.ParityMode = 'odd'
            case _: self.ParityMode = 'Disabled'

    def Clock_Generator(self):
        self.baud_Tick = False
        if self.tickCounter >= self.UBRR0:
            self.baud_Tick = True
            self.tickCounter = 0 
        else:
            self.tickCounter += 1

        self.tickCounter += 1 
        self.tickCounter &= 0xFFFF 
        self.USART_CLK_val = 1 if self.baud_Tick else 0

    def TX_logic(self):
        if self.baud_Tick == True:
            if self.TXEN0 == 1: 
                if self.opp_mode == 'Asynchronous':
                    ticks_per_bit = 8 if self.U2X0 else 16
                else:
                    ticks_per_bit = 2

                if self.TXB_full:
                    match self.tx_state:
                        case 'IDLE':
                            self.TXD_val = 1
                            if self.TXB_full:
                                self.tx_shift_reg = self.TXB_buffer
                                self._v_tx_byte = self.TXB_buffer

                                self.TXB_full = False
                                self.TXB_buffer = 0 
                                self.UDRE0 = 1
                                self.update_UCSR0A()

                                if self.nbBits == 9:
                                    self.tx_shift_reg |= (self.TXB80 << 8)
                                self.tx_bits_left = self.nbBits

                                mask = (1 << self.nbBits) - 1
                                self.tx_parity = bin(self.tx_shift_reg & mask).count('1') & 1
                                self.tx_stop_cnt = self.nbStopBits
                                self.tx_tick_cnt = 0
                                self.tx_state = 'START'
                        
                        case 'START':
                            self.TXD_val = 0
                            self.tx_tick_cnt += 1
                            if self.tx_tick_cnt >= ticks_per_bit:
                                self.tx_tick_cnt = 0
                                self.tx_state = 'DATA'

                        case 'DATA':
                            self.tx_tick_cnt += 1
                            if self.tx_tick_cnt >= ticks_per_bit:
                                self.tx_tick_cnt = 0
                                self.TXD_val = self.tx_shift_reg & 1                         
                                self.tx_shift_reg >>= 1
                                self.tx_bits_left -= 1 

                                if self.tx_bits_left == 0:
                                    if self.ParityMode != 'Disabled':
                                        self.tx_state = 'PARITY'
                                    else:
                                        self.tx_state = 'STOP'

                        case 'PARITY':
                            self.tx_tick_cnt += 1
                            if self.tx_tick_cnt >= ticks_per_bit:
                                self.tx_tick_cnt = 0
                                if self.ParityMode == 'even':
                                    self.TXD_val = self.tx_parity
                                else:
                                    self.TXD_val = self.tx_parity ^ 1
                                self.tx_state = 'STOP'

                        case 'STOP':
                            self.TXD_val = 1
                            self.tx_tick_cnt += 1
                            if self.tx_tick_cnt >= ticks_per_bit:
                                self.tx_tick_cnt = 0
                                self.tx_stop_cnt -= 1
                                if self.tx_stop_cnt == 0:
                                    self.TXC0 = 1
                                    self.update_UCSR0A()
                                    self.tx_state = 'IDLE'
                else:
                    self.TXD_val = 1
                    self.tx_state = 'IDLE' 

    def RX_logic(self):
        if self.baud_Tick == True:
            if self.RXEN0 == 1: 
                if self.opp_mode == 'Asynchronous':
                    ticks_per_bit = 8 if self.U2X0 else 16
                else:
                    ticks_per_bit = 2

                sample_tick = ticks_per_bit >> 2 
                rxd = self.RXD.get() & 1 

                match self.rx_state:
                    case 'IDLE':
                        if rxd == 0:
                            self.rx_tick_cnt = 0 
                            self.rx_shift_reg = 0
                            self.rx_bits_rcvd = 0 
                            self.rx_parity = 0
                            self.rx_fe = 0
                            self.rx_upe = 0
                            self.rx_state = 'START'

                    case 'START':
                        self.rx_tick_cnt += 1
                        if self.rx_tick_cnt == sample_tick:
                            if rxd == 1:
                                self.rx_state = 'IDLE'
                            else:
                                self.rx_state = 'DATA'
                                self.rx_tick_cnt = 0
                        
                    case 'DATA':
                        self.rx_tick_cnt += 1
                        if self.rx_tick_cnt == ticks_per_bit:
                            self.rx_tick_cnt = 0
                            bit = rxd 
                            self.rx_shift_reg |= (bit << self.rx_bits_rcvd)
                            self.rx_parity ^= bit 
                            self.rx_bits_rcvd += 1
                            if self.rx_bits_rcvd == self.nbBits:
                                if self.ParityMode != 'Disabled':
                                    self.rx_state = 'PARITY'
                                else:
                                    self.rx_stop_cnt = self.nbStopBits
                                    self.rx_state = 'STOP'

                    case 'PARITY':
                        self.rx_tick_cnt += 1
                        if self.rx_tick_cnt == ticks_per_bit:
                            self.rx_tick_cnt = 0
                            parity_bit = rxd 
                            expected_even = self.rx_parity
                            expected_odd = self.rx_parity ^ 1
                            if (self.ParityMode == 'even') and (parity_bit != expected_even):
                                self.rx_upe = 1
                            elif (self.ParityMode == 'odd') and (parity_bit != expected_odd):
                                self.rx_upe = 1 
                            self.rx_stop_cnt = self.nbStopBits
                            self.rx_state = 'STOP'

                    case 'STOP':
                        self.rx_tick_cnt += 1 
                        if self.rx_tick_cnt == ticks_per_bit:
                            self.rx_tick_cnt = 0
                            stop_bit = rxd
                            self.rx_stop_cnt -= 1

                            if stop_bit != 1:
                                self.rx_fe = 1

                            if self.rx_stop_cnt == 0:
                                assembled_byte = self.rx_shift_reg & 0xFF
                                
                                # Send the physical line's reconstructed byte back to AVRDUDE
                                if self.v_serial and self.v_serial.is_open:
                                    self.v_serial.write(bytes([assembled_byte]))
                                    
                                self.rx_state = 'IDLE'
            else:
                self.rx_state = 'IDLE'

    def update_interrupts(self):
        self.RXC_INT_val = 1 if (self.RXCIE0 and self.RXC0) else 0 
        self.TXC_INT_val = 1 if (self.TXCIE0 and self.TXC0) else 0
        self.UDRE_INT_val = 1 if (self.UDRIE0 and self.UDRE0) else 0

    def Virtual_RX_logic(self):
        """ Reads bytes sent by AVRDUDE and passes them out onto the physical TXD wire line """
        if self.v_serial and self.v_serial.is_open and self.TXEN0 == 1:
            if not self.TXB_full and self.v_serial.in_waiting > 0:
                in_data = self.v_serial.read(1)
                if in_data:
                    self.TXB_buffer = in_data[0]
                    self.TXB_full = True

    def update_Outputs(self):
        self.TXD.prepare(self.TXD_val)

    def clock(self):
        self.Parse_control_registers() 
        self.setSettings()             
        self.Clock_Generator()         

        # Update bridge state machines
        self.TX_logic()
        self.RX_logic()
        self.Virtual_RX_logic() 

        self.update_interrupts()
        self.update_Outputs()