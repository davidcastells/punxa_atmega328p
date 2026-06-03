import py4hw
from .UART_test_Comp import *
from punxa_atmega328p.Memory import *
from punxa_atmega328p.USART0 import *
import os
import subprocess
import time


def run_uart_test():


    sys = py4hw.HWSystem()
    USART_rx = py4hw.Wire(sys, 'USART_rx', 1)
    USART_tx = py4hw.Wire(sys, 'USART_tx', 1)
    USART_clk = py4hw.Wire(sys,'USART_clk',1)
    RXC_int0 = py4hw.Wire(sys,'RXC_int0',1)
    TXC_int0 = py4hw.Wire(sys,'TXC_int0',1)
    UDRE_int0 = py4hw.Wire(sys,'UDRE_int0',1)
    interface0 = MemoryInterface(sys,'port0',8,16)
    interface1 = MemoryInterface(sys,'port1',8,16)

    RXC_int1 = py4hw.Wire(sys,'RXC_int1',1)
    TXC_int1 = py4hw.Wire(sys,'TXC_int1',1)
    UDRE_int1 = py4hw.Wire(sys,'UDRE_int1',1)

    AVRDUDE_COMMAND = '/home/patrick/.arduino15/packages/arduino/tools/avrdude/8.0.0-arduino1/bin/avrdude -C /home/patrick/.arduino15/packages/arduino/tools/avrdude/8.0.0-arduino1/etc/avrdude.conf -v -p atmega328p -c stk500v1 -P /dev/ttyUSB0 -b 115200 -D -U flash:w:"/home/patrick/.cache/arduino/sketches/AC97C57634ABD88BF8A3E694093236AE/arithmetic_test.ino.hex":i'
    OPEN_VIRTUAL_PORT = "sudo socat PTY,link=/dev/ttyUSB0,raw,echo=0,mode=666 PTY,link=/dev/ttyV1,raw,echo=0,mode=666"

    # Open the virtual port

    #Virtual_port_process = subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{OPEN_VIRTUAL_PORT}; exec bash"])
    time.sleep(5)



    #virtual_port = VirtualPort_to_USART(sys, "VirtualUART", RXD=USART_tx,TXD=USART_rx,USART_CLK=USART_clk)
    USART0 = USART(sys,"USART0",interface0 ,USART_rx,USART_tx,USART_clk,RXC_int0,TXC_int0,UDRE_int0)
    USART1 = USART_1(sys,"USART1",interface1,USART_tx,USART_rx,USART_clk,RXC_int1,TXC_int1,UDRE_int1)


    # READ and write data form perpheral test
    ADDRESS0 = [0xC6,0xC6,0xC6,0xC6]
    INSTYPE0 = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    READ0 = [0]
    READ_DATA0 = [0]
    RESP0 = [0]
    WRITE0 = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    WRITE_DATA0 = [0xFF]

    ADDRESS1 = [0xC6,0xC6,0xC6,0xC6]
    INSTYPE1 = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    READ1 = [0]
    READ_DATA1 = [0]
    RESP1 = [0]
    WRITE1 = [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    WRITE_DATA1 = [0xFF]


    USART0.UCSR0A = 0x00
    USART0.UCSR0B = 0x18
    USART0.UCSR0C = 0x06 # 8 bits
    USART0.UBRR0L = 0x68
    USART0.UBRR0H = 0x00


    USART1.UCSR0A = 0x00
    USART1.UCSR0B = 0x18
    USART1.UCSR0C = 0x06 # 8 bits 
    USART1.UBRR0L = 0x68
    USART1.UBRR0H = 0x00



#    py4hw.Sequence(sys,'ADDRESS0',ADDRESS0,interface0.address)
#    py4hw.Sequence(sys,'INSTYPE0',INSTYPE0,interface0.instype)
#    py4hw.Sequence(sys,'READ0',READ0,interface0.read)
#    py4hw.Sequence(sys,'WRITE0',WRITE0,interface0.write)
#    py4hw.Sequence(sys,'WRITE_DATA0',WRITE_DATA0,interface0.write_data)


#    py4hw.Sequence(sys,'ADDRESS1',ADDRESS1,interface1.address)
#    py4hw.Sequence(sys,'INSTYPE1',INSTYPE1,interface1.instype)
#    py4hw.Sequence(sys,'READ1',READ1,interface1.read)
#    py4hw.Sequence(sys,'WRITE1',WRITE1,interface1.write)
#    py4hw.Sequence(sys,'WRITE_DATA1',WRITE_DATA1,interface1.write_data)

    SIGNAL = []

    SIGNAL.append(interface0.address)
    SIGNAL.append(interface0.instype)
    SIGNAL.append(interface0.read)
    SIGNAL.append(interface0.write)
    SIGNAL.append(interface0.write_data)
    
    SIGNAL.append(interface1.address)
    SIGNAL.append(interface1.instype)
    SIGNAL.append(interface1.read)
    SIGNAL.append(interface1.write)
    SIGNAL.append(interface1.write_data)

    SIGNAL.append(USART_tx)
    SIGNAL.append(USART_rx)
    SIGNAL.append(USART_clk)

    #interruts
    SIGNAL.append(RXC_int0)
    SIGNAL.append(TXC_int0)
    SIGNAL.append(UDRE_int0)

    SIGNAL.append(RXC_int1)
    SIGNAL.append(TXC_int1)
    SIGNAL.append(UDRE_int1)

    wvf = py4hw.Waveform(sys,'wvf',SIGNAL)

    # Test the functionality
    # Launch the Avrdude command

    #process = subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{AVRDUDE_COMMAND}; exec bash"])
    #for i in range(50000):
    #    sys.getSimulator().clk(1)


    #prepare
    interface0.address.put(0xC6)
    interface0.instype.put(1)
    interface0.read.put(0)
    interface0.write.put(1)
    interface0.write_data.put(0xAA)
    sys.getSimulator().clk(1)
    interface0.address.put(0xC6)
    interface0.instype.put(1)
    interface0.read.put(0)
    interface0.write.put(1)
    interface0.write_data.put(0xAA)
    sys.getSimulator().clk(2)
    print("TXB_buffer:{}".format(USART0.TXB_buffer))
    #wvf.gui()
    interface0.address.put(0)
    interface0.instype.put(0)
    interface0.read.put(0)
    interface0.write.put(0)
    interface0.write_data.put(0)
    sys.getSimulator().clk(2)
    

    while 1:
        n = input()

        print("State of the TB")
        print("UCSR0A:{} UCSR0B:{} USCR0C:{} UBRR0L:{} UBRR0H:{}".format(USART0.UCSR0A,USART0.UCSR0B,USART0.UCSR0C,USART0.UBRR0L,USART0.UBRR0H))
        print("USART_TX:{} USART_RX:{} USART_CLK:{}".format(USART_tx.get(),USART_rx.get(),USART_clk.get()))
        print("UCSR0A:{} UCSR0B:{} USCR0C:{} UBRR0L:{} UBRR0H:{}".format(USART1.UCSR0A,USART1.UCSR0B,USART1.UCSR0C,USART1.UBRR0L,USART1.UBRR0H))
        print("TxState:{}".format(USART0.tx_state))
        print("Ticks_per_bit:{}".format(USART0.ticks_per_bit))

        print("Read_buffer{}".format(USART1.readBuffer))
        if n =='s':
           break 
        
        if n == 'n':
            sys.getSimulator().clk(53)
        

    wvf.gui()









if __name__ == "__main__":
    run_uart_test()

