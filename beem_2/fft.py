import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# Lad os antage, at du har læst et lydspor ind i en variabel kaldet "samples"
# Samples skal være et array med lyd-amplitude-værdier

# Beregn FFT
duration = 5
samples = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
sd.wait()
fft_out = np.fft.fft(samples)

# Find de forskellige frekvenser, der udgør lydsporet
frequencies = np.fft.fftfreq(len(samples))

# Lav et plot
plt.plot(frequencies, fft_out)
plt.xlabel('Frekvens')
plt.ylabel('Amplitude')
plt.show()
