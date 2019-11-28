import noisereduce as nr
import pydub 
import numpy as np
import scipy as sp
from pydub.playback import play

# https://stackoverflow.com/questions/53633177/how-to-read-a-mp3-audio-file-into-a-numpy-array-save-a-numpy-array-to-mp3?noredirect=1&lq=1
def read(f, normalized=True):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y

def write(f, sr, x, normalized=True):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")

def main():
	print("[+] Importing audio...")
	rate, data = read('testclip.mp3')
	# rate, data = sp.io.wavfile.read("testclip.wav")
	print("[+] Length of clip array:", len(data))
	print("[+] Getting noise...")
	noise = data[0:140000]
	print("[+] Reducing noise...")
	reducedNoise = nr.reduce_noise(audio_clip=data, noise_clip=noise, verbose=True)
	
	# write('out.mp3', rate, data)

main()