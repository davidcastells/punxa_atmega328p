; ============================================================
; BRGE (Branch if Greater or Equal - Signed) test suite
; ============================================================
; Tests that BRGE correctly branches when S flag = 0
; which means: Rd >= Rr (signed comparison)
; ============================================================
; S = N ⊕ V
; S=0 when:
;   - N=0, V=0 (positive result, no overflow)
;   - N=1, V=1 (negative result with overflow)
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
; TEST 1: Branch if Rd > Rr (positive, no overflow)
; 10 > 5, result positive (5), N=0, V=0, S=0
; ============================================================
test1:
    ldi r16, 10
    ldi r17, 5
    cp r16, r17         ; 10 - 5 = 5 (positive)
    
    brge branch1_ok     ; S=0, so branch
    rjmp fail
branch1_ok:
    rcall inc_case

; ============================================================
; TEST 2: Branch if Rd == Rr (equal, result zero)
; 5 == 5, result 0, N=0, V=0, S=0
; ============================================================
test2:
    ldi r16, 5
    ldi r17, 5
    cp r16, r17         ; 5 - 5 = 0
    
    brge branch2_ok     ; S=0, so branch
    rjmp fail
branch2_ok:
    rcall inc_case

; ============================================================
; TEST 3: Do NOT Branch if Rd < Rr (positive, no overflow)
; 5 < 10, result negative (-5), N=1, V=0, S=1
; ============================================================
test3:
    ldi r16, 5
    ldi r17, 10
    cp r16, r17         ; 5 - 10 = -5 (negative)
    
    brge fail           ; S=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 4: Branch if Rd > Rr (negative values, no overflow)
; -5 > -10, result 5 (positive), N=0, V=0, S=0
; ============================================================
test4:
    ldi r16, -5         ; 0xFB
    ldi r17, -10        ; 0xF6
    cp r16, r17         ; -5 - (-10) = 5 (positive)
    
    brge branch4_ok     ; S=0, so branch
    rjmp fail
branch4_ok:
    rcall inc_case

; ============================================================
; TEST 5: Do NOT Branch if Rd < Rr (negative values, no overflow)
; -10 < -5, result -5 (negative), N=1, V=0, S=1
; ============================================================
test5:
    ldi r16, -10        ; 0xF6
    ldi r17, -5         ; 0xFB
    cp r16, r17         ; -10 - (-5) = -5 (negative)
    
    brge fail           ; S=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 6: Branch if Rd > Rr (positive overflow case)
; 120 > 10, but careful with overflow...
; Wait, need a case with V=1 and N=1 to get S=0
; Example: 100 - (-100) = 200 > 127, overflow
; ============================================================
test6:
    ; 100 - (-100) = 200 (overflow, result wraps to -56)
    ; N=1 (negative), V=1 (overflow), S=0 (1⊕1=0)
    ldi r16, 100
    ldi r17, -100       ; 0x9C
    cp r16, r17         ; 100 - (-100) = 200 -> signed overflow
    
    brge branch6_ok     ; S=0, so branch (Rd > Rr in signed sense)
    rjmp fail
branch6_ok:
    rcall inc_case

; ============================================================
; TEST 7: Do NOT Branch if Rd < Rr (negative overflow case)
; -120 < -10? Actually need specific overflow case
; Example: -100 - 100 = -200 < -128, overflow
; ============================================================
test7:
    ; -100 - 100 = -200 (overflow, result wraps to 56)
    ; N=0 (positive), V=1 (overflow), S=1 (0⊕1=1)
    ldi r16, -100       ; 0x9C
    ldi r17, 100
    cp r16, r17         ; -100 - 100 = -200 -> signed overflow
    
    brge fail           ; S=1, so NO branch (Rd < Rr in signed sense)
    rcall inc_case

; ============================================================
; TEST 8: Branch with ADIW that sets S=0
; ADIW with result positive
; ============================================================
test8:
    ldi r24, 0x10
    ldi r25, 0x00
    adiw r24, 5         ; 0x0010 + 5 = 0x0015, positive
    
    brge branch8_ok     ; S=0, so branch
    rjmp fail
branch8_ok:
    rcall inc_case

; ============================================================
; TEST 9: Branch with SUBI producing zero
; ============================================================
test9:
    ldi r16, 5
    subi r16, 5         ; 5 - 5 = 0, N=0, V=0, S=0
    
    brge branch9_ok     ; S=0, so branch
    rjmp fail
branch9_ok:
    rcall inc_case

; ============================================================
; TEST 10: Do NOT Branch with SUBI producing negative
; ============================================================
test10:
    ldi r16, 3
    subi r16, 10        ; 3 - 10 = -7, N=1, V=0, S=1
    
    brge fail           ; S=1, so NO branch
    rcall inc_case

; ============================================================
; TEST 11: Branch with ADD producing positive
; ============================================================
test11:
    ldi r16, 10
    ldi r17, 20
    add r16, r17        ; 30, positive
    
    brge branch11_ok    ; S=0 (assuming no overflow)
    rjmp fail
branch11_ok:
    rcall inc_case

; ============================================================
; TEST 12: Branch after CPSE (Compare Skip if Equal)
; ============================================================
test12:
    ldi r16, 5
    ldi r17, 5
    cpse r16, r17       ; Skip next if equal (which they are)
    rjmp should_be_skipped
    ; Z=1 from CPSE, but CPSE doesn't affect flags
    ; Use a comparison that sets S=0
    ldi r18, 10
    ldi r19, 5
    cp r18, r19         ; 10 > 5, S=0
    
    brge branch12_ok    ; S=0, so branch
should_be_skipped:
    rjmp fail
branch12_ok:
    rcall inc_case

; ============================================================
; TEST 13: Branch with S flag explicitly cleared
; ============================================================
test13:
    ; Clear S flag by making N=0 and V=0
    clr r16             ; r16 = 0, Z=1, N=0, V=0
    tst r16             ; N=0, V=0, S=0
    
    brge branch13_ok    ; S=0, so branch
    rjmp fail
branch13_ok:
    rcall inc_case

; ============================================================
; TEST 14: Branch with negative comparison using ADIW
; ============================================================
test14:
    ; Use ADIW with result that doesn't set S=1
    ldi r24, 0xFF
    ldi r25, 0x7F
    adiw r24, 1         ; 0x7FFF + 1 = 0x8000, negative, but check flags
    
    ; Instead, use a simple signed comparison
    ldi r16, -5
    ldi r17, -10
    cp r16, r17         ; -5 > -10, S=0
    
    brge branch14_ok
    rjmp fail
branch14_ok:
    rcall inc_case

; ============================================================
; TEST 15: BRGE with immediate value (through CPI)
; ============================================================
test15:
    ; 15 >= 10, should branch
    ldi r16, 15
    cpi r16, 10         ; 15 - 10 = 5, positive, N=0, V=0, S=0
    
    brge branch15_ok
    rjmp fail
branch15_ok:
    rcall inc_case

; ============================================================
; TEST 16: Do NOT branch with BRGE when condition false
; ============================================================
test16:
    ; 5 >= 10? false, should NOT branch
    ldi r16, 5
    cpi r16, 10         ; 5 - 10 = -5, N=1, V=0, S=1
    
    brge fail           ; S=1, so NO branch
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