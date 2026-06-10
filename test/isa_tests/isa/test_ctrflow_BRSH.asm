; ============================================================
; BRSH (Branch if Same or Higher - Unsigned) test suite
; ============================================================
; Tests that BRSH correctly branches when C flag = 0
; which means: Rd >= Rr (unsigned comparison)
; ============================================================
; BRSH = Branch if Same or Higher (unsigned)
; Equivalent to BRBC 0 (Branch if Bit Clear, C flag)
; Also known as BRCC (Branch if Carry Clear)
; C=0 when Rd >= Rr (no borrow occurs)
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
; TEST 1: Branch if Rd > Rr (unsigned)
; 10 > 5, so C=0, should branch
; ============================================================
test1:
    ldi r16, 10
    ldi r17, 5
    cp r16, r17         ; 10 - 5 = no borrow, C=0
    
    brsh branch1_ok     ; C=0, so branch
    rjmp fail
branch1_ok:
    rcall inc_case

; ============================================================
; TEST 2: Branch if Rd == Rr (unsigned)
; 5 == 5, so C=0, should branch
; ============================================================
test2:
    ldi r16, 5
    ldi r17, 5
    cp r16, r17         ; 5 - 5 = 0, no borrow, C=0
    
    brsh branch2_ok     ; C=0, so branch
    rjmp fail
branch2_ok:
    rcall inc_case

; ============================================================
; TEST 3: Do NOT Branch if Rd < Rr (unsigned)
; 5 < 10, so C=1, should NOT branch
; ============================================================
test3:
    ldi r16, 5
    ldi r17, 10
    cp r16, r17         ; 5 - 10 = borrow, C=1
    
    brsh fail           ; C=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 4: Branch with CPI (Rd > Rr)
; 200 > 100, so C=0, should branch
; ============================================================
test4:
    ldi r16, 200
    cpi r16, 100        ; 200 - 100 = no borrow, C=0
    
    brsh branch4_ok     ; C=0, so branch
    rjmp fail
branch4_ok:
    rcall inc_case

; ============================================================
; TEST 5: Branch with CPI (Rd == Rr)
; 150 == 150, so C=0, should branch
; ============================================================
test5:
    ldi r16, 150
    cpi r16, 150        ; 150 - 150 = 0, no borrow, C=0
    
    brsh branch5_ok     ; C=0, so branch
    rjmp fail
branch5_ok:
    rcall inc_case

; ============================================================
; TEST 6: Do NOT Branch with CPI (Rd < Rr)
; 50 < 100, so C=1, should NOT branch
; ============================================================
test6:
    ldi r16, 50
    cpi r16, 100        ; 50 - 100 = borrow, C=1
    
    brsh fail           ; C=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 7: Branch with SUB that doesn't cause borrow
; 10 - 3 = 7, no borrow, C=0, should branch
; ============================================================
test7:
    ldi r16, 10
    ldi r17, 3
    sub r16, r17        ; 10 - 3 = 7, no borrow, C=0
    
    brsh branch7_ok     ; C=0, so branch
    rjmp fail
branch7_ok:
    rcall inc_case

; ============================================================
; TEST 8: Do NOT Branch with SUB that causes borrow
; 3 - 10 = borrow, C=1, should NOT branch
; ============================================================
test8:
    ldi r16, 3
    ldi r17, 10
    sub r16, r17        ; 3 - 10 = borrow, C=1
    
    brsh fail           ; C=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 9: Branch with maximum values (Rd == Rr)
; 255 == 255, no borrow, C=0, should branch
; ============================================================
test9:
    ldi r16, 255
    ldi r17, 255
    cp r16, r17         ; 255 - 255 = 0, C=0
    
    brsh branch9_ok     ; C=0, so branch
    rjmp fail
branch9_ok:
    rcall inc_case

; ============================================================
; TEST 10: Branch with Rd > Rr (boundary)
; 255 > 254, no borrow, C=0, should branch
; ============================================================
test10:
    ldi r16, 255
    ldi r17, 254
    cp r16, r17         ; 255 - 254 = 1, no borrow, C=0
    
    brsh branch10_ok    ; C=0, so branch
    rjmp fail
branch10_ok:
    rcall inc_case

; ============================================================
; TEST 11: Branch with ADD that doesn't set C
; ADD with no carry, C=0, should branch
; ============================================================
test11:
    ldi r16, 10
    ldi r17, 20
    add r16, r17        ; 30, C=0
    
    brsh branch11_ok    ; C=0, so branch
    rjmp fail
branch11_ok:
    rcall inc_case

; ============================================================
; TEST 12: Do NOT Branch with ADD that sets C
; ADD with carry, C=1, should NOT branch
; ============================================================
test12:
    ldi r16, 0xFF
    ldi r17, 0x01
    add r16, r17        ; 0x100, C=1
    
    brsh fail           ; C=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 13: Branch with ADIW (unsigned word addition)
; ADIW with no carry, C=0, should branch
; ============================================================
test13:
    ldi r24, 0xF0
    ldi r25, 0x00
    adiw r24, 16        ; 0x00F0 + 16 = 0x0100, no carry out of bit 15, C=0
    
    brsh branch13_ok    ; C=0, so branch
    rjmp fail
branch13_ok:
    rcall inc_case

; ============================================================
; TEST 14: Branch after CLC (explicitly clear carry)
; C=0, should branch
; ============================================================
test14:
    clc                 ; C=0
    
    brsh branch14_ok    ; C=0, so branch
    rjmp fail
branch14_ok:
    rcall inc_case

; ============================================================
; TEST 15: Branch with LSL that doesn't set C
; LSL with no carry out, C=0, should branch
; ============================================================
test15:
    ldi r16, 0x40
    lsl r16             ; 0x40 << 1 = 0x80, bit 7 out = 0, C=0
    
    brsh branch15_ok    ; C=0, so branch
    rjmp fail
branch15_ok:
    rcall inc_case

; ============================================================
; TEST 16: Do NOT Branch with LSL that sets C
; LSL with carry out, C=1, should NOT branch
; ============================================================
test16:
    ldi r16, 0x80
    lsl r16             ; 0x80 << 1 = 0x00, bit 7 out = 1, C=1
    
    brsh fail           ; C=1, so NO branch
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