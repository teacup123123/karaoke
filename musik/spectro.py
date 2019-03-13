## imports
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
from scipy import signal

## load data
rate, data = wav.read('exports/基準 in A.wav')

left = data[:, 0]
right = data[:, 1]

## detection
A4 = 440
# lowest = B3 (-10)
# highest = D6 (24+5)

probe = np.arange(-10, 30, 0.25)
frequencies = 2 ** (probe / 12) * A4
dfs = frequencies * (2 ** (1 / 48) - 1)
freqsNormed=dfs/rate
samplenums = np.round(2/freqsNormed) # window should be - this number ~ 0

cumsums=np.zeros((np.size(probe),),dtype=int)

window = 0.25  # s
windowSamples = int(window * rate)
