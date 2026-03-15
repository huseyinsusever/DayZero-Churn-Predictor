from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import sqlite3
from datetime import datetime

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
            churn_prob REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(session_count, login_days, prediction):
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO churn_logs (timestamp, session_count, login_days, churn_prob)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now(), session_count, login_days, float(prediction)))
    conn.commit()
    conn.close()

# API başladığında veritabanını hazırla
init_db()

# --- APP INITIALIZATION ---
app = FastAPI(title="Game Player Churn Prediction API", version="1.0")

# Model dosyasını yükle
try:
    with open('churn_model.pkl', 'rb') as file:
        model = pickle.load(file)
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Error: Could not find 'churn_model.pkl'.")

# --- DATA STRUCTURE ---
class PlayerData(BaseModel):
    day_0_sessions: int
    install_day_of_week: int

# --- ENDPOINTS ---
@app.post("/predict")
def predict_churn(player: PlayerData):
    # Step A: Convert JSON to DataFrame
    input_df = pd.DataFrame([{
        'day_0_sessions': player.day_0_sessions,
        'install_day_of_week': player.install_day_of_week
    }])
    
    # Step B: Get prediction (0 or 1)
    prediction = model.predict(input_df)
    result = int(prediction[0])
    
    # Step C: VERİTABANINA KAYDETME (Mülakatta şov yapacağımız yer)
    # Modelin 'predict_proba' desteği varsa olasılık skorunu, yoksa 0/1 sonucunu kaydederiz
    save_prediction(player.day_0_sessions, player.install_day_of_week, result)
    
    # Step D: Return results
    return {
        "status": "success",
        "prediction": result,
        "message": "This player is likely to CHURN (leave the game)." if result == 1 else "This player is likely to STAY."
    }