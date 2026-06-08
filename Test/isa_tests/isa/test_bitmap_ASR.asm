; ============================================================
; ASR (Arithmetic Shift Right) instruction test suite
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D

reset:
    ldi r16, 0x03
    out SPH, r16
    ldi r16, 0xFF
    out SPL, r16

    ldi r16, 1
    sts test_case, r16
    ldi r16, 1
    sts final_result, r16

; ============================================================
; TEST 1: Positive number shift
; 0x20 (00100000) -> 0x10 (00010000)
; ============================================================
test1:
    ldi r16, 0x20
    asr r16

    cpi r16, 0x10
    brne fail
    rcall inc_case

; ============================================================
; TEST 2: Sign-bit preservation
; 0x80 (10000000) -> 0xC0 (11000000)
; ============================================================
test2:
    ldi r16, 0x80
    asr r16

    cpi r16, 0xC0
    brne fail
    rcall inc_case

; ============================================================
; TEST 3: Carry flag verification
; 0x01 (00000001) -> 0x00, Carry flag should be set
; ============================================================
test3:
    ldi r16, 0x01
    asr r16
    
    ; Verify register
    cpi r16, 0
    brne fail
    
    ; Check Carry (C) flag
    ; ASR shifts bit 0 into the Carry flag
    brcc fail           ; Branch if Carry NOT set
    rcall inc_case

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