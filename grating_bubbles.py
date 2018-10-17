import pyglet 
import math
import numpy as np
import dill
import matplotlib
 


class BubblesStack(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.radius = np.random.randint(3, 15)
        self.x_pos = np.random.randint(1, 1366)
        self.y_pos = np.random.randint(1, 768)
        self.frames = []

    def make_frame(self, phase):
        frame = np.empty((self.height, self.width), dtype=np.uint8)
        for [y_pos, x_pos], _ in np.ndenumerate(frame):
            frame[y_pos,x_pos] = (pow(y_pos, 2)-phase + pow(x_pos, 2))-phase
        return frame

    def make(self):
        phase = 0
        while phase < 100:
            self.frames.append(self.make_frame(phase))
            phase += 3
            print(phase, '/', 100)

    def make_animation_sprite(width, height, batch = None):
        BS = BubblesStack(width, height)
        BS.make()
        images = []

        for frame in BS.frames:
            img = pyglet.image.ImageData(width, height, 'I', frame.tostring())
            aframe = pyglet.image.AnimationFrame(img, 1/60)
            images.append(aframe)

        anim = pyglet.image.Animation(images)
        sprite = pyglet.sprite.Sprite(img = anim, batch = batch)

        return sprite
    
    def save_animation(width, height, filename):
        anim = BubblesStack(width, height)
        anim.make()
        with open(filename, 'wb') as anim_file:
            dill.dump(anim, anim_file)

    def from_BS(ani_file):
        images = []
        with open(ani_file, 'rb') as bsfile:
            BS = dill.load(bsfile)
        for frame in BS.frames:
            img = pyglet.image.ImageData(BS.width, BS.height, 'I', frame.tostring())
            aframe = pyglet.image.AnimationFrame(img, 1/60)
            images.append(aframe)
            print('\rFrames loaded', len(images), end='\r')
        print()
        anim = pyglet.image.Animation(images)
        sprite = pyglet.sprite.Sprite(img=anim)

        return sprite

if __name__ == '__main__':
    from multiprocessing import Pool
    width, height = 800, 600
    batch = pyglet.graphics.Batch()

    sprite_1 = BubblesStack.make_animation_sprite(400, 300, batch)
    sprite_1.set_position(0,0)

    window = pyglet.window.Window(width, height, fullscreen = False)
    window.set_vsync(False)
    fps_display = pyglet.window.FPSDisplay(window)

    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        fps_display.draw()

    pyglet.app.run()