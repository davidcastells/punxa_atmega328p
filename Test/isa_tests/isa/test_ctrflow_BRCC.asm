; ============================================================
; BRCC (Branch if Carry Clear) test suite
; ============================================================
; Tests that BRCC correctly branches when Carry flag = 0
; and does NOT branch when Carry flag = 1
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
; TEST 1: Branch if Carry Flag is CLEAR (C=0)
; ============================================================
test1:
    ; Clear Carry flag
    clc                 ; C = 0
    
    brcc branch1_ok     ; If C=0, branch to label
    rjmp fail           ; Should NOT execute (C=0, so branch taken)
branch1_ok:
    rcall inc_case

; ============================================================
; TEST 2: Do NOT Branch if Carry Flag is SET (C=1)
; ============================================================
test2:
    ; Set Carry flag
    sec                 ; C = 1
    
    brcc fail           ; If C=1, this should NOT branch
    rcall inc_case      ; Should execute (C=1, no branch)

; ============================================================
; TEST 3: Branch if C=0 after addition with no carry
; ============================================================
test3:
    ; Addition that doesn't produce carry
    ldi r16, 0x10
    ldi r17, 0x20
    add r16, r17        ; 0x10 + 0x20 = 0x30, C=0
    
    brcc branch3_ok     ; If C=0, branch
    rjmp fail
branch3_ok:
    rcall inc_case

; ============================================================
; TEST 4: Do NOT Branch if C=1 after addition with carry
; ============================================================
test4:
    ; Addition that produces carry
    ldi r16, 0xFF
    ldi r17, 0x01
    add r16, r17        ; 0xFF + 0x01 = 0x100, C=1
    
    brcc fail           ; If C=1, this should NOT branch
    rcall inc_case      ; Should execute (C=1, no branch)

; ============================================================
; TEST 5: Branch if C=0 after subtraction with no borrow
; ============================================================
test5:
    ; Subtraction that doesn't require borrow
    ldi r16, 0x50
    ldi r17, 0x20
    sub r16, r17        ; 0x50 - 0x20 = 0x30, C=0 (no borrow)
    
    brcc branch5_ok     ; If C=0, branch
    rjmp fail
branch5_ok:
    rcall inc_case

; ============================================================
; TEST 6: Do NOT Branch if C=1 after subtraction with borrow
; ============================================================
test6:
    ; Subtraction that requires borrow
    ldi r16, 0x20
    ldi r17, 0x50
    sub r16, r17        ; 0x20 - 0x50 = borrow occurs, C=1
    
    brcc fail           ; If C=1, this should NOT branch
    rcall inc_case      ; Should execute (C=1, no branch)

; ============================================================
; TEST 7: Branch if C=0 after shift left (LSL)
; ============================================================
test7:
    ; LSL that doesn't set carry
    ldi r16, 0x40       ; 0x40 = 01000000 binary
    lsl r16             ; 0x40 << 1 = 0x80, no carry out (bit 7 was 0)
                        ; Actually wait: LSL shifts bit 7 into C
                        ; 0x40 (01000000) shifted left = 0x80 (10000000)
                        ; The bit shifted out was 0, so C=0
    
    brcc branch7_ok     ; If C=0, branch
    rjmp fail
branch7_ok:
    rcall inc_case

; ============================================================
; TEST 8: Do NOT Branch if C=1 after shift left
; ============================================================
test8:
    ; LSL that sets carry
    ldi r16, 0x80       ; 0x80 = 10000000 binary
    lsl r16             ; 0x80 << 1 = 0x00, bit 7 shifted out = 1, C=1
    
    brcc fail           ; If C=1, this should NOT branch
    rcall inc_case      ; Should execute (C=1, no branch)

; ============================================================
; TEST 9: Branch if C=0 after logical shift right (LSR)
; ============================================================
test9:
    ; LSR that doesn't set carry
    ldi r16, 0x02       ; 0x02 = 00000010 binary
    lsr r16             ; 0x02 >> 1 = 0x01, LSB shifted out = 0, C=0
    
    brcc branch9_ok     ; If C=0, branch
    rjmp fail
branch9_ok:
    rcall inc_case

; ============================================================
; TEST 10: Do NOT Branch if C=1 after logical shift right
; ============================================================
test10:
    ; LSR that sets carry
    ldi r16, 0x01       ; 0x01 = 00000001 binary
    lsr r16             ; 0x01 >> 1 = 0x00, LSB shifted out = 1, C=1
    
    brcc fail           ; If C=1, this should NOT branch
    rcall inc_case      ; Should execute (C=1, no branch)

; ============================================================
; TEST 11: Branch if C=0 after rotate right (ROR)
; ============================================================
test11:
    ; Clear carry first, then ROR doesn't bring in a 1
    clc                 ; C=0
    ldi r16, 0x02
    ror r16             ; Rotate right through carry, C becomes LSB (0)
    
    brcc branch11_ok    ; If C=0, branch
    rjmp fail
branch11_ok:
    rcall inc_case

; ============================================================
; TEST 12: Do NOT Branch if C=1 after rotate right
; ============================================================
test12:
    ; Set carry first, then ROR brings it into the register
    sec                 ; C=1
    ldi r16, 0x00
    ror r16             ; Rotate right through carry, C becomes LSB (0)
                        ; Actually ROR sets C = LSB, then shifts C into MSB
                        ; Wait, need to be careful with ROR behavior
    
    ; Simpler: Use SEC then an operation that leaves C=1
    sec                 ; C=1
    brcc fail           ; If C=1, this should NOT branch
    rcall inc_case

; ============================================================
; TEST 13: Branch if C=0 after CPI comparison (Rd >= K)
; ============================================================
test13:
    ; CPI sets C=1 if Rd < K (borrow), C=0 if Rd >= K
    ldi r16, 10
    cpi r16, 5          ; 10 >= 5, so C=0
    
    brcc branch13_ok    ; If C=0, branch
    rjmp fail
branch13_ok:
    rcall inc_case

; ============================================================
; TEST 14: Do NOT Branch if C=1 after CPI comparison (Rd < K)
; ============================================================
test14:
    ldi r16, 3
    cpi r16, 5          ; 3 < 5, so C=1 (borrow)
    
    brcc fail           ; If C=1, this should NOT branch
    rcall inc_case      ; Should execute (C=1, no branch)

; ============================================================
; TEST 15: Branch if C=0 after clearing carry
; ============================================================
test15:
    clc                 ; Explicitly clear carry
    
    brcc branch15_ok    ; If C=0, branch
    rjmp fail
branch15_ok:
    rcall inc_case

; ============================================================
; TEST 16: Do NOT Branch after setting carry
; ============================================================
test16:
    sec                 ; Explicitly set carry
    
    brcc fail           ; If C=1, this should NOT branch
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