from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import sqlite3
from datetime import datetime
import time

# --- DATABASE LOGIC ---
def init_db():
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS churn_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            session_count INTEGER,
            login_days INTEGER,
            churn_prob REAL,
            process_time REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(session_count, login_days, prediction, process_time):
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO churn_logs (timestamp, session_count, login_days, churn_prob, process_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now(), session_count, login_days, float(prediction), process_time))
    conn.commit()
    conn.close()

init_db()

# --- APP BRANDING ---
app = FastAPI(
    title="Day-0 Player Churn Predictor",
    description="""
    Predicts mobile game player churn probability based on Day-0 behavior. 
    Built for high-performance gaming analytics.
    
    ### 🛠 Tech Stack:
    * **Backend**: FastAPI
    * **ML Model**: Scikit-Learn (Logistic Regression)
    * **Database**: SQLite (Real-time logging)
    """,
    version="2.0.0",
    contact={
        "name": "Hüseyin Susever",
        "url": "https://github.com/hsusever",
    }
)

# --- MODEL LOADING ---
try:
    with open('churn_model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    model = None

# --- DATA STRUCTURE ---
class PlayerData(BaseModel):
    day_0_sessions: int
    install_day_of_week: int

# --- ENDPOINT ---
@app.post("/predict")
async def predict_churn(player: PlayerData):
    start_time = time.time() # Performans ölçümü başlasın
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model file missing.")

    try:
        input_df = pd.DataFrame([{
            'day_0_sessions': player.day_0_sessions,
            'install_day_of_week': player.install_day_of_week
        }])
        
        prediction = model.predict(input_df)
        result = int(prediction[0])
        
        # Yanıt süresini hesapla
        duration = time.time() - start_time
        
        # Veritabanına hem tahmini hem de hızı kaydet
        save_prediction(player.day_0_sessions, player.install_day_of_week, result, duration)
        
        return {
            "status": "success",
            "prediction": result,
            "latency_sec": round(duration, 4),
            "message": "Player likely to CHURN" if result == 1 else "Player likely to STAY"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))py api.py