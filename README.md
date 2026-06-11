# punxa_atmega328p
Python-based ATmega328P Full System Simulator.

Punxa-ATmega328P provides HDL models of different parts of a full ATmega328P system designed in different design styles using py4hw.

The single-cycle version suppports full system simulation.

## Assembly

We implemented an assembler. It supports the following features:

- Instructions and pseudo-instructions
- Labels
- Simple macros (high, low)

## Testing

We have some ISA tests with the following results.

Total: 67 Correct: 20 (29.9 %)
<pre>
29.9 %   |██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
</pre>