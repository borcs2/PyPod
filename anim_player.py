import grating_animation
import grating_frame
import pyglet
import time
from lj_input import LJInput
import VisStimManager
import sys
import settings

from time import sleep
from threading import Thread, Timer


class PlayerWindow(pyglet.window.Window):
    def __init__(self, animations, res=(800, 600), fullscreen=False, screen_id=1):
        disp = pyglet.window.Display()
        screens = disp.get_screens()
        self.animations = animations
        self.io = LJInput(silent=False)
        super().__init__(res[0], res[1],
                         screen=screens[screen_id-1],
                         resizable=False, vsync=True,
                         fullscreen=fullscreen, visible=True)

        # Colored frames setup
        self.white_img = pyglet.image.SolidColorImagePattern(
            color=(255, 255, 255, 255)).create_image(res[0], res[1])
        self.black_img = pyglet.image.SolidColorImagePattern(
            color=(0, 0, 0, 255)).create_image(res[0], res[1])
        self.grey_img = pyglet.image.SolidColorImagePattern(
            color=(128, 128, 128, 255)).create_image(res[0], res[1])
        self.current_img = self.grey_img

        self.io.set_handler('on_falling', self.set_anim)
        #self.io.set_handler('on_rising', self.set_paused)

        pyglet.clock.schedule(self.io.read)

    def set_anim(self, ljid):
        if ljid == 4:
            state_image = pyglet.image.load(settings.globvar[7])
            anim_thread = Thread(target=self.animation,
                                 args=(ljid-4, state_image, ))

            # self.animation(0)
        if ljid == 5:
            state_image = pyglet.image.load(settings.globvar[8])
            anim_thread = Thread(target=self.animation,
                                 args=(ljid-4, state_image, ))
            # self.animation(1)

        anim_thread.start()

    def animation(self, anim_id, state_image):
        print('Anim id', anim_id)
        self.current_img = state_image
        sleep(settings.globvar[2])
        self.current_img = self.animations[anim_id]
        sleep(settings.globvar[3])
        self.current_img = state_image
        sleep(settings.globvar[4])
        self.current_img = self.animations[anim_id]
        sleep(settings.globvar[5])
        self.current_img = state_image
        sleep(settings.globvar[6])
        self.grey()

    def white(self):
        self.current_img = self.white_img

    def black(self):
        self.current_img = self.black_img

    def grey(self):
        self.current_img = self.grey_img

    def on_draw(self):
        pyglet.gl.glFlush()
        self.clear()
        if isinstance(self.current_img, pyglet.image.ImageData):
            self.current_img.blit(0, 0)
        if isinstance(self.current_img, pyglet.sprite.Sprite):
            self.current_img.draw()

    def on_close(self):
        self.io.close()
        pyglet.app.exit()
        exit()


def make_animations(width, height):
    grating_animation.save_animation(width, height, 768, 0, 16, 'media\\Sin0.ani')
    grating_animation.save_animation(width, height, 200, 45, 4, 'media\\Sin45.ani')
    grating_animation.save_animation(width, height, 200, 90, 4, 'media\\Sin90.ani')
    grating_animation.save_animation(width, height, 200, 135, 4, 'media\\Sin135.ani')
    grating_animation.save_animation(width, height, 200, 180, 4, 'media\\Sin180.ani')
    grating_animation.save_animation(width, height, 200, 225, 4, 'media\\Sin225.ani')
    grating_animation.save_animation(width, height, 200, 270, 4, 'media\\Sin270.ani')
    grating_animation.save_animation(width, height, 200, 315, 4, 'media\\Sin315.ani')
    grating_animation.save_animation(width, height, 200, 360, 4, 'media\\Sin360.ani')


def run():
    width, height = 1366, 768
    #make_animations(width, height)
    right = grating_animation.from_GS("media\\" + settings.globvar[0])
    left = grating_animation.from_GS("media\\" + settings.globvar[1])
    WIN = PlayerWindow((right, left), (width, height),
                       fullscreen=True, screen_id=2)
    pyglet.app.run()


def closeByGui():
    exit()


if __name__ == '__main__':
    width, height = 1366, 768
    #make_animations(width, height)
    right = grating_animation.from_GS('media\\Square0.ani')
    left = grating_animation.from_GS('media\\Square180.ani')
    WIN = PlayerWindow((right, left), (width, height),
                       fullscreen=True,     screen_id=2)
    pyglet.app.run()
