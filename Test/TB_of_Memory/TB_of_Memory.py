import py4hw
from Source.Memory import *
from Source.GPIO import *


sys = py4hw.HWSystem()


Interface = MemoryInterface(sys,'port0',8,16)

Module = Memory(sys,'Memory',8,16,Interface)


#read
#read_data
#address
#write
#write_data
#be
#resp


#Interface.read_data = py4hw.Wire(sys,'read_data',1)
#Interface.resp = py4hw.Wire(sys,'resp',1)


py4hw.Sequence(sys,'read',[0,0,0,1,1,0,0,0,0],Interface.read)
#py4hw.Sequence(sys,'read_data',[0,0,0,0,0,0,0,0,1],Interface.read_data)
py4hw.Sequence(sys,'address',[0x101],Interface.address)
py4hw.Sequence(sys,'write',[1,1,0,0,0,0,0,0,0],Interface.write)
py4hw.Sequence(sys,'write_data',[0xFF],Interface.write_data)
py4hw.Sequence(sys,'instype',[1],Interface.instype)
#py4hw.Sequence(sys,'be',[1,1,0,0,0,0,0,0,0],Interface.be)
#py4hw.Sequence(sys,'resp',[0,0,0,0,0,0,0,0,1],Interface.resp)

wvf = py4hw.Waveform(sys, 'wvf', [Interface.read_data,Interface.resp,Interface.read,Interface.address,Interface.write,Interface.write_data,Interface.instype])

sys.getSimulator().clk(9)
wvf.gui()

sch = py4hw.Schematic(sys)
sch.draw()