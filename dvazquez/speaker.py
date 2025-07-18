import numpy as np
import simpleaudio as sa
import os

class Speaker:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        print("Speaker initialized")

    def play_tone(self, freq_hz=440, duration_sec=1, volume=0.5):
        """Generate and play a sine wave tone."""
        t = np.linspace(0, duration_sec, int(self.sample_rate * duration_sec), False)
        wave = np.sin(2 * np.pi * freq_hz * t) * volume
        audio = (wave * 32767).astype(np.int16)  # Convert to 16-bit PCM
        play_obj = sa.play_buffer(audio, 1, 2, self.sample_rate)
        play_obj.wait_done()
        print(f"Played {freq_hz}Hz tone for {duration_sec}s")

    def play_wav(self, file_path):
        """Play a WAV file from disk."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"WAV file not found: {file_path}")
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
        print(f"Played WAV file: {file_path}")

if __name__ == "__main__":
    speaker = Speaker()

    # Play 440Hz tone for 1 second
    speaker.play_tone(freq_hz=440, duration_sec=1, volume=0.8)

    # Play a WAV file
    speaker.play_wav(".boxing_bell.wav")
