import os
import pyaudio
import wave
from threading import Event


class Audio:
    def __init__(self):
        self.chunk = 1024
        self.audioGate = Event()
        self.audioGate.set()
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 16000  # Record at 16000 samples per second
        self.input = None
        self.stream = None
        self.data = None
        self.wf = None
        self.p = None

    def load(self, filename, output=True):
        self.input = not output
        self.p = None
        self.wf = None
        self.stream = None

        try:
            self.audioGate.wait()  # Blocks until the following is done (event is re-set)
            self.audioGate.clear()
            self.p = pyaudio.PyAudio()
            if self.input:
                self.audioGate.set()
            else:
                self.wf = wave.open(filename, 'rb')
            self.stream = self.p.open(format=self.sample_format,
                                      channels=self.channels,
                                      rate=self.fs,
                                      output=output,
                                      input=self.input)
            if output:
                # Read data in chunks
                self.data = self.wf.readframes(self.chunk)

        except AttributeError:
            pass  # Program probably closed while playing audio

        except Exception as err:
            filename = os.path.basename(filename)
            print('Unable to load "{}" sound.'.format(filename))
            print(err)

    def play(self, filename):
        self.load(filename)
        while len(self.data) > 0:
            self.stream.write(self.data)
            self.data = self.wf.readframes(self.chunk)

        # Close and terminate the stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        # Close PyAudio
        if self.p:
            self.p.terminate()

        # Close the wav file
        if self.wf:
            self.wf.close()

    def record(self, filename, duration):
        self.load(filename, output=False)
        assert self.stream, f'could not load audio file {filename}'
        frames = []  # Initialize array to store frames
        for i in range(0, int(self.fs / self.chunk * duration)):
            self.data = self.stream.read(self.chunk)
            frames.append(self.data)

        # Save the recorded data as a WAV file
        self.wf = wave.open(filename, 'wb')
        self.wf.setnchannels(self.channels)
        self.wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        self.wf.setframerate(self.fs)
        self.wf.writeframes(b''.join(frames))

        # Stop and close the stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        # Close PyAudio
        if self.p:
            self.p.terminate()

        # Close the wav file
        if self.wf:
            self.wf.close()

        print('Finished recording')
