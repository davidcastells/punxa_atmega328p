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
    
    if (op == 'ADD'):
        # ADD Rd, Rr -> 0000 11rd dddd rrrr
        p0 = 0b0000
        Rd = reg_to_index(parts[1])
        Rr = reg_to_index(parts[2])
        p1 = 0b1100 | ((Rr >> 4) << 1) | (Rd>>4)
        p2 = Rd & 0xF
        p3 = Rr & 0xF
        
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]
    
    elif (op == 'BRNE'):
        # BRNE k -> 1111 01kk kkkk k001
        p0 = 0b1111
        k = get_int(parts[1])
        p1 = (1 << 2) | (k >> 5)
        p2 = (k >> 1)
        p3 = (k & 1) << 3 | 1
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]
    
    elif (op == 'CLR'):
        p0 = 0b0010
        r =  reg_to_index(parts[1]) 
    
        p1 = (1<<2) | ((r >> 4) << 1) | (r>>4)
        p2 = (r & 0xF)
        p3 = (r & 0xF)
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]
    
    elif (op == 'CPI'):
        p0 = 0b0011
        r = reg_to_index(parts[1])
        k = get_int(parts[2])
        p1 = k >> 4
        assert(r >= 16)
        p2 = r - 16
        p3 = k & 0xF
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]
    
    elif (op == 'CPSE'):
        p0 = 0b0001
        Rd =  reg_to_index(parts[1]) 
        Rr =  reg_to_index(parts[1]) 
        p1 = ((Rr >> 4) << 1) | (Rd>>4)
        p2 = (Rd & 0xF)
        p3 = (Rr & 0xF)
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]
    
    elif (op == 'INC'):
        # INC Rd --> 1001 010d dddd 0011.
        p0 = 0b1001
        Rd =  reg_to_index(parts[1]) 
        p1 = 0b0100 | (Rd >> 4)
        p2 = Rd & 0xF
        p3 = 0b0011
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]
        
    elif (op == 'LDI'):
        # LDI Rd, K -> 1110 KKKK dddd KKKK
        p0 = 0b1110
        r = reg_to_index(parts[1]) 
        off = get_int(parts[2]) & 0xFF
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
    
    elif (op == 'RCALL'):
        # RCALl k -> 1101 kkkk kkkk kkkk
        p0 = 0b1101
        k = get_int(parts[1])
        p1 = k >> 8
        p2 = (k >> 4) & 0xF
        p3 = k & 0xF
        
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]
    
    elif (op == 'RET'):
        return [0b1001_0101_0000_1000]
    
    elif (op == 'RJMP'):
        p0 = 0b1100
        off = get_int(parts[1]) 
        p1 = (off >> 8) & 0xF
        w1 = off & 0xFF
        
        return [((p0 << 12) | (p1 << 8) | w1) ]
    
    elif (op == 'OR'):
        p0 = 0b0010
        Rd = reg_to_index(parts[1])
        Rr = reg_to_index(parts[2])
        p1 = 0b1000 | ((Rr >> 4) << 1) | (Rd>>4)
        p2 = Rd & 0xF
        p3 = Rr & 0xF
        
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]

    elif (op == 'OUT'):
        p0 = 0b1011
        r = reg_to_index(parts[2])
        A = get_int(parts[1])
        p1 = (1 << 3) | (A >> 4) << 1 | (r >> 4)
        p2 = r & 0XF
        p3 = A & 0xF
        return [((p0 << 12) | (p1 << 8) | (p2 << 4) | p3) ]
        
    elif (op == 'SBRS'):
        # SBRS Rd, b -> 1111 111r rrrr 0bbb
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

def is_relative_jump(asm):
    parts = split_parts(asm.upper())
    
    if (parts[0] == 'RCALL'): return True
    if (parts[0] == 'RJMP'): return True
    if (parts[0] == 'BRNE'): return True
    if (parts[0] == 'BRBC'): return True
    
    return False

def assemble_program(program, debug=False):
    ret = []
    
    labels = []
    lines = []
    
    # Step 1: remove empty lines and comments and collect labels
    for line in program.split('\n'):
        if (';' in line):
            line = line.split(';')[0]
            
        line = line.strip()
        
        if (len(line) == 0):
            continue
        
        if (line[-1] == ':'):
            labels.append(line[:-1])
            
        lines.append(line)
            
    # Step 2: assemble substituting labels for zeros to compute label addresses 
    # also process definifions
    off = 0 
    label_address = {}
    
    for line in lines:
        if (line[-1] == ':'):
            label = line[:-1]
            label_address[label] = off
        elif ('.equ' in line.lower()):
            parts = line[5:].split('=')
            label = parts[0].strip()
            v = get_int(parts[1].strip())
            labels.append(label)
            label_address[label] = v
        else:
            # substitute the labels
            for label in labels:
                if (label in line):
                    line = line.replace(label, '0')
                
            words = assemble(line)  
            #print(line, '-', words)
            off += len(words)
            
    # Step 3: substitute labels by offsets
    off = 0 
    for line in lines:
        # ignore labels
        if (line[-1] == ':'):
            continue
        if (line[0] == '.'):
            continue
        
        for label in labels:
            if (label in line):
                add = label_address[label]
                if is_relative_jump(line):
                    add -= off + 1
                line = line.replace(label, f'{add}')
                
        print(f'0x{off:02X} -', line)
        words = assemble(line)   
        ret.extend(words)
        off += len(words)
        
        if (debug):
            sbytes = ''
            for word in words:
                sbytes += f'{word:04X} '
                
            print(f'{sbytes:20}', line)
            
    #print(label_address)
    
    return ret, label_address