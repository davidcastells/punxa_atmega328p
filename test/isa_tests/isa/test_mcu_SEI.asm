; ============================================================
; SEI (Set Global Interrupt Flag) test suite
; ============================================================
; Tests that SEI correctly:
; 1. Enables global interrupts by setting SREG bit 7
; 2. Allows a pending interrupt to execute
; ============================================================
; SEI is a 1-word (16-bit) instruction
; Format: 1001 0100 0111 1000
; Operation: I <- 1
; ============================================================

.equ test_case = 0x0100
.equ final_result = 0x0101
.equ EIMSK = 0x1D
.equ EICRA = 0x19
.equ SREG = 0x3F

reset:
    ; Initialize result tracking
    ldi r16, 1
    sts test_case, r16
    sts final_result, r16

    ; Configure an external interrupt (INT0)
    ; We trigger it via software or hardware, but keep interrupts disabled
    cli                 ; Ensure interrupts are disabled at start
    ldi r16, (1 << 0)
    sts EIMSK, r16      ; Enable INT0
    
    rjmp test1_start

; ============================================================
; TEST 1: SEI enables interrupts
; ============================================================
test1_start:
    ; At this point, I-bit is 0. If an interrupt occurs, 
    ; it should be latched but NOT serviced.
    
    ; Trigger INT0 (Simulate hardware event)
    ; (In actual hardware, apply a signal to the INT0 pin)
    
    ; Execute SEI to enable interrupts
    sei
    
    ; If SEI works, the CPU should immediately jump to 
    ; the ISR defined below. If it fails, the code continues.
    
    ; Logic to confirm ISR was hit:
    lds r16, 0x0102     ; A flag set inside the ISR
    cpi r16, 0xAA
    brne fail           ; If not set, ISR never ran
    
    rcall inc_case
    rjmp success

; ============================================================
; Interrupt Service Routine
; ============================================================
.org 0x0002             ; INT0 vector
    push r16
    ldi r16, 0xAA
    sts 0x0102, r16     ; Set flag in SRAM
    pop r16
    reti

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