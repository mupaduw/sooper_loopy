
# mididings control script for Rough Diamonds 2020

from mididings import Scene
from mididings import SysEx

from novation_sl_mk2 import sl2_display as sl2

class SL2Scene(Scene):

    def __init__(self, name, patch, init_patch=None, exit_patch=None):
        init_patch = init_patch or []
        self.controller = self.setup_controller(name)
        for x in self.controller.update():
            init_patch.append(SysEx('SL2Out2', x))
        # print('init_patch', name) 
        super(SL2Scene, self).__init__(name, patch, init_patch, exit_patch)


    def setup_controller(self, row1_text):
        controller = sl2.Display()
        row1 = sl2.DisplayRow()
        row2 = sl2.DisplayRow()
        row1.add_cell(72, 'L', row1_text)
        for n in range(8):
            row2.add_cell(9, 'L', str(n) + ('.' * 6))
        
        # self.controls.initialise_display()

        # controller.set_display_mode(row1, row2)
        return controller

class SL2PanelScene(Scene):

    def __init__(self, name, controls, patch, init_patch=None, exit_patch=None):
        init_patch = init_patch or []

        self.controls = controls 

        scene_name = "%s (%s)" % (name, controls.name)

        self.controls.scene_name = scene_name

        self.controls.initialise_display()


        for sysex in self.controls.display.update():
            init_patch.append(SysEx('ToSL49b', sysex)) #TODO FIX this hardcoded gaff
        # print('init_patch', self.controls_name) 
        # print(init_patch)
        super(SL2PanelScene, self).__init__(scene_name, patch, init_patch, exit_patch)
