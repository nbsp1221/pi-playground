import threading
import time
import adafruit_dht
import board
import RPi.GPIO as GPIO

SEGMENTS = [26, 13, 0, 11, 5, 19, 6, 9]
DIGITS = [21, 20, 16, 12]

GPIO.setmode(GPIO.BCM)
GPIO.setup(SEGMENTS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(DIGITS, GPIO.OUT, initial=GPIO.HIGH)

PATTERNS = {
    '0': [1, 1, 1, 1, 1, 1, 0],
    '1': [0, 1, 1, 0, 0, 0, 0],
    '2': [1, 1, 0, 1, 1, 0, 1],
    '3': [1, 1, 1, 1, 0, 0, 1],
    '4': [0, 1, 1, 0, 0, 1, 1],
    '5': [1, 0, 1, 1, 0, 1, 1],
    '6': [1, 0, 1, 1, 1, 1, 1],
    '7': [1, 1, 1, 0, 0, 0, 0],
    '8': [1, 1, 1, 1, 1, 1, 1],
    '9': [1, 1, 1, 1, 0, 1, 1],
    'C': [1, 0, 0, 1, 1, 1, 0], # Celsius symbol (C)
    'H': [0, 1, 1, 0, 1, 1, 1]  # Humidity symbol (H)
}

dht11_sensor = adafruit_dht.DHT11(board.D2)

def display(value):
    str_value = str(value)
    for digit in range(4):
        GPIO.output(DIGITS[digit], GPIO.LOW)
        for i in range(7):
            GPIO.output(SEGMENTS[i], PATTERNS[str_value.replace('.', '')[digit]][i])
        if digit + 1 == str_value.find('.'):
            GPIO.output(SEGMENTS[7], GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SEGMENTS[7], GPIO.LOW)
        GPIO.output(DIGITS[digit], GPIO.HIGH)

def measure():
    try:
        return dht11_sensor.temperature, dht11_sensor.humidity
    except RuntimeError as error:
        print(error.args[0])
        return None, None

formatted_temperature = '00.00'
formatted_humidity = '00.00'
stop_event = threading.Event()

def display_threading():
    iteration = 2000

    while not stop_event.is_set():
        if iteration < 1000:
            display(formatted_temperature + 'C')
        else:
            display(formatted_humidity + 'H')

        if iteration < 2000:
            iteration += 1
        else:
            iteration = 0

        time.sleep(0.001)

def measure_threading():
    global formatted_temperature
    global formatted_humidity

    while not stop_event.is_set():
        temperature, humidity = measure()

        if temperature is None:
            continue
        if humidity is None:
            continue

        formatted_temperature = f"{temperature:.1f}"
        formatted_humidity = f"{humidity:.1f}"
        print(f"Temperature: {formatted_temperature} C, Humidity: {formatted_humidity}%")

        time.sleep(2)

def main():
    display_thread = threading.Thread(target=display_threading)
    measure_thread = threading.Thread(target=measure_threading)

    display_thread.daemon = True
    measure_thread.daemon = True

    display_thread.start()
    measure_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        GPIO.cleanup()
        dht11_sensor.exit()

if __name__ == '__main__':
    main()
