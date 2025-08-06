import math
import numpy as np
from gpiozero.tones import Tone

class MusicNotes:

    def __init__(self, sample_rate):
        self.midi_note_start = 21
        self.midi_note_stop = 127
        self.sample_rate = sample_rate
        self.target_note_len_s = 100e-3
        self.sample_period = 1/sample_rate

    def make_base_note(self, midi_number):
        if ((midi_number >= self.midi_note_start) and
            (midi_number <= self.midi_note_stop)):
            tone = Tone(midi=midi_number)
            note = tone.note
            ideal_note_freq = tone.frequency
            ideal_note_period = 1/ideal_note_freq
            note_len = ideal_note_period * math.ceil(self.target_note_len_s / ideal_note_period)
            # note_period_rem = ideal_note_period % self.sample_period
            # note_period = ideal_note_period - note_period_rem
            # note_freq = 1/note_period
            # sample_count = math.ceil(note_period / self.sample_period)
            sample_count = round(note_len / self.sample_period)
            time_arr = np.arange(0, note_len, self.sample_period)
            return (np.sin(2 * np.pi * ideal_note_freq * time_arr) * 127).astype('int8')

    def make_tuba_note(self, midi_number):
        if ((midi_number >= self.midi_note_start) and
            (midi_number <= self.midi_note_stop)):
            tone = Tone(midi=midi_number)
            note = tone.note
            ideal_note_freq = tone.frequency
            ideal_note_period = 1/ideal_note_freq
            note_len = ideal_note_period * math.ceil(self.target_note_len_s / ideal_note_period)
            sample_count = round(note_len / self.sample_period)
            time_arr = np.arange(0, note_len, self.sample_period)
            return self.tuba_note_lookup(ideal_note_freq, time_arr)

    def tuba_note_lookup(self, freq, time_arr):
        tuba_power_dB_dict = {
            1: -30,
            2: -33,
            3: -27,
            4: -26,
            5: -35,
            6: -25,
            7: -36,
            8: -30,
            9: -33,
            10: -33,
            11: -40,
            12: -40,
            13: -46,
            14: -46,
            15: -48,
            16: -48
            }

        total_lin_power = 0
        tuba_power_lin_dict = {}
        for key, value in tuba_power_dB_dict.items():
            total_lin_power += 10**(value/20)
            tuba_power_lin_dict[key] = 10**(value/20)

        # Normalize the values
        for key, value in tuba_power_lin_dict.items():
            tuba_power_lin_dict[key] = value / total_lin_power

        # Generate the composite tone
        comp_tone = np.zeros(len(time_arr))
        for key, value in tuba_power_lin_dict.items():
            comp_tone += value * np.sin(2 * np.pi * key * freq * time_arr)

        return (127 * comp_tone).astype('int8')
    
        
        
    
