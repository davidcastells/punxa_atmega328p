; ============================================================
; CLN (Clear Negative Flag) test suite
; ============================================================
; Tests that CLN correctly:
; 1. Clears the N flag (bit 2) in SREG (N=0)
; 2. Does not modify any other flags
; 3. Does not modify registers or memory
; ============================================================
; CLN is a 1-word (16-bit) instruction
; Format: 1001 0100 1011 1000 (0x94B8)
; Operation: N <- 0
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D
.equ SREG_ADDR = 0x5F
.equ GPIOR0 = 0x1E

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
; TEST 1: CLN clears the N flag from 1 to 0
; ============================================================
test1_start:
    sen                 ; Set N=1 first
    cln                 ; Should clear N flag
    
    ; Verify N flag is 0
    brpl n_clear1
    rjmp fail
n_clear1:
    rcall inc_case
    rjmp test2_start

; ============================================================
; TEST 2: CLN has no effect when N already 0
; ============================================================
test2_start:
    cln                 ; Ensure N=0
    cln                 ; Second CLN should do nothing (N stays 0)
    
    brpl n_still_clear2
    rjmp fail
n_still_clear2:
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: CLN does not affect other SREG flags (I, T, H, S, V, Z, C)
; ============================================================
test3_start:
    ; Set all flags to known values
    sei                 ; I=1
    set                 ; T=1
    seh                 ; H=1
    sev                 ; V=1
    sez                 ; Z=1
    sec                 ; C=1
    sen                 ; N=1
    
    ; Execute CLN (should clear N, preserve others)
    cln
    
    ; Verify N=0
    brpl n_ok3
    rjmp fail
n_ok3:
    
    ; Verify all other flags unchanged
    brie i_ok3          ; I should be 1
    rjmp fail
i_ok3:
    brts t_ok3          ; T should be 1
    rjmp fail
t_ok3:
    brhs h_ok3          ; H should be 1
    rjmp fail
h_ok3:
    brvs v_ok3          ; V should be 1
    rjmp fail
v_ok3:
    breq z_ok3          ; Z should be 1
    rjmp fail
z_ok3:
    brcs c_ok3          ; C should be 1
    rjmp fail
c_ok3:
    
    rcall inc_case
    rjmp test4_start

; ============================================================
; TEST 4: CLN does not modify registers
; ============================================================
test4_start:
    ldi r16, 0xAA
    ldi r17, 0xBB
    ldi r18, 0xCC
    ldi r19, 0xDD
    
    cln
    
    cpi r16, 0xAA
    brne fail
    cpi r17, 0xBB
    brne fail
    cpi r18, 0xCC
    brne fail
    cpi r19, 0xDD
    brne fail
    rcall inc_case
    rjmp test5_start

; ============================================================
; TEST 5: CLN does not modify SRAM
; ============================================================
test5_start:
    ldi r16, 0xDE
    sts 0x0200, r16
    
    cln
    
    lds r17, 0x0200
    cpi r17, 0xDE
    brne fail
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6: CLN does not modify I/O registers
; ============================================================
test6_start:
    ldi r16, 0xAD
    out GPIOR0, r16
    
    cln
    
    in r17, GPIOR0
    cpi r17, 0xAD
    brne fail
    rcall inc_case
    rjmp test7_start

; ============================================================
; TEST 7: CLN does not affect stack pointer
; ============================================================
test7_start:
    in r16, SPL
    in r17, SPH
    
    cln
    cln
    cln
    
    in r18, SPL
    in r19, SPH
    
    cp r16, r18
    brne fail
    cp r17, r19
    brne fail
    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8: CLN does not affect program flow
; ============================================================
test8_start:
    ldi r16, 0
    cln
    inc r16
    cln
    inc r16
    cln
    inc r16
    
    cpi r16, 3
    brne fail
    rcall inc_case
    rjmp test9_start

; ============================================================
; TEST 9: CLN affects S flag (S = N ⊕ V)
; ============================================================
test9_start:
    ; Case 1: V=0, N=1, CLN sets N=0, so S = 0 ⊕ 0 = 0
    clv                 ; V=0
    sen                 ; N=1
    cln                 ; N=0
    
    brge s_ok9a         ; S=0 should cause BRGE to branch
    rjmp fail
s_ok9a:
    
    ; Case 2: V=1, N=1, CLN sets N=0, so S = 0 ⊕ 1 = 1
    sev                 ; V=1
    sen                 ; N=1
    cln                 ; N=0
    
    brlt s_ok9b         ; S=1 should cause BRLT to branch
    rjmp fail
s_ok9b:
    
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10: CLN multiple times in sequence
; ============================================================
test10_start:
    sen                 ; N=1
    cln                 ; N=0
    cln                 ; N=0 (no change)
    cln                 ; N=0 (no change)
    
    brpl multi_clear_ok10
    rjmp fail
multi_clear_ok10:
    rcall inc_case
    rjmp test11_start

; ============================================================
; TEST 11: CLN then SEN (complete toggle cycle)
; ============================================================
test11_start:
    sen                 ; N=1
    cln                 ; N=0
    sen                 ; N=1
    
    brmi toggle_ok11
    rjmp fail
toggle_ok11:
    rcall inc_case
    rjmp test12_start

; ============================================================
; TEST 12: CLN preserves result of previous arithmetic
; ============================================================
test12_start:
    ldi r16, 0x80       ; -128 in signed
    ldi r17, 0x01
    add r16, r17        ; 0x81, N=1 (negative)
    
    cln                 ; Force N=0
    
    ; Arithmetic result unchanged
    cpi r16, 0x81
    brne fail
    
    ; N flag is now 0 (forced)
    brpl arithmetic_ok12
    rjmp fail
arithmetic_ok12:
    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13: CLN in subroutine (should not affect return)
; ============================================================
test13_start:
    sen                 ; N=1
    rcall cln_sub13
    ; After return, N should be 0
    brpl sub_ok13
    rjmp fail
sub_ok13:
    rcall inc_case
    rjmp test14_start

cln_sub13:
    cln
    ret

; ============================================================
; TEST 14: CLN with SEN in same routine
; ============================================================
test14_start:
    sen                 ; N=1
    cln                 ; N=0
    sen                 ; N=1
    cln                 ; N=0
    
    brpl clear_ok14
    rjmp fail
clear_ok14:
    rcall inc_case
    rjmp test15_start

; ============================================================
; TEST 15: CLN used to force positive condition for branch
; ============================================================
test15_start:
    ; Normally the result would be negative
    ldi r16, 3
    ldi r17, 5
    sub r16, r17        ; 3-5=-2, N=1
    
    ; Force N=0 with CLN
    cln
    
    ; Now branch on positive will be taken
    brpl forced_positive15
    rjmp fail
forced_positive15:
    rcall inc_case
    rjmp test16_start

; ============================================================
; TEST 16: CLN does not affect V flag
; ============================================================
test16_start:
    clv                 ; V=0
    cln                 ; N=0
    
    brvc v_ok16
    rjmp fail
v_ok16:
    
    sev                 ; V=1
    cln                 ; N=0
    
    brvs v_still_set16
    rjmp fail
v_still_set16:
    rcall inc_case
    rjmp test17_start

; ============================================================
; TEST 17: CLN encoding verification (indirect)
; ============================================================
test17_start:
    ; CLN is fixed at 0x94B8
    ; We can't test encoding directly, but we can verify behavior
    sen                 ; N=1
    cln                 ; Should clear N
    brpl encode_ok17
    rjmp fail
encode_ok17:
    rcall inc_case
    rjmp test18_start

; ============================================================
; TEST 18: CLN preserves carry flag
; ============================================================
test18_start:
    sec                 ; C=1
    cln
    
    brcs c_ok18
    rjmp fail
c_ok18:
    
    clc                 ; C=0
    cln
    
    brcc c_still_clear18
    rjmp fail
c_still_clear18:
    rcall inc_case
    rjmp test19_start

; ============================================================
; TEST 19: CLN preserves zero flag
; ============================================================
test19_start:
    sez                 ; Z=1
    cln
    
    breq z_ok19
    rjmp fail
z_ok19:
    
    clz                 ; Z=0
    cln
    
    brne z_still_clear19
    rjmp fail
z_still_clear19:
    rcall inc_case
    rjmp test20_start

; ============================================================
; TEST 20: CLN used before signed branch (forcing greater/equal)
; ============================================================
test20_start:
    ; Make two numbers equal
    ldi r16, 10
    ldi r17, 10
    cp r16, r17         ; Z=1, N=0
    
    ; Force S=0 by making N=0 with V=0
    clv                 ; V=0
    cln                 ; N=0, so S=0
    
    ; Now BRGE (branch if greater/equal, S=0) will be taken
    brge forced_ge20
    rjmp fail
forced_ge20:
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