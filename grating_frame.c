#include <stdio.h>
#include <math.h>

double deg2rad(double deg){
    return deg*(M_PI/180.0);
}

double norm(int x, int y, double angle){
    return x*cos(angle) + y*sin(angle);
}

int sign(double x){
    if (x > 128) return 255;
    if (x <= 128) return 0;
}

int wave(double base, double phase){
    return round(128+128*cos(base-phase));
}


int pixel(int x, int y, double angle, int wavelength, int phase, int sq_bool){
    angle = deg2rad(angle);
    double base = norm(x,y,angle);
    int val = 0;
    if (sq_bool == 1){
        val = sign(wave(base*(2*M_PI/wavelength),phase*(2*M_PI/wavelength)));
    }else{
        val = wave(base*(2*M_PI/wavelength),phase*(2*M_PI/wavelength));
    }
    return val;
}