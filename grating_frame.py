import ctypes
import os

DIR = os.path.dirname(__file__)

grating_lib = ctypes.CDLL(DIR+'/grating_frame.dll')
grating_lib.pixel.restype = ctypes.c_int
c_pixel = grating_lib.pixel

width, height = 1366, 768

def pixel(x, y, angle, wavelength, phase, wtype='sine'):
    c_x = ctypes.c_int(x)
    c_y = ctypes.c_int(y)
    c_angle = ctypes.c_double(angle)
    c_wavelength = ctypes.c_int(wavelength)
    c_phase = ctypes.c_int(phase)
    if wtype == 'sine':
        c_sq_bool = ctypes.c_int(0)
    if wtype == 'square':
        c_sq_bool = ctypes.c_int(1)

    return c_pixel(c_x, c_y, c_angle, c_wavelength, c_phase, c_sq_bool)


if __name__ == '__main__':
    import numpy as np
    from PIL import Image

    angle = 0
    wavelength = 768
    phase = 0

    IMG_sinHoriz = np.zeros((width, height))
    IMG_sinDiag = np.zeros((width, height))
    IMG_sinVert = np.zeros((width, height))
    IMG_sinInvDiag = np.zeros((width, height))
    IMG_squareHoriz = np.zeros((width, height))
    IMG_squareDiag = np.zeros((width, height))
    IMG_squareVert = np.zeros((width, height))
    IMG_squareInvDiag = np.zeros((width, height))
    IMG_sqrtest = np.zeros((width, height))

    for x in range(width):
        for y in range(height):
            #IMG_sine[x][y] = pixel(x, y, angle, wavelength, phase, wtype='sine')
            IMG_squareVert[x][y] = pixel(x, y, 0, wavelength, phase, wtype='square')
            IMG_squareDiag[x][y] = pixel(x, y, 45, wavelength, phase, wtype='square')
            IMG_squareHoriz[x][y] = pixel(x, y, 90, wavelength, phase, wtype='square')
            IMG_squareInvDiag[x][y] = pixel(x, y, 135, wavelength, phase, wtype='square')
            #IMG_sqrtest[x][y] = pixel(x, y, 45, wavelength, phase, wtype='sine')

    #img = Image.fromarray(np.transpose(IMG_sine))
    #img.convert('RGB').save('sine.png')

    img = Image.fromarray(np.transpose(IMG_squareHoriz))
    img.convert('RGB').save('squareHorizThick.png')
    img = Image.fromarray(np.transpose(IMG_squareDiag))
    img.convert('RGB').save('squareDiagThick.png')
    img = Image.fromarray(np.transpose(IMG_squareVert))
    img.convert('RGB').save('squareVertThick.png')
    img = Image.fromarray(np.transpose(IMG_squareInvDiag))
    img.convert('RGB').save('squareInvDiagThick.png')

    #img = Image.fromarray(np.transpose(IMG_sqrtest))
    #img.convert('RGB').save('sqrtest.png')

    #img.show()
    