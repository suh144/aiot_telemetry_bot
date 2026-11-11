import time
import sqlite3
import json
import ollama

DB_NAME = "factory.db"

print("Starting Resilient Local AI Triage Worker... Polling for telemetry events.")

while True:
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Fetch ONE unprocessed warning at a time to prevent overloading Ollama
        cursor.execute('''
            SELECT id, timestamp, device_id, temperature_celsius, vibration_g, status
            FROM telemetry 
            WHERE status = 'WARNING' AND processed = 0
            LIMIT 1
        ''')
        row = cursor.fetchone()
        
        if row:
            record_id, timestamp, device_id, temp, vib, status = row
            
            payload = {
                "timestamp": timestamp,
                "device_id": device_id,
                "temperature_celsius": temp,
                "vibration_g": vib,
                "status": status
            }
            
            print(f"\n⚠️ [ANOMALY DETECTED] Processing triage for {device_id} at {timestamp}...")
            
            prompt = f"""
            You are an industrial IoT diagnostic engine. Analyze this anomalous sensor event briefly:
            {json.dumps(payload, indent=2)}

            Provide a concise, structured response:
            1. Severity Level (LOW, MEDIUM, CRITICAL)
            2. Probable Cause (1 sentence)
            3. Recommended Remediation Action (1 sentence)
            """
            
            try:
                response = ollama.chat(
                    model='phi3',
                    messages=[{'role': 'user', 'content': prompt}]
                )
                print("\n--- AI TRIAGE REPORT ---")
                print(response['message']['content'])
                print("------------------------\n")
            except Exception as ai_err:
                print(f"⚠️ Ollama temporary busy/timeout: {ai_err}. Retrying next cycle...")
                conn.close()
                time.sleep(3)
                continue
                
            # Mark record as processed
            cursor.execute('UPDATE telemetry SET processed = 1 WHERE id = ?', (record_id,))
            conn.commit()
            
        conn.close()
    except Exception as db_err:
        print(f"Database error: {db_err}")
        
    time.sleep(3) # Polling interval
