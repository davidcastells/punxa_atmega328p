; ============================================================
; BRNE (Branch if Not Equal) test suite
; ============================================================
; Tests that BRNE correctly branches when Zero flag = 0
; which means: Rd != Rr (not equal)
; ============================================================
; BRNE = Branch if Not Equal
; Equivalent to BRBC 1 (Branch if Bit Clear, Z flag)
; Z=0 when result is non-zero or values are not equal
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
; TEST 1: Branch if Rd != Rr (different values)
; 5 != 10, so Z=0, should branch
; ============================================================
test1:
    ldi r16, 5
    ldi r17, 10
    cp r16, r17         ; 5 != 10, Z=0
    
    brne branch1_ok     ; Z=0, so branch
    rjmp fail
branch1_ok:
    rcall inc_case

; ============================================================
; TEST 2: Do NOT Branch if Rd == Rr (equal)
; 5 == 5, so Z=1, should NOT branch
; ============================================================
test2:
    ldi r16, 5
    ldi r17, 5
    cp r16, r17         ; 5 == 5, Z=1
    
    brne fail           ; Z=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 3: Branch with CPI (different immediate)
; 50 != 100, so Z=0, should branch
; ============================================================
test3:
    ldi r16, 50
    cpi r16, 100        ; 50 != 100, Z=0
    
    brne branch3_ok     ; Z=0, so branch
    rjmp fail
branch3_ok:
    rcall inc_case

; ============================================================
; TEST 4: Do NOT Branch with CPI (equal immediate)
; 50 == 50, so Z=1, should NOT branch
; ============================================================
test4:
    ldi r16, 50
    cpi r16, 50         ; 50 == 50, Z=1
    
    brne fail           ; Z=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 5: Branch with SUB giving non-zero result
; 10 - 3 = 7 (non-zero), Z=0, should branch
; ============================================================
test5:
    ldi r16, 10
    ldi r17, 3
    sub r16, r17        ; 10 - 3 = 7, non-zero, Z=0
    
    brne branch5_ok     ; Z=0, so branch
    rjmp fail
branch5_ok:
    rcall inc_case

; ============================================================
; TEST 6: Do NOT Branch with SUB giving zero result
; 5 - 5 = 0, Z=1, should NOT branch
; ============================================================
test6:
    ldi r16, 5
    ldi r17, 5
    sub r16, r17        ; 5 - 5 = 0, Z=1
    
    brne fail           ; Z=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 7: Branch with ADD giving non-zero result
; 10 + 20 = 30 (non-zero), Z=0, should branch
; ============================================================
test7:
    ldi r16, 10
    ldi r17, 20
    add r16, r17        ; 30, non-zero, Z=0
    
    brne branch7_ok     ; Z=0, so branch
    rjmp fail
branch7_ok:
    rcall inc_case

; ============================================================
; TEST 8: Branch with ADD giving zero result (wrap around)
; 0x80 + 0x80 = 0x00, Z=1, should NOT branch
; ============================================================
test8:
    ldi r16, 0x80
    ldi r17, 0x80
    add r16, r17        ; 0x80 + 0x80 = 0x100 -> 0x00, Z=1
    
    brne fail           ; Z=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 9: Branch with AND giving non-zero result
; 0x0F & 0xF0 = 0x00, Z=1, but we want Z=0
; 0xFF & 0x0F = 0x0F, non-zero, Z=0, should branch
; ============================================================
test9:
    ldi r16, 0xFF
    ldi r17, 0x0F
    and r16, r17        ; 0xFF & 0x0F = 0x0F, non-zero, Z=0
    
    brne branch9_ok     ; Z=0, so branch
    rjmp fail
branch9_ok:
    rcall inc_case

; ============================================================
; TEST 10: Do NOT Branch with AND giving zero result
; 0x0F & 0xF0 = 0x00, Z=1, should NOT branch
; ============================================================
test10:
    ldi r16, 0x0F
    ldi r17, 0xF0
    and r16, r17        ; 0x0F & 0xF0 = 0x00, Z=1
    
    brne fail           ; Z=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 11: Branch with OR giving non-zero result
; 0x00 | 0x0F = 0x0F, non-zero, Z=0, should branch
; ============================================================
test11:
    ldi r16, 0x00
    ldi r17, 0x0F
    or r16, r17         ; 0x00 | 0x0F = 0x0F, Z=0
    
    brne branch11_ok    ; Z=0, so branch
    rjmp fail
branch11_ok:
    rcall inc_case

; ============================================================
; TEST 12: Do NOT Branch with OR giving zero result
; 0x00 | 0x00 = 0x00, Z=1, should NOT branch
; ============================================================
test12:
    ldi r16, 0x00
    ldi r17, 0x00
    or r16, r17         ; 0x00 | 0x00 = 0x00, Z=1
    
    brne fail           ; Z=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 13: Branch with XOR giving non-zero result
; 0xAA ^ 0x55 = 0xFF, non-zero, Z=0, should branch
; ============================================================
test13:
    ldi r16, 0xAA
    ldi r17, 0x55
    eor r16, r17        ; 0xAA ^ 0x55 = 0xFF, Z=0
    
    brne branch13_ok    ; Z=0, so branch
    rjmp fail
branch13_ok:
    rcall inc_case

; ============================================================
; TEST 14: Do NOT Branch with XOR giving zero result
; 0xAA ^ 0xAA = 0x00, Z=1, should NOT branch
; ============================================================
test14:
    ldi r16, 0xAA
    ldi r17, 0xAA
    eor r16, r17        ; 0xAA ^ 0xAA = 0x00, Z=1
    
    brne fail           ; Z=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 15: Branch with INC not wrapping to zero
; 0x01 -> 0x02, non-zero, Z=0, should branch
; ============================================================
test15:
    ldi r16, 0x01
    inc r16             ; 0x01 -> 0x02, non-zero, Z=0
    
    brne branch15_ok    ; Z=0, so branch
    rjmp fail
branch15_ok:
    rcall inc_case

; ============================================================
; TEST 16: Do NOT Branch with INC wrapping to zero
; 0xFF -> 0x00, Z=1, should NOT branch
; ============================================================
test16:
    ldi r16, 0xFF
    inc r16             ; 0xFF -> 0x00, Z=1
    
    brne fail           ; Z=1, so NO branch
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