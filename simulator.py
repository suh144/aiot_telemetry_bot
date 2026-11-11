import time
import random
import sqlite3
import json

DB_NAME = "factory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            device_id TEXT,
            temperature_celsius REAL,
            vibration_g REAL,
            status TEXT,
            processed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()
devices = ["device_alpha", "device_beta", "device_gamma"]

print("Starting Embedded Queue IoT Simulator... Press Ctrl+C to stop.")

while True:
    device = random.choice(devices)
    # Simulate normal vs spike conditions
    temp = round(random.uniform(60.0, 75.0), 2) if random.random() > 0.2 else round(random.uniform(90.0, 115.0), 2)
    vibration = round(random.uniform(0.5, 2.0), 2) if temp < 85 else round(random.uniform(6.0, 9.5), 2)
    status = "NORMAL" if temp < 85 else "WARNING"
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO telemetry (timestamp, device_id, temperature_celsius, vibration_g, status, processed)
        VALUES (?, ?, ?, ?, ?, 0)
    ''', (timestamp, device, temp, vibration, status))
    conn.commit()
    conn.close()

    print(f"[EMITTED] Device: {device} | Temp: {temp}°C | Status: {status}")
    time.sleep(3)
