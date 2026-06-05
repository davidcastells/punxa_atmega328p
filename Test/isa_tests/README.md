# Testing Atmega328p ISA

We implemented some instruction tests in assembler in a similar way that RISC-V ISA tests are implemented (and was done in Punxa to verify the repertory).

In punxa_atmega328p we provide assembler code that we assemble with our own assembler.

To run the tests do

```
python tb_ISA_tests.py -c "runAllTests()"
```

***Summary***

<pre>
test_arith      14.3 %   |███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_bitmap     0.0 %    |░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_logic      0.0 %    |░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_ctrflow    0.0 %    |░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_data       0.0 %    |░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
test_mcu        0.0 %    |░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
</pre>

The detailed current output is:

```
Test test_arith_ADD.asm             = OK
Test test_arith_ADIW.asm            = FAILED - 'end'
Test test_arith_DEC.asm             = FAILED - 'end'
Test test_arith_INC.asm             = FAILED - 'end'
Test test_arith_MUL.asm             = FAILED - 'end'
Test test_arith_SBIW.asm            = FAILED - 'end'
Test test_arith_SUB.asm             = FAILED - 'end'
Test test_bitmap_ASR.asm            = FAILED - 'end'
Test test_bitmap_BLD.asm            = FAILED - 'end'
Test test_bitmap_BST.asm            = FAILED - 'end'
Test test_bitmap_CBI.asm            = FAILED - 'end'
Test test_bitmap_LSL.asm            = FAILED - 'end'
Test test_bitmap_LSR.asm            = FAILED - 'end'
Test test_bitmap_ROL.asm            = FAILED - 'end'
Test test_bitmap_ROR.asm            = FAILED - 'end'
Test test_bitmap_SBI.asm            = FAILED - 'end'
Test test_bitmap_SBIC.asm           = FAILED - 'end'
Test test_bitmap_SBIS.asm           = FAILED - 'end'
Test test_bitmap_SBRC.asm           = FAILED - 'end'
Test test_bitmap_SBRS.asm           = FAILED - 'end'
Test test_logic_AND.asm             = FAILED - 'end'
Test test_logic_CBR.asm             = FAILED - 'end'
Test test_logic_COM.asm             = FAILED - 'end'
Test test_logic_EOR.asm             = FAILED - 'end'
Test test_logic_NEG.asm             = FAILED - 'end'
Test test_logic_OR.asm              = FAILED - 'end'
Test test_logic_SBR.asm             = FAILED - 'end'
Test test_ctrflow_BRBC.asm          = FAILED - 'end'
Test test_ctrflow_BRBS.asm          = FAILED - 'end'
Test test_ctrflow_BRCC.asm          = FAILED - 'end'
Test test_ctrflow_BRCS.asm          = FAILED - 'end'
Test test_ctrflow_BREQ.asm          = FAILED - 'end'
Test test_ctrflow_BRGE.asm          = FAILED - 'end'
Test test_ctrflow_BRLO.asm          = FAILED - 'end'
Test test_ctrflow_BRLT.asm          = FAILED - 'end'
Test test_ctrflow_BRNE.asm          = FAILED - 'end'
Test test_ctrflow_BRSH.asm          = FAILED - 'end'
Test test_ctrflow_CALL.asm          = FAILED - 'end'
Test test_ctrflow_ICALL.asm         = FAILED - 'end'
Test test_ctrflow_IJMP.asm          = FAILED - 'end'
Test test_ctrflow_JMP.asm           = FAILED - 'end'
Test test_ctrflow_RCALL.asm         = FAILED - 'end'
Test test_ctrflow_RET.asm           = FAILED - 'end'
Test test_ctrflow_RETI.asm          = FAILED - 'end'
Test test_ctrflow_RJMP.asm          = FAILED - 'end'
Test test_data_IN.asm               = FAILED - 'end'
Test test_data_LD.asm               = FAILED - 'end'
Test test_data_LDI.asm              = FAILED - 'end'
Test test_data_LDS.asm              = FAILED - 'end'
Test test_data_MOV.asm              = FAILED - 'end'
Test test_data_OUT.asm              = FAILED - 'end'
Test test_data_POP.asm              = FAILED - 'end'
Test test_data_PUSH.asm             = FAILED - 'end'
Test test_data_ST.asm               = FAILED - 'end'
Test test_data_STS.asm              = FAILED - 'end'
Test test_mcu_BREAK.asm             = FAILED - 'end'
Test test_mcu_CLC.asm               = FAILED - 'end'
Test test_mcu_CLI.asm               = FAILED - 'end'
Test test_mcu_CLN.asm               = FAILED - 'end'
Test test_mcu_CLZ.asm               = FAILED - 'end'
Test test_mcu_NOP.asm               = FAILED - 'end'
Test test_mcu_SEC.asm               = FAILED - 'end'
Test test_mcu_SEI.asm               = FAILED - 'end'
Test test_mcu_SEN.asm               = FAILED - 'end'
Test test_mcu_SEZ.asm               = FAILED - 'end'
Test test_mcu_SLEEP.asm             = FAILED - 'end'
Test test_mcu_WDR.asm               = FAILED - 'end'
Total: 67 Correct: 1 (1.5 %)
```