import os
import math
import pyglet
import numpy as np
import grating_frame
import dill

class GratingStack(object):
    def __init__(self, width, height, wavelength, angle, speed):
        self.width = width
        self.height = height
        self.frames = []
        self.wavelength = wavelength
        self.angle = -angle
        self.speed = speed

    def norm(self, x, y):
        if math.pi/2 < abs(self.angle) < math.pi:  # Q2 eg 135
            x -= self.width

        if math.pi < abs(self.angle) < (3/2)*math.pi:  # Q3 eg 225 +
            x -= self.width
            y -= self.height

        if (3/2)*math.pi < abs(self.angle) < 2*math.pi:  # Q4 eg 315
            y -= self.height

        return math.cos(self.angle) * x + math.sin(self.angle) * y

    def make_frame(self, phase):
        frame = np.empty((self.height, self.width), dtype=np.uint8)
        for [y, x], _ in np.ndenumerate(frame):
            frame[y,x] = grating_frame.pixel(x,y,self.angle,self.wavelength,phase,wtype='square')
        return frame


    def make(self):
        # for I in range(150):
        #     self.frames.append(self.make_frame(I))
        #     print(I,'/150')


        phase = 0
        while phase < self.wavelength:
            self.frames.append(self.make_frame(phase))
            phase += self.speed
            print(phase,'/',self.wavelength)

        # phase = 0
        # while True:
        #     frame = self.make_frame(phase)
        #     if bool(self.frames) and np.array_equal(self.frames[0], frame):
        #         break
        #     else:
        #         self.frames.append(frame)
        #     phase += self.speed
        #     print(phase)


def make_animation_sprite(width, height, wavelength, angle, speed, batch=None):
    GS = GratingStack(width, height, wavelength, angle, speed)
    GS.make()
    images = []

    for frame in GS.frames:
        img = pyglet.image.ImageData(width, height, 'I', frame.tostring())
        aframe = pyglet.image.AnimationFrame(img, 1/60)
        images.append(aframe)

    anim = pyglet.image.Animation(images)
    sprite = pyglet.sprite.Sprite(img=anim, batch=batch)

    return sprite

def save_animation(width, height, wavelength, angle, speed, filename):
    anim = GratingStack(width, height, wavelength, angle, speed)
    anim.make()
    with open(filename,'wb') as anim_file:
        dill.dump(anim, anim_file)


def from_GS(ani_file):
    import dill
    images = []
    with open(ani_file,'rb') as gsfile:
        GS = dill.load(gsfile)
    for frame in GS.frames:
        img = pyglet.image.ImageData(GS.width, GS.height, 'I', frame.tostring())
        aframe = pyglet.image.AnimationFrame(img, 1/60)
        images.append(aframe)
        print('\rFrames loaded',len(images),end='\r')
    print()
    anim = pyglet.image.Animation(images)
    sprite = pyglet.sprite.Sprite(img=anim)

    return sprite
    
def goframe(width, height, wavelength, angle, speed):
    GS = GratingStack(width, height, wavelength, angle, speed)
    goframe = GS.make_frame(0)
    return goframe

def make_angle(angle):
    global width, height, batch
    sprite = make_animation_sprite(width//2, height//2, 200, angle, 4, batch)
    return sprite

if __name__ == '__main__':
    from multiprocessing import Pool
    width, height = 800, 600
    batch = pyglet.graphics.Batch()

    # angles = [45, 135, 225, 315]

    # P = Pool()
    # sprites = P.map(make_angle, angles)
    # P.close()
    # P.join()

    sprite_1 = make_animation_sprite(400, 300, 100, 45, 3, batch)
    sprite_1.set_position(0,0)


    window = pyglet.window.Window(width, height, fullscreen=False)
    window.set_vsync(False)
    fps_display = pyglet.window.FPSDisplay(window)

    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        fps_display.draw()

    pyglet.app.run()
