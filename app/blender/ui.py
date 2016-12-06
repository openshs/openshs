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

        self.sleep_btn      = bgui.FrameButton(self.frame, text='sleep', size=[0.1, 0.05], pos=[0.90, 0.95])
        self.eat_btn        = bgui.FrameButton(self.frame, text='eat', size=[0.1, 0.05], pos=[0.90, 0.90])
        self.personal_btn   = bgui.FrameButton(self.frame, text='personal', size=[0.1, 0.05], pos=[0.90, 0.85])
        self.work_btn       = bgui.FrameButton(self.frame, text='work', size=[0.1, 0.05], pos=[0.90, 0.80])
        self.leisure_btn       = bgui.FrameButton(self.frame, text='leisure', size=[0.1, 0.05], pos=[0.90, 0.75])
        self.anomaly_btn    = bgui.FrameButton(self.frame, text='anomaly', size=[0.1, 0.05], pos=[0.90, 0.70])
        self.other_btn      = bgui.FrameButton(self.frame, text='other', size=[0.1, 0.05], pos=[0.90, 0.65])

        self.ok_btn = bgui.FrameButton(self.frame, text='Ok',
                size=[0.3, 0.1], pos=[0, 0.2], options=bgui.BGUI_CENTERX)

        self.cancel_btn = bgui.FrameButton(self.frame, text='Cancel',
                size=[0.3, 0.1], pos=[0, 0.1], options=bgui.BGUI_CENTERX)

        self.activity_duration_input = bgui.TextInput(self.frame, prefix="Activity Duration: ", text='0',
                pt_size=30, pos=[0, 0.4], size=[0.3, 0.05], options=bgui.BGUI_CENTERX)
        self.activity_duration_input.visible = False
        self.activity_duration = 0

        # signals
        self.ok_btn.on_click = self.ok_btn_click
        self.cancel_btn.on_click = self.cancel_btn_click
        self.sleep_btn.on_click = self.set_activity_click
        self.eat_btn.on_click = self.set_activity_click
        self.personal_btn.on_click = self.set_activity_click
        self.work_btn.on_click = self.set_activity_click
        self.leisure_btn.on_click = self.set_activity_click
        self.anomaly_btn.on_click = self.set_activity_click
        self.other_btn.on_click = self.set_activity_click

    def show(self):
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

    def set_activity_click(self, widget):
        logic.states['Activity'] = widget.text

    def ok_btn_click(self, widget):
        if self.activity_duration_input.text.isdigit():
            self.activity_duration = int(self.activity_duration_input.text)
        else:
            self.activity_duration = int(self.activity_duration_input.text[:-1]) * 60

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
        own['sys'].run()
