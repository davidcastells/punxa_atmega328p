; ============================================================
; Expanded SBRC Test Suite
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ trap_flag = 0x0102

reset:
    ; ... (init stack and variables as before)
    ldi r16, 1
    sts test_case, r16
    sts final_result, r16
    ldi r16, 0
    sts trap_flag, r16

; ============================================================
; TEST 1: Skip 1-word instruction (Bit 0 is 0)
; ============================================================
test1:
    ldi r16, 0xFE           ; bit 0 is 0
    sbrc r16, 0
    sts trap_flag, r16      ; Should be skipped
    
    lds r17, trap_flag
    cpi r17, 0xFE           ; If trap_flag changed, skip failed
    breq fail
    rcall inc_case

; ============================================================
; TEST 2: Skip 2-word instruction (JMP)
; ============================================================
test2:
    ldi r16, 0x00
    sbrc r16, 0
    jmp fail                ; Should be skipped
    
    rcall inc_case

; ============================================================
; TEST 3: NO Skip (Bit is 1)
; ============================================================
test3:
    ldi r16, 0x01           ; bit 0 is 1
    sbrc r16, 0
    rjmp test3_pass         ; Should NOT be skipped
    
    rjmp fail               ; Incorrectly skipped

test3_pass:
    rcall inc_case

; ============================================================
; TEST 4: Skip Bit 7 (MSB)
; ============================================================
test4:
    ldi r16, 0x7F           ; bit 7 is 0
    sbrc r16, 7
    rjmp fail               ; Should be skipped
    
    rcall inc_case

; ============================================================
; Standard Success/Fail
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