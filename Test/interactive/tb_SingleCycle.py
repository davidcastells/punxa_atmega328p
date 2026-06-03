# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:56:55 2026

@author: dcr
"""

import py4hw

import punxa_atmega328p as punxa

#from punxa_atmega328p.single_cycle.singlecycle_processor import SingleCycleATmega328P
#from punxa_atmega328p.Memory import MemoryInterface
#from punxa_atmega328p.Memory import Memory
#from punxa_atmega328p.Memory import Memory

hw = py4hw.HWSystem()

dw = 8 
aw = 16

# Memory Map
# 0x0 - 0x1r   GP Registers r0-r31
# 0x0020 - 0x005F   I/O registers
# 0x0060 - 0x00FF   Extended I/O Registers
#   0x00C0 - 0x00C6    USART
# 0x0100 - 0x08FF   Internal SRAM

cpu_p = punxa.MemoryInterface(hw, 'cpu', dw, aw)
reg_p = punxa.MemoryInterface(hw, 'reg', dw, 5)         # 2^5 = 32 registers
usart_p = punxa.MemoryInterface(hw, 'usart', dw, 3)     # 2^3 = 8 registers
mem_p = punxa.MemoryInterface(hw, 'mem', dw, 11)        # 2048 bytes


punxa.MultiplexedBus(hw, 'bus', cpu_p, [(reg_p, 0x0), (usart_p, 0xC0), (mem_p, 0x100)])

cpu = punxa.SingleCycleATmega328P(hw, 'cpu', cpu_p)
reg = punxa.Ram_Memory(hw, 'reg', dw, 5, reg_p)
mem = punxa.Ram_Memory(hw, 'men', dw, 11, mem_p)
usart = punxa.VirtualUSART(hw, 'usart', usart_p)

py4hw.gui.Workbench(hw)