#! python3
#
# mididings control script for Kontact Only

from mididings import *
# from mididings.extra.osc import OSCInterface
# from midi_io import in_ports, out_ports, MAIN_BOARD, sl2_Port2_1

from novation_sl_mk2 import SL2Controls, DevicePanel
from sl2_scene import SL2PanelScene

in_ports = [
    ('FromSL49a', "coremidi:Port 1:.*"),
    ('FromSL49b', "coremidi:Port 2:.*"),
    ('FromKaosPro', "coremidi:PAD:.*"),
    #('FromSooperLooper', 'coremidi:sooperlooper_out:.*'),
    ]

print(in_ports)    

out_ports = [
    ('ToSL49a', "coremidi:Port 1:.*"),
    ('ToSL49b', "coremidi:Port 2:.*"),
    #out_port('KontactOut', 'virtual1'),
    ('ToKaosPro', "coremidi:SOUND:.*"),
    ('ToSooperLooper', 'coremidi:sooperlooper_in:.*'),
    #out_port('ToBitwig', 'virtual2'),
    #out_port('ToPrivia', "CASIO USB-MIDI"),
    ]

print(out_ports)
sl49_Port2_1 = OutputTemplate('ToSL49b', 1)
sooper1_out = OutputTemplate("ToSooperLooper", 1)

config(
    backend='jack',
    in_ports=in_ports,
    out_ports=out_ports,
    )

# main loop
scene_up, scene_down = 73, 72 ## with Transport ON
subscene_up, subscene_down, = 75, 74
panic = 84

scenelist= [SL2PanelScene(name="What I like about you", 
            controls=SL2Controls('Hey!', 
            sl2_out=sl49_Port2_1()), 
            patch=[]),
         SL2PanelScene(name="Black Dog", 
            controls=SL2Controls('Oooh', 
            sl2_out=sl49_Port2_1()),
            patch=[]),
        ]

# Create a sooper device control panel for the novations, 4 columns 
def new_sooper_panel(name="Sooper Looper", column_start=0, output=None):
    panel = DevicePanel(name, sl49_Port2_1(), output, 
        column_count=4, 
        row_count=4, column_start=column_start, row_start=0)  
    panel.add_row2_control("Sync", column_start+0, 23)
    panel.add_row2_control("Tempo", column_start+1, 24)
    panel.add_row4_control("Volume", column_start+0, 7) #Volume
    return panel

sooper_control = SL2Controls('Sooper Looper', sl2_out=sl49_Port2_1())
sooper_control.add_device_panel(new_sooper_panel(name='Looper1', column_start=0, output=sooper1_out()))

scenelist.append( 
    SL2PanelScene(
        name='Sooper Looper',
        controls = sooper_control,
        patch = [
            PortFilter('FromSL49b') >> Filter(CTRL) >> Process(sooper_control.execute), #Panel Controls
            PortFilter('FromSL49a') >> ~Filter(SYSRT_SENSING|PROGRAM|CTRL) >> [
                # privia(channel=5, program=syn_strings.program),
                ###. Here we need a new class to translate midi controls from FCB1010 or novation
                ### into OSC messages to sooper looper
                Print()
            ],
        ],
    ))

scenes = dict(zip([i+1 for i in range(len(scenelist))], scenelist))

run(scenes = scenes,
    control = CtrlValueFilter(1) >> 
        (CtrlFilter(scene_up) >> SceneSwitch(offset=1)) // 
        (CtrlFilter(scene_down) >> SceneSwitch(offset=-1)) //
        (CtrlFilter(subscene_up) >> SubSceneSwitch(offset=1)) // 
        (CtrlFilter(subscene_down) >> SubSceneSwitch(offset=-1)),
    # pre = ~CtrlFilter([down, up]),
)


