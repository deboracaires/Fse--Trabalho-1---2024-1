import socket
import json
import time
import RPi.GPIO as GPIO
import random

FLOOR = 'ground_floor'
HOST = '127.0.0.1'
PORT = 10791

ENTRY_SENSOR_PIN = 18
EXIT_SENSOR_PIN = 23
ENTRY_GATE_PIN = 24
EXIT_GATE_PIN = 25
VACANCY_SENSORS = [26, 27, 28, 29, 30, 31, 32, 33]

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENTRY_SENSOR_PIN, GPIO.IN)
GPIO.setup(EXIT_SENSOR_PIN, GPIO.IN)
GPIO.setup(ENTRY_GATE_PIN, GPIO.OUT)
GPIO.setup(EXIT_GATE_PIN, GPIO.OUT)
for pin in VACANCY_SENSORS:
    GPIO.setup(pin, GPIO.IN)

def open_gate(gate_pin):
    GPIO.output(gate_pin, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(gate_pin, GPIO.LOW)

def check_vacancy():
    for index, pin in enumerate(VACANCY_SENSORS):
        if GPIO.input(pin) == GPIO.LOW:
            return index + 1
    return None

def simulate_parking():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    while True:
        command = input("Digite 'entry' para entrada ou 'exit' para saída: ").strip().lower()
        
        if command == 'entry':
            open_gate(ENTRY_GATE_PIN)
            time.sleep(5)
            
            vacancy = check_vacancy()
            if vacancy:
                entry_message = {
                    'floor': FLOOR,
                    'action': 'entry',
                    'vacancy': vacancy
                }
                client.send(json.dumps(entry_message).encode('utf-8'))
                time.sleep(10)
            else:
                print("No vacancies available")
        
        elif command == 'exit':
            duration = 10 / 60
            exit_message = {
                'floor': FLOOR,
                'action': 'exit',
                'vacancy': random.randint(1, 8),
                'duration': duration
            }
            client.send(json.dumps(exit_message).encode('utf-8'))
            open_gate(EXIT_GATE_PIN)
            time.sleep(10)

        time.sleep(1)

simulate_parking()
