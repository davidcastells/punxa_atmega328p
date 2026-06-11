# Testing Atmega328p ISA

We implemented some instruction tests in assembler in a similar way that RISC-V ISA tests are implemented (and was done in Punxa to verify the repertory).

In punxa_atmega328p we provide assembler code that we assemble with our own assembler.

To run the tests do

```
python tb_ISA_tests.py -c "runAllTests()"
```

***Summary***

<pre>
test_arith      100.0 %  |█████████████████████████████████████████████|
test_bitmap     100.0 %  |█████████████████████████████████████████████|
test_logic      71.4 %   |█████████████████████████████████░░░░░░░░░░░░|
test_ctrflow    16.7 %   |████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_data       0.0 %    |░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_mcu        0.0 %    |░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
</pre>

The detailed current output is:

```
Test test_arith_ADD.asm             = OK
Test test_arith_ADIW.asm            = OK
Test test_arith_DEC.asm             = OK
Test test_arith_INC.asm             = OK
Test test_arith_MUL.asm             = OK
Test test_arith_SBIW.asm            = OK
Test test_arith_SUB.asm             = OK
Test test_bitmap_ASR.asm            = OK
Test test_bitmap_BLD.asm            = OK
Test test_bitmap_BST.asm            = OK
Test test_bitmap_CBI.asm            = OK
Test test_bitmap_LSL.asm            = OK
Test test_bitmap_LSR.asm            = OK
Test test_bitmap_ROL.asm            = OK
Test test_bitmap_ROR.asm            = OK
Test test_bitmap_SBI.asm            = OK
Test test_bitmap_SBIC.asm           = OK
Test test_bitmap_SBIS.asm           = OK
Test test_bitmap_SBRC.asm           = OK
Test test_bitmap_SBRS.asm           = OK
Test test_logic_AND.asm             = OK
Test test_logic_CBR.asm             = FAILED - Failed in test case 1
Test test_logic_COM.asm             = OK
Test test_logic_EOR.asm             = OK
Test test_logic_NEG.asm             = OK
Test test_logic_OR.asm              = FAILED - Failed in test case 1
Test test_logic_SBR.asm             = OK
Test test_ctrflow_BRBC.asm          = OK
Test test_ctrflow_BRBS.asm          = FAILED - SUBI not reviewed
Test test_ctrflow_BRCC.asm          = OK
Test test_ctrflow_BRCS.asm          = OK
Test test_ctrflow_BREQ.asm          = FAILED - Failed in test case 7
Test test_ctrflow_BRGE.asm          = FAILED - Failed in test case 6
Test test_ctrflow_BRLO.asm          = FAILED - Failed in test case 1
Test test_ctrflow_BRLT.asm          = FAILED - Failed in test case 7
Test test_ctrflow_BRNE.asm          = FAILED - Failed in test case 8
Test test_ctrflow_BRSH.asm          = FAILED - Failed in test case 1
Test test_ctrflow_CALL.asm          = FAILED - Failed in test case 3
Test test_ctrflow_ICALL.asm         = FAILED - Failed in test case 6
Test test_ctrflow_IJMP.asm          = FAILED - Failed in test case 4
Test test_ctrflow_JMP.asm           = FAILED - Failed in test case 7
Test test_ctrflow_RCALL.asm         = FAILED - Failed in test case 1
Test test_ctrflow_RET.asm           = FAILED - Failed in test case 5
Test test_ctrflow_RETI.asm          = FAILED - Step count > limit
Test test_ctrflow_RJMP.asm          = FAILED - Failed in test case 7
Test test_data_IN.asm               = FAILED - 8
Test test_data_LD.asm               = FAILED - Failed to assemble "sts 0+1, r17"
Test test_data_LDI.asm              = FAILED - Failed in test case 8
Test test_data_LDS.asm              = FAILED - Failed to assemble "sts 0+1, r16"
Test test_data_MOV.asm              = FAILED - Failed to assemble "in r20, SREG"
Test test_data_OUT.asm              = FAILED - Failed to assemble "ldi r0, 0xAA"
Test test_data_POP.asm              = FAILED - Failed in test case 1
Test test_data_PUSH.asm             = FAILED - Failed in test case 1
Test test_data_ST.asm               = FAILED - invalid literal for int() with base 10: '0+2'
Test test_data_STS.asm              = FAILED - Too many cycles waiting to complete instruction
Test test_mcu_BREAK.asm             = FAILED - BREAK not validated
Test test_mcu_CLC.asm               = FAILED - Too many cycles waiting to complete instruction
Test test_mcu_CLI.asm               = FAILED - Too many cycles waiting to complete instruction
Test test_mcu_CLN.asm               = FAILED - Failed in test case 5
Test test_mcu_CLZ.asm               = FAILED - Too many cycles waiting to complete instruction
Test test_mcu_NOP.asm               = FAILED - Step count > limit
Test test_mcu_SEC.asm               = FAILED - Too many cycles waiting to complete instruction
Test test_mcu_SEI.asm               = FAILED - Failed to assemble ".org 0x0002"
Test test_mcu_SEN.asm               = FAILED - Failed in test case 1
Test test_mcu_SEZ.asm               = FAILED - Too many cycles waiting to complete instruction
Test test_mcu_SLEEP.asm             = FAILED - Failed to assemble ".org 0x0002"
Test test_mcu_WDR.asm               = FAILED - WDR not validated
Total: 67 Correct: 28 (41.8 %)
```