; ============================================================
; SEN (Set Negative Flag) test suite
; ============================================================
; Tests that SEN correctly:
; 1. Sets the N flag (bit 2) in SREG (N=1)
; 2. Does not modify any other flags
; 3. Does not modify registers or memory
; ============================================================
; SEN is a 1-word (16-bit) instruction
; Format: 1001 0100 0011 1000 (0x9438)
; Operation: N <- 1
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
; TEST 1: SEN sets the N flag from 0 to 1
; ============================================================
test1_start:
    cln                 ; Ensure N=0 first
    sen                 ; Should set N=1
    
    ; Verify N flag is 1
    brmi n_set1
    rjmp fail
n_set1:
    rcall inc_case
    rjmp test2_start

; ============================================================
; TEST 2: SEN has no effect when N already 1
; ============================================================
test2_start:
    sen                 ; Ensure N=1
    sen                 ; Second SEN should do nothing (N stays 1)
    
    brmi n_still_set2
    rjmp fail
n_still_set2:
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: SEN does not affect other SREG flags (I, T, H, S, V, Z, C)
; ============================================================
test3_start:
    ; Clear all flags first
    cli                 ; I=0
    clt                 ; T=0
    clh                 ; H=0
    clv                 ; V=0
    clz                 ; Z=0
    clc                 ; C=0
    cln                 ; N=0
    
    ; Set other flags to 1 (except N which we'll set with SEN)
    sei                 ; I=1
    set                 ; T=1
    seh                 ; H=1
    sev                 ; V=1
    sez                 ; Z=1
    sec                 ; C=1
    
    ; Execute SEN (should set N=1, preserve others)
    sen
    
    ; Verify N=1
    brmi n_ok3
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
; TEST 4: SEN does not modify registers
; ============================================================
test4_start:
    ldi r16, 0xAA
    ldi r17, 0xBB
    ldi r18, 0xCC
    ldi r19, 0xDD
    
    sen
    
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
; TEST 5: SEN does not modify SRAM
; ============================================================
test5_start:
    ldi r16, 0xDE
    sts 0x0200, r16
    
    sen
    
    lds r17, 0x0200
    cpi r17, 0xDE
    brne fail
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6: SEN does not modify I/O registers
; ============================================================
test6_start:
    ldi r16, 0xAD
    out GPIOR0, r16
    
    sen
    
    in r17, GPIOR0
    cpi r17, 0xAD
    brne fail
    rcall inc_case
    rjmp test7_start

; ============================================================
; TEST 7: SEN does not affect stack pointer
; ============================================================
test7_start:
    in r16, SPL
    in r17, SPH
    
    sen
    sen
    sen
    
    in r18, SPL
    in r19, SPH
    
    cp r16, r18
    brne fail
    cp r17, r19
    brne fail
    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8: SEN does not affect program flow
; ============================================================
test8_start:
    ldi r16, 0
    sen
    inc r16
    sen
    inc r16
    sen
    inc r16
    
    cpi r16, 3
    brne fail
    rcall inc_case
    rjmp test9_start

; ============================================================
; TEST 9: SEN affects S flag (S = N ⊕ V)
; ============================================================
test9_start:
    ; Case 1: V=0, SEN sets N=1, so S = 1 ⊕ 0 = 1
    clv                 ; V=0
    cln                 ; N=0
    sen                 ; N=1
    
    brlt s_ok9a         ; S=1 should cause BRLT to branch
    rjmp fail
s_ok9a:
    
    ; Case 2: V=1, SEN sets N=1, so S = 1 ⊕ 1 = 0
    sev                 ; V=1
    cln                 ; N=0
    sen                 ; N=1
    
    brge s_ok9b         ; S=0 should cause BRGE to branch
    rjmp fail
s_ok9b:
    
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10: SEN multiple times in sequence
; ============================================================
test10_start:
    cln                 ; N=0
    sen                 ; N=1
    sen                 ; N=1 (no change)
    sen                 ; N=1 (no change)
    
    brmi multi_set_ok10
    rjmp fail
multi_set_ok10:
    rcall inc_case
    rjmp test11_start

; ============================================================
; TEST 11: SEN then CLN (complete toggle cycle)
; ============================================================
test11_start:
    cln                 ; N=0
    sen                 ; N=1
    cln                 ; N=0
    
    brpl toggle_ok11
    rjmp fail
toggle_ok11:
    rcall inc_case
    rjmp test12_start

; ============================================================
; TEST 12: SEN preserves result of previous arithmetic
; ============================================================
test12_start:
    ldi r16, 0x10
    ldi r17, 0x20
    add r16, r17        ; 0x30, N=0
    
    sen                 ; Force N=1
    
    ; Arithmetic result unchanged
    cpi r16, 0x30
    brne fail
    
    ; N flag is now 1 (forced)
    brmi arithmetic_ok12
    rjmp fail
arithmetic_ok12:
    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13: SEN in subroutine (should not affect return)
; ============================================================
test13_start:
    cln                 ; N=0
    rcall sen_sub13
    ; After return, N should be 1
    brmi sub_ok13
    rjmp fail
sub_ok13:
    rcall inc_case
    rjmp test14_start

sen_sub13:
    sen
    ret

; ============================================================
; TEST 14: SEN with CLN in same routine
; ============================================================
test14_start:
    cln                 ; N=0
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
; TEST 15: SEN used to force negative condition for branch
; ============================================================
test15_start:
    ; Normally the result would be positive
    ldi r16, 5
    ldi r17, 3
    sub r16, r17        ; 5-3=2, N=0
    
    ; Force N=1 with SEN
    sen
    
    ; Now branch on negative will be taken
    brmi forced_negative15
    rjmp fail
forced_negative15:
    rcall inc_case
    rjmp test16_start

; ============================================================
; TEST 16: SEN does not affect V flag
; ============================================================
test16_start:
    clv                 ; V=0
    sen                 ; N=1
    
    brvc v_ok16
    rjmp fail
v_ok16:
    
    sev                 ; V=1
    sen                 ; N=1
    
    brvs v_still_set16
    rjmp fail
v_still_set16:
    rcall inc_case
    rjmp test17_start

; ============================================================
; TEST 17: SEN encoding verification (indirect)
; ============================================================
test17_start:
    ; SEN is fixed at 0x9438
    ; We can't test encoding directly, but we can verify behavior
    cln                 ; N=0
    sen                 ; Should set N=1
    brmi encode_ok17
    rjmp fail
encode_ok17:
    rcall inc_case
    rjmp test18_start

; ============================================================
; TEST 18: SEN preserves carry flag
; ============================================================
test18_start:
    sec                 ; C=1
    sen
    
    brcs c_ok18
    rjmp fail
c_ok18:
    
    clc                 ; C=0
    sen
    
    brcc c_still_clear18
    rjmp fail
c_still_clear18:
    rcall inc_case
    rjmp test19_start

; ============================================================
; TEST 19: SEN preserves zero flag
; ============================================================
test19_start:
    sez                 ; Z=1
    sen
    
    breq z_ok19
    rjmp fail
z_ok19:
    
    clz                 ; Z=0
    sen
    
    brne z_still_clear19
    rjmp fail
z_still_clear19:
    rcall inc_case
    rjmp test20_start

; ============================================================
; TEST 20: SEN used before signed branch (forcing less than)
; ============================================================
test20_start:
    ; Make two numbers equal
    ldi r16, 10
    ldi r17, 10
    cp r16, r17         ; Z=1, N=0
    
    ; Force S=1 by setting N=1 with V=0
    clv                 ; V=0
    sen                 ; N=1, so S=1
    
    ; Now BRLT (branch if less than, S=1) will be taken
    brlt forced_lt20
    rjmp fail
forced_lt20:
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