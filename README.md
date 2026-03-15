🎮 Mobile Game Player Churn Predictor (End-to-End MLOps)
This project is a production-ready Machine Learning API designed to predict player retention for mobile games. It doesn't just make predictions; it collects data, monitors performance, and retrains itself.

🚀 Key Features
Real-time Prediction: FastAPI backend providing instant churn probability.

Data Persistence (SQL): Every API request and prediction is logged into a SQLite database for auditing and future training.

Automated Retraining: A dedicated retrain.py pipeline that updates the model using newly collected real-world data.

Performance Monitoring: Tracks API latency (ms) for every request to ensure high-speed delivery.

Business Intelligence: Includes advanced SQL scripts for player segmentation and behavioral analysis.

🛠 Tech Stack
Language: Python 3.10+

Framework: FastAPI (Backend) & Pydantic (Validation)

Machine Learning: Scikit-Learn (Logistic Regression)

Database: SQLite (SQL Logging)

Deployment: Render & RapidAPI

📂 Project Structure
api.py: The heart of the system. Handles requests and logs data to SQL.

retrain.py: The MLOps pipeline to refresh the model with new data.

business_analysis.sql: Complex SQL queries for data-driven decision making.

churn_model.pkl: The brain (Serialized ML model).

requirements.txt: Necessary libraries for cloud deployment.

📈 Advanced Analytics (SQL)
The system includes a business_analysis.sql file designed for Product Managers to identify "High-Value Players at Risk." It uses:

Window Functions (AVG OVER PARTITION)

CTEs for clean, readable analysis.

Aggregations to track daily churn trends.

⚙️ How to Run Locally
Install dependencies:

Bash
pip install -r requirements.txt
Start the API:

Bash
uvicorn api:app --reload
Retrain the model:

Bash
python retrain.py
Author: Hüseyin Susever

Focused on Data Science & Machine Learning Engineering.
