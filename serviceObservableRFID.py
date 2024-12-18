import serial
import time
from datetime import datetime
# import requests
import sqlite3
import uuid

conn = sqlite3.connect('db.sqlite3')

# Certifique-se de usar a porta correta
arduino_port = 'COM5'  # Substitua pela porta correta (no Linux, /dev/ttyUSB0)
baudrate = 9600
timeout = 1

# Inicializa a conexão com o Arduino
try:
    arduino = serial.Serial(arduino_port, baudrate, timeout=timeout)
    print(f"Conectado ao Arduino na porta {arduino_port}")
    time.sleep(2)  # Aguarda para garantir que o Arduino esteja pronto
except Exception as e:
    print(f"Erro ao conectar ao Arduino: {e}")
    exit()

# Variáveis para controle de múltiplos cartões
cards = {}  # Dicionário para armazenar informações de cada cartão
removal_threshold = 2  # Tempo máximo sem leitura antes de considerar o cartão removido (em segundos)

try:
    while True:
        # Lê a linha da porta serial
        rfid_data = arduino.readline().decode('utf-8').strip()

        if rfid_data:
            now = datetime.now()  # Hora atual

            if rfid_data.startswith("UID"):
                uid = rfid_data  # Extrai o UID do cartão

                if uid not in cards:
                    # Novo cartão detectado
                    cards[uid] = {'first_read': now, 'last_read': now}
                    print(f"Cartão detectado! UID: {uid}")
                    print(f"Primeira leitura: {now.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    # Atualiza o tempo da última leitura do cartão
                    cards[uid]['last_read'] = now

        # Verifica cartões ausentes
        to_remove = []
        for uid, times in cards.items():
            if (datetime.now() - times['last_read']).total_seconds() > removal_threshold:
                # Considera o cartão removido
                print(f"Cartão removido: UID {uid}")
                print(f"Última leitura: {times['last_read'].strftime('%Y-%m-%d %H:%M:%S')}")
                
                data = {
                    "uid": uid.replace("UID da tag : ", ""),
                    "first_read": times['first_read'].strftime('%Y-%m-%d %H:%M:%S'),
                    "last_read": times['last_read'].strftime('%Y-%m-%d %H:%M:%S'),
                    "duration_seconds": (times['last_read'] - times['first_read']).total_seconds(),
                }
                        
                # url = "http://127.0.0.1:8000/api/cattle/feeding"
                # postToApp = requests.post(url, {
                #     'UID': uid,
                #     'first_read': times['first_read'].strftime('%Y-%m-%d %H:%M:%S'),
                #     'last_read': times['last_read'].strftime('%Y-%m-%d %H:%M:%S'),
                #     'duration_seconds': (times['last_read'] - times['first_read']).total_seconds(),
                # })
                
                conn.execute("INSERT INTO iot_app_rfidmetrics (id, activation_time, deactivation_time, created_at, updated_at, duration_seconds, cattle_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (uuid.uuid4().hex, data['first_read'], data['last_read'], now.strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S'), data['duration_seconds'], data['uid']))
                conn.commit()


                to_remove.append(uid)

        # Remove cartões ausentes do dicionário
        for uid in to_remove:
            del cards[uid]

except KeyboardInterrupt:
    print("Encerrando o programa...")
    arduino.close()

