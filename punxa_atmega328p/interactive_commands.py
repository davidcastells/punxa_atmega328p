# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 11:33:21 2026

@author: dcr
"""

from .csr import *

_ci_hw = None
_ci_cpu = None

def list_commands():
    print('punxa interactive commands:')
    #print('  loadProgram - load a program (elf) in memory')
    #print('  checkpoint  - save the system state in a file')
    #print('  restore     - restore the system state from a file')
    #print('  run         - run the system for a number of cycles')
    print('  step        - run an instruction step')
    #print('  tbreak      - set a temporal breakpoint')
    #print('  go          - run until the temporal breakpoint')
    #print('  regs        - display the registers of the processor')
    #print('  reportCSR   - display the content of CSRs')
    print('  console     - display the content of the console')
    #print('  stack       - display the stack from [current] thread')
    #print('  memoryMap   - display the memory map')
    #print('  dump        - dump (binary/ascii) the content of memory locations')
    #print('  pageTables  - displays the page tables ')
    #print('  write_trace - exports function call traces')
    #print('  tlb         - display the content of the tlb')

def step(steps = 1):
    import time
    sim = _ci_hw.getSimulator()
    sim.do_run = True
    count = 0
    last_instret = _ci_cpu.getCSR(CSR_INSTRET)
    inst_to_stop = last_instret + steps
    
    if (steps >= 100):
        t0 = time.time()
        clk0 = sim.total_clks        
        
        
    while (_ci_cpu.getCSR(CSR_INSTRET) < inst_to_stop and sim.do_run == True ):
        sim.clk(1)
        
        cur_instret = _ci_cpu.getCSR(CSR_INSTRET)
        if (cur_instret == last_instret):
            count += 1
            if (count > 100):
                raise Exception('Too many cycles waiting to complete instruction')
        else:
            last_instret = cur_instret
            count = 0
        
                    
    if (steps >= 100):
        tf = time.time()
        clkf = sim.total_clks
        
        if (tf != t0):    
            freq = (clkf-clk0)/(tf-t0)
        else:
            freq = '?'
            
        print('clks: {} time: {} simulation freq: {}'.format(clkf-clk0, tf-t0, freq))
       