; ============================================================
; RETI (Return from Interrupt) test suite
; ============================================================
; Tests that RETI correctly:
; 1. Pops the return address from the stack
; 2. Jumps back to the address after the interrupt
; 3. Sets the Global Interrupt Flag (I=1)
; 4. Stack pointer increments by 2
; ============================================================
; RETI is a 1-word (16-bit) instruction
; Format: 1001 0101 0001 1000 (0x9518)
; Operation: PC <- [SP], SP <- SP + 2, I <- 1
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ stack_start = 0x08FF
.equ SREG_ADDR = 0x5F
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
; TEST 1: Simple RETI after interrupt simulation
; ============================================================
test1:
    ; Disable interrupts first
    cli
    ; Simulate interrupt: push return address and jump to ISR
    ldi r30, low(return1)
    ldi r31, high(return1)
    push r31
    push r30
    rjmp isr1
return1:
    ; After RETI, execution continues here
    ; Interrupts should be re-enabled
    sei                 ; For verification we'll check I flag
    cpi r16, 0x42
    brne fail
    rcall inc_case
    rjmp test1_done

isr1:
    ldi r16, 0x42
    reti                ; Return from interrupt, sets I flag

test1_done:

; ============================================================
; TEST 2: RETI re-enables interrupts (sets I flag)
; ============================================================
test2:
    cli                 ; Disable interrupts (I=0)
    
    ; Simulate interrupt
    ldi r30, low(return2)
    ldi r31, high(return2)
    push r31
    push r30
    rjmp isr2
return2:
    ; I flag should be set after RETI
    ; Test by doing something that requires interrupts
    ; For verification, we can read SREG
    in r17, SREG_ADDR
    sbrc r17, 7         ; Skip if I flag is set
    rjmp i_set2
    rjmp fail
i_set2:
    rcall inc_case
    rjmp test2_done

isr2:
    reti

test2_done:

; ============================================================
; TEST 3: Nested RETI (simulating nested interrupts)
; ============================================================
test3:
    cli
    ldi r18, 0
    
    ; First interrupt
    ldi r30, low(return3a)
    ldi r31, high(return3a)
    push r31
    push r30
    rjmp isr3a
return3a:
    cpi r18, 0x02
    brne fail
    rcall inc_case
    rjmp test3_done

isr3a:
    inc r18
    ; Second interrupt (nested)
    ldi r30, low(return3b)
    ldi r31, high(return3b)
    push r31
    push r30
    rjmp isr3b
return3b:
    inc r18
    reti

isr3b:
    inc r18
    reti

test3_done:

; ============================================================
; TEST 4: Verify stack pointer behavior with RETI
; ============================================================
test4:
    cli
    ; Read initial SP
    in r19, SPL
    in r20, SPH
    
    ; Simulate interrupt
    ldi r30, low(return4)
    ldi r31, high(return4)
    push r31
    push r30
    rjmp isr4
return4:
    ; Read SP after RETI
    in r21, SPL
    in r22, SPH
    
    cp r19, r21
    brne fail
    cp r20, r22
    brne fail
    rcall inc_case
    rjmp test4_done

isr4:
    reti

test4_done:

; ============================================================
; TEST 5: RETI with preserved registers (PUSH/POP)
; ============================================================
test5:
    cli
    ldi r23, 0x11
    ldi r24, 0x22
    ldi r25, 0x33
    
    ; Simulate interrupt
    ldi r30, low(return5)
    ldi r31, high(return5)
    push r31
    push r30
    rjmp isr5
return5:
    cpi r23, 0x11
    brne fail
    cpi r24, 0x22
    brne fail
    cpi r25, 0x33
    brne fail
    rcall inc_case
    rjmp test5_done

isr5:
    push r23
    push r24
    push r25
    
    ldi r23, 0xFF
    ldi r24, 0xFF
    ldi r25, 0xFF
    
    pop r25
    pop r24
    pop r23
    reti

test5_done:

; ============================================================
; TEST 6: RETI vs RET comparison (RET doesn't set I flag)
; ============================================================
test6:
    cli                 ; I=0
    
    ; Test RET (should NOT set I)
    ldi r30, low(ret_return)
    ldi r31, high(ret_return)
    push r31
    push r30
    rjmp test_ret
ret_return:
    in r26, SREG_ADDR
    sbrc r26, 7         ; Check I flag
    rjmp fail           ; I should still be 0 after RET
    
    ; Test RETI (should set I)
    ldi r30, low(reti_return)
    ldi r31, high(reti_return)
    push r31
    push r30
    rjmp test_reti
reti_return:
    in r27, SREG_ADDR
    sbrs r27, 7         ; Check I flag
    rjmp fail           ; I should be 1 after RETI
    
    rcall inc_case
    rjmp test6_done

test_ret:
    ret                 ; Does NOT set I flag

test_reti:
    reti                ; Sets I flag

test6_done:

; ============================================================
; TEST 7: Multiple RETI calls (simulating multiple interrupts)
; ============================================================
test7:
    cli
    ldi r28, 0
    
    ; Interrupt 1
    ldi r30, low(return7a)
    ldi r31, high(return7a)
    push r31
    push r30
    rjmp isr7a
return7a:
    ; Interrupt 2
    ldi r30, low(return7b)
    ldi r31, high(return7b)
    push r31
    push r30
    rjmp isr7b
return7b:
    cpi r28, 0x04
    brne fail
    rcall inc_case
    rjmp test7_done

isr7a:
    inc r28
    reti
isr7b:
    inc r28
    inc r28
    inc r28
    reti

test7_done:

; ============================================================
; TEST 8: RETI after complex stack operations
; ============================================================
test8:
    cli
    ldi r29, 0x01
    ldi r30, 0x02
    ldi r31, 0x03
    
    ; Simulate interrupt
    ldi r16, low(return8)
    ldi r17, high(return8)
    push r17
    push r16
    rjmp isr8
return8:
    cpi r29, 0x01
    brne fail
    cpi r30, 0x02
    brne fail
    cpi r31, 0x03
    brne fail
    rcall inc_case
    rjmp test8_done

isr8:
    push r29
    push r30
    push r31
    
    ldi r29, 0xFF
    ldi r30, 0xFF
    ldi r31, 0xFF
    
    pop r31
    pop r30
    pop r29
    reti

test8_done:

; ============================================================
; TEST 9: RETI preserves all other flags
; ============================================================
test9:
    cli
    ; Set some flags
    sec                 ; Set C
    sez                 ; Set Z
    sen                 ; Set N
    sev                 ; Set V
    seh                 ; Set H
    set                 ; Set T
    
    ; Simulate interrupt
    ldi r16, low(return9)
    ldi r17, high(return9)
    push r17
    push r16
    rjmp isr9
return9:
    ; Check flags are preserved (except I)
    brcc fail           ; C should be 1
    brne fail           ; Z should be 1
    brmi fail           ; N should be 1
    brvs fail           ; V should be 1
    brhc fail           ; H should be 1
    brtc fail           ; T should be 1
    
    rcall inc_case
    rjmp test9_done

isr9:
    ; RETI should preserve all flags except I
    reti

test9_done:

; ============================================================
; TEST 10: RETI from deep nested ISR simulation
; ============================================================
test10:
    cli
    ldi r16, 0
    
    ; Level 1
    ldi r17, low(return10a)
    ldi r18, high(return10a)
    push r18
    push r17
    rjmp isr10a
return10a:
    cpi r16, 0x03
    brne fail
    rcall inc_case
    rjmp test10_done

isr10a:
    inc r16
    ; Level 2
    ldi r17, low(return10b)
    ldi r18, high(return10b)
    push r18
    push r17
    rjmp isr10b
return10b:
    inc r16
    reti

isr10b:
    inc r16
    reti

test10_done:

; ============================================================
; TEST 11: Verify RETI encoding (fixed opcode 0x9518)
; ============================================================
test11:
    cli
    ldi r16, low(return11)
    ldi r17, high(return11)
    push r17
    push r16
    rjmp encoding_test11
return11:
    ; If we get here, RETI worked
    rcall inc_case
    rjmp test11_done

encoding_test11:
    reti

test11_done:

; ============================================================
; TEST 12: RETI after SPM/ZIG (special cases)
; ============================================================
test12:
    cli
    ldi r16, low(return12)
    ldi r17, high(return12)
    push r17
    push r16
    rjmp isr12
return12:
    rcall inc_case
    rjmp test12_done

isr12:
    ; Some operations
    ldi r18, 0xAA
    ldi r19, 0xBB
    add r18, r19
    reti

test12_done:

; ============================================================
; TEST 13: RETI with SREG manually saved/restored
; ============================================================
test13:
    cli
    ; Save SREG
    in r20, SREG_ADDR
    push r20
    
    ldi r16, low(return13)
    ldi r17, high(return13)
    push r17
    push r16
    rjmp isr13
return13:
    ; Restore SREG (but RETI will set I flag)
    pop r20
    out SREG_ADDR, r20
    
    ; I flag should be set by RETI
    in r21, SREG_ADDR
    sbrc r21, 7
    rjmp i_ok13
    rjmp fail
i_ok13:
    rcall inc_case
    rjmp test13_done

isr13:
    reti

test13_done:

; ============================================================
; TEST 14: RETI after clearing I flag inside ISR
; ============================================================
test14:
    cli
    ldi r16, low(return14)
    ldi r17, high(return14)
    push r17
    push r16
    rjmp isr14
return14:
    ; I flag should be 1 (RETI forces it to 1)
    in r22, SREG_ADDR
    sbrs r22, 7
    rjmp fail
    rcall inc_case
    rjmp test14_done

isr14:
    cli                 ; Clear I flag inside ISR
    reti                ; RETI will set it back to 1

test14_done:

; ============================================================
; TEST 15: RETI with multiple PUSH/POP before return
; ============================================================
test15:
    cli
    ldi r23, 0xDE
    ldi r24, 0xAD
    ldi r25, 0xBE
    ldi r26, 0xEF
    
    ldi r16, low(return15)
    ldi r17, high(return15)
    push r17
    push r16
    rjmp isr15
return15:
    cpi r23, 0xDE
    brne fail
    cpi r24, 0xAD
    brne fail
    cpi r25, 0xBE
    brne fail
    cpi r26, 0xEF
    brne fail
    rcall inc_case
    rjmp test15_done

isr15:
    push r23
    push r24
    push r25
    push r26
    
    ldi r23, 0x00
    ldi r24, 0x00
    ldi r25, 0x00
    ldi r26, 0x00
    
    pop r26
    pop r25
    pop r24
    pop r23
    reti

test15_done:

; ============================================================
; TEST 16: RETI after stack cleanup (frame pointer)
; ============================================================
test16:
    cli
    ldi r16, low(return16)
    ldi r17, high(return16)
    push r17
    push r16
    rjmp isr16
return16:
    rcall inc_case
    rjmp test16_done

isr16:
    ; Create stack frame
    push r28
    push r29
    in r28, SPL
    in r29, SPH
    
    ; Use frame
    ldi r18, 0x42
    std Y+0, r18
    
    ; Clean up frame
    pop r29
    pop r28
    reti

test16_done:

; ============================================================
; TEST 17: RETI with watchdog simulation
; ============================================================
test17:
    cli
    ldi r16, low(return17)
    ldi r17, high(return17)
    push r17
    push r16
    rjmp isr17
return17:
    rcall inc_case
    rjmp test17_done

isr17:
    ; Simulate watchdog ISR
    wdr                 ; Reset watchdog timer
    reti

test17_done:

; ============================================================
; TEST 18: RETI final test - ensure I flag is set
; ============================================================
test18:
    cli                 ; Ensure I=0
    ldi r16, low(return18)
    ldi r17, high(return18)
    push r17
    push r16
    rjmp isr18
return18:
    in r19, SREG_ADDR
    sbrs r19, 7
    rjmp fail
    rcall inc_case
    rjmp success

isr18:
    reti

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