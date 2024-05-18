import socket
import threading
import json

HOST = '0.0.0.0'
PORT = 10791

parking_data = {
    'ground_floor': {'total_spots': 8, 'occupied_spots': 0, 'vacancies': [0] * 8},
    'first_floor': {'total_spots': 8, 'occupied_spots': 0, 'vacancies': [0] * 8},
    'second_floor': {'total_spots': 8, 'occupied_spots': 0, 'vacancies': [0] * 8},
    'total_vehicles': 0,
    'total_revenue': 0.0
}

def handle_client(client_socket):
    global parking_data
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                data = json.loads(message)
                floor = data['floor']
                action = data['action']

                if action == 'entry':
                    vacancy = data['vacancy']
                    parking_data[floor]['occupied_spots'] += 1
                    parking_data[floor]['vacancies'][vacancy - 1] = 1
                    parking_data['total_vehicles'] += 1
                elif action == 'exit':
                    vacancy = data['vacancy']
                    parking_data[floor]['occupied_spots'] -= 1
                    parking_data[floor]['vacancies'][vacancy - 1] = 0
                    parking_data['total_vehicles'] -= 1
                    duration = data['duration']
                    parking_data['total_revenue'] += duration * 0.10

                print(json.dumps(parking_data, indent=2))
            else:
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Servidor central rodando em {HOST}:{PORT}")

while True:
    client_socket, addr = server.accept()
    print(f"Conexão estabelecida com {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
