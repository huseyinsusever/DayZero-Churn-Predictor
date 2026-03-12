# 🎮 Game Player Churn Prediction: End-to-End ML Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-00a393)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E) 

## 📌 Project Overview
This project is a complete, production-ready Machine Learning Micro-SaaS designed for the mobile gaming industry. It predicts whether a newly acquired player will churn (abandon the game) or stay loyal, based solely on their **Day-0 behavior**. 

Instead of just presenting a Jupyter Notebook, this project demonstrates a full engineering lifecycle: data processing, addressing highly imbalanced datasets, exposing the model via a RESTful API, and providing an interactive web interface for product managers.

## 🏗️ Architecture & Tech Stack
The project is built on a modern AI deployment architecture:
1. **Brain (Machine Learning):** `scikit-learn` & `pandas`. A Logistic Regression model trained with `class_weight='balanced'` to capture the rare positive class (retained users) in a highly skewed mobile game dataset (99.8% churn rate).
2. **Backend Engine (REST API):** `FastAPI` & `Uvicorn`. Serves the serialized model (`.pkl`) to the web, responding to real-time JSON payloads in milliseconds.
3. **Frontend UI (Micro-SaaS):** `Streamlit`. A clean, interactive web dashboard allowing non-technical stakeholders to input user metrics and receive immediate AI predictions.

## 📂 Project Structure
```text
📦 player-churn-predictor
 ┣ 📜 api.py              # The FastAPI backend server
 ┣ 📜 app.py              # The Streamlit frontend web application
 ┣ 📜 churn_model.pkl     # The serialized Machine Learning model
 ┣ 📜 README.md           # Project documentation
