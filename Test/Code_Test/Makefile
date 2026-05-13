

C: 
	avr-gcc -Wall -Os -DF_CPU=16000000UL -mmcu=atmega328p -c main.c -o main.o
	avr-gcc -mmcu=atmega328p main.o -o main.elf
	avr-objcopy -j .text -j .data -O ihex main.elf main.hex

A:
	avr-gcc -mmcu=atmega328p -o main.elf main.S 
	avr-objcopy -j .text -j .data -O ihex main.elf main.hex

clean: 
	-rm main.o 
	-rm main.hex
	-rm main.lss
	-rm main.elf

V:
	avr-gcc -mmcu=atmega328p -nostartfiles -o INSTRUCTION_TEST.elf INSTRUCTION_TEST.S
	avr-objcopy -j .text -j .data -O ihex INSTRUCTION_TEST.elf INSTRUCTION_TEST.hex

V2:
	avr-gcc -mmcu=atmega328p -nostartfiles -o INSTRUCTION_TESTV2.elf INSTRUCTION_TESTV2.S
	avr-objcopy -j .text -j .data -O ihex INSTRUCTION_TESTV2.elf INSTRUCTION_TESTV2.hex