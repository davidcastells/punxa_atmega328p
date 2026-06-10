; ============================================================
; IJMP (Indirect Jump) test suite with local trampolines
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
    rjmp test1

; ============================================================
; TEST 1: Simple IJMP to a label
; ============================================================
test1:
    ldi r16, 0
    ldi r30, low(target1)
    ldi r31, high(target1)
    ijmp
    rjmp fail
target1:
    inc r16
    cpi r16, 1
    brne local_fail1
    rcall inc_case
    rjmp test2
local_fail1: jmp fail

; ============================================================
; TEST 2: IJMP using jump table
; ============================================================
test2:
    ldi r17, 0
    ldi r30, low(func0)
    ldi r31, high(func0)
    ijmp
back_func0:
    ldi r30, low(func1)
    ldi r31, high(func1)
    ijmp
back_func1:
    ldi r30, low(func2)
    ldi r31, high(func2)
    ijmp
back_func2:
    cpi r17, 6
    brne local_fail2
    rcall inc_case
    rjmp test3
local_fail2: jmp fail

func0: inc r17
       inc r17
       rjmp back_func0
func1: inc r17
       inc r17
       rjmp back_func1
func2: inc r17
       inc r17
       rjmp back_func2

; ============================================================
; TEST 3: Verify IJMP does NOT affect stack
; ============================================================
test3:
    in r18, SPL
    in r19, SPH
    ldi r30, low(stack_check)
    ldi r31, high(stack_check)
    ijmp
stack_return:
    in r20, SPL
    in r21, SPH
    cp r18, r20
    brne local_fail3
    cp r19, r21
    brne local_fail3
    rcall inc_case
    rjmp test4
local_fail3: jmp fail

stack_check:
    in r22, SPL
    in r23, SPH
    cp r18, r22
    brne local_fail3
    cp r19, r23
    brne local_fail3
    rjmp stack_return

; ============================================================
; TEST 4: IJMP with address calculated at runtime
; ============================================================
test4:
    ldi r24, 0
    rcall calc_jump
    ldi r24, 1
    rcall calc_jump
    ldi r24, 2
    rcall calc_jump
    cpi r25, 3
    brne local_fail4
    rcall inc_case
    rjmp test5
local_fail4: jmp fail

calc_jump:
    push r30
    push r31
    ldi r30, low(jump_table)
    ldi r31, high(jump_table)
    lsl r24
    add r30, r24
    ldi r16, 0
    adc r31, r16
    ijmp
jump_table:
    rjmp dyn_func0
    rjmp dyn_func1
    rjmp dyn_func2
dyn_func0: inc r25
           pop r31
           pop r30
           ret
dyn_func1: inc r25
           pop r31
           pop r30
           ret
dyn_func2: inc r25
           pop r31
           pop r30
           ret

; ============================================================
; TEST 5: IJMP to itself
; ============================================================
test5:
    ldi r26, 0
    ldi r30, low(self_check)
    ldi r31, high(self_check)
    ijmp
self_done:
    cpi r26, 2
    brne local_fail5
    rcall inc_case
    rjmp test6
local_fail5: jmp fail

self_check:
    inc r26
    ldi r30, low(self_check2)
    ldi r31, high(self_check2)
    ijmp
self_check2:
    inc r26
    rjmp self_done

; ============================================================
; TEST 6: IJMP switch statement
; ============================================================
test6:
    ldi r27, 2
    ldi r30, low(switch_table)
    ldi r31, high(switch_table)
    lsl r27
    add r30, r27
    ldi r16, 0
    adc r31, r16
    ijmp
switch_return:
    cpi r28, 2
    brne local_fail6
    rcall inc_case
    rjmp test7
local_fail6: jmp fail

switch_table:
    rjmp case0
    rjmp case1
    rjmp case2
case0: ldi r28, 0
       rjmp switch_return
case1: ldi r28, 1
       rjmp switch_return
case2: ldi r28, 2
       rjmp switch_return

; ============================================================
; TEST 7: IJMP with Z modified
; ============================================================
test7:
    ldi r30, low(base_addr)
    ldi r31, high(base_addr)
    adiw r30, 2
    ijmp
modify_return:
    cpi r29, 2
    brne local_fail7
    rcall inc_case
    rjmp test8
local_fail7: jmp fail

base_addr:
    inc r29 ; Skipped
    rjmp local_fail7
    inc r29 ; Target
    rjmp modify_return

; ============================================================
; TEST 8: Encoding
; ============================================================
test8:
    ldi r30, low(encoding_target)
    ldi r31, high(encoding_target)
    ijmp
encoding_return:
    rcall inc_case
    rjmp test9
encoding_target: rjmp encoding_return

; ============================================================
; TEST 9: Loop dynamic dispatch
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
    brne local_fail9
    rcall inc_case
    rjmp test10
local_fail9: jmp fail
loop_target: inc r16
             rjmp loop_return

; ============================================================
; TEST 10: IJMP to RET
; ============================================================
test10:
    ldi r18, 0x55
    ldi r30, low(just_ret)
    ldi r31, high(just_ret)
    ijmp
ret_done:
    cpi r18, 0x55
    brne local_fail10
    rcall inc_case
    rjmp test11
local_fail10: jmp fail
just_ret: ret

; ============================================================
; TEST 11: Compare IJMP/ICALL behavior
; ============================================================
test11:
    ldi r19, 0
    ldi r30, low(ijmp_test_target)
    ldi r31, high(ijmp_test_target)
    ijmp
ijmp_test_target:
    inc r19
    ldi r30, low(ijmp_return)
    ldi r31, high(ijmp_return)
    ijmp
ijmp_return:
    cpi r19, 1
    brne local_fail11
    rcall inc_case
    rjmp test12
local_fail11: jmp fail

; ============================================================
; TEST 12: State machine
; ============================================================
test12:
    ldi r20, 0
state_machine:
    ldi r30, low(state_table)
    ldi r31, high(state_table)
    mov r21, r20
    lsl r21
    add r30, r21
    ldi r16, 0
    adc r31, r16
    ijmp
state_table:
    rjmp state0
    rjmp state1
    rjmp state2
    rjmp success
state0: inc r20
        rjmp state_machine
state1: inc r20
        rjmp state_machine
state2: inc r20
        rjmp state_machine

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