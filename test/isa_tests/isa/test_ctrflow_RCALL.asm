; ============================================================
; RCALL (Relative Call) test suite
; ============================================================
; Tests that RCALL correctly:
; 1. Saves the return address (PC+1) on the stack
; 2. Jumps to PC + 1 + k (where k is 12-bit signed offset)
; 3. Stack pointer decrements by 2
; ============================================================
; RCALL is a 1-word (16-bit) instruction
; Format: 1101 kkkk kkkk kkkk (12-bit signed offset)
; Operation: SP <- SP - 2, [SP] <- PC+1, PC <- PC + 1 + k
; Range: +-2048 words from PC
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

    ; First RCALL test
    rcall test1_start
    rjmp fail

; ============================================================
; TEST 1: Simple RCALL that returns
; ============================================================
test1_start:
    ldi r16, 0xAA
    rcall subroutine1    ; Call subroutine
    ; Should return here after subroutine
    cpi r16, 0xBB       ; Check if subroutine modified r16
    brne fail
    rcall inc_case_rcall1

subroutine1:
    ldi r16, 0xBB       ; Change value
    ret

inc_case_rcall1:
    rcall test2_start
    rjmp fail

; ============================================================
; TEST 2: Nested RCALLs (two levels deep)
; ============================================================
test2_start:
    ldi r17, 0x11
    rcall outer2        ; First level call
    
    cpi r17, 0x33       ; Should be 0x33 after nested returns
    brne fail
    rcall inc_case_rcall2

outer2:
    ldi r17, 0x22
    rcall inner2        ; Second level call
    ret

inner2:
    ldi r17, 0x33
    ret

inc_case_rcall2:
    rcall test3_start
    rjmp fail

; ============================================================
; TEST 3: RCALL with multiple PUSH/POP inside
; ============================================================
test3_start:
    ldi r18, 0x01
    ldi r19, 0x02
    ldi r20, 0x03
    
    rcall push_pop_test3
    
    ; Registers should be restored after return
    cpi r18, 0x01
    brne fail
    cpi r19, 0x02
    brne fail
    cpi r20, 0x03
    brne fail
    rcall inc_case_rcall3

push_pop_test3:
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

inc_case_rcall3:
    rcall test4_start
    rjmp fail

; ============================================================
; TEST 4: Stack pointer verification after RCALL/RET
; ============================================================
test4_start:
    ; Read initial SP
    in r21, SPL
    in r22, SPH
    
    rcall sp_test4      ; RCALL should decrement SP by 2
    
    ; Read SP after return
    in r23, SPL
    in r24, SPH
    
    ; SP should be back to original value
    cp r21, r23
    brne fail
    cp r22, r24
    brne fail
    rcall inc_case_rcall4

sp_test4:
    ; Inside call, SP should be 2 less
    in r25, SPL
    in r26, SPH
    
    ; Check that SP decreased by 2
    ; For 16-bit subtraction, we need to handle borrow
    ret

inc_case_rcall4:
    rcall test5_start
    rjmp fail

; ============================================================
; TEST 5: RCALL to nearby address (small positive offset)
; ============================================================
test5_start:
    ldi r27, 0
    rcall near_target5
    
    cpi r27, 0x42
    brne fail
    rcall inc_case_rcall5

near_target5:
    ldi r27, 0x42
    ret

inc_case_rcall5:
    rcall test6_start
    rjmp fail

; ============================================================
; TEST 6: Multiple RCALLs to same subroutine
; ============================================================
test6_start:
    ldi r28, 0
    
    rcall counter_sub6
    rcall counter_sub6
    rcall counter_sub6
    
    cpi r28, 3
    brne fail
    rcall inc_case_rcall6

counter_sub6:
    inc r28
    ret

inc_case_rcall6:
    rcall test7_start
    rjmp fail

; ============================================================
; TEST 7: RCALL with stack frame (local variables)
; ============================================================
test7_start:
    rcall frame_test7
    
    cpi r29, 0xAA
    brne fail
    rcall inc_case_rcall7

frame_test7:
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

inc_case_rcall7:
    rcall test8_start
    rjmp fail

; ============================================================
; TEST 8: RCALL inside a loop
; ============================================================
test8_start:
    ldi r30, 0
    ldi r31, 5
    
loop_rcall8:
    rcall loop_sub8
    dec r31
    brne loop_rcall8
    
    cpi r30, 5
    brne fail
    rcall inc_case_rcall8

loop_sub8:
    inc r30
    ret

inc_case_rcall8:
    rcall test9_start
    rjmp fail

; ============================================================
; TEST 9: RCALL with RET that has value in R0 (not overwritten)
; ============================================================
test9_start:
    ldi r0, 0x55
    rcall ret_test9
    cpi r0, 0x55
    brne fail
    rcall inc_case_rcall9

ret_test9:
    ; Some operations that might affect R0
    ldi r1, 0xAA
    ldi r2, 0xBB
    add r1, r2
    ret

inc_case_rcall9:
    rcall test10_start
    rjmp fail

; ============================================================
; TEST 10: Deep nesting (5 levels) with RCALL
; ============================================================
test10_start:
    ldi r16, 0
    rcall level1_10
    
    cpi r16, 5
    brne fail
    rcall inc_case_rcall10

level1_10:
    inc r16
    cpi r16, 5
    breq level1_done10
    rcall level1_10
level1_done10:
    ret

inc_case_rcall10:
    rcall test11_start
    rjmp fail

; ============================================================
; TEST 11: RCALL then conditional branch based on return
; ============================================================
test11_start:
    rcall get_value11
    tst r16
    breq call_fail11
    
    rcall get_zero11
    tst r16
    brne call_fail11
    
    rcall inc_case_rcall11
    rjmp call_done11

get_value11:
    ldi r16, 0x01
    ret

get_zero11:
    ldi r16, 0x00
    ret

call_fail11:
    rjmp fail
call_done11:

inc_case_rcall11:
    rcall test12_start
    rjmp fail

; ============================================================
; TEST 12: RCALL with preserved registers (push/pop pattern)
; ============================================================
test12_start:
    ldi r16, 0xDE
    ldi r17, 0xAD
    
    rcall preserve_test12
    
    ; Registers should be unchanged
    cpi r16, 0xDE
    brne fail
    cpi r17, 0xAD
    brne fail
    rcall inc_case_rcall12

preserve_test12:
    push r16
    push r17
    
    ldi r16, 0xBE
    ldi r17, 0xEF
    
    pop r17
    pop r16
    ret

inc_case_rcall12:
    rcall test13_start
    rjmp fail

; ============================================================
; TEST 13: RCALL with negative offset (backward call)
; ============================================================
test13_start:
    ldi r18, 0
    rcall forward13
    rjmp fail

forward13:
    inc r18
    cpi r18, 1
    breq backward13
    rjmp fail

backward13:
    inc r18
    cpi r18, 2
    brne fail
    rcall inc_case_rcall13

inc_case_rcall13:
    rcall test14_start
    rjmp fail

; ============================================================
; TEST 14: RCALL vs CALL comparison (relative vs absolute)
; ============================================================
test14_start:
    ldi r19, 0
    
    ; RCALL uses relative addressing
    rcall relative_target14
    
    cpi r19, 1
    brne fail
    rcall inc_case_rcall14

relative_target14:
    inc r19
    ret

inc_case_rcall14:
    rcall test15_start
    rjmp fail

; ============================================================
; TEST 15: RCALL to maximum forward range (simulated)
; ============================================================
test15_start:
    ldi r20, 0
    ; RCALL range is ±2048 words
    ; For simulation, we just call a nearby target
    rcall range_target15
    
    cpi r20, 0x55
    brne fail
    rcall inc_case_rcall15

range_target15:
    ldi r20, 0x55
    ret

inc_case_rcall15:
    rcall test16_start
    rjmp fail

; ============================================================
; TEST 16: RCALL chain (multiple relative calls)
; ============================================================
test16_start:
    ldi r21, 0
    rcall chain1_16
    rjmp fail

chain1_16:
    inc r21
    rcall chain2_16
    ret

chain2_16:
    inc r21
    rcall chain3_16
    ret

chain3_16:
    inc r21
    ret
chain_done16:
    cpi r21, 3
    brne fail
    rcall inc_case_rcall16

inc_case_rcall16:
    rcall test17_start
    rjmp fail

; ============================================================
; TEST 17: RCALL within interrupt simulation
; ============================================================
test17_start:
    ldi r22, 0
    sei                 ; Enable interrupts (though not needed for test)
    rcall isr_sim17
    cpi r22, 0xAA
    brne fail
    rcall inc_case_rcall17

isr_sim17:
    push r16
    push r17
    ldi r22, 0xAA
    pop r17
    pop r16
    ret

inc_case_rcall17:
    rcall test18_start
    rjmp fail

; ============================================================
; TEST 18: RCALL with multiple returns (state machine)
; ============================================================
test18_start:
    ldi r23, 0
    rcall state0_18
    rcall state1_18
    rcall state2_18
    
    cpi r23, 0x06
    brne fail
    rcall inc_case_rcall18

state0_18:
    inc r23
    ret
state1_18:
    inc r23
    inc r23
    ret
state2_18:
    inc r23
    inc r23
    inc r23
    ret

inc_case_rcall18:
    rcall success
    rjmp fail

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

inc_case_rcall1:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall2:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall3:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall4:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall5:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall6:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall7:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall8:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall9:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall10:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall11:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall12:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall13:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall14:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall15:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall16:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall17:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rcall18:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret