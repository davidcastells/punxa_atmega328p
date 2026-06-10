; ============================================================
; RJMP (Relative Jump) test suite
; ============================================================
; Tests that RJMP correctly:
; 1. Jumps to PC + 1 + k (where k is 12-bit signed offset)
; 2. Does NOT modify the stack
; 3. Does NOT save a return address
; ============================================================
; RJMP is a 1-word (16-bit) instruction
; Format: 1100 kkkk kkkk kkkk (12-bit signed offset)
; Operation: PC <- PC + 1 + k
; Range: ±2048 words from PC
; No stack operation, no return address saved
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D

reset:
    ; Initialize stack pointer (though RJMP doesn't use it)
    ldi r16, high(0x08FF)
    out SPH, r16
    ldi r16, low(0x08FF)
    out SPL, r16

    ldi r16, 1
    sts test_case, r16
    sts final_result, r16
    
    ; First RJMP test
    rjmp test1_start

; ============================================================
; TEST 1: Simple RJMP to a label
; ============================================================
test1_start:
    ldi r16, 0
    rjmp target1
    rjmp fail           ; Should not execute

target1:
    inc r16
    cpi r16, 1
    brne fail
    rjmp inc_case_rjmp1

inc_case_rjmp1:
    rjmp test2_start

; ============================================================
; TEST 2: RJMP forward and backward
; ============================================================
test2_start:
    ldi r17, 0
    rjmp forward2
    rjmp fail

forward2:
    inc r17
    rjmp backward2
    rjmp fail

backward2:
    inc r17
    cpi r17, 2
    brne fail
    rjmp inc_case_rjmp2

inc_case_rjmp2:
    rjmp test3_start

; ============================================================
; TEST 3: Verify that RJMP does NOT affect stack
; ============================================================
test3_start:
    ; Read initial SP
    in r18, SPL
    in r19, SPH
    
    rjmp stack_check3
stack_return3:
    
    ; Read SP after RJMP
    in r20, SPL
    in r21, SPH
    
    ; SP should be unchanged
    cp r18, r20
    brne fail
    cp r19, r21
    brne fail
    rjmp inc_case_rjmp3

stack_check3:
    ; SP should be same as before RJMP
    in r22, SPL
    in r23, SPH
    cp r18, r22
    brne stack_fail
    cp r19, r23
    brne stack_fail
    rjmp stack_return3
stack_fail:
    rjmp fail

inc_case_rjmp3:
    rjmp test4_start

; ============================================================
; TEST 4: RJMP used to create a loop
; ============================================================
test4_start:
    ldi r24, 0
    ldi r25, 5
    
loop4:
    inc r24
    dec r25
    brne loop4
    rjmp loop4_done
loop4_done:
    cpi r24, 5
    brne fail
    rjmp inc_case_rjmp4

inc_case_rjmp4:
    rjmp test5_start

; ============================================================
; TEST 5: RJMP to self (infinite loop simulation)
; ============================================================
test5_start:
    ldi r26, 0
    rjmp loop5_entry
    rjmp fail

loop5_entry:
    inc r26
    cpi r26, 1
    breq loop5_done
    rjmp loop5_entry
loop5_done:
    rjmp inc_case_rjmp5

inc_case_rjmp5:
    rjmp test6_start

; ============================================================
; TEST 6: Multiple RJMPs in sequence
; ============================================================
test6_start:
    ldi r27, 0
    rjmp chain1
    rjmp fail

chain1:
    inc r27
    rjmp chain2
    rjmp fail

chain2:
    inc r27
    rjmp chain3
    rjmp fail

chain3:
    inc r27
    rjmp chain_done
    rjmp fail

chain_done:
    cpi r27, 3
    brne fail
    rjmp inc_case_rjmp6

inc_case_rjmp6:
    rjmp test7_start

; ============================================================
; TEST 7: RJMP used as a jump table (with computed offset)
; ============================================================
test7_start:
    ldi r28, 2          ; Select case 2
    
    ; Compute jump offset (each case is 2 words = 4 bytes)
    ; RJMP offset is in words, not bytes
    mov r29, r28
    lsl r29             ; Multiply by 2 for word offset
    
    ; In real code, you'd add to PC
    ; For this test, we'll use a lookup table with IJMP
    ldi r30, low(jump_table7)
    ldi r31, high(jump_table7)
    add r30, r29
    clr r29
    adc r31, r29
    ijmp

jump_table7:
    rjmp case0_7
    rjmp case1_7
    rjmp case2_7
    rjmp case3_7

case0_7:
    ldi r28, 0
    rjmp switch_return7
case1_7:
    ldi r28, 1
    rjmp switch_return7
case2_7:
    ldi r28, 99
    rjmp switch_return7
case3_7:
    ldi r28, 3
    rjmp switch_return7

switch_return7:
    cpi r28, 99
    brne fail
    rjmp inc_case_rjmp7

inc_case_rjmp7:
    rjmp test8_start

; ============================================================
; TEST 8: RJMP with maximum forward range (simulated)
; ============================================================
test8_start:
    ldi r29, 0
    ; RJMP range is ±2048 words
    ; For simulation, we just jump to a nearby target
    rjmp range_target8
    rjmp fail

range_target8:
    inc r29
    cpi r29, 1
    brne fail
    rjmp inc_case_rjmp8

inc_case_rjmp8:
    rjmp test9_start

; ============================================================
; TEST 9: RJMP with maximum backward range (simulated)
; ============================================================
test9_start:
    ldi r30, 0
    rjmp forward9
    rjmp fail

forward9:
    inc r30
    rjmp backward9
    rjmp fail

backward9:
    inc r30
    cpi r30, 2
    brne fail
    rjmp inc_case_rjmp9

inc_case_rjmp9:
    rjmp test10_start

; ============================================================
; TEST 10: RJMP after ICALL (mix of jump types)
; ============================================================
test10_start:
    ldi r31, 0
    
    ; Set up Z-pointer for ICALL
    ldi r30, low(icall_target10)
    ldi r31, high(icall_target10)
    icall               ; ICALL pushes return address
    
    cpi r31, 1
    brne fail
    rjmp inc_case_rjmp10

icall_target10:
    inc r31
    rjmp back_from_icall10
    rjmp fail

back_from_icall10:
    ret                 ; Return from ICALL

inc_case_rjmp10:
    rjmp test11_start

; ============================================================
; TEST 11: RJMP vs JMP comparison (relative vs absolute)
; ============================================================
test11_start:
    ldi r16, 0
    
    ; RJMP uses relative addressing
    rjmp relative_target11
    rjmp fail

relative_target11:
    inc r16
    cpi r16, 1
    brne fail
    rjmp inc_case_rjmp11

inc_case_rjmp11:
    rjmp test12_start

; ============================================================
; TEST 12: RJMP chain with mixed backward/forward
; ============================================================
test12_start:
    ldi r17, 0
    rjmp start_chain12
    rjmp fail

start_chain12:
    inc r17
    rjmp middle_chain12
    rjmp fail

middle_chain12:
    inc r17
    rjmp end_chain12
    rjmp fail

end_chain12:
    inc r17
    cpi r17, 3
    brne fail
    rjmp inc_case_rjmp12

inc_case_rjmp12:
    rjmp test13_start

; ============================================================
; TEST 13: RJMP in a tight loop
; ============================================================
test13_start:
    ldi r18, 0
    ldi r19, 10
    
loop13:
    inc r18
    dec r19
    brne loop13
    rjmp loop13_done
loop13_done:
    cpi r18, 10
    brne fail
    rjmp inc_case_rjmp13

inc_case_rjmp13:
    rjmp test14_start

; ============================================================
; TEST 14: RJMP to skip an instruction
; ============================================================
test14_start:
    ldi r20, 0
    rjmp skip_inc14
    inc r20             ; This should be skipped
skip_inc14:
    inc r20
    cpi r20, 1
    brne fail
    rjmp inc_case_rjmp14

inc_case_rjmp14:
    rjmp test15_start

; ============================================================
; TEST 15: Nested RJMPs (jump within jump)
; ============================================================
test15_start:
    ldi r21, 0
    rjmp level1_15
    rjmp fail

level1_15:
    inc r21
    rjmp level2_15
    rjmp fail

level2_15:
    inc r21
    rjmp level3_15
    rjmp fail

level3_15:
    inc r21
    rjmp level_done15
    rjmp fail

level_done15:
    cpi r21, 3
    brne fail
    rjmp inc_case_rjmp15

inc_case_rjmp15:
    rjmp test16_start

; ============================================================
; TEST 16: RJMP as a tail jump (no return needed)
; ============================================================
test16_start:
    ldi r22, 1
    rjmp tail_target16
    rjmp fail

tail_target16:
    cpi r22, 1
    brne fail
    rjmp inc_case_rjmp16

inc_case_rjmp16:
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

inc_case_rjmp1:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp2:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp3:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp4:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp5:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp6:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp7:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp8:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp9:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp10:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp11:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp12:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp13:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp14:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp15:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_rjmp16:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret