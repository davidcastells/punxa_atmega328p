# Testing Atmega328p ISA

We implemented some instruction tests in assembler in a similar way that RISC-V ISA tests are implemented (and was done in Punxa to verify the repertory).

In punxa_atmega328p we provide assembler code that we assemble with our own assembler.

To run the tests do

```
python tb_ISA_tests.py -c "runAllTests()"
```

***Summary***

<pre>
test_arith      71.4 %   |█████████████████████████████████░░░░░░░░░░░░|
test_bitmap     38.5 %   |██████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_logic      42.9 %   |████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░|
test_ctrflow    5.6 %    |███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_data       10.0 %   |█████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_mcu        8.3 %    |████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
</pre>

The detailed current output is:

```
Test test_arith_ADD.asm             = OK
Test test_arith_ADIW.asm            = FAILED - Failed in test case 7
Test test_arith_DEC.asm             = OK
Test test_arith_INC.asm             = OK
Test test_arith_MUL.asm             = OK
Test test_arith_SBIW.asm            = OK
Test test_arith_SUB.asm             = FAILED - Failed in test case 2
Test test_bitmap_ASR.asm            = OK
Test test_bitmap_BLD.asm            = OK
Test test_bitmap_BST.asm            = OK
Test test_bitmap_CBI.asm            = OK
Test test_bitmap_LSL.asm            = FAILED - Failed in test case 1
Test test_bitmap_LSR.asm            = FAILED - LSR not reviewed
Test test_bitmap_ROL.asm            = FAILED - non finished
Test test_bitmap_ROR.asm            = FAILED - ROR not reviewed
Test test_bitmap_SBI.asm            = FAILED - SBI not reviewed
Test test_bitmap_SBIC.asm           = OK
Test test_bitmap_SBIS.asm           = FAILED - Failed in test case 1
Test test_bitmap_SBRC.asm           = FAILED - Failed to assemble "ldi r17, 0b11111110"
Test test_bitmap_SBRS.asm           = FAILED - Failed to assemble "ori r17, (1<<4)"
Test test_logic_AND.asm             = OK
Test test_logic_CBR.asm             = FAILED - cannot access local variable 'Rr' where it is not associated with a value
Test test_logic_COM.asm             = FAILED - Failed to assemble "com r16"
Test test_logic_EOR.asm             = OK
Test test_logic_NEG.asm             = OK
Test test_logic_OR.asm              = FAILED - Failed in test case 4
Test test_logic_SBR.asm             = FAILED - ORI not reviewed
Test test_ctrflow_BRBC.asm          = OK
Test test_ctrflow_BRBS.asm          = FAILED - Failed in test case 2
Test test_ctrflow_BRCC.asm          = FAILED - Failed in test case 7
Test test_ctrflow_BRCS.asm          = FAILED - Failed in test case 2
Test test_ctrflow_BREQ.asm          = FAILED - Failed in test case 4
Test test_ctrflow_BRGE.asm          = FAILED - relative jump outside of range 81 in brge fail
Test test_ctrflow_BRLO.asm          = FAILED - Failed in test case 1
Test test_ctrflow_BRLT.asm          = FAILED - Failed in test case 1
Test test_ctrflow_BRNE.asm          = FAILED - relative jump outside of range 78 in brne fail
Test test_ctrflow_BRSH.asm          = FAILED - Failed in test case 1
Test test_ctrflow_CALL.asm          = FAILED - Failed to assemble "ldi r0, 0x55"
Test test_ctrflow_ICALL.asm         = FAILED - relative jump outside of range 200 in brne fail
Test test_ctrflow_IJMP.asm          = FAILED - relative jump outside of range 203 in brne fail
Test test_ctrflow_JMP.asm           = FAILED - relative jump outside of range 189 in brne fail
Test test_ctrflow_RCALL.asm         = FAILED - Failed to assemble "ldi r0, 0x55"
Test test_ctrflow_RET.asm           = FAILED - relative jump outside of range 222 in brne fail
Test test_ctrflow_RETI.asm          = FAILED - Failed to assemble "std Y+0, r18"
Test test_ctrflow_RJMP.asm          = FAILED - relative jump outside of range 190 in brne fail
Test test_data_IN.asm               = FAILED - Failed to assemble "cpi r0, 0x78"
Test test_data_LD.asm               = FAILED - Failed to assemble "sts 0+1, r17"
Test test_data_LDI.asm              = FAILED - Failed in test case 2
Test test_data_LDS.asm              = FAILED - Failed to assemble "sts 0+1, r16"
Test test_data_MOV.asm              = FAILED - Failed to assemble "ldi r0, 0x7E"
Test test_data_OUT.asm              = FAILED - Failed to assemble "ldi r0, 0xAA"
Test test_data_POP.asm              = OK
Test test_data_PUSH.asm             = FAILED - SUBI not reviewed
Test test_data_ST.asm               = FAILED - invalid literal for int() with base 10: '0+2'
Test test_data_STS.asm              = FAILED - Failed to assemble "ldi r0, 0x11"
Test test_mcu_BREAK.asm             = FAILED - BREAK not validated
Test test_mcu_CLC.asm               = FAILED - Too many cycles waiting to complete instruction
Test test_mcu_CLI.asm               = FAILED - relative jump outside of range 189 in brcc fail
Test test_mcu_CLN.asm               = FAILED - relative jump outside of range 160 in brne fail
Test test_mcu_CLZ.asm               = FAILED - Too many cycles waiting to complete instruction
Test test_mcu_NOP.asm               = FAILED - relative jump outside of range 218 in brne fail
Test test_mcu_SEC.asm               = OK
Test test_mcu_SEI.asm               = FAILED - Failed to assemble ".org 0x0002"
Test test_mcu_SEN.asm               = FAILED - relative jump outside of range 161 in brne fail
Test test_mcu_SEZ.asm               = FAILED - Too many cycles waiting to complete instruction
Test test_mcu_SLEEP.asm             = FAILED - Failed to assemble ".org 0x0002"
Test test_mcu_WDR.asm               = FAILED - WDR not validated
Total: 67 Correct: 16 (23.9 %)
```