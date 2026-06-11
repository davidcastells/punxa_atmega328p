; ============================================================
; RJMP (Relative Jump) test suite with local trampolines
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ stack_start = 0x08FF
.equ SPH = 0x3E
.equ SPL = 0x3D

reset:
    ldi r16, high(stack_start)
    out SPH, r16
    ldi r16, low(stack_start)
    out SPL, r16
    ldi r16, 1
    sts test_case, r16
    sts final_result, r16
    rjmp test1_start

; ============================================================
; TEST 1: Simple RJMP
; ============================================================
test1_start:
    ldi r16, 0
    rjmp target1
    rjmp local_fail1
target1:
    inc r16
    cpi r16, 1
    brne local_fail1
    rcall inc_case
    rjmp test2_start
local_fail1: jmp fail

; ============================================================
; TEST 2: Forward/Backward RJMP
; ============================================================
test2_start:
    ldi r17, 0
    rjmp forward2
local_fail2: jmp fail
forward2:
    inc r17
    rjmp backward2
backward2:
    inc r17
    cpi r17, 2
    brne local_fail2
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: Verify stack neutrality
; ============================================================
test3_start:
    in r18, SPL
    in r19, SPH
    rjmp stack_check3
stack_return3:
    in r20, SPL
    in r21, SPH
    cp r18, r20
    brne local_fail3
    cp r19, r21
    brne local_fail3
    rcall inc_case
    rjmp test4_start
local_fail3: jmp fail

stack_check3:
    in r22, SPL
    in r23, SPH
    cp r18, r22
    brne local_fail3
    cp r19, r23
    brne local_fail3
    rjmp stack_return3

; ============================================================
; TEST 4: Tight Loop
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
    brne local_fail4
    rcall inc_case
    rjmp test5_start
local_fail4: jmp fail

; ============================================================
; TEST 5: Self-loop
; ============================================================
test5_start:
    ldi r26, 0
    rjmp loop5_entry
local_fail5: jmp fail
loop5_entry:
    inc r26
    cpi r26, 1
    breq loop5_done
    rjmp loop5_entry
loop5_done:
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6-9: Chain and Range
; ============================================================
test6_start:
    ldi r27, 0
    rjmp chain1
local_fail6: jmp fail
chain1: inc r27
        rjmp chain2
chain2: inc r27
        rjmp chain3
chain3: inc r27
        rjmp chain_done
chain_done:
    cpi r27, 3
    brne local_fail6
    rcall inc_case
    rjmp test7_start

test7_start:
    ldi r28, 2
    ldi r30, low(jump_table7)
    ldi r31, high(jump_table7)
    mov r29, r28
    lsl r29
    add r30, r29
    ldi r16, 0
    adc r31, r16
    ijmp
switch_return7:
    cpi r28, 99
    brne local_fail7
    rcall inc_case
    rjmp test8_start
local_fail7: jmp fail
jump_table7:
    rjmp case0_7
    rjmp case1_7
    rjmp case2_7
    rjmp case3_7
case0_7: ldi r28, 0
         rjmp switch_return7
case1_7: ldi r28, 1
         rjmp switch_return7
case2_7: ldi r28, 99
         rjmp switch_return7
case3_7: ldi r28, 3
         rjmp switch_return7

test8_start:
    ldi r29, 0
    rjmp range_target8
local_fail8: jmp fail
range_target8:
    inc r29
    cpi r29, 1
    brne local_fail8
    rcall inc_case
    rjmp test9_start

test9_start:
    ldi r30, 0
    rjmp forward9
local_fail9: jmp fail
forward9:
    inc r30
    rjmp backward9
backward9:
    inc r30
    cpi r30, 2
    brne local_fail9
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10-16: Mixed Jump Types, Loops, and Skips
; ============================================================
test10_start:
    ldi r31, 0
    ldi r30, low(icall_target10)
    ldi r31, high(icall_target10)
    icall
    cpi r31, 1
    brne local_fail10
    rcall inc_case
    rjmp test11_start
local_fail10: jmp fail
icall_target10:
    inc r31
    ret

test11_start:
    ldi r16, 0
    rjmp relative_target11
local_fail11: jmp fail
relative_target11:
    inc r16
    cpi r16, 1
    brne local_fail11
    rcall inc_case
    rjmp test12_start

test12_start:
    ldi r17, 0
    rjmp start_chain12
local_fail12: jmp fail
start_chain12: inc r17
               rjmp middle_chain12
middle_chain12: inc r17
                rjmp end_chain12
end_chain12: inc r17
             cpi r17, 3
             brne local_fail12
             rcall inc_case
             rjmp test13_start

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
    brne local_fail13
    rcall inc_case
    rjmp test14_start
local_fail13: jmp fail

test14_start:
    ldi r20, 0
    rjmp skip_inc14
    inc r20
skip_inc14:
    inc r20
    cpi r20, 1
    brne local_fail14
    rcall inc_case
    rjmp test15_start
local_fail14: jmp fail

test15_start:
    ldi r21, 0
    rjmp level1_15
local_fail15: jmp fail
level1_15: inc r21
           rjmp level2_15
level2_15: inc r21
           rjmp level3_15
level3_15: inc r21
           rjmp level_done15
level_done15:
    cpi r21, 3
    brne local_fail15
    rcall inc_case
    rjmp test16_start

test16_start:
    ldi r22, 1
    rjmp tail_target16
    rjmp fail
tail_target16:
    cpi r22, 1
    brne fail
    rcall inc_case
    rjmp success

; ============================================================
; SUCCESS / FAILURE logic
; ============================================================
success:
    ldi r16, 1
    sts final_result, r16
end: rjmp end

fail:
    ldi r16, 255
    sts final_result, r16
    rjmp end

inc_case:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret