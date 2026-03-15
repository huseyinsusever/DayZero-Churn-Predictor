import sqlite3
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from datetime import datetime

def retrain_model():
    print(f"[{datetime.now()}] Retraining process started...")

    # 1. Veritabanından (SQLite) yeni verileri çek
    try:
        conn = sqlite3.connect('predictions.db')
        # Sadece churn_prob (tahmin) olan değil, gerçek sonuçların (labels) 
        # olduğu bir tablo üzerinden eğitmek idealdir. 
        # Şimdilik mevcut verilerle mantığı kuralım:
        query = "SELECT session_count, login_days, churn_prob FROM churn_logs"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if len(df) < 10: # Çok az veri varsa eğitme
            print("Not enough new data to retrain. Need at least 10 samples.")
            return
            
        print(f"Retraining with {len(df)} new samples...")

        # 2. Veriyi Hazırla (X ve y)
        # Not: Gerçek bir senaryoda 'churn_prob' yerine oyuncunun 
        # gerçekten gidip gitmediğini gösteren 'actual_churn' kolonu kullanılır.
        X = df[['session_count', 'login_days']]
        # Basitlik olması için 0.5 üstünü 1 (Churn) kabul edelim
        y = (df['churn_prob'] > 0.5).astype(int)

        # 3. Modeli Yeniden Eğit
        new_model = LogisticRegression()
        new_model.fit(X, y)

        # 4. Eski modelin üzerine yaz (Update)
        with open('churn_model.pkl', 'wb') as file:
            pickle.dump(new_model, file)

        print(f"[{datetime.now()}] Success! 'churn_model.pkl' has been updated with new data.")

    except Exception as e:
        print(f"Error during retraining: {e}")

if __name__ == "__main__":
    retrain_model()