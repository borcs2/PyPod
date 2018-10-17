from pyglet.event import EventDispatcher
import threading
import time
import u3


class LJInput(EventDispatcher):
    def __init__(self, silent=False):
        super().__init__()
        self.io = u3.U3(localId=1)

        self.states = (self.io.getFIOState(4),
                       self.io.getFIOState(5),
                       self.io.getFIOState(6),
                       self.io.getFIOState(7))

        self.last_states = self.states
        self.running = True
        self.silent = silent

        LJInput.register_event_type('on_change')
        LJInput.register_event_type('on_rising')
        LJInput.register_event_type('on_falling')

    def read(self, dt):
        if not self.silent and dt != 0:
            print('\r ', int(1//dt), '  ', end='\r', sep='')
        self.states = (self.io.getFIOState(4),
                       self.io.getFIOState(5),
                       self.io.getFIOState(6),
                       self.io.getFIOState(7))
        if self.running and self.states != self.last_states:
            for state_id, state in enumerate(self.states):
                if state != self.last_states[state_id]:
                    self.dispatch_event('on_change', state_id+4)
            
                    if state == 0:
                        self.dispatch_event('on_falling', state_id+4)
                    if state == 1:
                        self.dispatch_event('on_rising', state_id+4)

            self.last_states = self.states

    def close(self):
        self.running = False
        self.io.close()

    def on_change(self, ljid):
        if not self.silent:
            print('FIO'+str(ljid)+' LickPort signal changed')

    def on_rising(self, ljid):
        if not self.silent:
            print('FIO'+str(ljid)+' LickPort signal risen')

    def on_falling(self, ljid):
        if not self.silent:
            print('FIO'+str(ljid)+' LickPort signal fallsen')

