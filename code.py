# test_code_for_pico_workshop_components.py
import board, time, neopixel, digitalio, pwmio
from adafruit_motor import servo
from adafruit_simplemath import map_range
from audiopwmio import PWMAudioOut as AudioOut # for CPB & Pico
from audiocore import WaveFile # only needed for wav
from rainbowio import colorwheel
from analogio import AnalogIn

# set up a servo on Pico pin
pwm = pwmio.PWMOut(board.GP13, frequency=50)
# Change min_pulse / max_pulse values to calibrate servo arm in either direction.
# min ~ 500, max ~ 2500. Defaults are below & can be eliminated.
servo_1 = servo.Servo(pwm, min_pulse = 750, max_pulse = 2250)

# set angle (range can be from 0 to 180 - this is 180)
servo_1.angle = 0
time.sleep(1.0)
servo_1.angle = 180
time.sleep(1.0)

# set up the speaker
audio = AudioOut(board.GP14) # Assuming you've got tip of speaker plug wired to GP14

# setup neopixel strip
strip = neopixel.NeoPixel(board.GP15, 30, brightness=0.5)
strip.fill((0,0,0)) # fill the strip with black (0 red, 0 green, 0 blue)

# Set up potentiometer
potentiometer = AnalogIn(board.A0)

# set path where sound files can be found CHANGE if different folder name
path = "sounds/"

def cycle_rainbow():
    for i in range(256): # i will loop 256 times, with numbers from 0 through 255
        # fill the strip with a colorwheel color from 0 through 255
        strip.fill(colorwheel(i)) # will go through the rainbow

# play_sound function - pass in the FULL NAME of file to play
def play_sound(filename):
    with open(path + filename, "rb") as wave_file:
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            cycle_rainbow()

print("*** Sample code running! ***")

play_sound("wondering.wav")

while True:
    reading = potentiometer.value
    print(f"Reading: {reading}")
    color_value = map_range(reading, 0, 65535, 0, 255)
    angle = map_range(reading, 0, 65535, 0, 180)
    servo_1.angle = angle
    strip.fill(colorwheel(color_value))