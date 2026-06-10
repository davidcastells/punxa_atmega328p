; ============================================================
; CLI (Clear Global Interrupt Flag) test suite
; ============================================================
; Tests that CLI correctly:
; 1. Clears the I flag (bit 7) in SREG (I=0)
; 2. Does not modify any other flags
; 3. Does not modify registers or memory
; ============================================================
; CLI is a 1-word (16-bit) instruction
; Format: 1001 0100 1111 1000 (0x94F8)
; Operation: I <- 0
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
; TEST 1: CLI clears the I flag from 1 to 0
; ============================================================
test1_start:
    sei                 ; Set I=1 first
    cli                 ; Should clear I flag
    
    ; Verify I flag is 0
    in r16, SREG_ADDR
    sbrs r16, 7         ; Skip if I=1
    rjmp i_clear1
    rjmp fail
i_clear1:
    rcall inc_case
    rjmp test2_start

; ============================================================
; TEST 2: CLI has no effect when I already 0
; ============================================================
test2_start:
    cli                 ; Ensure I=0
    cli                 ; Second CLI should do nothing
    
    in r16, SREG_ADDR
    sbrs r16, 7         ; Skip if I=1
    rjmp i_still_clear2
    rjmp fail
i_still_clear2:
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: CLI does not affect other SREG flags (Z, C, N, V, S, H, T)
; ============================================================
test3_start:
    ; Set all other flags to known values
    cli                 ; Start with I=0
    
    ; Set flags: C=1, Z=1, N=1, V=1, H=1, T=1
    sec                 ; C=1
    sez                 ; Z=1
    sen                 ; N=1
    sev                 ; V=1
    seh                 ; H=1
    set                 ; T=1
    
    ; Execute CLI (should only clear I)
    cli
    
    ; Verify I=0
    in r16, SREG_ADDR
    sbrs r16, 7
    rjmp i_ok3
    rjmp fail
i_ok3:
    
    ; Verify all other flags unchanged
    brcc fail           ; C should be 1
    brne fail           ; Z should be 1
    brmi fail           ; N should be 1
    brvs fail           ; V should be 1
    brhc fail           ; H should be 1
    brtc fail           ; T should be 1
    
    rcall inc_case
    rjmp test4_start

; ============================================================
; TEST 4: CLI does not modify registers
; ============================================================
test4_start:
    ldi r16, 0xAA
    ldi r17, 0xBB
    ldi r18, 0xCC
    ldi r19, 0xDD
    
    cli
    
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
; TEST 5: CLI does not modify SRAM
; ============================================================
test5_start:
    ldi r16, 0xDE
    sts 0x0200, r16
    
    cli
    
    lds r17, 0x0200
    cpi r17, 0xDE
    brne fail
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6: CLI does not modify I/O registers
; ============================================================
test6_start:
    ldi r16, 0xAD
    out GPIOR0, r16
    
    cli
    
    in r17, GPIOR0
    cpi r17, 0xAD
    brne fail
    rcall inc_case
    rjmp test7_start

; ============================================================
; TEST 7: CLI does not affect stack pointer
; ============================================================
test7_start:
    in r16, SPL
    in r17, SPH
    
    cli
    cli
    cli
    
    in r18, SPL
    in r19, SPH
    
    cp r16, r18
    brne fail
    cp r17, r19
    brne fail
    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8: CLI allows interrupts to be disabled during critical section
; ============================================================
test8_start:
    sei                 ; Enable interrupts
    cli                 ; Disable for critical section
    
    ; Simulate critical section
    ldi r16, 0x55
    ldi r17, 0xAA
    
    ; I should still be 0
    in r18, SREG_ADDR
    sbrs r18, 7
    rjmp critical_ok8
    rjmp fail
critical_ok8:
    rcall inc_case
    rjmp test9_start

; ============================================================
; TEST 9: CLI before SEI (ensure proper toggling)
; ============================================================
test9_start:
    cli                 ; I=0
    sei                 ; I=1
    cli                 ; I=0
    
    in r16, SREG_ADDR
    sbrs r16, 7
    rjmp final_clear9
    rjmp fail
final_clear9:
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10: CLI multiple times in sequence
; ============================================================
test10_start:
    sei                 ; I=1
    cli                 ; I=0
    cli                 ; I=0 (no change)
    cli                 ; I=0 (no change)
    
    in r16, SREG_ADDR
    sbrs r16, 7
    rjmp multi_clear_ok10
    rjmp fail
multi_clear_ok10:
    rcall inc_case
    rjmp test11_start

; ============================================================
; TEST 11: CLI does not affect program flow (non-branch)
; ============================================================
test11_start:
    ldi r16, 0
    cli
    inc r16
    cli
    inc r16
    cli
    inc r16
    
    cpi r16, 3
    brne fail
    rcall inc_case
    rjmp test12_start

; ============================================================
; TEST 12: CLI before interrupt (simulate interrupt masking)
; ============================================================
test12_start:
    sei                 ; I=1
    cli                 ; I=0 - interrupts disabled
    
    ; In a real system, an interrupt occurring now would be ignored
    ; We'll just verify I=0
    in r16, SREG_ADDR
    sbrs r16, 7
    rjmp masked_ok12
    rjmp fail
masked_ok12:
    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13: CLI preserves flags after arithmetic
; ============================================================
test13_start:
    ldi r16, 0x7F
    ldi r17, 0x01
    add r16, r17        ; Sets N=1, V=1, C=0, Z=0, H=1
    
    cli                 ; Should preserve all arithmetic flags
    
    ; Verify flags unchanged (except I)
    brmi n_ok13
    rjmp fail
n_ok13:
    brvs v_ok13
    rjmp fail
v_ok13:
    brcc c_ok13
    rjmp fail
c_ok13:
    brne z_ok13
    rjmp fail
z_ok13:
    brhs h_ok13
    rjmp fail
h_ok13:
    
    rcall inc_case
    rjmp test14_start

; ============================================================
; TEST 14: CLI in subroutine (should not affect return)
; ============================================================
test14_start:
    sei                 ; I=1
    rcall cli_sub14
    ; After return, I should be 0
    in r16, SREG_ADDR
    sbrs r16, 7
    rjmp sub_ok14
    rjmp fail
sub_ok14:
    rcall inc_case
    rjmp test15_start

cli_sub14:
    cli
    ret

; ============================================================
; TEST 15: CLI after push/pop (verify I flag not restored by POP)
; ============================================================
test15_start:
    sei                 ; I=1
    push r16
    cli                 ; I=0
    pop r16             ; POP does not affect SREG
    
    in r17, SREG_ADDR
    sbrs r17, 7
    rjmp pop_no_restore15
    rjmp fail
pop_no_restore15:
    rcall inc_case
    rjmp test16_start

; ============================================================
; TEST 16: CLI then SEI (complete toggle cycle)
; ============================================================
test16_start:
    cli                 ; I=0
    nop
    sei                 ; I=1
    nop
    cli                 ; I=0
    
    in r16, SREG_ADDR
    sbrs r16, 7
    rjmp toggle_ok16
    rjmp fail
toggle_ok16:
    rcall inc_case
    rjmp test17_start

; ============================================================
; TEST 17: CLI encoding verification (indirect)
; ============================================================
test17_start:
    ; CLI is fixed at 0x94F8
    ; We can't test encoding directly, but we can verify behavior
    sei                 ; I=1
    cli                 ; Should set I=0
    in r16, SREG_ADDR
    sbrs r16, 7
    rjmp encode_ok17
    rjmp fail
encode_ok17:
    rcall inc_case
    rjmp test18_start

; ============================================================
; TEST 18: CLI inside interrupt simulation (should disable further interrupts)
; ============================================================
test18_start:
    sei                 ; I=1
    cli                 ; Disable interrupts
    
    ; Simulate ISR: interrupts should remain disabled
    in r16, SREG_ADDR
    sbrs r16, 7
    rjmp isr_masked18
    rjmp fail
isr_masked18:
    rcall inc_case
    rjmp test19_start

; ============================================================
; TEST 19: CLI before SLEEP (wake-up behavior simulation)
; ============================================================
test19_start:
    sei                 ; I=1
    cli                 ; Disable before sleep
    
    ; I should be 0, so wake-up from sleep would not occur
    in r16, SREG_ADDR
    sbrs r16, 7
    rjmp sleep_ok19
    rjmp fail
sleep_ok19:
    rcall inc_case
    rjmp test20_start

; ============================================================
; TEST 20: CLI preserves sign flag (S = N ^ V) integrity
; ============================================================
test20_start:
    ; Create scenario where S=1 (N=1, V=0)
    cli
    ldi r16, 0xF0       ; -16 in signed
    tst r16             ; N=1, V=0, S=1
    
    cli                 ; Should preserve S
    
    brlt s_ok20         ; Branch if S=1
    rjmp fail
s_ok20:
    
    ; Create scenario where S=0 (N=0, V=0)
    ldi r16, 0x10       ; 16
    tst r16             ; N=0, V=0, S=0
    cli                 ; Should preserve S
    brge s_zero_ok20    ; Branch if S=0
    rjmp fail
s_zero_ok20:
    
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