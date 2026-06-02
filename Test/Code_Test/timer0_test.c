#ifndef F_CPU
#define F_CPU 16000000UL
#endif

#include <avr/io.h>
#include <avr/interrupt.h>

// Volatile trackers so the interrupt vectors can communicate with main()
volatile uint8_t ovf_count = 0;
volatile uint8_t compa_count = 0;
volatile uint8_t current_mode = 0;

// Helper function to scrub the timer clean before starting a new mode
void reset_timer0() {
    // Stop the timer (clear clock select bits)
    TCCR0B &= ~((1 << CS02) | (1 << CS01) | (1 << CS00));
    
    // Clear all configuration and counts
    TCCR0A = 0x00;
    TCCR0B = 0x00;
    TCNT0  = 0x00;
    OCR0A  = 0x00;
    OCR0B  = 0x00;
    
    // Clear any pending interrupt flags
    TIFR0  = (1 << OCF0B) | (1 << OCF0A) | (1 << TOV0);
    
    // Disable Timer0 interrupts
    TIMSK0 = 0x00;
    
    // Reset our trackers
    ovf_count = 0;
    compa_count = 0;
}

// Timer0 Overflow Interrupt
ISR(TIMER0_OVF_vect) {
    ovf_count++;
}

// Timer0 Compare Match A Interrupt
ISR(TIMER0_COMPA_vect) {
    compa_count++;
}

int main(void) {
    // Set PD6 (OC0A) and PD5 (OC0B) as outputs so the hardware can toggle them
    DDRD |= (1 << PD6) | (1 << PD5);
    
    sei(); // Enable global interrupts

    // ==========================================
    // MODE 0: Normal Mode
    // Top: 0xFF, Update: Immediate, TOV Flag: MAX
    // ==========================================
    current_mode = 0;
    reset_timer0();
    TIMSK0 |= (1 << TOIE0); // Enable Overflow Interrupt
    // Start timer: Prescaler 8
    TCCR0B |= (1 << CS01); 
    while (ovf_count < 5) { asm volatile("nop"); } // Wait for 5 overflows

    // ==========================================
    // MODE 1: Phase Correct PWM, Top = 0xFF
    // Top: 0xFF, Update: TOP, TOV Flag: BOTTOM
    // ==========================================
    current_mode = 1;
    reset_timer0();
    OCR0A = 127; // 50% Duty cycle
    OCR0B = 64;  // 25% Duty cycle
    // Set WGM00. Set COM0A1/COM0B1 to clear OC0A/OC0B on compare match when up-counting
    TCCR0A |= (1 << COM0A1) | (1 << COM0B1) | (1 << WGM00);
    TIMSK0 |= (1 << TOIE0);
    TCCR0B |= (1 << CS01); // Prescaler 8
    while (ovf_count < 5) { asm volatile("nop"); }

    // ==========================================
    // MODE 2: CTC (Clear Timer on Compare Match)
    // Top: OCR0A, Update: Immediate, TOV Flag: MAX
    // ==========================================
    current_mode = 2;
    reset_timer0();
    OCR0A = 150; // Timer should reset exactly at 150, never reaching 0xFF
    // Set WGM01. Set COM0A0 to toggle OC0A pin on compare match
    TCCR0A |= (1 << COM0A0) | (1 << WGM01);
    TIMSK0 |= (1 << OCIE0A); // Enable Compare Match A interrupt
    TCCR0B |= (1 << CS01); 
    while (compa_count < 5) { asm volatile("nop"); }

    // ==========================================
    // MODE 3: Fast PWM, Top = 0xFF
    // Top: 0xFF, Update: BOTTOM, TOV Flag: MAX
    // ==========================================
    current_mode = 3;
    reset_timer0();
    OCR0A = 200;
    // Set WGM01 and WGM00. Set COM0A1 to Clear OC0A on Compare Match, set at BOTTOM
    TCCR0A |= (1 << COM0A1) | (1 << WGM01) | (1 << WGM00);
    TIMSK0 |= (1 << TOIE0);
    TCCR0B |= (1 << CS01);
    while (ovf_count < 5) { asm volatile("nop"); }

    // ==========================================
    // MODE 5: Phase Correct PWM, Top = OCR0A
    // Top: OCR0A, Update: TOP, TOV Flag: BOTTOM
    // ==========================================
    current_mode = 5;
    reset_timer0();
    OCR0A = 180; // Timer counts 0 -> 180 -> 0
    // Set WGM02 (in TCCR0B) and WGM00 (in TCCR0A). Toggle OC0A on Compare Match.
    TCCR0A |= (1 << COM0A0) | (1 << WGM00);
    TIMSK0 |= (1 << TOIE0);
    TCCR0B |= (1 << WGM02) | (1 << CS01);
    while (ovf_count < 5) { asm volatile("nop"); }

    // ==========================================
    // MODE 7: Fast PWM, Top = OCR0A
    // Top: OCR0A, Update: BOTTOM, TOV Flag: TOP
    // ==========================================
    current_mode = 7;
    reset_timer0();
    OCR0A = 100; // Timer counts 0 -> 100, then instantly resets to 0
    // Set WGM02, WGM01, WGM00. Toggle OC0A on Compare Match.
    TCCR0A |= (1 << COM0A0) | (1 << WGM01) | (1 << WGM00);
    TIMSK0 |= (1 << TOIE0);
    TCCR0B |= (1 << WGM02) | (1 << CS01);
    while (ovf_count < 5) { asm volatile("nop"); }

    // ==========================================
    // TEST COMPLETE: Halt CPU
    // ==========================================
    reset_timer0();
    current_mode = 0xFF; // Signal to emulator that test is done
    
    while(1) {
        asm volatile("nop");
    }
}