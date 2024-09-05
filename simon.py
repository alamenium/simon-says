from machine import Pin, PWM
import random
import time

speaker_pin = Pin(8, Pin.OUT)
speaker_pwm = PWM(speaker_pin)
speaker_pwm.freq(1000)

notes = [440, 494, 523, 587]  # Frequencies for "a1", "b1", "c1", "d1" in Hz
lose_note = 200

button_pins = [
    Pin(3, Pin.IN, Pin.PULL_UP),
    Pin(7, Pin.IN, Pin.PULL_UP),
    Pin(11, Pin.IN, Pin.PULL_UP),
    Pin(15, Pin.IN, Pin.PULL_UP)
]

start_btn = Pin(9, Pin.IN, Pin.PULL_UP)

led_pins = [
    Pin(2, Pin.OUT),
    Pin(6, Pin.OUT),
    Pin(10, Pin.OUT),
    Pin(14, Pin.OUT)
]

led_seq = [0, 0, 0, 0]
btn_seq = [0, 0, 0, 0]
start_led = Pin(12, Pin.OUT)
length = 0

def play_tone(frequency, duration):
    speaker_pwm.freq(frequency)
    speaker_pwm.duty_u16(32768)
    time.sleep(duration)
    speaker_pwm.duty_u16(0)

while True:
    random_seq = [random.randint(0, 3) for _ in range(150)]
    start_led.value(1)
    while True:
        if start_btn.value() == 0:
            break
        else:
            continue
    start_led.value(0)
    while True:
        length += 1
        if length > len(random_seq):
            length = len(random_seq)

        for i in range(length):
            if i < 4:
                led_pins[random_seq[i]].value(1)
                led_seq[i % 4] = random_seq[i]
                play_tone(notes[random_seq[i]], 0.25)
                time.sleep(0.25)
                led_pins[random_seq[i]].value(0)
                time.sleep(0.25)

        prev_btn_values = [button_pins[0].value(),
                           button_pins[1].value(),
                           button_pins[2].value(),
                           button_pins[3].value()]

        counter = 0
        lose = False  # Initialize lose flag at the beginning of each sequence check
        while counter < length:
            for i in range(4):
                if prev_btn_values[i] != button_pins[i].value():
                    led_pins[i].value(1)
                    btn_seq[counter] = i
                    play_tone(notes[i], 0.25)
                    time.sleep(0.25)
                    led_pins[i].value(0)
                    
                    # Check if the pressed button matches the sequence
                    if led_seq[counter] != btn_seq[counter]:
                        lose = True
                        length = 0
                        break
                    
                    counter += 1
                    if counter >= length:
                        break

            if lose:
                length = 0
                break

            prev_btn_values = [button_pins[0].value(),
                               button_pins[1].value(),
                               button_pins[2].value(),
                               button_pins[3].value()]
            time.sleep(0.1)

        if lose:
            play_tone(lose_note, 0.5)
            break

