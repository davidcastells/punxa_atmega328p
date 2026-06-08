; ============================================================
; SUB instruction test suite for ATmega328P
; SUB Rd, Rr  ->  Rd = Rd - Rr
; Affected flags: H, S, V, N, Z, C
;
; Flag definitions for SUB:
;   C = set if unsigned borrow (Rd < Rr)
;   Z = set if result == 0
;   N = set if result bit 7 == 1
;   V = set if signed overflow
;       (pos - neg = neg) or (neg - pos = pos)
;   S = N XOR V  (signed comparison flag)
;   H = set if borrow from bit 3
;       (i.e. low nibble of Rd < low nibble of Rr)
;
; test_case      -> SRAM location tracking current test
; final_result   -> 1 = OK, -1 = FAIL
; ============================================================
; -------------------------
; SRAM variables
; -------------------------
.equ test_case    = 0x0100
.equ final_result = 0x0101
.equ SREG         = 0x3F
.equ SPH          = 0x3E
.equ SPL          = 0x3D
; -------------------------
; Reset
; -------------------------
reset:
    ; init stack
    ldi r16, 0x03
    out SPH, r16
    ldi r16, 0xFF
    out SPL, r16
    ; init state
    ldi r16, 0
    sts test_case, r16
    ldi r16, 1
    sts final_result, r16

; ============================================================
; TEST 1: simple subtraction, positive result
; 30 - 10 = 20
; C=0, Z=0, N=0, V=0, S=0, H=0
; ============================================================
test1:
    ldi r16, 30
    ldi r17, 10
    sub r16, r17
    ; -- result --
    cpi r16, 20
    brne fail1
    ; -- C=0 --
    brcs fail1
    ; -- Z=0 --
    breq fail1
    ; -- N=0 --
    brmi fail1
    ; -- V=0 --
    brvs fail1
    ; -- S=0: read SREG bit 4 --
    in r18, SREG
    sbrc r18, 4
    rjmp fail1
    ; -- H=0: read SREG bit 5 --
    in r18, SREG
    sbrc r18, 5
    rjmp fail1
    rcall inc_case
    rjmp test2
fail1: 
    jmp fail

; ============================================================
; TEST 2: result is zero
; 42 - 42 = 0
; C=0, Z=1, N=0, V=0, S=0, H=0
; ============================================================
test2:
    ldi r16, 42
    ldi r17, 42
    sub r16, r17
    ; -- result --
    cpi r16, 0
    brne fail2
    ; -- C=0 --
    brcs fail2
    ; -- Z=1 --
    brne fail2
    ; -- N=0 --
    brmi fail2
    ; -- V=0 --
    brvs fail2
    ; -- S=0 --
    in r18, SREG
    sbrc r18, 4
    rjmp fail2
    ; -- H=0 --
    in r18, SREG
    sbrc r18, 5
    rjmp fail2
    rcall inc_case
    rjmp test3
fail2: 
    jmp fail

; ============================================================
; TEST 3: unsigned borrow, carry set
; 10 - 20 = 246 (mod 256)
; C=1, Z=0, N=1, V=0, S=1, H=0
; ============================================================
test3:
    ldi r16, 10
    ldi r17, 20
    sub r16, r17
    ; -- result --
    cpi r16, 246
    brne fail3
    ; -- C=1 --
    brcc fail3
    ; -- Z=0 --
    breq fail3
    ; -- N=1 --
    brpl fail3
    ; -- V=0 --
    brvs fail3
    ; -- S=1 (N=1, V=0 -> S=1) --
    in r18, SREG
    sbrs r18, 4
    rjmp fail3
    ; -- H=0 --
    in r18, SREG
    sbrc r18, 5
    rjmp fail3
    rcall inc_case
    rjmp test4
fail3: 
    jmp fail

; ============================================================
; TEST 4: half-carry (borrow from bit 3)
; 0x10 - 0x01 = 0x0F
; low nibbles: 0x0 - 0x1 borrows from bit3 -> H=1
; C=0, Z=0, N=0, V=0, S=0, H=1
; ============================================================
test4:
    ldi r16, 0x10
    ldi r17, 0x01
    sub r16, r17
    ; -- result --
    cpi r16, 0x0F
    brne fail4
    ; -- C=0 --
    brcs fail4
    ; -- Z=0 --
    breq fail4
    ; -- N=0 --
    brmi fail4
    ; -- V=0 --
    brvs fail4
    ; -- S=0 --
    in r18, SREG
    sbrc r18, 4
    rjmp fail4
    ; -- H=1 --
    in r18, SREG
    sbrs r18, 5
    rjmp fail4
    rcall inc_case
    rjmp test5
fail4:
    jmp fail

; ============================================================
; TEST 5: signed overflow, positive - negative = negative
; 0x70 (112) - 0x90 (144 unsigned / -112 signed) = 0xE0
; C=1, Z=0, N=1, V=1, S=0 (N^V=1^1), H=0
; ============================================================
test5:
    ldi r16, 0x70
    ldi r17, 0x90
    sub r16, r17
    ; -- result --
    cpi r16, 0xE0
    brne fail5
    ; -- C=1 --
    brcc fail5
    ; -- Z=0 --
    breq fail5
    ; -- N=1 --
    brpl fail5
    ; -- V=1 --
    brvc fail5
    ; -- S=0 (N=1, V=1 -> S=0) --
    in r18, SREG
    sbrc r18, 4
    rjmp fail5
    ; -- H=0 --
    in r18, SREG
    sbrc r18, 5
    rjmp fail5
    rcall inc_case
    rjmp test6
fail5:
    jmp fail

; ============================================================
; TEST 6: signed overflow, negative - positive = positive
; 0x80 (-128) - 0x01 (1) = 0x7F (127)
; True signed result = -129, overflows -> V=1
; C=0, Z=0, N=0, V=1, S=1 (N^V=0^1), H=0
; ============================================================
test6:
    ldi r16, 0x80
    ldi r17, 0x01
    sub r16, r17
    ; -- result --
    cpi r16, 0x7F
    brne fail6
    ; -- C=0 --
    brcs fail6
    ; -- Z=0 --
    breq fail6
    ; -- N=0 --
    brmi fail6
    ; -- V=1 --
    brvc fail6
    ; -- S=1 (N=0, V=1 -> S=1) --
    in r18, SREG
    sbrs r18, 4
    rjmp fail6
    ; -- H=0 --
    in r18, SREG
    sbrc r18, 5
    rjmp fail6
    rcall inc_case
    rjmp test7
fail6: 
    jmp fail

; ============================================================
; TEST 7: subtract from self (all ones scenario)
; 0xFF - 0xFF = 0
; C=0, Z=1, N=0, V=0, S=0, H=0
; ============================================================
test7:
    ldi r16, 0xFF
    ldi r17, 0xFF
    sub r16, r17
    ; -- result --
    cpi r16, 0
    brne fail7
    ; -- C=0 --
    brcs fail7
    ; -- Z=1 --
    brne fail7
    ; -- N=0 --
    brmi fail7
    ; -- V=0 --
    brvs fail7
    ; -- S=0 --
    in r18, SREG
    sbrc r18, 4
    rjmp fail7
    ; -- H=0 --
    in r18, SREG
    sbrc r18, 5
    rjmp fail7
    rcall inc_case
    rjmp test8
fail7: 
    jmp fail

; ============================================================
; TEST 8: half-carry with borrow chain
; 0x20 - 0x19 = 0x07
; low nibbles: 0x0 - 0x9 -> borrows from bit3 -> H=1
; C=0, Z=0, N=0, V=0, S=0, H=1
; ============================================================
test8:
    ldi r16, 0x20
    ldi r17, 0x19
    sub r16, r17
    ; -- result --
    cpi r16, 0x07
    brne fail8
    ; -- C=0 --
    brcs fail8
    ; -- Z=0 --
    breq fail8
    ; -- N=0 --
    brmi fail8
    ; -- V=0 --
    brvs fail8
    ; -- S=0 --
    in r18, SREG
    sbrc r18, 4
    rjmp fail8
    ; -- H=1 --
    in r18, SREG
    sbrs r18, 5
    rjmp fail8
    rcall inc_case
    rjmp success
fail8: 
    jmp fail

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
; final_result = -1, stop execution
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
