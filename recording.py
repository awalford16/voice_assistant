import pyaudio
import wave

chunk = 1024  # the number of audio frames per buffer
FORMAT = pyaudio.paInt16  # audio data format
CHANNELS = 1  # number of audio channels
RATE = 44100  # sampling rate in Hz
RECORD_SECONDS = 5  # duration of recording in seconds
WAVE_OUTPUT_FILENAME = "output.wav"  # name of the output file

p = pyaudio.PyAudio()  # create an instance of the PyAudio class

# create an input audio stream from the default microphone
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=chunk)

frames = []  # list to store the recorded audio frames

print("Recording...")
for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
    data = stream.read(chunk)
    frames.append(data)

print("Finished recording.")

stream.stop_stream()  # stop the input stream
stream.close()  # close the input stream
p.terminate()  # terminate the PyAudio instance

# write the recorded audio frames to a WAV file
wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()
