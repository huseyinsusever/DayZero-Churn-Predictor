from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# api
app = FastAPI(
    title="Mobile Game Player Churn Predictor",
    description="Bu API, oyuncu istatistiklerini analiz ederek churn (oyunu bırakma) olasılığını tahmin eder.",
    version="1.0.0"
)

#  Data Schema (Type checking with Pydantic)
class PlayerData(BaseModel):
    session_length: float
    purchase_frequency: int
    drop_off_points: int 

# Home (to check if the API is working)
@app.get("/")
def home():
    return {"status": "Online", "message": "Churn Prediction API is running!"}


@app.post("/predict_churn")
async def predict(data: PlayerData):
    # NOT: Gerçek model dosyanı (.pkl) buraya bağlayacağız. 
    # Şu anlık mantıksal bir simülasyon döndürüyoruz.
    churn_prob = 85.0
    action = "Send discount voucher" if churn_prob > 50 else "Keep monitoring"
    
    return {
        "churn_probability": f"{churn_prob}%",
        "action": action,
        "input_received": data
    }

# Launch uvicorn when the file is run directly (Ease of local testing)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
