; ============================================================
; MOV (Copy Register) test suite
; ============================================================
; Tests that MOV correctly:
; 1. Copies data from source register to destination register
; 2. Works with all registers R0-R31
; 3. Does not modify the source register
; 4. Does not modify any flags
; ============================================================
; MOV is a 1-word (16-bit) instruction
; Format: 0010 11rd dddd rrrr
; Operation: Rd <- Rr
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D

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
; TEST 1: MOV from R16 to R17
; ============================================================
test1_start:
    ldi r16, 0x42
    mov r17, r16
    cpi r17, 0x42
    brne fail
    rcall inc_case
    rjmp test2_start

; ============================================================
; TEST 2: MOV from R0 to R31 (lowest to highest)
; ============================================================
test2_start:
    ldi r0, 0x7E
    mov r31, r0
    cpi r31, 0x7E
    brne fail
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: MOV from R31 to R0 (highest to lowest)
; ============================================================
test3_start:
    ldi r31, 0xAA
    mov r0, r31
    cpi r0, 0xAA
    brne fail
    rcall inc_case
    rjmp test4_start

; ============================================================
; TEST 4: MOV to itself (Rd = Rr)
; ============================================================
test4_start:
    ldi r16, 0x55
    mov r16, r16        ; Should have no effect
    cpi r16, 0x55
    brne fail
    rcall inc_case
    rjmp test5_start

; ============================================================
; TEST 5: MOV with value 0x00
; ============================================================
test5_start:
    ldi r16, 0x00
    mov r17, r16
    cpi r17, 0x00
    brne fail
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6: MOV with value 0xFF
; ============================================================
test6_start:
    ldi r16, 0xFF
    mov r17, r16
    cpi r17, 0xFF
    brne fail
    rcall inc_case
    rjmp test7_start

; ============================================================
; TEST 7: MOV does not modify source register
; ============================================================
test7_start:
    ldi r16, 0x33
    mov r17, r16
    cpi r16, 0x33      ; Source unchanged
    brne fail
    cpi r17, 0x33      ; Destination has copy
    brne fail
    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8: MOV does not modify flags
; ============================================================
test8_start:
    ; Set all flags
    sec                 ; C=1
    sez                 ; Z=1
    sen                 ; N=1
    sev                 ; V=1
    seh                 ; H=1
    set                 ; T=1
    
    ; MOV should preserve flags
    ldi r16, 0x55
    mov r17, r16
    
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
; TEST 9: MOV chain (cascade)
; ============================================================
test9_start:
    ldi r16, 0x12
    mov r17, r16
    mov r18, r17
    mov r19, r18
    mov r20, r19
    
    cpi r20, 0x12
    brne fail
    cpi r16, 0x12
    brne fail
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10: MOV all register pairs (R0-R31)
; ============================================================
test10_start:
    ldi r16, 0x01
    mov r17, r16
    mov r18, r17
    mov r19, r18
    mov r20, r19
    mov r21, r20
    mov r22, r21
    mov r23, r22
    mov r24, r23
    mov r25, r24
    mov r26, r25
    mov r27, r26
    mov r28, r27
    mov r29, r28
    mov r30, r29
    mov r31, r30
    
    cpi r31, 0x01
    brne fail
    rcall inc_case
    rjmp test11_start

; ============================================================
; TEST 11: MOV then modify original
; ============================================================
test11_start:
    ldi r16, 0xAB
    mov r17, r16
    ldi r16, 0xCD      ; Modify original
    
    cpi r17, 0xAB      ; Copy should still be old value
    brne fail
    cpi r16, 0xCD
    brne fail
    rcall inc_case
    rjmp test12_start

; ============================================================
; TEST 12: MOV then modify copy
; ============================================================
test12_start:
    ldi r16, 0xDE
    mov r17, r16
    ldi r17, 0xAD      ; Modify copy
    
    cpi r16, 0xDE      ; Original unchanged
    brne fail
    cpi r17, 0xAD
    brne fail
    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13: MOV used in swap operation
; ============================================================
test13_start:
    ldi r16, 0x12
    ldi r17, 0x34
    
    ; Swap using temporary register
    mov r18, r16
    mov r16, r17
    mov r17, r18
    
    cpi r16, 0x34
    brne fail
    cpi r17, 0x12
    brne fail
    rcall inc_case
    rjmp test14_start

; ============================================================
; TEST 14: MOV with pattern alternating bits
; ============================================================
test14_start:
    ldi r16, 0x55
    mov r17, r16
    cpi r17, 0x55
    brne fail
    
    ldi r16, 0xAA
    mov r17, r16
    cpi r17, 0xAA
    brne fail
    rcall inc_case
    rjmp test15_start

; ============================================================
; TEST 15: MOV used in push/pop sequence
; ============================================================
test15_start:
    ldi r16, 0xCA
    mov r17, r16
    push r17
    ldi r17, 0x00
    pop r18
    cpi r18, 0xCA
    brne fail
    rcall inc_case
    rjmp test16_start

; ============================================================
; TEST 16: MOV then arithmetic on copy
; ============================================================
test16_start:
    ldi r16, 10
    mov r17, r16
    inc r17
    cpi r17, 11
    brne fail
    cpi r16, 10        ; Original unchanged
    brne fail
    rcall inc_case
    rjmp test17_start

; ============================================================
; TEST 17: MOV with value 0x01
; ============================================================
test17_start:
    ldi r16, 0x01
    mov r17, r16
    cpi r17, 0x01
    brne fail
    rcall inc_case
    rjmp test18_start

; ============================================================
; TEST 18: MOV with value 0x80 (MSB set)
; ============================================================
test18_start:
    ldi r16, 0x80
    mov r17, r16
    cpi r17, 0x80
    brne fail
    rcall inc_case
    rjmp test19_start

; ============================================================
; TEST 19: MOV used in function call setup
; ============================================================
test19_start:
    ldi r16, 0xFE
    mov r17, r16
    call mov_sub19
    cpi r17, 0xFE
    brne fail
    rcall inc_case
    rjmp test20_start

mov_sub19:
    ; Subroutine shouldn't modify r17
    ldi r18, 0xFF
    ret

; ============================================================
; TEST 20: MOV then conditional branch
; ============================================================
test20_start:
    ldi r16, 0x00
    mov r17, r16
    tst r17
    breq mov_zero_ok20
    rjmp fail
mov_zero_ok20:
    
    ldi r16, 0x01
    mov r17, r16
    tst r17
    brne mov_nonzero_ok20
    rjmp fail
mov_nonzero_ok20:
    
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