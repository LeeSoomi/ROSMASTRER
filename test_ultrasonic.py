# 실행 
# cd ~/yahboomcar_ros2_ws/yahboomcar_ws/src/auto_drive/test
# python3 test_ultrasonic.py

# 권한 오류나오면
# sudo python3 test_ultrasonic.py


#!/usr/bin/env python3

import time
import gpiod

CHIP_NAME = "gpiochip0"

TRIG_LINE = 142
ECHO_LINE = 143

chip = gpiod.Chip(CHIP_NAME)

trig = chip.get_line(TRIG_LINE)
echo = chip.get_line(ECHO_LINE)

trig.request(consumer="hcsr04_trig", type=gpiod.LINE_REQ_DIR_OUT)
echo.request(consumer="hcsr04_echo", type=gpiod.LINE_REQ_DIR_IN)

trig.set_value(0)
time.sleep(0.5)

print("HC-SR04 gpiod Test Start")
print("TRIG: gpiochip0 line 142")
print("ECHO: gpiochip0 line 143")

try:
    while True:
        trig.set_value(0)
        time.sleep(0.000002)

        trig.set_value(1)
        time.sleep(0.00001)
        trig.set_value(0)

        timeout_start = time.time()

        while echo.get_value() == 0:
            pulse_start = time.time()
            if pulse_start - timeout_start > 0.03:
                print("Timeout waiting for echo start")
                pulse_start = None
                break

        if pulse_start is None:
            time.sleep(0.1)
            continue

        timeout_start = time.time()

        while echo.get_value() == 1:
            pulse_end = time.time()
            if pulse_end - timeout_start > 0.03:
                print("Timeout waiting for echo end")
                pulse_end = None
                break

        if pulse_end is None:
            time.sleep(0.1)
            continue

        duration = pulse_end - pulse_start
        distance_cm = duration * 17150

        if 2 <= distance_cm <= 400:
            print(f"Distance: {distance_cm:.1f} cm")
        else:
            print(f"Out of range: {distance_cm:.1f} cm")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExit")

finally:
    trig.set_value(0)
    trig.release()
    echo.release()
    chip.close()
