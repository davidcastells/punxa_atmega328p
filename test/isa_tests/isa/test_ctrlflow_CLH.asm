; ============================================================
; CLH (Clear Half Carry Flag) instruction test suite for ATmega328P
; test_case      -> SRAM location tracking current test
; final_result   -> 1 = OK, -1 = FAIL
;
; Instruction used: BCLR 5 (Clears H-Flag)
; H-Flag is bit 5 of the Status Register (SREG).
; ============================================================
; -------------------------
; SRAM variables
; -------------------------
.equ test_case    = 0x0100
.equ final_result = 0x0101
.equ SREG         = 0x3F      ; SREG I/O address
; -------------------------
; Reset
; -------------------------
reset:
    ldi r16, 0
    sts test_case, r16
    ldi r16, 1
    sts final_result, r16

; ============================================================
; TEST 1: Clear H-Flag when already cleared (H=0)
; ============================================================
test1:
    out SREG, r0          ; Ensure all flags are 0
    bclr 5                ; Clear H-Flag
    in r16, SREG
    sbrc r16, 5           ; Fail if bit 5 is set
    rjmp fail
    rcall inc_case

; ============================================================
; TEST 2: Clear H-Flag after setting it
; ============================================================
test2:
    bset 5                ; Set H-Flag
    bclr 5                ; Clear H-Flag
    in r16, SREG
    sbrc r16, 5           ; Fail if bit 5 is set
    rjmp fail
    rcall inc_case

; ============================================================
; TEST 3: Verify BCLR 5 does not affect other bits
; Set Carry (C=bit 0) and H-Flag, clear H, check C.
; ============================================================
test3:
    out SREG, r0
    bset 0                ; Set Carry
    bset 5                ; Set H-Flag
    bclr 5                ; Clear H-Flag
    
    in r16, SREG
    sbrc r16, 5           ; Fail if H-flag is still set
    rjmp fail
    sbrs r16, 0           ; Fail if Carry is NOT set
    rjmp fail
    rcall inc_case

; ============================================================
; SUCCESS
; ============================================================
success:
    ldi r16, 1
    sts final_result, r16
end:
    rjmp end

; ============================================================
; FAILURE
; ============================================================
fail:
    ldi r16, -1
    sts final_result, r16
    rjmp end

; ============================================================
; increment test_case
; ============================================================
inc_case:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret