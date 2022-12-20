import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
import sounddevice as sd
import math
from sklearn.preprocessing import normalize

def afstand(a,b):
    return (a-b)*(a*b);

ka = 4
duration = 0.002
speed_sound = 343
afstan = 0.26
samplerat = 44100*4
vinkel_afsnit = 3600

while True:
    # save audio snipet 
    mid_vadi = np.zeros((int(duration * samplerat),vinkel_afsnit))
    recording = sd.rec(int(duration * samplerat), samplerate=samplerat, channels=4)
    sd.wait()

    # gain filter
    if (recording-recording.min()).sum() < 100:
        continue

    lis = np.zeros(vinkel_afsnit)
    # normilise and smuding
    for channel in range(ka):
        recording[:, channel] = np.interp(recording[:, channel], (recording[:, channel].min(), recording[:, channel].max()), (0, 1))
        kernel_size = 3
        kernel = np.ones(kernel_size) / kernel_size
        recording[:, channel] = np.convolve(recording[:, channel], kernel, mode='same')
    
    # find angel
    for i in range(vinkel_afsnit):
        v = i*(2*math.pi/vinkel_afsnit)
        rol = [0,0,0,0]

        for j in range(ka):
            tid = (math.sin(v+j*math.pi/2)+1)*afstan/(speed_sound)
            rol[j] = int(tid*samplerat);

        mid_spor = [0,0,0,0];
        for j in range(ka):
            mid_spor[-j] = recording[:,j].copy()
        trim_int = int(afstan*2*samplerat/(speed_sound))+1
        trim_mid_vadi = mid_spor[0][rol[0]:-(trim_int-rol[0])] +  mid_spor[1][rol[1]:-(trim_int-rol[1])] +  mid_spor[2][rol[2]:-(trim_int-rol[2])] +  mid_spor[3][rol[3]:-(trim_int-rol[3])]  
        lis[i] = trim_mid_vadi.max()
    print(lis.argmax()/10)
