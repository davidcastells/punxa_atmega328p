; ============================================================
; LD (Load Indirect from Data Space) test suite
; ============================================================
; Tests that LD correctly:
; 1. Loads data from SRAM address pointed to by X/Y/Z
; 2. Can load with/without displacement (LDD)
; 3. Can post-increment or pre-decrement pointer
; ============================================================
; LD is a 1-word (16-bit) instruction
; Formats:
;   LD Rd, X        (1001 000d dddd 1100)
;   LD Rd, X+       (1001 000d dddd 1101)
;   LD Rd, -X       (1001 000d dddd 1110)
;   LD Rd, Y        (1000 000d dddd 1000)
;   LD Rd, Y+       (1001 000d dddd 1001)
;   LD Rd, -Y       (1001 000d dddd 1010)
;   LDD Rd, Y+q     (10q0 qq0d dddd 1qqq)
;   LD Rd, Z        (1000 000d dddd 0000)
;   LD Rd, Z+       (1001 000d dddd 0001)
;   LD Rd, -Z       (1001 000d dddd 0010)
;   LDD Rd, Z+q     (10q0 qq0d dddd 0qqq)
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
; TEST 1: LD Rd, X (load from X pointer)
; ============================================================
test1_start:
    ; Prepare test data in SRAM
    ldi r17, 0x42
    sts DATA_START, r17
    
    ; Load X pointer
    ldi r26, low(DATA_START)
    ldi r27, high(DATA_START)
    
    ; Load from X
    ld r16, X
    cpi r16, 0x42
    brne fail
    rcall inc_case
    rjmp test2_start

; ============================================================
; TEST 2: LD Rd, X+ (load and post-increment)
; ============================================================
test2_start:
    ; Prepare test data
    ldi r17, 0xAA
    sts DATA_START, r17
    ldi r17, 0xBB
    sts DATA_START+1, r17
    
    ; Load X pointer
    ldi r26, low(DATA_START)
    ldi r27, high(DATA_START)
    
    ; Load with post-increment
    ld r16, X+
    cpi r16, 0xAA
    brne fail
    ; Verify X increased
    cpi r26, low(DATA_START+1)
    brne fail
    cpi r27, high(DATA_START+1)
    brne fail
    
    ; Second load
    ld r16, X+
    cpi r16, 0xBB
    brne fail
    
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: LD Rd, -X (pre-decrement and load)
; ============================================================
test3_start:
    ; Prepare test data
    ldi r17, 0xCC
    sts DATA_START+2, r17
    
    ; Load X pointer to DATA_START+3
    ldi r26, low(DATA_START+3)
    ldi r27, high(DATA_START+3)
    
    ; Pre-decrement then load
    ld r16, -X
    cpi r16, 0xCC
    brne fail
    ; Verify X decreased
    cpi r26, low(DATA_START+2)
    brne fail
    cpi r27, high(DATA_START+2)
    brne fail
    
    rcall inc_case
    rjmp test4_start

; ============================================================
; TEST 4: LD Rd, Y (load from Y pointer)
; ============================================================
test4_start:
    ; Prepare test data
    ldi r17, 0x5A
    sts DATA_START, r17
    
    ; Load Y pointer
    ldi r28, low(DATA_START)
    ldi r29, high(DATA_START)
    
    ; Load from Y
    ld r16, Y
    cpi r16, 0x5A
    brne fail
    
    rcall inc_case
    rjmp test5_start

; ============================================================
; TEST 5: LD Rd, Y+ (load and post-increment)
; ============================================================
test5_start:
    ; Prepare test data
    ldi r17, 0x11
    sts DATA_START, r17
    ldi r17, 0x22
    sts DATA_START+1, r17
    
    ; Load Y pointer
    ldi r28, low(DATA_START)
    ldi r29, high(DATA_START)
    
    ; Load with post-increment
    ld r16, Y+
    cpi r16, 0x11
    brne fail
    cpi r28, low(DATA_START+1)
    brne fail
    
    ld r16, Y+
    cpi r16, 0x22
    brne fail
    
    rcall inc_case
    rjmp test6_start

; ============================================================
; TEST 6: LD Rd, -Y (pre-decrement and load)
; ============================================================
test6_start:
    ; Prepare test data
    ldi r17, 0xDD
    sts DATA_START+2, r17
    
    ; Load Y pointer to DATA_START+3
    ldi r28, low(DATA_START+3)
    ldi r29, high(DATA_START+3)
    
    ; Pre-decrement then load
    ld r16, -Y
    cpi r16, 0xDD
    brne fail
    cpi r28, low(DATA_START+2)
    brne fail
    
    rcall inc_case
    rjmp test7_start

; ============================================================
; TEST 7: LD Rd, Z (load from Z pointer)
; ============================================================
test7_start:
    ; Prepare test data
    ldi r17, 0x3C
    sts DATA_START, r17
    
    ; Load Z pointer
    ldi r30, low(DATA_START)
    ldi r31, high(DATA_START)
    
    ; Load from Z
    ld r16, Z
    cpi r16, 0x3C
    brne fail
    
    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8: LD Rd, Z+ (load and post-increment)
; ============================================================
test8_start:
    ; Prepare test data
    ldi r17, 0x77
    sts DATA_START, r17
    ldi r17, 0x88
    sts DATA_START+1, r17
    
    ; Load Z pointer
    ldi r30, low(DATA_START)
    ldi r31, high(DATA_START)
    
    ; Load with post-increment
    ld r16, Z+
    cpi r16, 0x77
    brne fail
    cpi r30, low(DATA_START+1)
    brne fail
    
    ld r16, Z+
    cpi r16, 0x88
    brne fail
    
    rcall inc_case
    rjmp test9_start

; ============================================================
; TEST 9: LD Rd, -Z (pre-decrement and load)
; ============================================================
test9_start:
    ; Prepare test data
    ldi r17, 0xEE
    sts DATA_START+2, r17
    
    ; Load Z pointer to DATA_START+3
    ldi r30, low(DATA_START+3)
    ldi r31, high(DATA_START+3)
    
    ; Pre-decrement then load
    ld r16, -Z
    cpi r16, 0xEE
    brne fail
    cpi r30, low(DATA_START+2)
    brne fail
    
    rcall inc_case
    rjmp test10_start

; ============================================================
; TEST 10: LDD Rd, Y+q (load with displacement)
; ============================================================
test10_start:
    ; Prepare test data array
    ldi r17, 0x01
    sts DATA_START, r17
    ldi r17, 0x02
    sts DATA_START+1, r17
    ldi r17, 0x03
    sts DATA_START+2, r17
    ldi r17, 0x04
    sts DATA_START+3, r17
    ldi r17, 0x05
    sts DATA_START+4, r17
    
    ; Load Y pointer to base
    ldi r28, low(DATA_START)
    ldi r29, high(DATA_START)
    
    ; Load with displacements
    ldd r16, Y+0
    cpi r16, 0x01
    brne fail
    ldd r16, Y+1
    cpi r16, 0x02
    brne fail
    ldd r16, Y+2
    cpi r16, 0x03
    brne fail
    ldd r16, Y+3
    cpi r16, 0x04
    brne fail
    ldd r16, Y+4
    cpi r16, 0x05
    brne fail
    
    rcall inc_case
    rjmp test11_start

; ============================================================
; TEST 11: LDD Rd, Z+q (load with displacement)
; ============================================================
test11_start:
    ; Prepare test data
    ldi r17, 0x10
    sts DATA_START, r17
    ldi r17, 0x20
    sts DATA_START+1, r17
    
    ; Load Z pointer to base
    ldi r30, low(DATA_START)
    ldi r31, high(DATA_START)
    
    ; Load with displacements
    ldd r16, Z+0
    cpi r16, 0x10
    brne fail
    ldd r16, Z+1
    cpi r16, 0x20
    brne fail
    
    rcall inc_case
    rjmp test12_start

; ============================================================
; TEST 12: LD to different registers (R0-R31)
; ============================================================
test12_start:
    ; Prepare test data
    ldi r17, 0xAB
    sts DATA_START, r17
    
    ; Load X pointer
    ldi r26, low(DATA_START)
    ldi r27, high(DATA_START)
    
    ; Test loading to various registers
    ld r0, X
    cpi r0, 0xAB
    brne fail
    
    ld r16, X
    cpi r16, 0xAB
    brne fail
    
    ld r31, X
    cpi r31, 0xAB
    brne fail
    
    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13: LD does not modify flags
; ============================================================
test13_start:
    ; Set flags
    sec                 ; C=1
    sez                 ; Z=1
    sen                 ; N=1
    sev                 ; V=1
    seh                 ; H=1
    set                 ; T=1
    
    ; Load data
    ldi r26, low(DATA_START)
    ldi r27, high(DATA_START)
    ld r16, X
    
    ; Check all flags preserved
    brcc fail
    brne fail
    brmi fail
    brvs fail
    brhc fail
    brtc fail
    
    rcall inc_case
    rjmp test14_start

; ============================================================
; TEST 14: LD with pointer crossing page boundary
; ============================================================
test14_start:
    ; Prepare data at page boundary
    ldi r17, 0xFF
    sts 0x02FF, r17
    
    ; Load X pointer to 0x02FF
    ldi r26, 0xFF
    ldi r27, 0x02
    
    ld r16, X
    cpi r16, 0xFF
    brne fail
    
    ; Test post-increment across boundary
    ld r16, X+
    cpi r16, 0xFF
    brne fail
    cpi r26, 0x00
    brne fail
    cpi r27, 0x03
    brne fail
    
    rcall inc_case
    rjmp test15_start

; ============================================================
; TEST 15: LDD with maximum displacement (63)
; ============================================================
test15_start:
    ; Prepare data at offset 63
    ldi r17, 0x63
    sts DATA_START+63, r17
    
    ; Load Y pointer to base
    ldi r28, low(DATA_START)
    ldi r29, high(DATA_START)
    
    ; Load with maximum displacement
    ldd r16, Y+63
    cpi r16, 0x63
    brne fail
    
    rcall inc_case
    rjmp test16_start

; ============================================================
; TEST 16: LD inside loop (string copy simulation)
; ============================================================
test16_start:
    ; Setup source and destination
    ldi r26, low(DATA_START)      ; X = source
    ldi r27, high(DATA_START)
    ldi r28, low(DATA_START+32)   ; Y = destination
    ldi r29, high(DATA_START+32)
    
    ; Prepare source data
    ldi r16, 1
    sts DATA_START, r16
    ldi r16, 2
    sts DATA_START+1, r16
    ldi r16, 3
    sts DATA_START+2, r16
    ldi r16, 4
    sts DATA_START+3, r16
    
    ; Copy 4 bytes
    ldi r18, 4
copy_loop:
    ld r16, X+
    st Y+, r16
    dec r18
    brne copy_loop
    
    ; Verify destination
    ldi r28, low(DATA_START+32)
    ldi r29, high(DATA_START+32)
    ld r16, Y+
    cpi r16, 1
    brne fail
    ld r16, Y+
    cpi r16, 2
    brne fail
    ld r16, Y+
    cpi r16, 3
    brne fail
    ld r16, Y+
    cpi r16, 4
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