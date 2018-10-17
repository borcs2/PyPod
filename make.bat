gcc -m64 -c grating_frame.c
gcc -shared -o grating_frame.dll grating_frame.o -Wl,--out-implib,grating_frame.a