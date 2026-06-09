; ============================================================
; NOP (No Operation) test suite
; ============================================================
; Tests that NOP correctly:
; 1. Does not modify any registers
; 2. Does not modify any flags
; 3. Does not modify SRAM or I/O
; 4. Does not affect stack or program flow
; 5. Simply consumes 1 cycle and advances PC by 1
; ============================================================
; NOP is a 1-word (16-bit) instruction
; Format: 0000 0000 0000 0000 (0x0000)
; Operation: None (PC <- PC + 1)
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D
.equ GPIOR0 = 0x1E
.equ DATA_START = 0x0200

reset:
    ; Initialize stack pointer
    ldi r16, high(0x08FF)
    out SPH, r16
    ldi r16, low(0x08FF)
    out SPL, r16

    ldi r16, 1
    sts test_case, r16
    sts final_result, r16

    rjmp test1_start

; ============================================================
; TEST 1: NOP does not affect register values
; ============================================================
test1_start:
    ldi r16, 0x42
    ldi r17, 0x55
    ldi r18, 0xAA
    
    ; Insert NOPs
    nop
    nop
    nop
    
    ; Registers should be unchanged
    cpi r16, 0x42
    brne fail
    cpi r17, 0x55
    brne fail
    cpi r18, 0xAA
    brne fail
    rcall inc_case
    rjmp test2_start

; ============================================================
; TEST 2: NOP does not affect flags (C flag)
; ============================================================
test2_start:
    clc                 ; C=0
    nop
    brcs fail           ; Should not branch
    
    sec                 ; C=1
    nop
    brcc fail           ; Should not branch
    
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: NOP does not affect flags (Z flag)
; ============================================================
test3_start:
    ; Z=1 case
    ldi r16, 0
    tst r16             ; Z=1
    nop
    brne fail           ; Should not branch
    
    ; Z=0 case
    ldi r16, 1
    tst r16             ; Z=0
    nop
    breq fail           ; Should not branch
    
    rcall inc_case
    rjmp test4_start

; ============================================================
; TEST 4: NOP does not affect flags (N flag)
; ============================================================
test4_start:
    ; N=1 case
    ldi r16, 0x80
    tst r16             ; N=1
    nop
    brpl fail           ; Should not branch
    
    ; N=0 case
    ldi r16, 0x7F
    tst r16             ; N=0
    nop
    brmi fail           ; Should not branch
    
    rcall inc_case
    rjmp test5_start

; ============================================================
; TEST 5: NOP does not affect flags (V flag)
; ============================================================
test5_start:
    ; V=1 case (overflow)
    ldi r16, 0x7F
    ldi r17, 1
    add r16, r17        ; 127+1=128, overflow V=1
    nop
    brvc fail           ; Should not branch
    
    ; V=0 case
    clv                 ; Clear V
    nop
    brvs fail           ; Should not branch
    
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6: NOP does not affect flags (H flag)
; ============================================================
test6_start:
    ; H=1 case (half carry)
    ldi r16, 0x0F
    ldi r17, 1
    add r16, r17        ; 0x0F+1=0x10, H=1
    nop
    brhc fail           ; Should not branch
    
    ; H=0 case
    clh                 ; Clear H
    nop
    brhs fail           ; Should not branch
    
    rcall inc_case
    rjmp test7_start

; ============================================================
; TEST 7: NOP does not affect flags (T flag)
; ============================================================
test7_start:
    ; T=1 case
    set                 ; T=1
    nop
    brtc fail           ; Should not branch
    
    ; T=0 case
    clt                 ; T=0
    nop
    brts fail           ; Should not branch
    
    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8: NOP does not affect flags (I flag)
; ============================================================
test8_start:
    ; I=1 case
    sei                 ; I=1
    nop
    brid fail           ; Should not branch
    
    ; I=0 case
    cli                 ; I=0
    nop
    brie fail           ; Should not branch
    
    ; Restore I=1 for rest of tests
    sei
    rcall inc_case
    rjmp test9_start

; ============================================================
; TEST 9: NOP does not affect SRAM
; ============================================================
test9_start:
    ldi r16, 0xDE
    sts DATA_START, r16
    
    nop
    nop
    nop
    
    lds r17, DATA_START
    cpi r17, 0xDE
    brne fail
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10: NOP does not affect I/O registers
; ============================================================
test10_start:
    ldi r16, 0xAD
    out GPIOR0, r16
    
    nop
    nop
    
    in r17, GPIOR0
    cpi r17, 0xAD
    brne fail
    rcall inc_case
    rjmp test11_start

; ============================================================
; TEST 11: NOP does not affect stack pointer
; ============================================================
test11_start:
    in r16, SPL
    in r17, SPH
    
    nop
    nop
    nop
    
    in r18, SPL
    in r19, SPH
    
    cp r16, r18
    brne fail
    cp r17, r19
    brne fail
    rcall inc_case
    rjmp test12_start

; ============================================================
; TEST 12: NOP does not affect program counter flow (non-branch)
; ============================================================
test12_start:
    ldi r16, 0
    nop
    inc r16
    nop
    inc r16
    nop
    inc r16
    
    cpi r16, 3
    brne fail
    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13: NOP used in delay loop (doesn't corrupt loop counter)
; ============================================================
test13_start:
    ldi r16, 5
delay_loop:
    nop
    nop
    nop
    dec r16
    brne delay_loop
    
    cpi r16, 0
    brne fail
    rcall inc_case
    rjmp test14_start

; ============================================================
; TEST 14: NOP does not affect push/pop operations
; ============================================================
test14_start:
    ldi r16, 0xCA
    push r16
    nop
    nop
    pop r17
    
    cpi r17, 0xCA
    brne fail
    rcall inc_case
    rjmp test15_start

; ============================================================
; TEST 15: Multiple NOPs in sequence
; ============================================================
test15_start:
    ldi r16, 0x12
    ldi r17, 0x34
    
    nop
    nop
    nop
    nop
    nop
    
    cpi r16, 0x12
    brne fail
    cpi r17, 0x34
    brne fail
    rcall inc_case
    rjmp test16_start

; ============================================================
; TEST 16: NOP before conditional branch (does not affect condition)
; ============================================================
test16_start:
    ldi r16, 10
    ldi r17, 10
    cp r16, r17        ; Z=1
    nop
    breq branch_taken16
    rjmp fail
branch_taken16:
    
    ldi r16, 10
    ldi r17, 20
    cp r16, r17        ; Z=0
    nop
    brne branch_taken16b
    rjmp fail
branch_taken16b:
    
    rcall inc_case
    rjmp test17_start

; ============================================================
; TEST 17: NOP after CALL (does not affect return)
; ============================================================
test17_start:
    ldi r16, 0
    rcall nop_sub17
    cpi r16, 1
    brne fail
    rcall inc_case
    rjmp test18_start

nop_sub17:
    nop
    nop
    inc r16
    ret

; ============================================================
; TEST 18: NOP before RET (does not affect stack)
; ============================================================
test18_start:
    rcall ret_sub18
    rcall inc_case
    rjmp test19_start

ret_sub18:
    push r16
    ldi r16, 0x55
    nop
    nop
    pop r16
    ret

; ============================================================
; TEST 19: NOP with SREG preservation
; ============================================================
test19_start:
    ; Set all flags to specific pattern
    cli
    clt
    clh
    clv
    cln
    clz
    clc
    
    nop
    nop
    
    ; Verify all flags still clear
    brid fail
    brtc ok_t19
    rjmp fail
ok_t19:
    brhc ok_h19
    rjmp fail
ok_h19:
    brvc ok_v19
    rjmp fail
ok_v19:
    brpl ok_n19
    rjmp fail
ok_n19:
    brne ok_z19
    rjmp fail
ok_z19:
    brcc ok_c19
    rjmp fail
ok_c19:
    
    rcall inc_case
    rjmp test20_start

; ============================================================
; TEST 20: NOP encoding verification (indirect)
; ============================================================
test20_start:
    ; NOP is 0x0000. If a NOP is executed, it should not crash
    ; and should continue to next instruction
    ldi r16, 0x00
    nop
    inc r16
    nop
    inc r16
    
    cpi r16, 2
    brne fail
    rcall inc_case
    rjmp success

; ============================================================
; SUCCESS / FAILURE logic
; ============================================================
success:
    ldi r16, 1
    sts final_result, r16
end:
    rjmp end

fail:
    ldi r16, 255
    sts final_result, r16
    rjmp end

inc_case:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret