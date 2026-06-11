; ============================================================
; SEN (Set Negative Flag) test suite - Strictly Local Trampolines
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
    rjmp test1

fail:
    ldi r16, 255
    sts final_result, r16
end: rjmp end

; --- Test Logic with Local Trampolines ---

test1:
    cln
    sen
    brmi t1_ok
    rjmp fail
t1_ok:
    rcall inc_case
test2:
    sen
    sen
    brmi t2_ok
    rjmp fail
t2_ok:
    rcall inc_case
test3:
    cli; clt; clh; clv; clz; clc; cln
    sei; set; seh; sev; sez; sec
    sen
    brmi t3_n
    rjmp fail
t3_n:
    brie t3_i
    rjmp fail
t3_i:
    brts t3_t
    rjmp fail
t3_t:
    brhs t3_h
    rjmp fail
t3_h:
    brvs t3_v
    rjmp fail
t3_v:
    breq t3_z
    rjmp fail
t3_z:
    brcs t3_c
    rjmp fail
t3_c:
    rcall inc_case
test4:
    ldi r16, 0xAA
    ldi r17, 0xBB
    sen
    cpi r16, 0xAA
    brne t4_fail
    cpi r17, 0xBB
    brne t4_fail
    rcall inc_case
    rjmp test5
t4_fail: rjmp fail
test5:
    ldi r16, 0xDE
    sts 0x0200, r16
    sen
    lds r17, 0x0200
    cpi r17, 0xDE
    brne t5_fail
    rcall inc_case
    rjmp test6
t5_fail: rjmp fail
test6:
    ldi r16, 0xAD
    out GPIOR0, r16
    sen
    in r17, GPIOR0
    cpi r17, 0xAD
    brne t6_fail
    rcall inc_case
    rjmp test7
t6_fail: rjmp fail
test7:
    in r16, SPL
    in r17, SPH
    sen
    sen
    sen
    in r18, SPL
    in r19, SPH
    cp r16, r18
    brne t7_fail
    cp r17, r19
    brne t7_fail
    rcall inc_case
    rjmp test8
t7_fail: rjmp fail
test8:
    ldi r16, 0
    sen
    inc r16
    sen
    inc r16
    sen
    inc r16
    cpi r16, 3
    brne t8_fail
    rcall inc_case
    rjmp test9
t8_fail: rjmp fail
test9:
    clv; cln; sen
    brlt t9_a
    rjmp fail
t9_a:
    sev; cln; sen
    brge t9_ok
    rjmp fail
t9_ok:
    rcall inc_case
test10:
    cln; sen; sen; sen
    brmi t10_ok
    rjmp fail
t10_ok:
    rcall inc_case
test11:
    cln; sen; cln
    brpl t11_ok
    rjmp fail
t11_ok:
    rcall inc_case
test12:
    ldi r16, 0x10
    ldi r17, 0x20
    add r16, r17
    sen
    cpi r16, 0x30
    brne t12_fail
    brmi t12_ok
    rjmp t12_fail
t12_ok:
    rcall inc_case
    rjmp test13
t12_fail: rjmp fail
test13:
    cln
    rcall sen_sub
    brmi t13_ok
    rjmp fail
t13_ok:
    rcall inc_case
test14:
    cln; sen; cln; sen; cln
    brpl t14_ok
    rjmp fail
t14_ok:
    rcall inc_case
test15:
    ldi r16, 5
    ldi r17, 3
    sub r16, r17
    sen
    brmi t15_ok
    rjmp fail
t15_ok:
    rcall inc_case
test16:
    clv; sen
    brvc t16_a
    rjmp fail
t16_a:
    sev; sen
    brvs t16_ok
    rjmp fail
t16_ok:
    rcall inc_case
test17:
    cln; sen
    brmi t17_ok
    rjmp fail
t17_ok:
    rcall inc_case
test18:
    sec; sen
    brcs t18_a
    rjmp fail
t18_a:
    clc; sen
    brcc t18_ok
    rjmp fail
t18_ok:
    rcall inc_case
test19:
    sez; sen
    breq t19_a
    rjmp fail
t19_a:
    clz; sen
    brne t19_ok
    rjmp fail
t19_ok:
    rcall inc_case
test20:
    ldi r16, 10
    ldi r17, 10
    cp r16, r17
    clv; sen
    brlt t20_ok
    rjmp fail
t20_ok:
    ldi r16, 1
    sts final_result, r16
    rjmp end

sen_sub:
    sen
    ret

inc_case:
    lds r16, test_case
    inc r16
    sts test_case, r16
    ret