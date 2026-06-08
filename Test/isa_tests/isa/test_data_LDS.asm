; ============================================================
; LDS (Load Direct from Data Space) test suite
; ============================================================
; Tests that LDS correctly:
; 1. Loads data from any SRAM address (0x0000-0x08FF)
; 2. Works with all registers R0-R31
; 3. Does not modify any flags
; ============================================================
; LDS is a 2-word (32-bit) instruction
; Format: Word1: 1001 000d dddd 0000
;         Word2: kkkk kkkk kkkk kkkk (16-bit address)
; Operation: Rd <- [k]
; Range: Full 64KB data space (2KB SRAM on ATmega328P)
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D
.equ DATA_START = 0x0200
.equ EXT_ADDR = 0x08FF

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
; TEST 1: LDS to R16 from low SRAM address
; ============================================================
test1_start:
    ; Prepare test data
    ldi r16, 0x42
    sts DATA_START, r16
    
    ; Load using LDS
    lds r17, DATA_START
    cpi r17, 0x42
    brne fail
    rcall inc_case
    rjmp test2_start

; ============================================================
; TEST 2: LDS to R0 (lowest register)
; ============================================================
test2_start:
    ldi r16, 0xAA
    sts DATA_START+1, r16
    
    lds r0, DATA_START+1
    cpi r0, 0xAA
    brne fail
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: LDS to R31 (highest register)
; ============================================================
test3_start:
    ldi r16, 0xBB
    sts DATA_START+2, r16
    
    lds r31, DATA_START+2
    cpi r31, 0xBB
    brne fail
    rcall inc_case
    rjmp test4_start

; ============================================================
; TEST 4: LDS from maximum SRAM address (0x08FF)
; ============================================================
test4_start:
    ldi r16, 0xCC
    sts EXT_ADDR, r16
    
    lds r17, EXT_ADDR
    cpi r17, 0xCC
    brne fail
    rcall inc_case
    rjmp test5_start

; ============================================================
; TEST 5: LDS from minimum SRAM address (0x0100)
; ============================================================
test5_start:
    ldi r16, 0xDD
    sts 0x0100, r16
    
    lds r17, 0x0100
    cpi r17, 0xDD
    brne fail
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6: LDS with value 0x00
; ============================================================
test6_start:
    ldi r16, 0x00
    sts DATA_START+3, r16
    
    lds r17, DATA_START+3
    cpi r17, 0x00
    brne fail
    rcall inc_case
    rjmp test7_start

; ============================================================
; TEST 7: LDS with value 0xFF
; ============================================================
test7_start:
    ldi r16, 0xFF
    sts DATA_START+4, r16
    
    lds r17, DATA_START+4
    cpi r17, 0xFF
    brne fail
    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8: LDS does not modify flags
; ============================================================
test8_start:
    ; Set all flags
    sec                 ; C=1
    sez                 ; Z=1
    sen                 ; N=1
    sev                 ; V=1
    seh                 ; H=1
    set                 ; T=1
    
    ; LDS should preserve flags
    lds r16, DATA_START+4
    
    ; Verify all flags still set
    brcc fail
    brne fail
    brmi fail
    brvs fail
    brhc fail
    brtc fail
    
    rcall inc_case
    rjmp test9_start

; ============================================================
; TEST 9: LDS from overlapping addresses
; ============================================================
test9_start:
    ldi r16, 0x11
    sts DATA_START+5, r16
    ldi r16, 0x22
    sts DATA_START+6, r16
    
    lds r17, DATA_START+5
    lds r18, DATA_START+6
    
    cpi r17, 0x11
    brne fail
    cpi r18, 0x22
    brne fail
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10: LDS then modify loaded register
; ============================================================
test10_start:
    ldi r16, 0x10
    sts DATA_START+7, r16
    
    lds r17, DATA_START+7
    inc r17
    cpi r17, 0x11
    brne fail
    
    ; Verify SRAM unchanged
    lds r18, DATA_START+7
    cpi r18, 0x10
    brne fail
    rcall inc_case
    rjmp test11_start

; ============================================================
; TEST 11: LDS into register used as pointer
; ============================================================
test11_start:
    ldi r16, 0x99
    sts DATA_START+8, r16
    ldi r16, 0x88
    sts DATA_START+9, r16
    
    lds r26, DATA_START+8   ; X low byte
    lds r27, DATA_START+9   ; X high byte
    
    cpi r26, 0x99
    brne fail
    cpi r27, 0x88
    brne fail
    rcall inc_case
    rjmp test12_start

; ============================================================
; TEST 12: Multiple LDS from same address
; ============================================================
test12_start:
    ldi r16, 0x77
    sts DATA_START+10, r16
    
    lds r17, DATA_START+10
    lds r18, DATA_START+10
    lds r19, DATA_START+10
    
    cpi r17, 0x77
    brne fail
    cpi r18, 0x77
    brne fail
    cpi r19, 0x77
    brne fail
    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13: LDS from I/O space address (0x20-0x5F mapping)
; ============================================================
test13_start:
    ; GPIOR0 is at I/O 0x1E, SRAM 0x3E
    ldi r16, 0x5A
    sts 0x003E, r16     ; Write via SRAM address
    
    lds r17, 0x003E     ; Read via LDS
    cpi r17, 0x5A
    brne fail
    rcall inc_case
    rjmp test14_start

; ============================================================
; TEST 14: LDS then store back with STS
; ============================================================
test14_start:
    ldi r16, 0x12
    sts DATA_START+11, r16
    
    lds r17, DATA_START+11
    inc r17
    sts DATA_START+12, r17
    
    lds r18, DATA_START+12
    cpi r18, 0x13
    brne fail
    rcall inc_case
    rjmp test15_start

; ============================================================
; TEST 15: LDS within a loop (array read)
; ============================================================
test15_start:
    ; Initialize array
    ldi r16, 1
    sts DATA_START+16, r16
    ldi r16, 2
    sts DATA_START+17, r16
    ldi r16, 3
    sts DATA_START+18, r16
    ldi r16, 4
    sts DATA_START+19, r16
    
    ldi r20, 0
    ldi r21, 4
    ldi r22, 16
    
test15_loop:
    lds r23, DATA_START+16
    add r20, r23
    inc r22
    dec r21
    brne test15_loop
    
    cpi r20, 10         ; 1+2+3+4 = 10
    brne fail
    rcall inc_case
    rjmp test16_start

; ============================================================
; TEST 16: LDS across page boundary (0x02FF to 0x0300)
; ============================================================
test16_start:
    ldi r16, 0xAB
    sts 0x02FF, r16
    ldi r16, 0xCD
    sts 0x0300, r16
    
    lds r17, 0x02FF
    lds r18, 0x0300
    
    cpi r17, 0xAB
    brne fail
    cpi r18, 0xCD
    brne fail
    rcall inc_case
    rjmp test17_start

; ============================================================
; TEST 17: LDS to all register types in sequence
; ============================================================
test17_start:
    ldi r16, 0xAA
    sts DATA_START+20, r16
    
    lds r0, DATA_START+20
    lds r16, DATA_START+20
    lds r31, DATA_START+20
    
    cpi r0, 0xAA
    brne fail
    cpi r16, 0xAA
    brne fail
    cpi r31, 0xAA
    brne fail
    rcall inc_case
    rjmp test18_start

; ============================================================
; TEST 18: LDS from addresses with pattern
; ============================================================
test18_start:
    ldi r16, 0x55
    sts DATA_START+32, r16
    ldi r16, 0xAA
    sts DATA_START+33, r16
    ldi r16, 0x55
    sts DATA_START+34, r16
    
    lds r17, DATA_START+32
    lds r18, DATA_START+33
    lds r19, DATA_START+34
    
    cpi r17, 0x55
    brne fail
    cpi r18, 0xAA
    brne fail
    cpi r19, 0x55
    brne fail
    rcall inc_case
    rjmp test19_start

; ============================================================
; TEST 19: LDS used in arithmetic chain
; ============================================================
test19_start:
    ldi r16, 10
    sts DATA_START+40, r16
    ldi r16, 20
    sts DATA_START+41, r16
    ldi r16, 30
    sts DATA_START+42, r16
    
    lds r17, DATA_START+40
    lds r18, DATA_START+41
    lds r19, DATA_START+42
    
    add r17, r18
    add r17, r19
    
    cpi r17, 60
    brne fail
    rcall inc_case
    rjmp test20_start

; ============================================================
; TEST 20: LDS with immediate value then conditional branch
; ============================================================
test20_start:
    ldi r16, 0x00
    sts DATA_START+50, r16
    
    lds r17, DATA_START+50
    tst r17
    breq lds_zero_ok20
    rjmp fail
lds_zero_ok20:
    
    ldi r16, 0x01
    sts DATA_START+51, r16
    lds r17, DATA_START+51
    tst r17
    brne lds_nonzero_ok20
    rjmp fail
lds_nonzero_ok20:
    
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