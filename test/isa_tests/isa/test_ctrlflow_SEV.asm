; ============================================================
; SEV instruction test suite for ATmega328P
; test_case      -> SRAM location tracking current test
; final_result   -> 1 = OK, -1 = FAIL
;
; SEV  : Set Overflow Flag (V) in Status Register
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
; TEST 1: Basic Set
; Ensure SEV sets bit 3 in SREG.
; ============================================================
test1:
    out SREG, r0          ; Ensure all flags are 0
    sev                   ; Set Overflow Flag
    in r16, SREG
    sbrs r16, 3           ; Bit 3 is V-flag
    rjmp fail
    rcall inc_case

; ============================================================
; TEST 2: Verify SEV does not affect other flags
; Set Carry (C=bit 0) then call SEV
; ============================================================
test2:
    out SREG, r0
    sec                   ; Set C (bit 0)
    sev                   ; Set V (bit 3)
    in r16, SREG
    sbrs r16, 0           ; Ensure C is still set
    rjmp fail
    sbrs r16, 3           ; Ensure V is set
    rjmp fail
    rcall inc_case

; ============================================================
; TEST 3: Branching after SEV
; Use BRVS to verify the flag was correctly set.
; ============================================================
test3:
    out SREG, r0
    sev
    brvs branch3          ; Should branch
    rjmp fail
branch3:
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