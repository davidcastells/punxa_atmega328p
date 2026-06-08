; ============================================================
; ADIW instruction test suite for ATmega328P
; ADIW adds a 6-bit immediate (0..63) to a register pair:
;   Rd+1:Rd  where Rd in {r24, r26, r28, r30}
; test_case      -> SRAM location tracking current test
; final_result   -> 1 = OK, -1 = FAIL
; ============================================================
; -------------------------
; SRAM variables
; -------------------------
.equ test_case    = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D
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
; TEST 1: simple addition, no carry expected
; r25:r24 = 0x0010 + 1 = 0x0011, C=0
; ============================================================
test1:
    ldi r24, 0x10
    ldi r25, 0x00
    adiw r24, 1
    brcs fail                 ; C must be 0
    cpi r24, 0x11
    brne fail
    cpi r25, 0x00
    brne fail
    rcall inc_case
; ============================================================
; TEST 2: carry propagation low->high byte, no carry out
; r25:r24 = 0x00FF + 1 = 0x0100, C=0
; ============================================================
test2:
    ldi r24, 0xFF
    ldi r25, 0x00
    adiw r24, 1
    brcs fail                 ; carry out of 16-bit result? No
    cpi r24, 0x00
    brne fail
    cpi r25, 0x01
    brne fail
    rcall inc_case
; ============================================================
; TEST 3: zero identity
; r25:r24 = 0x1234 + 0 = 0x1234, C=0
; ============================================================
test3:
    ldi r24, 0x34
    ldi r25, 0x12
    adiw r24, 0
    brcs fail                 ; C must be 0
    cpi r24, 0x34
    brne fail
    cpi r25, 0x12
    brne fail
    rcall inc_case
; ============================================================
; TEST 4: maximum immediate (63), no carry out
; r25:r24 = 0x0001 + 63 = 0x0040, C=0
; ============================================================
test4:
    ldi r24, 0x01
    ldi r25, 0x00
    adiw r24, 63
    brcs fail                 ; C must be 0
    cpi r24, 0x40
    brne fail
    cpi r25, 0x00
    brne fail
    rcall inc_case
; ============================================================
; TEST 5: 16-bit wrap-around, carry SET
; r25:r24 = 0xFFFF + 1 = 0x0000, C=1
; ============================================================
test5:
    ldi r24, 0xFF
    ldi r25, 0xFF
    adiw r24, 1
    brcc fail                 ; C must be 1
    cpi r24, 0x00
    brne fail
    cpi r25, 0x00
    brne fail
    rcall inc_case
; ============================================================
; TEST 6: near overflow, carry SET
; r25:r24 = 0xFFFE + 63 = 0x003D, C=1
; ============================================================
test6:
    ldi r24, 0xFE
    ldi r25, 0xFF
    adiw r24, 63
    brcc fail                 ; C must be 1
    cpi r24, 0x3D
    brne fail
    cpi r25, 0x00
    brne fail
    rcall inc_case
; ============================================================
; TEST 7: X register pair (r27:r26), no carry
; r27:r26 = 0x0064 + 10 = 0x006E, C=0
; ============================================================
test7:
    ldi r26, 0x64
    ldi r27, 0x00
    adiw r26, 10
    brcs fail                 ; C must be 0
    cpi r26, 0x6E
    brne fail
    cpi r27, 0x00
    brne fail
    rcall inc_case
; ============================================================
; TEST 8: Y register pair (r29:r28), carry propagation, no carry out
; r29:r28 = 0x00F0 + 16 = 0x0100, C=0
; ============================================================
test8:
    ldi r28, 0xF0
    ldi r29, 0x00
    adiw r28, 16
    brcs fail                 ; C must be 0
    cpi r28, 0x00
    brne fail
    cpi r29, 0x01
    brne fail
    rcall inc_case
; ============================================================
; TEST 9: Z register pair (r31:r30), carry SET
; r31:r30 = 0xFFFF + 1 = 0x0000, C=1
; ============================================================
test9:
    ldi r30, 0xFF
    ldi r31, 0xFF
    adiw r30, 1
    brcc fail                 ; C must be 1
    cpi r30, 0x00
    brne fail
    cpi r31, 0x00
    brne fail
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