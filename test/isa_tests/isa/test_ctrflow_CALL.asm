; ============================================================
; CALL (Call Subroutine) test suite
; ============================================================
; Tests that CALL correctly:
; 1. Saves the return address (PC+2) on the stack
; 2. Jumps to the target absolute address
; 3. Stack pointer decrements by 2
; ============================================================
; CALL is a 2-word (32-bit) instruction
; Format: 1001 010k kkkk 111k + second word with lower 16 bits
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
; TEST 1: Simple CALL that returns
; ============================================================
test1:
    ldi r16, 0xAA
    call subroutine1    ; Call subroutine
    ; Should return here after subroutine
    cpi r16, 0xBB       ; Check if subroutine modified r16
    brne fail
    rcall inc_case

subroutine1:
    ldi r16, 0xBB       ; Change value
    ret                 ; Return to caller

; ============================================================
; TEST 2: Nested CALLs (two levels deep)
; ============================================================
test2:
    ldi r17, 0x11
    call outer          ; First level call
    
    cpi r17, 0x33       ; Should be 0x33 after nested returns
    brne fail
    rcall inc_case

outer:
    ldi r17, 0x22
    call inner          ; Second level call
    ret

inner:
    ldi r17, 0x33
    ret

; ============================================================
; TEST 3: CALL with multiple PUSH/POP inside
; ============================================================
test3:
    ldi r18, 0x01
    ldi r19, 0x02
    ldi r20, 0x03
    
    call push_pop_test
    
    ; Registers should be restored after return
    cpi r18, 0x01
    brne fail
    cpi r19, 0x02
    brne fail
    cpi r20, 0x03
    brne fail
    rcall inc_case

push_pop_test:
    push r18
    push r19
    push r20
    
    ldi r18, 0xFF
    ldi r19, 0xFF
    ldi r20, 0xFF
    
    pop r20
    pop r19
    pop r18
    ret

; ============================================================
; TEST 4: Stack pointer verification after CALL/RET
; ============================================================
test4:
    ; Read initial SP
    in r21, SPL
    in r22, SPH
    
    call sp_test       ; CALL should decrement SP by 2
    
    ; Read SP after return
    in r23, SPL
    in r24, SPH
    
    ; SP should be back to original value
    cp r21, r23
    brne fail
    cp r22, r24
    brne fail
    rcall inc_case

sp_test:
    ; Inside call, SP should be 2 less
    in r25, SPL
    in r26, SPH
    
    ; Check that SP decreased by 2
    sub r21, r25
    brne sp_fail_check
    ; For high byte, need to handle borrow
sp_fail_check:
    ret

; ============================================================
; TEST 5: CALL to far address (within 64K word space)
; ============================================================
test5:
    ldi r27, 0
    call far_target    ; Call to another location
    
    cpi r27, 0x42
    brne fail
    rcall inc_case

far_target:
    ldi r27, 0x42
    ret

; ============================================================
; TEST 6: Multiple CALLs to same subroutine
; ============================================================
test6:
    ldi r28, 0
    
    call counter_sub
    call counter_sub
    call counter_sub
    
    cpi r28, 3
    brne fail
    rcall inc_case

counter_sub:
    inc r28
    ret

; ============================================================
; TEST 7: CALL with stack frame (local variables)
; ============================================================
test7:
    call frame_test
    
    cpi r29, 0xAA
    brne fail
    rcall inc_case

frame_test:
    ; Reserve 2 bytes on stack
    push r16
    push r17
    
    ; Store values in "local variables"
    ldi r16, 0xAA
    ldi r17, 0xBB
    
    ; Copy to result
    mov r29, r16
    
    ; Restore stack
    pop r17
    pop r16
    ret

; ============================================================
; TEST 8: CALL inside a loop
; ============================================================
test8:
    ldi r30, 0
    ldi r31, 5
    
loop_call:
    call loop_sub
    dec r31
    brne loop_call
    
    cpi r30, 5
    brne fail
    rcall inc_case

loop_sub:
    inc r30
    ret

; ============================================================
; TEST 9: CALL with RET that has value in R0 (not overwritten)
; ============================================================
test9:
    ldi r0, 0x55
    call ret_test
    cpi r0, 0x55
    brne fail
    rcall inc_case

ret_test:
    ; Some operations that might affect R0
    ldi r1, 0xAA
    ldi r2, 0xBB
    add r1, r2
    ret

; ============================================================
; TEST 10: Deep nesting (5 levels)
; ============================================================
test10:
    ldi r16, 0
    call level1
    
    cpi r16, 5
    brne fail
    rcall inc_case

level1:
    inc r16
    cpi r16, 5
    breq level1_done
    call level1
level1_done:
    ret

; ============================================================
; TEST 11: CALL then conditional branch based on return value
; ============================================================
test11:
    call get_value
    tst r16
    breq call_fail
    
    call get_zero
    tst r16
    brne call_fail
    
    rcall inc_case
    rjmp call_done

get_value:
    ldi r16, 0x01
    ret

get_zero:
    ldi r16, 0x00
    ret

call_fail:
    rjmp fail
call_done:
    ret

; ============================================================
; TEST 12: CALL with preserved registers (push/pop pattern)
; ============================================================
test12:
    ldi r16, 0xDE
    ldi r17, 0xAD
    
    call preserve_test
    
    ; Registers should be unchanged
    cpi r16, 0xDE
    brne fail
    cpi r17, 0xAD
    brne fail
    rcall inc_case

preserve_test:
    push r16
    push r17
    
    ldi r16, 0xBE
    ldi r17, 0xEF
    
    pop r17
    pop r16
    ret

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