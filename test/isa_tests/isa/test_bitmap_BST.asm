; ============================================================
; BST (Bit Store) instruction test suite
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
; TEST 1: Store Bit 0 into T flag
; R16 = 0x01 (00000001), store bit 0 -> T = 1
; ============================================================
test1:
    ldi r16, 0x01
    bst r16, 0          ; Move bit 0 to T flag
    
    ; Verification: We use BLD to bring it back to a register
    ; so we can check if it worked.
    ldi r17, 0x00
    bld r17, 0          ; Load T into bit 0 of R17
    
    cpi r17, 1
    brne fail
    rcall inc_case

; ============================================================
; TEST 2: Store Bit 7 into T flag
; R16 = 0x80 (10000000), store bit 7 -> T = 1
; ============================================================
test2:
    ldi r16, 0x80
    bst r16, 7          ; Move bit 7 to T flag
    
    ldi r17, 0x00
    bld r17, 0          ; Move T back to bit 0 of R17
    
    cpi r17, 1
    brne fail
    rcall inc_case

; ============================================================
; TEST 3: Store a 0 bit into T flag
; R16 = 0xFE (11111110), store bit 0 -> T = 0
; ============================================================
test3:
    ldi r16, 0xFE
    bst r16, 0          ; Bit 0 is 0, so T becomes 0
    
    set                 ; Set T to 1 manually
    bld r17, 0          ; (Just to clear R17)
    
    bld r17, 0          ; Load T (0) into bit 0 of R17
    
    cpi r17, 0
    brne fail
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