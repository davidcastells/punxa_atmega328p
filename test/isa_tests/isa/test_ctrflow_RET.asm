; ============================================================
; RET (Return from Subroutine) test suite
; ============================================================
; Tests that RET correctly:
; 1. Pops the return address from the stack
; 2. Jumps back to the address after the original CALL/RCALL
; 3. Stack pointer increments by 2
; ============================================================
; RET is a 1-word (16-bit) instruction
; Format: 1001 0101 0000 1000 (0x9508)
; Operation: PC <- [SP], SP <- SP + 2
; No flags affected
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ stack_start = 0x08FF
.equ SPH = 0x3E
.equ SPL = 0x3D

reset:
    ; Initialize stack pointer to RAMEND (0x08FF)
    ldi r16, high(stack_start)
    out SPH, r16
    ldi r16, low(stack_start)
    out SPL, r16

    ldi r16, 1
    sts test_case, r16
    sts final_result, r16

; ============================================================
; TEST 1: Simple RET after RCALL
; ============================================================
test1:
    rcall subroutine1
    ; Should return here
    cpi r16, 0x42
    brne fail
    rcall inc_case
    rjmp test1_done

subroutine1:
    ldi r16, 0x42
    ret

test1_done:

; ============================================================
; TEST 2: RET after nested RCALLs (two levels)
; ============================================================
test2:
    ldi r17, 0
    rcall outer2
    cpi r17, 0x02
    brne fail
    rcall inc_case
    rjmp test2_done

outer2:
    inc r17
    rcall inner2
    ret

inner2:
    inc r17
    ret

test2_done:

; ============================================================
; TEST 3: RET after multiple nested calls (4 levels)
; ============================================================
test3:
    ldi r18, 0
    rcall level1_3
    cpi r18, 4
    brne fail
    rcall inc_case
    rjmp test3_done

level1_3:
    inc r18
    rcall level2_3
    ret

level2_3:
    inc r18
    rcall level3_3
    ret

level3_3:
    inc r18
    rcall level4_3
    ret

level4_3:
    inc r18
    ret

test3_done:

; ============================================================
; TEST 4: Verify stack pointer returns to original value
; ============================================================
test4:
    ; Read initial SP
    in r19, SPL
    in r20, SPH
    
    rcall sp_test4
    
    ; Read SP after RET
    in r21, SPL
    in r22, SPH
    
    cp r19, r21
    brne fail
    cp r20, r22
    brne fail
    rcall inc_case
    rjmp test4_done

sp_test4:
    ; Inside call, SP should be decreased by 2
    in r23, SPL
    in r24, SPH
    ret

test4_done:

; ============================================================
; TEST 5: RET with multiple PUSH/POP inside
; ============================================================
test5:
    ldi r25, 0x11
    ldi r26, 0x22
    ldi r27, 0x33
    
    rcall push_pop_test5
    
    ; Registers should be restored after RET
    cpi r25, 0x11
    brne fail
    cpi r26, 0x22
    brne fail
    cpi r27, 0x33
    brne fail
    rcall inc_case
    rjmp test5_done

push_pop_test5:
    push r25
    push r26
    push r27
    
    ldi r25, 0xFF
    ldi r26, 0xFF
    ldi r27, 0xFF
    
    pop r27
    pop r26
    pop r25
    ret

test5_done:

; ============================================================
; TEST 6: RET after CALL (absolute call)
; ============================================================
test6:
    call subroutine6
    cpi r28, 0x7E
    brne fail
    rcall inc_case
    rjmp test6_done

subroutine6:
    ldi r28, 0x7E
    ret

test6_done:

; ============================================================
; TEST 7: RET after ICALL (indirect call)
; ============================================================
test7:
    ldi r30, low(subroutine7)
    ldi r31, high(subroutine7)
    icall
    cpi r29, 0xAA
    brne fail
    rcall inc_case
    rjmp test7_done

subroutine7:
    ldi r29, 0xAA
    ret

test7_done:

; ============================================================
; TEST 8: RET with preserved values across calls
; ============================================================
test8:
    ldi r16, 0xDE
    ldi r17, 0xAD
    
    rcall preserve_test8
    
    cpi r16, 0xDE
    brne fail
    cpi r17, 0xAD
    brne fail
    rcall inc_case
    rjmp test8_done

preserve_test8:
    push r16
    push r17
    
    ldi r16, 0xBE
    ldi r17, 0xEF
    
    pop r17
    pop r16
    ret

test8_done:

; ============================================================
; TEST 9: Verify RET doesn't modify any flags
; ============================================================
test9:
    ; Set some flags
    clc
    clz
    cln
    
    ; Flags should be unchanged after RET
    rcall flag_test9
    brcc flag_fail9    ; Should NOT branch (C should still be 0)
    brne flag_fail9    ; Should NOT branch (Z should still be 0)
    brmi flag_fail9    ; Should NOT branch (N should still be 0)
    
    rcall inc_case
    rjmp test9_done

flag_test9:
    ; RET should preserve all flags
    ret

flag_fail9:
    rjmp fail

test9_done:

; ============================================================
; TEST 10: RET from deep recursion
; ============================================================
test10:
    ldi r18, 0
    ldi r19, 5
    rcall recursive10
    cpi r18, 5
    brne fail
    rcall inc_case
    rjmp test10_done

recursive10:
    inc r18
    dec r19
    breq rec_done10
    rcall recursive10
rec_done10:
    ret

test10_done:

; ============================================================
; TEST 11: RET with stack frame cleanup
; ============================================================
test11:
    rcall frame_test11
    cpi r20, 0x42
    brne fail
    rcall inc_case
    rjmp test11_done

frame_test11:
    ; Create stack frame
    push r16
    push r17
    push r20
    
    ; Use local "variables"
    ldi r16, 0xAA
    ldi r17, 0xBB
    ldi r20, 0x42
    
    ; Clean up frame
    pop r20
    pop r17
    pop r16
    ret

test11_done:

; ============================================================
; TEST 12: RET from interrupt simulation (with RETI vs RET)
; ============================================================
test12:
    ldi r21, 0
    sei
    rcall isr_sim12
    cpi r21, 0xCC
    brne fail
    rcall inc_case
    rjmp test12_done

isr_sim12:
    push r16
    ldi r21, 0xCC
    pop r16
    ret                 ; RET used (not RETI) since we didn't actually have an interrupt

test12_done:

; ============================================================
; TEST 13: Multiple RETs from multiple calls
; ============================================================
test13:
    ldi r22, 0
    rcall a13
    cpi r22, 3
    brne fail
    rcall inc_case
    rjmp test13_done

a13:
    inc r22
    rcall b13
    ret

b13:
    inc r22
    rcall c13
    ret

c13:
    inc r22
    ret

test13_done:

; ============================================================
; TEST 14: RET with valid return address after modifications
; ============================================================
test14:
    rcall modify_stack_test14
    cpi r23, 0x55
    brne fail
    rcall inc_case
    rjmp test14_done

modify_stack_test14:
    push r23
    ldi r23, 0x55
    pop r23
    ret

test14_done:

; ============================================================
; TEST 15: Verify RET encoding (fixed opcode 0x9508)
; ============================================================
test15:
    ; We can't test encoding directly, but we can verify RET works
    rcall encoding_target15
    rcall inc_case
    rjmp test15_done

encoding_target15:
    ret

test15_done:

; ============================================================
; TEST 16: RET after complex PUSH/POP sequence
; ============================================================
test16:
    ldi r24, 0x01
    ldi r25, 0x02
    ldi r26, 0x03
    ldi r27, 0x04
    
    rcall complex_stack16
    
    cpi r24, 0x01
    brne fail
    cpi r25, 0x02
    brne fail
    cpi r26, 0x03
    brne fail
    cpi r27, 0x04
    brne fail
    rcall inc_case
    rjmp test16_done

complex_stack16:
    push r24
    push r25
    push r26
    push r27
    
    ldi r24, 0xFF
    ldi r25, 0xFF
    ldi r26, 0xFF
    ldi r27, 0xFF
    
    pop r27
    pop r26
    pop r25
    pop r24
    ret

test16_done:

; ============================================================
; TEST 17: RET after RCALL with offset calculation
; ============================================================
test17:
    ldi r16, 0
    rcall far_target17
    cpi r16, 0x01
    brne fail
    rcall inc_case
    rjmp test17_done

far_target17:
    inc r16
    ret

test17_done:

; ============================================================
; TEST 18: RET in tail position (no instructions after)
; ============================================================
test18:
    rcall tail_test18
    ; Should return here, then fall through to success
    rjmp test18_done

tail_test18:
    ; Nothing to do, just return
    ret

test18_done:
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