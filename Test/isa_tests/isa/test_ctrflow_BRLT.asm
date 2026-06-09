; ============================================================
; BRLT (Branch if Less Than - Signed) test suite
; ============================================================
; Tests that BRLT correctly branches when S flag = 1
; which means: Rd < Rr (signed comparison)
; ============================================================
; S = N ^ V
; S=1 when:
;   - N=1, V=0 (negative result, no overflow)
;   - N=0, V=1 (positive result with overflow, actually Rd < Rr in signed)
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
; TEST 1: Branch if Rd < Rr (positive, no overflow)
; 5 < 10, result negative (-5), N=1, V=0, S=1
; ============================================================
test1:
    ldi r16, 5
    ldi r17, 10
    cp r16, r17         ; 5 - 10 = -5 (negative)
    
    brlt branch1_ok     ; S=1, so branch
    rjmp fail
branch1_ok:
    rcall inc_case

; ============================================================
; TEST 2: Do NOT Branch if Rd > Rr (positive, no overflow)
; 10 > 5, result positive (5), N=0, V=0, S=0
; ============================================================
test2:
    ldi r16, 10
    ldi r17, 5
    cp r16, r17         ; 10 - 5 = 5 (positive)
    
    brlt fail           ; S=0, so NO branch
    rcall inc_case

; ============================================================
; TEST 3: Do NOT Branch if Rd == Rr (equal)
; 5 == 5, result 0, N=0, V=0, S=0
; ============================================================
test3:
    ldi r16, 5
    ldi r17, 5
    cp r16, r17         ; 5 - 5 = 0
    
    brlt fail           ; S=0, so NO branch
    rcall inc_case

; ============================================================
; TEST 4: Branch if Rd < Rr (negative values, no overflow)
; -10 < -5, result negative (-5), N=1, V=0, S=1
; ============================================================
test4:
    ldi r16, -10        ; 0xF6
    ldi r17, -5         ; 0xFB
    cp r16, r17         ; -10 - (-5) = -5 (negative)
    
    brlt branch4_ok     ; S=1, so branch
    rjmp fail
branch4_ok:
    rcall inc_case

; ============================================================
; TEST 5: Do NOT Branch if Rd > Rr (negative values, no overflow)
; -5 > -10, result positive (5), N=0, V=0, S=0
; ============================================================
test5:
    ldi r16, -5         ; 0xFB
    ldi r17, -10        ; 0xF6
    cp r16, r17         ; -5 - (-10) = 5 (positive)
    
    brlt fail           ; S=0, so NO branch
    rcall inc_case

; ============================================================
; TEST 6: Branch if Rd < Rr (positive overflow case)
; -100 < 100? Actually need Rd < Rr with overflow
; Example: -100 - 100 = -200 < -128, overflow
; ============================================================
test6:
    ; -100 - 100 = -200 (overflow, result wraps to 56)
    ; N=0 (positive), V=1 (overflow), S=1 (0⊕1=1)
    ldi r16, -100       ; 0x9C
    ldi r17, 100
    cp r16, r17         ; -100 - 100 = -200 -> signed overflow
    
    brlt branch6_ok     ; S=1, so branch (Rd < Rr in signed sense)
    rjmp fail
branch6_ok:
    rcall inc_case

; ============================================================
; TEST 7: Do NOT Branch if Rd > Rr (negative overflow case)
; 100 > -100? Actually need Rd > Rr with overflow
; ============================================================
test7:
    ; 100 - (-100) = 200 (overflow, result wraps to -56)
    ; N=1 (negative), V=1 (overflow), S=0 (1⊕1=0)
    ldi r16, 100
    ldi r17, -100       ; 0x9C
    cp r16, r17         ; 100 - (-100) = 200 -> signed overflow
    
    brlt fail           ; S=0, so NO branch (Rd > Rr in signed sense)
    rcall inc_case

; ============================================================
; TEST 8: Branch with SUBI producing negative
; ============================================================
test8:
    ldi r16, 3
    subi r16, 10        ; 3 - 10 = -7, N=1, V=0, S=1
    
    brlt branch8_ok     ; S=1, so branch
    rjmp fail
branch8_ok:
    rcall inc_case

; ============================================================
; TEST 9: Do NOT Branch with SUBI producing positive
; ============================================================
test9:
    ldi r16, 10
    subi r16, 3         ; 10 - 3 = 7, N=0, V=0, S=0
    
    brlt fail           ; S=0, so NO branch
    rcall inc_case

; ============================================================
; TEST 10: Branch with ADD that sets S=1 (overflow case)
; ============================================================
test10:
    ; 100 + 100 = 200 > 127, overflow
    ldi r16, 100
    ldi r17, 100
    add r16, r17        ; 200 -> overflow, N=0?, V=1, let's check
    ; Actually 100+100=200 -> 0xC8, bit7=1, N=1, V=1, S=0? Need different values
    
    ; Better: Use negative addition
    ldi r16, -128
    ldi r17, -1
    add r16, r17        ; -128 + (-1) = -129 -> overflow, N=0?, V=1, S=1
    
    brlt branch10_ok
    rjmp fail
branch10_ok:
    rcall inc_case

; ============================================================
; TEST 11: Branch after CPSE (Compare Skip if Equal)
; ============================================================
test11:
    ldi r16, 5
    ldi r17, 10
    cpse r16, r17       ; Not equal, so no skip
    ; Z=0 from CPSE
    cp r16, r17         ; 5 - 10 = -5, S=1
    
    brlt branch11_ok    ; S=1, so branch
    rjmp fail
branch11_ok:
    rcall inc_case

; ============================================================
; TEST 12: Branch with S flag explicitly set
; ============================================================
test12:
    ; Set S flag by making N=1, V=0
    ldi r16, -5
    tst r16             ; N=1 (negative), V=0, S=1
    
    brlt branch12_ok    ; S=1, so branch
    rjmp fail
branch12_ok:
    rcall inc_case

; ============================================================
; TEST 13: Branch with negative comparison using CPI
; ============================================================
test13:
    ; Compare signed negative with positive
    ldi r16, -10
    cpi r16, 5          ; -10 - 5 = -15, N=1, V=0, S=1
    ; Note: CPI uses unsigned compare, but flags still work for signed
    
    brlt branch13_ok
    rjmp fail
branch13_ok:
    rcall inc_case

; ============================================================
; TEST 14: Do NOT branch with BRLT when condition false
; ============================================================
test14:
    ldi r16, 10
    ldi r17, 5
    cp r16, r17         ; 10 - 5 = 5, S=0
    
    brlt fail           ; S=0, so NO branch
    rcall inc_case

; ============================================================
; TEST 15: Branch with negative value comparison
; ============================================================
test15:
    ldi r16, -20
    ldi r17, -5
    cp r16, r17         ; -20 - (-5) = -15, S=1
    
    brlt branch15_ok
    rjmp fail
branch15_ok:
    rcall inc_case

; ============================================================
; TEST 16: Do NOT branch with BRLT when equal
; ============================================================
test16:
    ldi r16, 100
    ldi r17, 100
    cp r16, r17         ; 0, S=0
    
    brlt fail           ; S=0, so NO branch
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