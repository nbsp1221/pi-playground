import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

TRIG = 2
ECHO = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

camera = Picamera2()
video_config = camera.create_video_configuration()
camera.configure(video_config)
encoder = H264Encoder(10000000)

try:
    while True:
        GPIO.output(TRIG, False)
        time.sleep(0.5)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        print('Distance:', distance, 'cm')

        if distance <= 10:
            print('Detected! Recording video...')
            camera.start_recording(encoder, 'video.h264')
            time.sleep(5)
            camera.stop_recording()

except KeyboardInterrupt:
    GPIO.cleanup()
