# 설치
# sudo pip3 install Jetson.GPIO
# sudo groupadd -f -r gpio
# sudo usermod -a -G gpio $USER
# # 재로그인 또는 재부팅

import Jetson.GPIO as GPIO
import time

TRIG = 13   # BOARD 13번 핀
ECHO = 15   # BOARD 15번 핀

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    # 10us 트리거 펄스
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    timeout = time.time() + 0.04  # 타임아웃 40ms

    # ECHO HIGH 시작 대기
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    # ECHO LOW 될 때까지 대기
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    duration = pulse_end - pulse_start
    distance = duration * 34300 / 2   # cm (음속 343m/s)
    return round(distance, 1)

try:
    print("초음파 센서 테스트 시작 (Ctrl+C 종료)")
    time.sleep(0.5)  # 센서 안정화
    while True:
        d = get_distance()
        if d is None:
            print("측정 실패 (타임아웃) - 배선 확인")
        elif d < 2 or d > 400:
            print(f"측정 범위 초과: {d} cm")
        else:
            print(f"거리: {d} cm")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n종료")
finally:
    GPIO.cleanup()
