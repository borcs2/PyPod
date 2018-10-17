from pyglet.event import EventDispatcher
import threading
import time
import u3

class LickPort(EventDispatcher):
    def __init__(self, silent=False):
        super().__init__()
        self.io = u3.U3(localId=1)
        self.state = self.io.getFIOState(4)
        self.last_state = self.state
        self.running = True
        self.silent = silent

        LickPort.register_event_type('on_change')
        LickPort.register_event_type('on_rising')
        LickPort.register_event_type('on_falling')
        LickPort.register_event_type('on_water')

    def read(self, dt):
        if not self.silent and dt != 0:
            print('\r ', int(1//dt), '  ', end='\r', sep='')
        self.state = self.io.getFIOState(4)
        if self.running and self.state != self.last_state:
            self.dispatch_event('on_change')

            if self.state == 0:
                self.dispatch_event('on_falling')
            if self.state == 1:
                self.dispatch_event('on_rising')

            self.last_state = self.state

    def close(self):
        self.running = False
        self.io.close()

    def water_bcg(self):
        self.io.setFIOState(7, 0)
        self.io.setFIOState(6, 1)
        time.sleep(0.5)
        self.io.setFIOState(6, 0)
        time.sleep(1)
        self.io.setFIOState(7, 1)
        time.sleep(0.3)
        self.io.setFIOState(7, 0)

    def water(self):
        w_thread = threading.Thread(target=self.water_bcg)
        self.dispatch_event('on_water')
        w_thread.start()

    def on_change(self):
        if not self.silent:
            print('LickPort signal changed')

    def on_rising(self):
        if not self.silent:
            print('LickPort signal risen')

    def on_falling(self):
        if not self.silent:
            print('LickPort signal fallen')

    def on_water(self):
        if not self.silent:
            print('Water dropplet given')
