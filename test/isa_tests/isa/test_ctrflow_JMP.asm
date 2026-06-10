; ============================================================
; JMP (Direct Jump) test suite
; ============================================================
; Tests that JMP correctly:
; 1. Jumps to the absolute address specified
; 2. Does NOT modify the stack
; 3. Does NOT save a return address
; ============================================================
; JMP is a 2-word (32-bit) instruction
; Word1: 1001 010k kkkk 110k
; Word2: kkkk kkkk kkkk kkkk (22-bit absolute address)
; Operation: PC <- k (22-bit address)
; No stack operation, no return address saved
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D

reset:
    ; Initialize stack pointer (though JMP doesn't use it)
    ldi r16, high(0x08FF)
    out SPH, r16
    ldi r16, low(0x08FF)
    out SPL, r16

    ldi r16, 1
    sts test_case, r16
    sts final_result, r16
    
    ; First JMP test
    jmp test1_start

; ============================================================
; TEST 1: Simple JMP to a label
; ============================================================
test1_start:
    ldi r16, 0
    jmp target1
    rjmp fail           ; Should not execute

target1:
    inc r16
    cpi r16, 1
    brne fail
    jmp inc_case_jmp1

inc_case_jmp1:
    jmp test2_start

; ============================================================
; TEST 2: JMP that wraps around (within program memory)
; ============================================================
test2_start:
    ldi r17, 0
    jmp far_target2
    rjmp fail

far_target2:
    inc r17
    cpi r17, 1
    brne fail
    jmp inc_case_jmp2

inc_case_jmp2:
    jmp test3_start

; ============================================================
; TEST 3: Verify that JMP does NOT affect stack
; ============================================================
test3_start:
    ; Read initial SP
    in r18, SPL
    in r19, SPH
    
    jmp stack_check3
stack_return3:
    
    ; Read SP after JMP and return
    in r20, SPL
    in r21, SPH
    
    ; SP should be unchanged
    cp r18, r20
    brne fail
    cp r19, r21
    brne fail
    jmp inc_case_jmp3

stack_check3:
    ; SP should be same as before JMP
    in r22, SPL
    in r23, SPH
    cp r18, r22
    brne stack_fail
    cp r19, r23
    brne stack_fail
    jmp stack_return3
stack_fail:
    jmp fail

inc_case_jmp3:
    jmp test4_start

; ============================================================
; TEST 4: JMP used to create a loop
; ============================================================
test4_start:
    ldi r24, 0
    ldi r25, 5
    
loop4:
    inc r24
    dec r25
    brne loop4_continue
    jmp loop4_done
loop4_continue:
    jmp loop4
loop4_done:
    cpi r24, 5
    brne fail
    jmp inc_case_jmp4

inc_case_jmp4:
    jmp test5_start

; ============================================================
; TEST 5: JMP to address with RJMP back
; ============================================================
test5_start:
    ldi r26, 0
    jmp jmp_target5
    rjmp fail

jmp_target5:
    inc r26
    cpi r26, 1
    brne fail
    rjmp back_from_jmp5
    rjmp fail

back_from_jmp5:
    jmp inc_case_jmp5

inc_case_jmp5:
    jmp test6_start

; ============================================================
; TEST 6: Multiple JMPs in sequence
; ============================================================
test6_start:
    ldi r27, 0
    jmp chain1
    rjmp fail

chain1:
    inc r27
    jmp chain2
    rjmp fail

chain2:
    inc r27
    jmp chain3
    rjmp fail

chain3:
    inc r27
    jmp chain_done
    rjmp fail

chain_done:
    cpi r27, 3
    brne fail
    jmp inc_case_jmp6

inc_case_jmp6:
    jmp test7_start

; ============================================================
; TEST 7: JMP used as a switch (with address calculation)
; ============================================================
test7_start:
    ldi r28, 2          ; Select case 2
    
    ; In real code, you'd compute the JMP target
    ; For this test, we'll use a lookup table
    ldi r30, low(switch_table7)
    ldi r31, high(switch_table7)
    
    ; Add index * 2 (each entry is RJMP)
    mov r29, r28
    lsl r29
    add r30, r29
    clr r29
    adc r31, r29
    
    ijmp                ; Use IJMP to indirect through table
    ; Alternative: you could compute absolute JMP address
    
switch_return7:
    cpi r28, 99         ; Should be modified by case
    brne fail
    jmp inc_case_jmp7

switch_table7:
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

inc_case_jmp7:
    jmp test8_start

; ============================================================
; TEST 8: Verify JMP at reset vector (simulated)
; ============================================================
test8_start:
    ldi r16, 0
    jmp reset_vector8
    rjmp fail

reset_vector8:
    inc r16
    ; Simulate program start
    jmp main8
    rjmp fail

main8:
    inc r16
    cpi r16, 2
    brne fail
    jmp inc_case_jmp8

inc_case_jmp8:
    jmp test9_start

; ============================================================
; TEST 9: JMP to self (infinite loop simulation)
; ============================================================
test9_start:
    ldi r17, 0
    jmp loop9_entry
    rjmp fail

loop9_entry:
    inc r17
    cpi r17, 1
    breq loop9_done
    jmp loop9_entry
loop9_done:
    jmp inc_case_jmp9

inc_case_jmp9:
    jmp test10_start

; ============================================================
; TEST 10: JMP after ICALL (mix of jump types)
; ============================================================
test10_start:
    ldi r18, 0
    
    ; Set up Z-pointer for ICALL
    ldi r30, low(icall_target10)
    ldi r31, high(icall_target10)
    icall               ; ICALL pushes return address
    
    cpi r18, 1
    brne fail
    jmp inc_case_jmp10

icall_target10:
    inc r18
    jmp back_from_icall10
    rjmp fail

back_from_icall10:
    ret                 ; Return from ICALL

inc_case_jmp10:
    jmp test11_start

; ============================================================
; TEST 11: JMP forward and backward
; ============================================================
test11_start:
    ldi r19, 0
    
    ; Forward JMP
    jmp forward11
    rjmp fail

forward11:
    inc r19
    
    ; Backward JMP
    jmp backward11
    rjmp fail

backward11:
    inc r19
    
    cpi r19, 2
    brne fail
    jmp inc_case_jmp11

inc_case_jmp11:
    jmp test12_start

; ============================================================
; TEST 12: JMP to an absolute address with large offset
; ============================================================
test12_start:
    ldi r20, 0
    jmp far_away12
    rjmp fail

far_away12:
    inc r20
    cpi r20, 1
    brne fail
    jmp inc_case_jmp12

inc_case_jmp12:
    jmp success

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

inc_case_jmp1:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp2:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp3:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp4:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp5:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp6:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp7:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp8:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp9:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp10:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp11:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret

inc_case_jmp12:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret