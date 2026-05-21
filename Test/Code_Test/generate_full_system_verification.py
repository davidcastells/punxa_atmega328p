import pysimulavr
import time 
from rich.progress import Progress

# 1. Initialize the microcontroller
dev = pysimulavr.AvrFactory.instance().makeDevice("atmega328")

# 2. Load the native ELF file directly!
dev.Load("INSTRUCTION_TESTV3.elf")

# 3. Mount to the SystemClock
sc = pysimulavr.SystemClock.Instance()
sc.Add(dev)

print("Starting simulation...\n")
FULL_SYSTEM_TEST_EXPECTED_REGISTER_VALUES = [
# AVR_CORE_TEST + RAM_TEST + TIMER0_TEST + TIMER1_TEST + TIMER2_TEST + USART0_TEST + SPI_TEST + TWI_TEST + EEPROM_TEST + GPIO_TEST + INTERRUPTS_TEST + SYSTEM_CONTROL_TEST + ANALOG_COMPARATOR_TEST 
]

time.sleep(1)
start_time = time.time()
with Progress() as p:
    t = p.add_task("Executing step by step...",total= 10000)
    last_pc = 0 
    instructions_executed = 0
    for cycle_count in range(10000):
        #initialisation of lists 
        AVR_CORE_TEST_EXPECTED_REGISTER_VALUES = [
        #R:0|R:1|R:2|R:3|R:4|R:5|R:6|R:7|R:8|R:9|R:10|R:11|R:12|R:13|R:14|R:15|R:16|R:17|R:18|R:19|R:20|R:21|R:22|R:23|R:24|R:25|R:26|R:27|R:28|R:29|R:30|R:31|SREG      |PC|SP
        #    [0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0  ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0   ,0    ,0  ,0b00000000,0,0],
        ]

        RAM_TEST = [
        #    |Memory Change|
        ]

        TIMER0_TEST = [
        #    |TCCR0A|TCCR0B|TCNT0|OCR0A|OCR0B|TIMSK0|TIFR0|
        ]

        TIMER1_TEST = [
        #    |TCCR1A|TCCR1B|TCCR1C|TCNT1H|TCNT1L|OCR1AH|OCR1AL|OCR1BH|OCR1BL|ICR1H|ICR1L|TIMSK1|TIFR1|GTCCR|
        ]

        TIMER2_TEST = [
        #    |TCCR2A|TCCR2B|TCNT2|OCR2A|OCR2B|TIMSK2|TIFR2|ASSR|
        ]

        ADC_TEST = [
        #    |ADMUX|ADCSRA|ADCSRB|ADCL|ADCH|
        ]

        SPI_TEST = [
        #    |SPCR|SPSR|SPDR|
        ]

        USART0_TEST =[
        #    |UCSR0A|UCSR0B|UCSR0C|UBRR0L|UBRR0H|UDR0|
        ]

        GPIO_TEST = [
        #    |PINB|DDRB|PORTB|PINC|DDRC|PORTC|PIND|DDRD|PORTD|
        ]

        INTERRUPT_TEST = [
        #    |EIMSK|EIFR|PCIFR|EICRA|PCICR|PCMSK0|PCMSK1|PCMSK2|
        ]


        # Step the simulation forward by one clock cycle

        ThisCycle =[]
        sc.Step()
        
        #AVR_CORE registers
        for i in range(32):
            reg = dev.GetRWMem(i)
            AVR_CORE_TEST_EXPECTED_REGISTER_VALUES.append(reg)
        # Extract SREG (0x5F)
        sreg_val = dev.GetRWMem(0x5F)
        AVR_CORE_TEST_EXPECTED_REGISTER_VALUES.append(sreg_val)
        # Extract Program Counter (PC)
        pc_val = dev.PC if hasattr(dev, 'PC') else 0
        AVR_CORE_TEST_EXPECTED_REGISTER_VALUES.append(pc_val)
        # Extract Stack Pointer (SPH and SPL)
        spl = dev.GetRWMem(0x3D)
        sph = dev.GetRWMem(0x3E)
        SP_val = (sph << 8) | spl
        AVR_CORE_TEST_EXPECTED_REGISTER_VALUES.append(SP_val)
        ThisCycle.append(AVR_CORE_TEST_EXPECTED_REGISTER_VALUES)

        #RAM_TEST
        ram_memory = {}
        for i in range(0x100,0x8FF,1):
            Ram_val = dev.getRWMem(i)
            if Ram_val != 0:
                ram_memory[i] = Ram_val

        RAM_TEST.append(ram_memory)
        ThisCycle.append(RAM_TEST)


        #TIMER0 
        TCCR0A_val = dev.getRWMem(0x44)
        TIMER0_TEST.append(TCCR0A_val)
        TCCR0B_val = dev.getRWMem(0x45)
        TIMER0_TEST.append(TCCR0B_val)
        TCNT0_val = dev.getRWMem(0x46)
        TIMER0_TEST.append(TCNT0_val)
        OCR0A_val = dev.getRWMem(0x47)
        TIMER0_TEST.append(OCR0A_val)
        OCR0B_val = dev.getRWMem(0x48)
        TIMER0_TEST.append(OCR0B_val)
        TIMSK0_val = dev.getRWMem(0x6E)
        TIMER0_TEST.append(TIMSK0_val)
        TIFR0_val = dev.getRWMem(0x35)
        TIMER0_TEST.append(TIFR0_val)
        ThisCycle.append(TIMER0_TEST)


        #TIMER1
        TCCR1A_val = dev.getRWMem(0x80)
        TIMER1_TEST.append(TCCR1A_val)
        TCCR1B_val = dev.getRWMem(0x81)
        TIMER1_TEST.append(TCCR1B_val)
        TCCR1C_val = dev.getRWMem(0x82)
        TIMER1_TEST.append(TCCR1C_val)
        TCNT1H_val = dev.getRWMem(0x85)
        TIMER1_TEST.append(TCNT1H_val)
        TCNT1L_val = dev.getRWMem(0x84)
        TIMER1_TEST.append(TCNT1L_val)
        OCR1AH_val = dev.getRWMem(0x89)
        TIMER1_TEST.append(OCR1AH_val)
        OCR1AL_val = dev.getRWMem(0x88)
        TIMER1_TEST.append(OCR1AL_val)
        OCR1BH_val = dev.getRWMem(0x8B)
        TIMER1_TEST.append(OCR1BH_val)
        OCR1BL_val = dev.getRWMem(0x8A)
        TIMER1_TEST.append(OCR1BL_val)
        ICR1H_val = dev.getRWMem(0x87)
        TIMER1_TEST.append(ICR1H_val)
        ICR1L_val = dev.getRWMem(0x86)
        TIMER1_TEST.append(ICR1L_val)
        TIMSK1_val = dev.getRWMem(0x6F)
        TIMER1_TEST.append(TIMSK1_val)
        TIFR1_val = dev.getRWMem(0x36)
        TIMER1_TEST.append(TIFR1_val)
        GTCCR_val = dev.getRWMem(0x43)
        TIMER1_TEST.append(GTCCR_val)
        ThisCycle.append(TIMER1_TEST)


        #TIMER2 
        TCCR2A_val = dev.getRWMem(0xB0)
        TIMER2_TEST.append(TCCR2A_val)
        TCCR2B_val = dev.getRWMem(0xB1)
        TIMER2_TEST.append(TCCR2B_val)
        TCNT2_val = dev.getRWMem(0xB2)
        TIMER2_TEST.append(TCNT2_val)
        OCR2A_val = dev.getRWMem(0xB3)
        TIMER2_TEST.append(OCR2A_val)
        OCR2B_val = dev.getRWMem(0xB4)
        TIMER2_TEST.append(OCR2B_val)
        TIMSK2_val = dev.getRWMem(0x70)
        TIMER2_TEST.append(TIMSK2_val)
        TIFR2_val = dev.getRWMem(0x37)
        ASSR_val = dev.getRWMem(0xB6)
        TIMER2_TEST.append(ASSR_val)
        TIMER2_TEST.append(TIFR2_val)
        ThisCycle.append(TIMER2_TEST)

        #USART0
        UCSR0A_val = dev.getRWMem(0xC0)
        USART0_TEST.append(UCSR0A_val)
        UCSR0B_val = dev.getRWMem(0xC1)
        USART0_TEST.append(UCSR0B_val)
        UCSR0C_val = dev.getRWMem(0xC2)
        USART0_TEST.append(UCSR0C_val)
        UBRR0L_val = dev.getRWMem(0xC4)
        USART0_TEST.append(UBRR0L_val)
        UBRR0H_val = dev.getRWMem(0xC5)
        USART0_TEST.append(UBRR0H_val)
        UDR0_val = dev.getRWMem(0xC6)
        USART0_TEST.append(UDR0_val)
        ThisCycle.append(USART0_TEST)


        #SPI
        SPCR_val = dev.getRWMem(0x4C)
        SPI_TEST.append(SPCR_val)
        SPSR_val = dev.getRWMem(0x4D)
        SPI_TEST.append(SPSR_val)
        SPDR_val = dev.getRWMem(0x4E)
        SPI_TEST.append(SPDR_val)
        ThisCycle.append(SPI_TEST)


        #ADC
        ADMUX_val = dev.getRWMem(0x7C)
        ADC_TEST.append(ADMUX_val)
        ADCSRA_val = dev.getRWMem(0x7A)
        ADC_TEST.append(ADCSRA_val)
        ADCSRB_val = dev.getRWMem(0x7B)
        ADC_TEST.append(ADCSRB_val)
        ADCL_val = dev.getRWMem(0x78)
        ADC_TEST.append(ADCL_val)
        ADCH_val = dev.getRWMem(0x79)
        ADC_TEST.append(ADCH_val)
        ThisCycle.append(ADC_TEST)



        #GPIO PORTB
        PINB_val = dev.getRWMem(0x03)
        GPIO_TEST.append(PINB_val)
        DDRB_val = dev.getRWMem(0x04)
        GPIO_TEST.append(DDRB_val)
        PORTB_val = dev.getRWMem(0x05)
        GPIO_TEST.append(PORTB_val)

        #GPIO PORTC
        PINC_val = dev.getRWMem(0x06)
        GPIO_TEST.append(PINC_val)
        DDRC_val = dev.getRWMem(0x07)
        GPIO_TEST.append(DDRC_val)
        PORTC_val = dev.getRWMem(0x08)
        GPIO_TEST.append(PORTC_val)

        #GPIO PORTD
        PIND_val = dev.getRWMem(0x09)
        GPIO_TEST.append(PIND_val)
        DDRD_val = dev.getRWMem(0x0A)
        GPIO_TEST.append(DDRD_val)
        PORTD_val = dev.getRWMem(0x0B)
        GPIO_TEST.append(PORTD_val)
        ThisCycle.append(GPIO_TEST)


        #INTERRUPTS
        EIMSK_val = dev.getRWMem(0x1D)
        INTERRUPT_TEST.append(EIMSK_val)
        EIFR_val = dev.getRWMem(0x1C)
        INTERRUPT_TEST.append(EIFR_val)
        PCIFR_val = dev.getRWMem(0x1B)
        INTERRUPT_TEST.append(PCIFR_val)
        EICRA_val = dev.getRWMem(0x69)
        INTERRUPT_TEST.append(EICRA_val)
        PCICR_val = dev.getRWMem(0x68)
        INTERRUPT_TEST.append(PCICR_val)
        PCMSK0_val = dev.getRWMem(0x6B)
        INTERRUPT_TEST.append(PCMSK0_val)
        PCMSK1_val = dev.getRWMem(0x6C)
        INTERRUPT_TEST.append(PCMSK1_val)
        PCMSK2_val = dev.getRWMem(0x6D)
        INTERRUPT_TEST.append(PCMSK2_val)
        ThisCycle.append(INTERRUPT_TEST)






        FULL_SYSTEM_TEST_EXPECTED_REGISTER_VALUES.append(ThisCycle)
        p.update(t,advance=1)

with open('EXPECTED_REGISTER_VALUES_FS.txt','w+') as f:

    for items in FULL_SYSTEM_TEST_EXPECTED_REGISTER_VALUES:
        f.write('%s\n' %items)
    print("File written successfully")

f.close()

End_Time =  time.time()
print("The opperation took:",End_Time-start_time)