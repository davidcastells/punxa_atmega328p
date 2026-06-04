# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:21:50 2026

@author: dcr
"""

import re

def split_parts(s):
    parts = re.split('[, ()]', s)
    ret = []
    
    for part in parts:
        if len(part)>0:
            ret.append(part)
            
    return ret

def reg_to_index(reg):
    reg = reg.lower()
    if (reg[0] == 'r'): return int(reg[1:])
    raise Exception(f'unknown register {reg}')
    
def get_int(v):
    if (isinstance(v, int)):
        return v
    if (isinstance(v, str)):
        if (v[0:2] == '0x'):
            return int(v, 16)
        else:
            return int(v)
    
def parts_to_ins(parts):
    
    op = parts[0].upper()
    
    if (op == 'LDI'):
        p0 = 0b1110
        r = reg_to_index(parts[1]) 
        off = get_int(parts[2])
        p1 = off >> 4
        p2 = (r - 16) 
        p3 = off & 0xF
    
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]


    elif (op == 'LDS'):
        p0 = 0b1001
        r = reg_to_index(parts[1])
        p1 = 0b0000 | (r >> 4)
        p2 = r & 0xF
        p3 = 0
        w1 = get_int(parts[2]) >> 8
        w2 = get_int(parts[2]) & 0xFF
        
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) , ((w1 << 8) | w2 )]
    
    elif (op == 'RJMP'):
        p0 = 0b1100
        off = get_int(parts[1]) 
        p1 = (off >> 8) & 0xF
        w1 = off & 0xFF
        
        return [((p0 << 12) | (p1 << 8) | w1)]
        
    elif (op == 'SBRS'):
        p0 = 0b1111
        r = reg_to_index(parts[1])
        p1 = 0b1110 | (r >> 4)
        p2 = r & 0xF
        p3 = get_int(parts[2])
        
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]
    
    elif (op == 'STS'):
        p0 = 0b1001
        r = reg_to_index(parts[2])
        p1 = 0b0010 | (r >> 4)
        p2 = r & 0xF
        p3 = 0
        w1 = get_int(parts[1]) >> 8
        w2 = get_int(parts[1]) & 0xFF
    
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) , ((w1 << 8) | w2 )]
    
    else:
        raise Exception(f'{op} not supported')
    
    return
    
def assemble(asm):
    ret = 0
    
    ret = parts_to_ins(split_parts(asm))
    
    
    return ret 


def assemble_program(program, debug=False):
    ret = []
    
    for line in program.split('\n'):
        if (';' in line):
            line = line.split(';')[0]
            
        line = line.strip()
        
        if (len(line) == 0):
            continue
        
        #print('line:', line)
        bytes = assemble(line)   
        ret.extend(bytes)
        
        if (debug):
            sbytes = ''
            for byte in bytes:
                sbytes += f'{byte:02X} '
                
            print(f'{sbytes:20}', line)
            
        
    return ret