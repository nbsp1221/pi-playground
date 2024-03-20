import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

TRIG = 2
ECHO = 3
LED = 4

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

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
            GPIO.output(LED, True)
        else:
            GPIO.output(LED, False)

except KeyboardInterrupt:
    GPIO.cleanup()
