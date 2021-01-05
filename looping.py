#!looping.py 
from mididings import *
from mididings.event import CtrlEvent
from kaos_kontrol import KaosKontrol
  
in_ports = [
    ('SL49Ina', "coremidi:Port 1:.*"),
    ('SL49Inb', "coremidi:Port 2:.*"),
    ('KaosPro', "coremidi:PAD:.*"),
    ('SooperLooper', 'coremidi:sooperlooper_out:.*'),
    ]

print(in_ports)    

out_ports = [
    #out_port('SL49Out1', "Port 1"),
    #out_port('SL49Out2', "Port 2"),
    #out_port('KontactOut', 'virtual1'),
    ('ToKaosPro', "coremidi:SOUND:.*"),
    ('ToSooperLooper', 'coremidi:sooperlooper_in:.*'),
    #out_port('ToBitwig', 'virtual2'),
    #out_port('ToPrivia', "CASIO USB-MIDI"),
    ]

print(out_ports) 

config(
    backend='jack',
    in_ports=in_ports,
    out_ports=out_ports,
    )

to_kaos = OutputTemplate('ToKaosPro', 11)
to_sooper = OutputTemplate('ToSooperLooper', 1)

kaos_ctrl = KaosKontrol()

train = Scene(name="Training",
    patch = [
        PortFilter('SL49Ina') >> to_kaos() >> Process(kaos_ctrl.handle_event) >> CtrlRange(13, 0, 127, in_min=4),
        ],
    )

run(scenes = {
        1: train,
    })