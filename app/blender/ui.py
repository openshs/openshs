#import sys
#sys.path.append('../..')

import bgui
import bgui.bge_utils
import bge
from bge import logic

class SimpleLayout(bgui.bge_utils.Layout):
    """A layout showcasing various Bgui features"""

    def __init__(self, sys, data, name):
        super().__init__(sys, data)

        self.frame = bgui.Frame(self, name=name, border=1)
        self.frame.colors = [(0.1, 0.3, 0.5, 0.5) for i in range(4)]
        self.frame.visible = False
        self.cam = logic.getCurrentScene().objects['Camera']
        self.actor = logic.getCurrentScene().objects['actor']
        self.init = logic.getCurrentScene().objects['init']


class ActivityLayout(SimpleLayout):
    def __init__(self, sys, data):
        super().__init__(sys, data, name='ActivityFrame')

        self.ok_btn = bgui.FrameButton(self.frame, text='Ok',
                size=[0.3, 0.1], pos=[0, 0.2], options=bgui.BGUI_CENTERX)

        self.cancel_btn = bgui.FrameButton(self.frame, text='Cancel',
                size=[0.3, 0.1], pos=[0, 0.1], options=bgui.BGUI_CENTERX)

        self.activity_name_input = bgui.TextInput(self.frame, prefix="Activity Name: ", text='',
                pt_size=30, size=[0.3, 0.05], options=bgui.BGUI_CENTERED)
        self.activity_name = ''

        self.activity_duration_input = bgui.TextInput(self.frame, prefix="Activity Duration: ", text='0',
                pt_size=30, pos=[0, 0.4], size=[0.3, 0.05], options=bgui.BGUI_CENTERX)
        self.activity_duration_input.visible = False
        self.activity_duration = 0

        self.ok_btn.on_click = self.ok_btn_click
        self.cancel_btn.on_click = self.cancel_btn_click

    def show(self):
        self.activity_name_input.text = logic.states['Activity']
        self.frame.visible = True
        self.cam['mmc.mouselook'] = False
        self.actor['active'] = False
        self.init['ticker_active'] = False
        logic.SensorsActive = False

    def hide(self):
        self.frame.visible = False
        self.cam['mmc.mouselook'] = True
        self.actor['active'] = True
        self.init['ticker_active'] = True
        logic.SensorsActive = True

    def toggle_duration(self):
        if not self.activity_duration_input.visible:
            self.activity_duration_input.visible = True
        else:
            self.activity_duration_input.visible = False
            self.activity_duration_input.text = '0'

    def ok_btn_click(self, widget):
        self.activity_name = self.activity_name_input.text
        self.activity_duration = int(self.activity_duration_input.text)
        logic.states['Activity'] = self.activity_name
        for i in range(self.activity_duration):
            logic.out.write(','.join([str(logic.states[i]) for i in sorted(logic.states.keys(), reverse=True)]) + '\n')
        self.activity_duration_input.visible = False
        self.activity_duration_input.text = '0'
        self.hide()

    def cancel_btn_click(self, widget):
        self.hide()

def main(cont):
    own = cont.owner
    mouse = bge.logic.mouse

    if 'sys' not in own:
        # Create our system and show the mouse
        own['sys'] = bgui.bge_utils.System()
        own['sys'].load_layout(ActivityLayout, None)
        mouse.visible = True
    else:
        # print(own['sys'].children['1'].activity_duration)
        own['sys'].run()
