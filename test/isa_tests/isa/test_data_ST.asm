; ============================================================
; ST (Store Indirect to Data Space) test suite
; ============================================================
; Tests that ST correctly:
; 1. Stores data to SRAM address pointed to by X/Y/Z
; 2. Can store with/without displacement (STD)
; 3. Can post-increment or pre-decrement pointer
; 4. Does not modify the source register or flags
; ============================================================
; ST is a 1-word (16-bit) instruction
; Formats:
;   ST X, Rr         (1001 001r rrrr 1100)
;   ST X+, Rr        (1001 001r rrrr 1101)
;   ST -X, Rr        (1001 001r rrrr 1110)
;   ST Y, Rr         (1000 001r rrrr 1000)
;   ST Y+, Rr        (1001 001r rrrr 1001)
;   ST -Y, Rr        (1001 001r rrrr 1010)
;   STD Y+q, Rr      (10q0 qq1r rrrr 1qqq)
;   ST Z, Rr         (1000 001r rrrr 0000)
;   ST Z+, Rr        (1001 001r rrrr 0001)
;   ST -Z, Rr        (1001 001r rrrr 0010)
;   STD Z+q, Rr      (10q0 qq1r rrrr 0qqq)
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D
.equ DATA_START = 0x0200

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
; TEST 1: ST X, Rr (store through X pointer)
; ============================================================
test1_start:
    ; Load X pointer to test location
    ldi r26, low(DATA_START)
    ldi r27, high(DATA_START)
    
    ; Store value
    ldi r16, 0x42
    st X, r16
    
    ; Verify by loading back
    ld r17, X
    cpi r17, 0x42
    brne fail
    rcall inc_case
    rjmp test2_start

; ============================================================
; TEST 2: ST X+, Rr (store and post-increment)
; ============================================================
test2_start:
    ; Load X pointer
    ldi r26, low(DATA_START)
    ldi r27, high(DATA_START)
    
    ; Store with post-increment
    ldi r16, 0xAA
    st X+, r16
    ; Store next value
    ldi r16, 0xBB
    st X+, r16
    
    ; Verify X pointer incremented
    cpi r26, low(DATA_START+2)
    brne fail
    cpi r27, high(DATA_START+2)
    brne fail
    
    ; Verify data
    ldi r26, low(DATA_START)
    ldi r27, high(DATA_START)
    ld r17, X+
    cpi r17, 0xAA
    brne fail
    ld r17, X+
    cpi r17, 0xBB
    brne fail
    
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: ST -X, Rr (pre-decrement and store)
; ============================================================
test3_start:
    ; Load X pointer to DATA_START+2
    ldi r26, low(DATA_START+2)
    ldi r27, high(DATA_START+2)
    
    ; Pre-decrement then store
    ldi r16, 0xCC
    st -X, r16
    
    ; Verify X pointer decremented
    cpi r26, low(DATA_START+1)
    brne fail
    cpi r27, high(DATA_START+1)
    brne fail
    
    ; Verify data at DATA_START+1
    ldi r26, low(DATA_START+1)
    ldi r27, high(DATA_START+1)
    ld r17, X
    cpi r17, 0xCC
    brne fail
    
    rcall inc_case
    rjmp test4_start

; ============================================================
; TEST 4: ST Y, Rr (store through Y pointer)
; ============================================================
test4_start:
    ; Load Y pointer
    ldi r28, low(DATA_START)
    ldi r29, high(DATA_START)
    
    ldi r16, 0x5A
    st Y, r16
    
    ; Verify
    ld r17, Y
    cpi r17, 0x5A
    brne fail
    rcall inc_case
    rjmp test5_start

; ============================================================
; TEST 5: ST Y+, Rr (store and post-increment with Y)
; ============================================================
test5_start:
    ldi r28, low(DATA_START)
    ldi r29, high(DATA_START)
    
    ldi r16, 0x11
    st Y+, r16
    ldi r16, 0x22
    st Y+, r16
    
    ; Verify Y pointer
    cpi r28, low(DATA_START+2)
    brne fail
    
    ; Verify data
    ldi r28, low(DATA_START)
    ldi r29, high(DATA_START)
    ld r17, Y+
    cpi r17, 0x11
    brne fail
    ld r17, Y+
    cpi r17, 0x22
    brne fail
    
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6: ST -Y, Rr (pre-decrement and store with Y)
; ============================================================
test6_start:
    ldi r28, low(DATA_START+2)
    ldi r29, high(DATA_START+2)
    
    ldi r16, 0xDD
    st -Y, r16
    
    cpi r28, low(DATA_START+1)
    brne fail
    
    ldi r28, low(DATA_START+1)
    ldi r29, high(DATA_START+1)
    ld r17, Y
    cpi r17, 0xDD
    brne fail
    
    rcall inc_case
    rjmp test7_start

; ============================================================
; TEST 7: ST Z, Rr (store through Z pointer)
; ============================================================
test7_start:
    ldi r30, low(DATA_START)
    ldi r31, high(DATA_START)
    
    ldi r16, 0x3C
    st Z, r16
    
    ld r17, Z
    cpi r17, 0x3C
    brne fail
    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8: ST Z+, Rr (store and post-increment with Z)
; ============================================================
test8_start:
    ldi r30, low(DATA_START)
    ldi r31, high(DATA_START)
    
    ldi r16, 0x77
    st Z+, r16
    ldi r16, 0x88
    st Z+, r16
    
    cpi r30, low(DATA_START+2)
    brne fail
    
    ldi r30, low(DATA_START)
    ldi r31, high(DATA_START)
    ld r17, Z+
    cpi r17, 0x77
    brne fail
    ld r17, Z+
    cpi r17, 0x88
    brne fail
    
    rcall inc_case
    rjmp test9_start

; ============================================================
; TEST 9: ST -Z, Rr (pre-decrement and store with Z)
; ============================================================
test9_start:
    ldi r30, low(DATA_START+2)
    ldi r31, high(DATA_START+2)
    
    ldi r16, 0xEE
    st -Z, r16
    
    cpi r30, low(DATA_START+1)
    brne fail
    
    ldi r30, low(DATA_START+1)
    ldi r31, high(DATA_START+1)
    ld r17, Z
    cpi r17, 0xEE
    brne fail
    
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10: STD Y+q, Rr (store with displacement Y)
; ============================================================
test10_start:
    ldi r28, low(DATA_START)
    ldi r29, high(DATA_START)
    
    ; Store with various displacements
    ldi r16, 0x01
    std Y+0, r16
    ldi r16, 0x02
    std Y+1, r16
    ldi r16, 0x03
    std Y+2, r16
    ldi r16, 0x04
    std Y+3, r16
    ldi r16, 0x05
    std Y+4, r16
    
    ; Verify
    ldd r17, Y+0
    cpi r17, 0x01
    brne fail
    ldd r17, Y+1
    cpi r17, 0x02
    brne fail
    ldd r17, Y+2
    cpi r17, 0x03
    brne fail
    ldd r17, Y+3
    cpi r17, 0x04
    brne fail
    ldd r17, Y+4
    cpi r17, 0x05
    brne fail
    
    rcall inc_case
    rjmp test11_start

; ============================================================
; TEST 11: STD Z+q, Rr (store with displacement Z)
; ============================================================
test11_start:
    ldi r30, low(DATA_START)
    ldi r31, high(DATA_START)
    
    ldi r16, 0x10
    std Z+0, r16
    ldi r16, 0x20
    std Z+1, r16
    
    ldd r17, Z+0
    cpi r17, 0x10
    brne fail
    ldd r17, Z+1
    cpi r17, 0x20
    brne fail
    
    rcall inc_case
    rjmp test12_start

; ============================================================
; TEST 12: ST from different registers (R0-R31)
; ============================================================
test12_start:
    ldi r26, low(DATA_START+16)
    ldi r27, high(DATA_START+16)
    
    ; Store from various registers
    ldi r0, 0xAB
    st X+, r0
    ldi r16, 0xCD
    st X+, r16
    ldi r31, 0xEF
    st X+, r31
    
    ; Verify
    ldi r26, low(DATA_START+16)
    ldi r27, high(DATA_START+16)
    ld r17, X+
    cpi r17, 0xAB
    brne fail
    ld r17, X+
    cpi r17, 0xCD
    brne fail
    ld r17, X+
    cpi r17, 0xEF
    brne fail
    
    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13: ST does not modify source register
; ============================================================
test13_start:
    ldi r26, low(DATA_START)
    ldi r27, high(DATA_START)
    
    ldi r16, 0x55
    st X, r16
    
    cpi r16, 0x55      ; Source unchanged
    brne fail
    
    rcall inc_case
    rjmp test14_start

; ============================================================
; TEST 14: ST does not modify flags
; ============================================================
test14_start:
    ldi r26, low(DATA_START)
    ldi r27, high(DATA_START)
    
    ; Set all flags
    sec                 ; C=1
    sez                 ; Z=1
    sen                 ; N=1
    sev                 ; V=1
    seh                 ; H=1
    set                 ; T=1
    
    ldi r16, 0xAA
    st X, r16
    
    ; Verify all flags still set
    brcc fail
    brne fail
    brmi fail
    brvs fail
    brhc fail
    brtc fail
    
    rcall inc_case
    rjmp test15_start

; ============================================================
; TEST 15: STD with maximum displacement (63)
; ============================================================
test15_start:
    ldi r28, low(DATA_START)
    ldi r29, high(DATA_START)
    
    ldi r16, 0x63
    std Y+63, r16
    
    ; Verify
    ldd r17, Y+63
    cpi r17, 0x63
    brne fail
    
    rcall inc_case
    rjmp test16_start

; ============================================================
; TEST 16: ST inside loop (array fill)
; ============================================================
test16_start:
    ldi r26, low(DATA_START+32)
    ldi r27, high(DATA_START+32)
    
    ldi r16, 0
    ldi r17, 10
fill_loop:
    st X+, r16
    inc r16
    dec r17
    brne fill_loop
    
    ; Verify first 10 values
    ldi r26, low(DATA_START+32)
    ldi r27, high(DATA_START+32)
    ldi r17, 0
    ldi r18, 10
verify_loop:
    ld r19, X+
    cp r17, r19
    brne fail
    inc r17
    dec r18
    brne verify_loop
    
    rcall inc_case
    rjmp test17_start

; ============================================================
; TEST 17: ST with pointer crossing page boundary
; ============================================================
test17_start:
    ldi r26, 0xFF
    ldi r27, 0x02
    ldi r16, 0xAA
    st X+, r16
    
    cpi r26, 0x00
    brne fail
    cpi r27, 0x03
    brne fail
    
    ; Verify data at 0x02FF (should be 0xAA)
    ldi r26, 0xFF
    ldi r27, 0x02
    ld r17, X
    cpi r17, 0xAA
    brne fail
    
    rcall inc_case
    rjmp test18_start

; ============================================================
; TEST 18: ST then LD from same address
; ============================================================
test18_start:
    ldi r26, low(DATA_START+50)
    ldi r27, high(DATA_START+50)
    
    ldi r16, 0xDE
    st X, r16
    
    ld r17, X
    cpi r17, 0xDE
    brne fail
    
    rcall inc_case
    rjmp test19_start

; ============================================================
; TEST 19: STD with negative displacement (simulated via address calc)
; ============================================================
test19_start:
    ldi r28, low(DATA_START+60)
    ldi r29, high(DATA_START+60)
    
    ; Store at offset 5 from base
    ldi r16, 0x99
    std Y+5, r16
    
    ; Read back using base + 5
    ldd r17, Y+5
    cpi r17, 0x99
    brne fail
    
    rcall inc_case
    rjmp test20_start

; ============================================================
; TEST 20: Multiple ST operations with different pointers
; ============================================================
test20_start:
    ; Store using X
    ldi r26, low(DATA_START+80)
    ldi r27, high(DATA_START+80)
    ldi r16, 0xAA
    st X, r16
    
    ; Store using Y
    ldi r28, low(DATA_START+81)
    ldi r29, high(DATA_START+81)
    ldi r16, 0xBB
    st Y, r16
    
    ; Store using Z
    ldi r30, low(DATA_START+82)
    ldi r31, high(DATA_START+82)
    ldi r16, 0xCC
    st Z, r16
    
    ; Verify all three
    lds r17, DATA_START+80
    cpi r17, 0xAA
    brne fail
    lds r17, DATA_START+81
    cpi r17, 0xBB
    brne fail
    lds r17, DATA_START+82
    cpi r17, 0xCC
    brne fail
    
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