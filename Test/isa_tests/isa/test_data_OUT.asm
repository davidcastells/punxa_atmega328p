; ============================================================
; OUT (Store to I/O Register) test suite
; ============================================================
; Tests that OUT correctly:
; 1. Writes data from register to I/O space address (0x00-0x3F)
; 2. Works with all registers R0-R31
; 3. Does not modify any flags
; ============================================================
; OUT is a 1-word (16-bit) instruction
; Format: 1011 0AAd dddd AAAA
; Operation: I/O(A) <- Rd
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D
.equ SREG = 0x3F
.equ PORTC = 0x08
.equ DDRC = 0x07
.equ PINC = 0x06

; Test I/O registers (using GPIORs for testing)
.equ GPIOR0 = 0x1E
.equ GPIOR1 = 0x1A

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
; TEST 1: OUT to GPIOR0 from R16
; ============================================================
test1_start:
    ldi r16, 0x42
    out GPIOR0, r16
    
    ; Verify by reading back
    in r17, GPIOR0
    cpi r17, 0x42
    brne fail
    rcall inc_case
    rjmp test2_start

; ============================================================
; TEST 2: OUT to GPIOR1 from R0 (lowest register)
; ============================================================
test2_start:
    ldi r0, 0xAA
    out GPIOR1, r0
    
    in r17, GPIOR1
    cpi r17, 0xAA
    brne fail
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: OUT to GPIOR0 from R31 (highest register)
; ============================================================
test3_start:
    ldi r31, 0xBB
    out GPIOR0, r31
    
    in r16, GPIOR0
    cpi r16, 0xBB
    brne fail
    rcall inc_case
    rjmp test4_start

; ============================================================
; TEST 4: OUT with value 0x00
; ============================================================
test4_start:
    ldi r16, 0x00
    out GPIOR0, r16
    
    in r17, GPIOR0
    cpi r17, 0x00
    brne fail
    rcall inc_case
    rjmp test5_start

; ============================================================
; TEST 5: OUT with value 0xFF
; ============================================================
test5_start:
    ldi r16, 0xFF
    out GPIOR0, r16
    
    in r17, GPIOR0
    cpi r17, 0xFF
    brne fail
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6: OUT does not modify flags
; ============================================================
test6_start:
    ; Set all flags
    sec                 ; C=1
    sez                 ; Z=1
    sen                 ; N=1
    sev                 ; V=1
    seh                 ; H=1
    set                 ; T=1
    
    ; OUT should preserve flags
    ldi r16, 0x55
    out GPIOR0, r16
    
    ; Verify all flags still set
    brcc fail
    brne fail
    brmi fail
    brvs fail
    brhc fail
    brtc fail
    
    rcall inc_case
    rjmp test7_start

; ============================================================
; TEST 7: OUT to multiple I/O addresses
; ============================================================
test7_start:
    ldi r16, 0x11
    out GPIOR0, r16
    ldi r16, 0x22
    out GPIOR1, r16
    
    in r17, GPIOR0
    in r18, GPIOR1
    
    cpi r17, 0x11
    brne fail
    cpi r18, 0x22
    brne fail
    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8: OUT to PORTC (output port)
; ============================================================
test8_start:
    ; Configure PORTC as output
    ldi r16, 0xFF
    out DDRC, r16
    
    ; Write to PORTC
    ldi r16, 0x5A
    out PORTC, r16
    
    ; Read back via PINC (if configured as output)
    in r17, PORTC
    cpi r17, 0x5A
    brne fail
    rcall inc_case
    rjmp test9_start

; ============================================================
; TEST 9: OUT to SREG (Status Register)
; ============================================================
test9_start:
    ; Read current SREG
    in r16, SREG
    push r16
    
    ; Write new value to SREG
    ldi r16, 0b11000000  ; Set I and T flags
    out SREG, r16
    
    ; Verify
    in r17, SREG
    cpi r17, 0b11000000
    brne fail
    
    ; Restore original SREG
    pop r16
    out SREG, r16
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10: OUT to SPH/SPL (Stack Pointer)
; ============================================================
test10_start:
    ; Save original SP
    in r16, SPL
    in r17, SPH
    push r16
    push r17
    
    ; Write new SP value
    ldi r16, 0x34
    out SPL, r16
    ldi r16, 0x12
    out SPH, r16
    
    ; Verify
    in r18, SPL
    in r19, SPH
    cpi r18, 0x34
    brne fail
    cpi r19, 0x12
    brne fail
    
    ; Restore original SP
    pop r17
    pop r16
    out SPH, r17
    out SPL, r16
    rcall inc_case
    rjmp test11_start

; ============================================================
; TEST 11: OUT with pattern alternating bits (0x55)
; ============================================================
test11_start:
    ldi r16, 0x55
    out GPIOR0, r16
    
    in r17, GPIOR0
    cpi r17, 0x55
    brne fail
    rcall inc_case
    rjmp test12_start

; ============================================================
; TEST 12: OUT with pattern alternating bits (0xAA)
; ============================================================
test12_start:
    ldi r16, 0xAA
    out GPIOR0, r16
    
    in r17, GPIOR0
    cpi r17, 0xAA
    brne fail
    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13: OUT from register that is then modified
; ============================================================
test13_start:
    ldi r16, 0xDE
    out GPIOR0, r16
    ldi r16, 0xAD     ; Modify source
    
    ; I/O should still have original value
    in r17, GPIOR0
    cpi r17, 0xDE
    brne fail
    rcall inc_case
    rjmp test14_start

; ============================================================
; TEST 14: OUT to same address multiple times
; ============================================================
test14_start:
    ldi r16, 0x01
    out GPIOR0, r16
    ldi r16, 0x02
    out GPIOR0, r16
    ldi r16, 0x03
    out GPIOR0, r16
    
    in r17, GPIOR0
    cpi r17, 0x03
    brne fail
    rcall inc_case
    rjmp test15_start

; ============================================================
; TEST 15: OUT using all register types in sequence
; ============================================================
test15_start:
    ldi r0, 0xAA
    out GPIOR0, r0
    in r16, GPIOR0
    cpi r16, 0xAA
    brne fail
    
    ldi r16, 0xBB
    out GPIOR0, r16
    in r17, GPIOR0
    cpi r17, 0xBB
    brne fail
    
    ldi r31, 0xCC
    out GPIOR0, r31
    in r18, GPIOR0
    cpi r18, 0xCC
    brne fail
    rcall inc_case
    rjmp test16_start

; ============================================================
; TEST 16: OUT after IN (verify no interference)
; ============================================================
test16_start:
    ldi r16, 0x12
    out GPIOR0, r16
    
    in r17, GPIOR0
    cpi r17, 0x12
    brne fail
    
    ldi r18, 0x34
    out GPIOR0, r18
    
    in r19, GPIOR0
    cpi r19, 0x34
    brne fail
    rcall inc_case
    rjmp test17_start

; ============================================================
; TEST 17: OUT with value 0x01
; ============================================================
test17_start:
    ldi r16, 0x01
    out GPIOR0, r16
    
    in r17, GPIOR0
    cpi r17, 0x01
    brne fail
    rcall inc_case
    rjmp test18_start

; ============================================================
; TEST 18: OUT with value 0x80 (MSB set)
; ============================================================
test18_start:
    ldi r16, 0x80
    out GPIOR0, r16
    
    in r17, GPIOR0
    cpi r17, 0x80
    brne fail
    rcall inc_case
    rjmp test19_start

; ============================================================
; TEST 19: OUT inside a loop
; ============================================================
test19_start:
    ldi r16, 0
    ldi r17, 5
test19_loop:
    out GPIOR0, r16
    inc r16
    dec r17
    brne test19_loop
    
    ; Last value written should be 4
    in r18, GPIOR0
    cpi r18, 4
    brne fail
    rcall inc_case
    rjmp test20_start

; ============================================================
; TEST 20: OUT then conditional branch
; ============================================================
test20_start:
    ldi r16, 0x00
    out GPIOR0, r16
    in r17, GPIOR0
    tst r17
    breq out_zero_ok20
    rjmp fail
out_zero_ok20:
    
    ldi r16, 0x01
    out GPIOR0, r16
    in r17, GPIOR0
    tst r17
    brne out_nonzero_ok20
    rjmp fail
out_nonzero_ok20:
    
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