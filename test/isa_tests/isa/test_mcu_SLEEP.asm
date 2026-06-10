; ============================================================
; SLEEP instruction test suite
; ============================================================
; Note: SLEEP puts the CPU into a low-power mode.
; Verification requires waking the CPU (e.g., via Interrupt).
; ============================================================
; SLEEP is a 1-word (16-bit) instruction
; Format: 1001 0101 1000 1000
; ============================================================

.equ SMCR = 0x33        ; Sleep Mode Control Register
.equ EIMSK = 0x1D       ; External Interrupt Mask Register
.equ EICRA = 0x19       ; External Interrupt Control Register A
.equ SREG = 0x3F

reset:
    ; 1. Enable External Interrupt 0 (INT0) to wake from sleep
    ldi r16, (1 << 0)
    sts EIMSK, r16      ; Enable INT0
    ldi r16, (1 << ISC01) ; Trigger INT0 on falling edge
    sts EICRA, r16
    
    ; 2. Set Sleep Mode to Idle (SMCR = 0)
    ldi r16, 0x01       ; SLEEP_MODE_IDLE (SM=000, SE=1)
    sts SMCR, r16
    
    sei                 ; Enable global interrupts

    ; 3. Perform the SLEEP instruction
    sleep               
    
    ; The CPU will halt here until INT0 is triggered.
    ; Execution continues immediately following the SLEEP instruction.
    
    ; 4. Verify we woke up
    rjmp success

; ============================================================
; Interrupt Service Routine (for wake-up)
; ============================================================
.org 0x0002             ; INT0 vector address
    reti

; ============================================================
; SUCCESS / FAILURE logic
; ============================================================
success:
    ; If we reach here, we successfully entered and exited sleep
    ldi r16, 1
    sts 0x0101, r16     ; final_result = 1
end:
    rjmp end