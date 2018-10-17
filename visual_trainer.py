import pyglet
import time
import threading
import random
import grating_animation
import dill
from lickport import LickPort

class TrainingWindow(pyglet.window.Window):
    def __init__(self, sprites, res=(800, 600), fullscreen=False):
        disp = pyglet.window.Display()
        screens = disp.get_screens()
        super().__init__(res[0], res[1],
                         screen=screens[0],
                         resizable=False, vsync=True,
                         fullscreen=fullscreen, visible=True)

        # Sprites setup
        self.sprites = sprites

        # Colored frames setup
        self.white_img = pyglet.image.SolidColorImagePattern(
            color=(255, 255, 255, 255)).create_image(res[0], res[1])
        self.black_img = pyglet.image.SolidColorImagePattern(
            color=(0, 0, 0, 255)).create_image(res[0], res[1])
        self.grey_img = pyglet.image.SolidColorImagePattern(
            color=(128, 128, 128, 255)).create_image(res[0], res[1])
        self.current_img = self.grey_img

        # Lickport setup
        self.lickport = LickPort(silent=True)
        # self.lickport.set_handler('on_rising',self.white)
        # self.lickport.set_handler('on_falling',self.black)
        # self.lickport.set_handler('on_change', self.lickport.water)

        pyglet.clock.schedule(self.lickport.read)

        # To remove event handling:
        # self.lickport.remove_handler('on_rising',self.white)
        # self.lickport.remove_handler('on_falling',self.black)

        # self.lickport.push_handlers(on_rising=self.white) #Alternative
        # self.lickport.on_change = self.grey #To overrirde

    def animation(self, name):
        self.current_img = self.sprites[name]

    def white(self):
        self.current_img = self.white_img

    def black(self):
        self.current_img = self.black_img

    def grey(self):
        self.current_img = self.grey_img

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.A:
            self.white()
        if symbol == pyglet.window.key.S:
            self.black()
        if symbol == pyglet.window.key.D:
            self.grey()
        if symbol == pyglet.window.key.R:
            pass

    def on_draw(self):
        pyglet.gl.glFlush()
        self.clear()
        if isinstance(self.current_img, pyglet.image.ImageData):
            self.current_img.blit(0, 0)
        if isinstance(self.current_img, pyglet.sprite.Sprite):
            self.current_img.draw()

    def on_close(self):
        self.lickport.close()
        pyglet.app.exit()
        exit()


class GNGTraining(object):
    def __init__(self, win_res, go_stim, nogo_stim, min_delay, max_delay, grace, trial, punishment, go_count, nogo_count):
        sprites = {'go': go_stim, 'nogo': nogo_stim}
        self.nogo_stim = nogo_stim

        self.min_delay = min_delay
        self.max_delay = max_delay
        self.grace = grace
        self.trial = trial
        self.punishment = punishment

        self.punishable = False

        self.lick_log = []

        go_trials = ['go' for i in range(go_count)]
        nogo_trials = ['nogo' for i in range(nogo_count)]
        self.trials = go_trials + nogo_trials
        random.shuffle(self.trials)

        self.window = TrainingWindow(sprites, res=win_res, fullscreen=False)
        # self.window.lickport.set_handler('on_rising', lambda: print(self.lick_log))

    def start(self):
        gng_thread = threading.Thread(target=self.gng_loop)
        self.start_time = time.time()
        gng_thread.start()

    def rec_lick(self):
        lick_time = time.time()-self.start_time
        self.lick_log.append(lick_time)
        print(self.lick_log)

    def set_punishable(self):
        self.punishable = True

    def gng_loop(self):
        # self.window.lickport.set_handler('on_rising', self.rec_lick)
        @self.window.lickport.event
        def on_rising():
            self.rec_lick()

        # say_asd = lambda sym, mod: print('asd')
        # self.window.lickport.set_handler('on_rising', say_asd)
        # self.window.set_handler('on_key_press', lambda sym, mod: print('asd'))

        for trial in self.trials:
            # Delay phase
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)

            # Stim start
            if trial == 'go':
                self.window.animation('go')
            if trial == 'nogo':
                self.window.animation('nogo')

            # Grace period
            time.sleep(self.grace)

            # Set reward or punishment
            if trial == 'go':
                give_water = self.window.lickport.water
                self.window.lickport.set_handler('on_change', give_water)

                def ban_water(): return self.window.lickport.remove_handler('on_change', give_water)
                self.window.lickport.set_handler('on_water', ban_water)

            if trial == 'nogo':
                self.window.lickport.set_handler(
                    'on_change', self.set_punishable)

            # Trial period
            time.sleep(self.trial)

            # Stim stop
            self.window.grey()

            # Punishment
            if self.punishable:
                time.sleep(self.punishment)
                self.punishable = False

        print(self.lick_log)

def make_animations(width, height):
    right = grating_animation.GratingStack(width, height, 200, 45, 4)
    left = grating_animation.GratingStack(width, height, 200, 135, 4)
    right.make()
    left.make()
    with open('right.ani','wb') as right_file:
        dill.dump(right, right_file)
    with open('left.ani','wb') as left_file:
        dill.dump(left, left_file)


if __name__ == '__main__':
    width, height = 800, 600
    # make_animations(width, height)
    right = grating_animation.from_GS('right.ani')
    left = grating_animation.from_GS('left.ani')
    training = GNGTraining((width, height), right, left, 3, 5, 0.2, 3, 7, 10, 10)
    #win_res, go_stim, nogo_stim, min_delay, max_delay, grace, trial, punishment, go_count, nogo_count
    training.start()

    pyglet.app.run()

