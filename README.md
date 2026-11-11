# 🏭 Smart Factory Edge AIoT Triage Dashboard

A 100% offline, hardware-free Edge AI telemetry triage system built to monitor industrial sensor streams, detect threshold anomalies, and generate automated diagnostic reports using a local Large Language Model (Ollama / Phi-3).

---

## 🚀 Key Features
* **Zero API Keys & 100% Offline:** Operates entirely locally on your machine with no external cloud dependencies or paid APIs.
* **Decoupled 3-Process Architecture:** Utilizes a SQLite-backed messaging queue to decouple data ingestion, AI processing, and real-time visualization.
* **Automated AI Triage Engine:** Automatically intercepts sensor anomalies (`WARNING` states) and queries a local **Phi-3** model via Ollama to generate severity assessments, probable causes, and remediation actions.
* **Interactive Streamlit Dashboard:** Features live fleet metrics, status alerts ("Operational" vs "High Alert"), a searchable telemetry log, and continuous multi-line chronological charts powered by **Altair**.

---

## 🛠️ Tech Stack
* **Core Language:** Python
* **Database & Message Queue:** SQLite (`factory.db`)
* **Local Generative AI:** Ollama (Phi-3 Model)
* **Frontend & Visualization:** Streamlit, Pandas, Altair
* **Concurrency:** Multi-process Python worker threads

---

## 📂 Project Structure
```text
aiot_telemetry_bot/
│
├── simulator.py       # Simulates industrial IoT sensor streams & writes to SQLite
├── triage_worker.py   # Background worker that polls warnings & triggers local Phi-3 AI triage
├── app.py             # Real-time Streamlit web dashboard with Altair time-series charts
└── factory.db         # Local SQLite database acting as the edge message queue

```

---

## ⚙️ Quickstart Guide

### 1. Prerequisites

Ensure you have **Python** and **Ollama** installed on your machine.

* Pull the Phi-3 model locally via your terminal:
```bash
ollama pull phi3

```



### 2. Install Dependencies

Install the required Python packages:

```bash
python -m pip install paho-mqtt fastapi uvicorn ollama pydantic streamlit pandas altair

```

### 3. Running the System

To run the full pipeline, open **three separate terminal windows** in your project directory:

* **Window 1 (The Sensor Simulator):**
```bash
python simulator.py

```


* **Window 2 (The Local AI Triage Worker):**
```bash
python triage_worker.py

```


* **Window 3 (The Streamlit Web Dashboard):**
```bash
python -m streamlit run app.py

```



Open the local URL provided by Streamlit (usually `http://localhost:8501`) in your browser to view your live industrial dashboard!

```

---

### How to update it on GitHub:
1. Go to your repository on GitHub (`suh144/aiot_telemetry_bot`)[cite: 13].
2. Click on `README.md`[cite: 13].
3. Click the **pencil icon (Edit)** in the top right corner of the file view.
4. Paste the text above, scroll down, and click **Commit changes**. 

Your repository will instantly look polished and professional! Let me know if you want to tweak anything else.

```
