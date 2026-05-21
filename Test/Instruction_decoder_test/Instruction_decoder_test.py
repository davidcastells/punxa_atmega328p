# source cpu_env/bin/activate

import datetime
import py4hw
from punxa_atmega328p.Instruction_Decoder import ins_to_str

list = []
f = open("output.txt", "a")
x = datetime.datetime.now()
f.write("Test conducted on {time} \n".format(time = x))
for ins in range(2**16):
    with open("output.txt", "a") as f:
        f.write("Ins {0:>016b} is {instruction}\n".format(ins,instruction = ins_to_str(ins)))
    if ins_to_str(ins) not in list:
        list.append(ins_to_str(ins))
print(list)
print(len(list))