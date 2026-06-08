; ============================================================
; BREQ (Branch if Equal) test suite
; ============================================================
; Tests that BREQ correctly branches when Zero flag = 1 (equal)
; and does NOT branch when Zero flag = 0 (not equal)
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
; TEST 1: Branch if Zero Flag is SET (Z=1) using TST
; ============================================================
test1:
    ; Set Z flag to 1 by making result zero
    ldi r16, 0
    tst r16             ; Result is 0, so Z=1
    
    breq branch1_ok     ; If Z=1, branch to label
    rjmp fail           ; Should NOT execute (Z=1, so branch taken)
branch1_ok:
    rcall inc_case

; ============================================================
; TEST 2: Do NOT Branch if Zero Flag is CLEAR (Z=0) using TST
; ============================================================
test2:
    ; Set Z flag to 0 by making result non-zero
    ldi r16, 1
    tst r16             ; Result is 1, so Z=0
    
    breq fail           ; If Z=0, this should NOT branch
    rcall inc_case      ; Should execute (Z=0, no branch)

; ============================================================
; TEST 3: Branch if Z=1 after CP (equal registers)
; ============================================================
test3:
    ; Compare equal registers
    ldi r16, 0x55
    ldi r17, 0x55
    cp r16, r17         ; Equal, so Z=1
    
    breq branch3_ok     ; If Z=1, branch
    rjmp fail
branch3_ok:
    rcall inc_case

; ============================================================
; TEST 4: Do NOT Branch if Z=0 after CP (different registers)
; ============================================================
test4:
    ; Compare different registers
    ldi r16, 0x55
    ldi r17, 0xAA
    cp r16, r17         ; Not equal, so Z=0
    
    breq fail           ; If Z=0, this should NOT branch
    rcall inc_case      ; Should execute (Z=0, no branch)

; ============================================================
; TEST 5: Branch if Z=1 after CPI (equal immediate)
; ============================================================
test5:
    ; Compare with immediate (equal)
    ldi r16, 0x42
    cpi r16, 0x42       ; Equal, so Z=1
    
    breq branch5_ok     ; If Z=1, branch
    rjmp fail
branch5_ok:
    rcall inc_case

; ============================================================
; TEST 6: Do NOT Branch if Z=0 after CPI (different immediate)
; ============================================================
test6:
    ; Compare with immediate (not equal)
    ldi r16, 0x42
    cpi r16, 0x24       ; Not equal, so Z=0
    
    breq fail           ; If Z=0, this should NOT branch
    rcall inc_case      ; Should execute (Z=0, no branch)

; ============================================================
; TEST 7: Branch if Z=1 after ADD that results in zero
; ============================================================
test7:
    ; Addition that results in zero (with wrap)
    ldi r16, 0x80
    ldi r17, 0x80
    add r16, r17        ; 0x80 + 0x80 = 0x100, result masked to 0x00, Z=1
    
    breq branch7_ok     ; If Z=1, branch
    rjmp fail
branch7_ok:
    rcall inc_case

; ============================================================
; TEST 8: Do NOT Branch if Z=0 after ADD that results non-zero
; ============================================================
test8:
    ; Addition that results non-zero
    ldi r16, 0x10
    ldi r17, 0x20
    add r16, r17        ; 0x30, not zero, Z=0
    
    breq fail           ; If Z=0, this should NOT branch
    rcall inc_case      ; Should execute (Z=0, no branch)

; ============================================================
; TEST 9: Branch if Z=1 after SUB that results in zero
; ============================================================
test9:
    ; Subtraction that results in zero
    ldi r16, 0x50
    ldi r17, 0x50
    sub r16, r17        ; 0x50 - 0x50 = 0x00, Z=1
    
    breq branch9_ok     ; If Z=1, branch
    rjmp fail
branch9_ok:
    rcall inc_case

; ============================================================
; TEST 10: Do NOT Branch if Z=0 after SUB that results non-zero
; ============================================================
test10:
    ; Subtraction that results non-zero
    ldi r16, 0x50
    ldi r17, 0x30
    sub r16, r17        ; 0x20, not zero, Z=0
    
    breq fail           ; If Z=0, this should NOT branch
    rcall inc_case      ; Should execute (Z=0, no branch)

; ============================================================
; TEST 11: Branch if Z=1 after AND that results in zero
; ============================================================
test11:
    ; AND that results in zero
    ldi r16, 0x0F
    ldi r17, 0xF0
    and r16, r17        ; 0x0F & 0xF0 = 0x00, Z=1
    
    breq branch11_ok    ; If Z=1, branch
    rjmp fail
branch11_ok:
    rcall inc_case

; ============================================================
; TEST 12: Do NOT Branch if Z=0 after AND that results non-zero
; ============================================================
test12:
    ; AND that results non-zero
    ldi r16, 0xFF
    ldi r17, 0x0F
    and r16, r17        ; 0xFF & 0x0F = 0x0F, not zero, Z=0
    
    breq fail           ; If Z=0, this should NOT branch
    rcall inc_case      ; Should execute (Z=0, no branch)

; ============================================================
; TEST 13: Branch if Z=1 after OR that results in zero
; ============================================================
test13:
    ; OR that results in zero (both zero)
    ldi r16, 0x00
    ldi r17, 0x00
    or r16, r17         ; 0x00 | 0x00 = 0x00, Z=1
    
    breq branch13_ok    ; If Z=1, branch
    rjmp fail
branch13_ok:
    rcall inc_case

; ============================================================
; TEST 14: Do NOT Branch if Z=0 after OR that results non-zero
; ============================================================
test14:
    ; OR that results non-zero
    ldi r16, 0x00
    ldi r17, 0x0F
    or r16, r17         ; 0x00 | 0x0F = 0x0F, not zero, Z=0
    
    breq fail           ; If Z=0, this should NOT branch
    rcall inc_case      ; Should execute (Z=0, no branch)

; ============================================================
; TEST 15: Branch if Z=1 after XOR that results in zero
; ============================================================
test15:
    ; XOR that results in zero (same values)
    ldi r16, 0xAA
    ldi r17, 0xAA
    eor r16, r17        ; 0xAA ^ 0xAA = 0x00, Z=1
    
    breq branch15_ok    ; If Z=1, branch
    rjmp fail
branch15_ok:
    rcall inc_case

; ============================================================
; TEST 16: Do NOT Branch if Z=0 after XOR that results non-zero
; ============================================================
test16:
    ; XOR that results non-zero (different values)
    ldi r16, 0xAA
    ldi r17, 0x55
    eor r16, r17        ; 0xAA ^ 0x55 = 0xFF, not zero, Z=0
    
    breq fail           ; If Z=0, this should NOT branch
    rcall inc_case      ; Should execute (Z=0, no branch)

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