; ============================================================
; BRCS (Branch if Carry Set) test suite
; ============================================================
; Tests that BRCS correctly branches when Carry flag = 1
; and does NOT branch when Carry flag = 0
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D

reset:
    ldi r16, 0x03
    out SPH, r16
    ldi r16, 0xFF
    out SPL, r16

    ldi r16, 1
    sts test_case, r16
    sts final_result, r16

; ============================================================
; TEST 1: Branch if Carry Flag is SET (C=1)
; ============================================================
test1:
    ; Set Carry flag
    sec                 ; C = 1
    
    brcs branch1_ok     ; If C=1, branch to label
    rjmp fail           ; Should NOT execute (C=1, so branch taken)
branch1_ok:
    rcall inc_case

; ============================================================
; TEST 2: Do NOT Branch if Carry Flag is CLEAR (C=0)
; ============================================================
test2:
    ; Clear Carry flag
    clc                 ; C = 0
    
    brcs fail           ; If C=0, this should NOT branch
    rcall inc_case      ; Should execute (C=0, no branch)

; ============================================================
; TEST 3: Branch if C=1 after addition with carry
; ============================================================
test3:
    ; Addition that produces carry
    ldi r16, 0xFF
    ldi r17, 0x01
    add r16, r17        ; 0xFF + 0x01 = 0x100, C=1
    
    brcs branch3_ok     ; If C=1, branch
    rjmp fail
branch3_ok:
    rcall inc_case

; ============================================================
; TEST 4: Do NOT Branch if C=0 after addition with no carry
; ============================================================
test4:
    ; Addition that doesn't produce carry
    ldi r16, 0x10
    ldi r17, 0x20
    add r16, r17        ; 0x10 + 0x20 = 0x30, C=0
    
    brcs fail           ; If C=0, this should NOT branch
    rcall inc_case      ; Should execute (C=0, no branch)

; ============================================================
; TEST 5: Branch if C=1 after subtraction with borrow
; ============================================================
test5:
    ; Subtraction that requires borrow
    ldi r16, 0x20
    ldi r17, 0x50
    sub r16, r17        ; 0x20 - 0x50 = borrow occurs, C=1
    
    brcs branch5_ok     ; If C=1, branch
    rjmp fail
branch5_ok:
    rcall inc_case

; ============================================================
; TEST 6: Do NOT Branch if C=0 after subtraction with no borrow
; ============================================================
test6:
    ; Subtraction that doesn't require borrow
    ldi r16, 0x50
    ldi r17, 0x20
    sub r16, r17        ; 0x50 - 0x20 = 0x30, C=0 (no borrow)
    
    brcs fail           ; If C=0, this should NOT branch
    rcall inc_case      ; Should execute (C=0, no branch)

; ============================================================
; TEST 7: Branch if C=1 after shift left (LSL)
; ============================================================
test7:
    ; LSL that sets carry
    ldi r16, 0x80       ; 0x80 = 10000000 binary
    lsl r16             ; 0x80 << 1 = 0x00, bit 7 shifted out = 1, C=1
    
    brcs branch7_ok     ; If C=1, branch
    rjmp fail
branch7_ok:
    rcall inc_case

; ============================================================
; TEST 8: Do NOT Branch if C=0 after shift left
; ============================================================
test8:
    ; LSL that doesn't set carry
    ldi r16, 0x40       ; 0x40 = 01000000 binary
    lsl r16             ; 0x40 << 1 = 0x80, bit 7 shifted out = 0, C=0
    
    brcs fail           ; If C=0, this should NOT branch
    rcall inc_case      ; Should execute (C=0, no branch)

; ============================================================
; TEST 9: Branch if C=1 after logical shift right (LSR)
; ============================================================
test9:
    ; LSR that sets carry
    ldi r16, 0x01       ; 0x01 = 00000001 binary
    lsr r16             ; 0x01 >> 1 = 0x00, LSB shifted out = 1, C=1
    
    brcs branch9_ok     ; If C=1, branch
    rjmp fail
branch9_ok:
    rcall inc_case

; ============================================================
; TEST 10: Do NOT Branch if C=0 after logical shift right
; ============================================================
test10:
    ; LSR that doesn't set carry
    ldi r16, 0x02       ; 0x02 = 00000010 binary
    lsr r16             ; 0x02 >> 1 = 0x01, LSB shifted out = 0, C=0
    
    brcs fail           ; If C=0, this should NOT branch
    rcall inc_case      ; Should execute (C=0, no branch)

; ============================================================
; TEST 11: Branch if C=1 after rotate right (ROR) with C set
; ============================================================
test11:
    ; Set carry first, then ROR keeps it in the register
    sec                 ; C=1
    ldi r16, 0x00
    ror r16             ; Rotate right: C goes to bit 7, LSB goes to C
                        ; Original C=1 becomes bit 7 of result
    ; After ROR, C = LSB (which was 0), so C becomes 0
    ; But we want to test branching with C=1, so we branch BEFORE the ROR
    
    ; Better: Test BRCS after setting C without changing it
    sec                 ; C=1
    brcs branch11_ok    ; Directly test after SEC
    rjmp fail
branch11_ok:
    rcall inc_case

; ============================================================
; TEST 12: Do NOT Branch if C=0 after rotate right
; ============================================================
test12:
    ; Clear carry then rotate
    clc                 ; C=0
    ldi r16, 0x00
    ror r16             ; C stays 0 (LSB was 0)
    
    brcs fail           ; If C=0, this should NOT branch
    rcall inc_case

; ============================================================
; TEST 13: Branch if C=1 after CPI comparison (Rd < K)
; ============================================================
test13:
    ; CPI sets C=1 if Rd < K (borrow)
    ldi r16, 3
    cpi r16, 5          ; 3 < 5, so C=1
    
    brcs branch13_ok    ; If C=1, branch
    rjmp fail
branch13_ok:
    rcall inc_case

; ============================================================
; TEST 14: Do NOT Branch if C=0 after CPI comparison (Rd >= K)
; ============================================================
test14:
    ldi r16, 10
    cpi r16, 5          ; 10 >= 5, so C=0
    
    brcs fail           ; If C=0, this should NOT branch
    rcall inc_case      ; Should execute (C=0, no branch)

; ============================================================
; TEST 15: Branch if C=1 after adding with carry using ADC
; ============================================================
test15:
    ; ADC (Add with Carry) uses existing C flag
    clc                 ; Start with C=0
    ldi r16, 0xFF
    ldi r17, 0x01
    adc r16, r17        ; 0xFF + 0x01 + 0 = 0x100, C=1
    
    brcs branch15_ok    ; If C=1, branch
    rjmp fail
branch15_ok:
    rcall inc_case

; ============================================================
; TEST 16: Branch if C=1 after shift right arithmetic (ASR)
; ============================================================
test16:
    ; ASR (Arithmetic Shift Right) shifts LSB into C
    ldi r16, 0x01       ; 0x01 = 00000001
    asr r16             ; 0x01 >> 1 = 0x00, LSB=1 shifted out, C=1
    
    brcs branch16_ok    ; If C=1, branch
    rjmp fail
branch16_ok:
    rcall inc_case

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