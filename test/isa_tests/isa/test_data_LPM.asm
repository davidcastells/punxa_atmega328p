; ============================================================
; LPM instruction test suite for ATmega328P
; test_case      -> SRAM location tracking current test
; final_result   -> 1 = OK, -1 = FAIL
;
; LPM Rd, Z   : Load byte from Flash at address Z into Rd
; Updates: None.
; ============================================================
; -------------------------
; SRAM variables
; -------------------------
.equ test_case    = 0x0100
.equ final_result = 0x0101

; -------------------------
; Flash Data
; -------------------------
.org 0x0100                   ; Data stored in Program Memory
test_data:
.db 0xAA, 0x55, 0xFF, 0x00

; -------------------------
; Reset
; -------------------------
reset:
    ldi r16, 0
    sts test_case, r16
    ldi r16, 1
    sts final_result, r16

; ============================================================
; TEST 1: Load first byte from Flash
; ============================================================
test1:
    ldi r30, low(test_data * 2) ; Byte address = word address * 2
    ldi r31, high(test_data * 2)
    lpm r16, Z
    
    cpi r16, 0xAA
    brne fail
    rcall inc_case

; ============================================================
; TEST 2: Load second byte from Flash
; ============================================================
test2:
    ldi r30, low(test_data * 2 + 1)
    ldi r31, high(test_data * 2 + 1)
    lpm r16, Z
    
    cpi r16, 0x55
    brne fail
    rcall inc_case

; ============================================================
; TEST 3: Load third byte (0xFF)
; ============================================================
test3:
    ldi r30, low(test_data * 2 + 2)
    ldi r31, high(test_data * 2 + 2)
    lpm r16, Z
    
    cpi r16, 0xFF
    brne fail
    rcall inc_case

; ============================================================
; TEST 4: Verify Flags are not affected
; Set Zero flag, execute LPM, check if Z flag is still set.
; ============================================================
test4:
    ldi r16, 0
    tst r16               ; Set Z flag
    
    ldi r30, low(test_data * 2)
    ldi r31, high(test_data * 2)
    lpm r16, Z            ; LPM should not change Z
    
    brne fail             ; If Z was cleared, this fails
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