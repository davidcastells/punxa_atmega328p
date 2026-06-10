; ============================================================
; IJMP (Indirect Jump) test suite
; ============================================================
; Tests that IJMP correctly:
; 1. Jumps to the address in Z-pointer (R31:R30)
; 2. Does NOT modify the stack
; 3. Does NOT save a return address
; ============================================================
; IJMP is a 1-word (16-bit) instruction
; Format: 1001 0100 0001 1001 (0x9409)
; Operation: PC <- Z (R31:R30)
; No stack operation, no return address saved
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D

reset:
    ; Initialize stack pointer (though IJMP doesn't use it)
    ldi r16, high(0x08FF)
    out SPH, r16
    ldi r16, low(0x08FF)
    out SPL, r16

    ldi r16, 1
    sts test_case, r16
    sts final_result, r16

; ============================================================
; TEST 1: Simple IJMP to a label
; ============================================================
test1:
    ldi r16, 0
    ldi r30, low(target1)
    ldi r31, high(target1)
    ijmp
    rjmp fail           ; Should not execute

target1:
    inc r16
    cpi r16, 1
    brne fail
    rcall inc_case

; ============================================================
; TEST 2: IJMP using computed address (jump table)
; ============================================================
test2:
    ldi r17, 0
    
    ; Jump to function 0
    ldi r30, low(func0)
    ldi r31, high(func0)
    ijmp
back_func0:
    
    ; Jump to function 1
    ldi r30, low(func1)
    ldi r31, high(func1)
    ijmp
back_func1:
    
    ; Jump to function 2
    ldi r30, low(func2)
    ldi r31, high(func2)
    ijmp
back_func2:
    
    cpi r17, 0x06
    brne fail
    rcall inc_case
    rjmp test2_done

func0:
    inc r17
    inc r17
    rjmp back_func0
func1:
    inc r17
    inc r17
    rjmp back_func1
func2:
    inc r17
    inc r17
    rjmp back_func2

test2_done:

; ============================================================
; TEST 3: Verify that IJMP does NOT affect stack
; ============================================================
test3:
    ; Read initial SP
    in r18, SPL
    in r19, SPH
    
    ldi r30, low(stack_check)
    ldi r31, high(stack_check)
    ijmp
stack_return:
    
    ; Read SP after IJMP and return
    in r20, SPL
    in r21, SPH
    
    ; SP should be unchanged
    cp r18, r20
    brne fail
    cp r19, r21
    brne fail
    rcall inc_case
    rjmp test3_done

stack_check:
    ; SP should be same as before IJMP
    in r22, SPL
    in r23, SPH
    cp r18, r22
    brne stack_fail
    cp r19, r23
    brne stack_fail
    rjmp stack_return
stack_fail:
    rjmp fail

test3_done:

; ============================================================
; TEST 4: IJMP with address calculated at runtime
; ============================================================
test4:
    ldi r24, 0          ; Select function 0
    call calc_jump
    
    ldi r24, 1          ; Select function 1
    call calc_jump
    
    ldi r24, 2          ; Select function 2
    call calc_jump
    
    cpi r25, 0x03
    brne fail
    rcall inc_case
    rjmp test4_done

calc_jump:
    push r30
    push r31
    
    ; Base address of jump table
    ldi r30, low(jump_table)
    ldi r31, high(jump_table)
    
    ; Each entry is 2 words (4 bytes) for RJMP
    lsl r24             ; Multiply index by 2 (words)
    add r30, r24
    clr r24
    adc r31, r24
    
    ; Load the target address (simplified - in real code,
    ; you'd have a table of addresses)
    ijmp

jump_table:
    rjmp dyn_func0
    rjmp dyn_func1
    rjmp dyn_func2

dyn_func0:
    inc r25
    pop r31
    pop r30
    ret
dyn_func1:
    inc r25
    pop r31
    pop r30
    ret
dyn_func2:
    inc r25
    pop r31
    pop r30
    ret

test4_done:

; ============================================================
; TEST 5: IJMP to itself (infinite loop simulation)
; ============================================================
test5:
    ldi r26, 0
    ldi r30, low(self_check)
    ldi r31, high(self_check)
    ijmp
self_done:
    cpi r26, 1
    brne fail
    rcall inc_case
    rjmp test5_done

self_check:
    inc r26
    ; Jump back to check
    ldi r30, low(self_check2)
    ldi r31, high(self_check2)
    ijmp

self_check2:
    inc r26
    cpi r26, 2
    breq self_exit
    rjmp fail
self_exit:
    rjmp self_done

test5_done:

; ============================================================
; TEST 6: IJMP used as a switch statement
; ============================================================
test6:
    ldi r27, 2          ; Case 2
    
    ; Load base of jump table
    ldi r30, low(switch_table)
    ldi r31, high(switch_table)
    
    ; Add case index * 2 (each entry 2 words)
    lsl r27
    add r30, r27
    clr r27
    adc r31, r27
    
    ijmp
switch_return:
    cpi r28, 0x03
    brne fail
    rcall inc_case
    rjmp test6_done

switch_table:
    rjmp case0
    rjmp case1
    rjmp case2
    rjmp case3

case0:
    ldi r28, 0
    rjmp switch_return
case1:
    ldi r28, 1
    rjmp switch_return
case2:
    ldi r28, 2
    rjmp switch_return
case3:
    ldi r28, 3
    rjmp switch_return

test6_done:

; ============================================================
; TEST 7: IJMP with Z modified before jump
; ============================================================
test7:
    ldi r30, low(base_addr)
    ldi r31, high(base_addr)
    
    ; Add offset to Z
    adiw r30, 4         ; Skip first function
    
    ijmp
modify_return:
    cpi r29, 0x02
    brne fail
    rcall inc_case
    rjmp test7_done

base_addr:
    ; Function 0 (skipped)
    ldi r29, 1
    rjmp fail
    ; Function 1 (target)
    ldi r29, 2
    rjmp modify_return

test7_done:

; ============================================================
; TEST 8: Verify IJMP encoding (fixed opcode)
; IJMP is fixed at 0x9409 (little-endian: 0x09 0x94)
; ============================================================
test8:
    ; We can't easily test encoding in assembly,
    ; but we can verify IJMP works correctly
    ldi r30, low(encoding_target)
    ldi r31, high(encoding_target)
    ijmp
encoding_return:
    rcall inc_case
    rjmp test8_done

encoding_target:
    rjmp encoding_return

test8_done:

; ============================================================
; TEST 9: IJMP within a loop (dynamic dispatch)
; ============================================================
test9:
    ldi r16, 0
    ldi r17, 5
    
loop_ijmp:
    ldi r30, low(loop_target)
    ldi r31, high(loop_target)
    ijmp
loop_return:
    dec r17
    brne loop_ijmp
    
    cpi r16, 5
    brne fail
    rcall inc_case
    rjmp test9_done

loop_target:
    inc r16
    rjmp loop_return

test9_done:

; ============================================================
; TEST 10: IJMP to RET (should just return to caller)
; ============================================================
test10:
    ldi r18, 0x55
    
    ldi r30, low(just_ret)
    ldi r31, high(just_ret)
    ijmp
ret_done:
    cpi r18, 0x55
    brne fail
    rcall inc_case
    rjmp test10_done

just_ret:
    ret

test10_done:

; ============================================================
; TEST 11: Compare IJMP and ICALL (no return address push)
; ============================================================
test11:
    ldi r19, 0
    
    ; Test that IJMP doesn't push return address
    ldi r30, low(ijmp_test_target)
    ldi r31, high(ijmp_test_target)
    ijmp
ijmp_should_not_return:
    ; This should NOT execute because IJMP doesn't return
    rjmp fail

ijmp_test_target:
    inc r19
    ; Manually jump back
    ldi r30, low(ijmp_return)
    ldi r31, high(ijmp_return)
    ijmp

ijmp_return:
    cpi r19, 1
    brne fail
    rcall inc_case
    rjmp test11_done

test11_done:

; ============================================================
; TEST 12: Complex state machine using IJMP
; ============================================================
test12:
    ldi r20, 0          ; State 0
    
state_machine:
    ldi r30, low(state_table)
    ldi r31, high(state_table)
    
    ; Add state * 2 (each entry 2 words)
    mov r21, r20
    lsl r21
    add r30, r21
    clr r21
    adc r31, r21
    
    ijmp

state_table:
    rjmp state0
    rjmp state1
    rjmp state2
    rjmp state_done

state0:
    inc r20
    rjmp state_machine
state1:
    inc r20
    rjmp state_machine
state2:
    inc r20
    rjmp state_machine
state_done:
    cpi r20, 3
    brne fail
    rcall inc_case
    rjmp test12_done

test12_done:

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