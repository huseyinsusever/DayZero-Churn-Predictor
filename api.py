from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle

# 1. Initialize the FastAPI application
app = FastAPI(title="Game Player Churn Prediction API", version="1.0")

# 2. Load the trained brain (model) into memory
# Make sure 'churn_model.pkl' is in the same folder as this api.py file
try:
    with open('churn_model.pkl', 'rb') as file:
        model = pickle.load(file)
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Error: Could not find 'churn_model.pkl'.")

# 3. Define the structure of the incoming data (JSON payload)
# This acts as a strict rulebook: Users must send these exact two clues
class PlayerData(BaseModel):
    day_0_sessions: int
    install_day_of_week: int

# 4. Create the prediction endpoint
# When someone sends data to "/predict", this function wakes up
@app.post("/predict")
def predict_churn(player: PlayerData):
    
    # Step A: Convert the incoming JSON into a pandas DataFrame format that our model understands
    input_df = pd.DataFrame([{
        'day_0_sessions': player.day_0_sessions,
        'install_day_of_week': player.install_day_of_week
    }])
    
    # Step B: Ask the model to make a prediction
    prediction = model.predict(input_df)
    
    # Step C: Return the result cleanly to the user
    # 1 means Churn (Will leave), 0 means Retained (Will stay)
    result = int(prediction[0])
    
    return {
        "status": "success",
        "prediction": result,
        "message": "This player is likely to CHURN (leave the game)." if result == 1 else "This player is likely to STAY."
    }