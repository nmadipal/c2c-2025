from music_notes import MusicNotes
import pygame as pg

from gpiozero import RGBLED, LED, ButtonBoard, Button
from matrix_led import MatrixLED, MatrixRGB
from matrix_scan import MatrixScan, MatrixScanButton
from matrix_led_pin_factory import MatrixLEDPinFactory, MatrixLEDPin, MatrixLEDBoardInfo
from matrix_scan_pin_factory import MatrixScanPinFactory, MatrixScanPin, MatrixScanBoardInfo
import time
from colorzero import Color


# Sample Rate
sr = 48000
# Audio bit width
# Positive: Unsigned
# Negative: Signed
bit_width = -16
# Channels
# 1: Mono
# 2: Stero
channels = 1
# Time to fadeout in ms
fadeout_ms = 100
# Device
device = 'Built-in Audio Stereo'

# Tuba B-flat Concert Scale
# scale_3_4
midi_Bb3 = 58
midi_C4 = 60
midi_D4 = 61
midi_Eb4 = 63
midi_F4 = 65
midi_G4 = 67
midi_A4 = 69
midi_Bb4 = 70

# scale_2_3
midi_Bb2 = 46
midi_C3 = 48
midi_D3 = 50
midi_Eb3 = 51
midi_F3 = 53
midi_G3 = 55
midi_A3 = 57
midi_Bb3 = 58

# scale_1_2
midi_Bb1 = 34
midi_C2 = 36
midi_D2 = 38
midi_Eb2 = 39
midi_F2 = 41
midi_G2 = 43
midi_A2 = 45
midi_Bb2 = 46

note_maker = MusicNotes(sr)

print('Making Bb1')
note_Bb1 = note_maker.make_tuba_note(midi_Bb1)
print('Making C2')
note_C2 = note_maker.make_tuba_note(midi_C2)
print('Making D2')
note_D2 = note_maker.make_tuba_note(midi_D2)
print('Making Eb2')
note_Eb2 = note_maker.make_tuba_note(midi_Eb2)
print('Making F2')
note_F2 = note_maker.make_tuba_note(midi_F2)
print('Making G2')
note_G2 = note_maker.make_tuba_note(midi_G2)
print('Making A2')
note_A2 = note_maker.make_tuba_note(midi_A2)
print('Making Bb2')
note_Bb2 = note_maker.make_tuba_note(midi_Bb2)

# Initializing the mixer
pg.mixer.pre_init(frequency=sr, size=bit_width, channels=channels,
                  devicename=device)
pg.mixer.init(frequency=sr, size=bit_width, channels=channels,
              devicename=device)
# Create the notes
sound_Bb1 = pg.mixer.Sound(note_Bb1)
sound_C2 = pg.mixer.Sound(note_C2)
sound_D2 = pg.mixer.Sound(note_D2)
sound_Eb2 = pg.mixer.Sound(note_Eb2)
sound_F2 = pg.mixer.Sound(note_F2)
sound_G2 = pg.mixer.Sound(note_G2)
sound_A2 = pg.mixer.Sound(note_A2)
sound_Bb2 = pg.mixer.Sound(note_Bb2)

# Build the sound list
sound_list = [sound_Bb1, sound_C2, sound_D2, sound_Eb2, sound_F2, sound_G2,
              sound_A2, sound_Bb2]

button_count = 16
# Create the button and LED factories
button_factory = MatrixScanPinFactory()
led_factory = MatrixLEDPinFactory()
# Create the button board
matrix_button_board = ButtonBoard(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16, pull_up=None, active_state=True, pin_factory=button_factory)
# Create the RGB array
rgb_leds = []
for idx in range(button_count):
    rgb_leds.append(RGBLED(f'RED {idx+1}', f'GREEN {idx+1}', f'BLUE {idx+1}', pin_factory=led_factory))

# Update the button scan parameters
scan_delay = 0.004 # 250 Hz
button_factory.matrix_scan.update_scan_delay(scan_delay)
    
# Update the RGB scan parameters
pwm_freq = 10000
display_pause = 0.0004
led_factory.matrix_led.set_pwm_freq(pwm_freq)
led_factory.matrix_led.update_display_pause(display_pause)

# Assign the Buttons and LEDs

def when_pressed(button):
    button_num = button.pin.info.number
    button_idx = button_num - 1
    rgb_leds[button_idx].color = Color('green')
    if button_num <= len(sound_list):
        sound_list[button_idx].play(-1)

def when_held(button):
    button_num = button.pin.info.number
    button_idx = button_num - 1
    rgb_leds[button_idx].color = Color('red')

def when_released(button):
    button_num = button.pin.info.number
    button_idx = button_num - 1
    rgb_leds[button_idx].color = Color('black')
    if button_num <= len(sound_list):
        sound_list[button_idx].fadeout(fadeout_ms)

for button in range(button_count):
    matrix_button_board[button].when_pressed = when_pressed
    matrix_button_board[button].when_held = when_held
    matrix_button_board[button].when_released = when_released


input('Press <ENTER> to close the test')

button_factory.close()
matrix_button_board.close()
led_factory.close()
pg.mixer.stop()
pg.mixer.quit()

