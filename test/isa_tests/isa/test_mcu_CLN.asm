; ============================================================
; CLN (Clear Negative Flag) test suite (TRAMPOLINE SAFE)
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ SPH = 0x3E
.equ SPL = 0x3D
.equ SREG_ADDR = 0x5F
.equ GPIOR0 = 0x1E

reset:
    ldi r16, high(0x08FF)
    out SPH, r16
    ldi r16, low(0x08FF)
    out SPL, r16

    ldi r16, 1
    sts test_case, r16
    sts final_result, r16

    rjmp test1_start

; ============================================================
; TEST 1-2: CLN basic operation
; ============================================================

test1_start:
    sen
    cln
    brpl n_clear1
    jmp fail
n_clear1:
    rcall inc_case
    rjmp test2_start

test2_start:
    cln
    cln
    brpl n_still_clear2
    jmp fail
n_still_clear2:
    rcall inc_case
    rjmp test3_start

; ============================================================
; TEST 3: Flag preservation
; ============================================================

test3_start:
    sei
    set
    seh
    sev
    sez
    sec
    sen
    cln

    brpl t3_ok1
    jmp fail
t3_ok1:

    brie t3_ok2
    jmp fail
t3_ok2:

    brts t3_ok3
    jmp fail
t3_ok3:

    brhs t3_ok4
    jmp fail
t3_ok4:

    brvs t3_ok5
    jmp fail
t3_ok5:

    breq t3_ok6
    jmp fail
t3_ok6:

    brcs t3_ok7
    jmp fail
t3_ok7:

    rcall inc_case
    rjmp test4_start

; ============================================================
; TEST 4-7: No side effects
; ============================================================

test4_start:
    ldi r16, 0xAA
    ldi r17, 0xBB
    cln

    cpi r16, 0xAA
    breq t4_ok1
    jmp fail
t4_ok1:

    cpi r17, 0xBB
    breq t4_ok2
    jmp fail
t4_ok2:

    rcall inc_case
    rjmp test5_start

test5_start:
    ldi r16, 0xDE
    sts 0x0200, r16
    cln
    lds r17, 0x0200

    cpi r17, 0xDE
    breq t5_ok
    jmp fail
t5_ok:

    rcall inc_case
    rjmp test6_start

test6_start:
    ldi r16, 0xAD
    out GPIOR0, r16
    cln
    in r17, GPIOR0

    cpi r17, 0xAD
    breq t6_ok
    jmp fail
t6_ok:

    rcall inc_case
    rjmp test7_start

test7_start:
    in r16, SPL
    in r17, SPH
    cln
    cln
    cln

    in r18, SPL
    in r19, SPH

    cp r16, r18
    breq t7_ok1
    jmp fail
t7_ok1:

    cp r17, r19
    breq t7_ok2
    jmp fail
t7_ok2:

    rcall inc_case
    rjmp test8_start

; ============================================================
; TEST 8-12: Logic and Flow
; ============================================================

test8_start:
    ldi r16, 0
    cln
    inc r16
    cln
    inc r16
    cln
    inc r16

    cpi r16, 3
    breq t8_ok
    jmp fail
t8_ok:

    rcall inc_case
    rjmp test9_start

test9_start:
    clv
    sen
    cln

    brge t9_ok1
    jmp fail
t9_ok1:

    sev
    sen
    cln

    brlt t9_ok2
    jmp fail
t9_ok2:

    rcall inc_case
    rjmp test10_start

test10_start:
    sen
    cln
    cln
    cln

    brpl t10_ok
    jmp fail
t10_ok:

    rcall inc_case
    rjmp test11_start

test11_start:
    sen
    cln
    sen

    brmi t11_ok
    jmp fail
t11_ok:

    rcall inc_case
    rjmp test12_start

test12_start:
    ldi r16, 0x80
    ldi r17, 0x01
    add r16, r17
    cln

    cpi r16, 0x81
    breq t12_ok1
    jmp fail
t12_ok1:

    brpl t12_ok2
    jmp fail
t12_ok2:

    rcall inc_case
    rjmp test13_start

; ============================================================
; TEST 13-16: Advanced Scenarios
; ============================================================

test13_start:
    sen
    rcall cln_sub13

    brpl t13_ok
    jmp fail
t13_ok:

    rcall inc_case
    rjmp test14_start

cln_sub13:
    cln
    ret

test14_start:
    sen
    cln
    sen
    cln

    brpl t14_ok
    jmp fail
t14_ok:

    rcall inc_case
    rjmp test15_start

test15_start:
    ldi r16, 3
    ldi r17, 5
    sub r16, r17
    cln

    brpl t15_ok
    jmp fail
t15_ok:

    rcall inc_case
    rjmp test16_start

test16_start:
    clv
    cln

    brvc t16_ok1
    jmp fail
t16_ok1:

    sev
    cln

    brvs t16_ok2
    jmp fail
t16_ok2:

    rcall inc_case
    rjmp success

; ============================================================
; SUCCESS / FAILURE
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