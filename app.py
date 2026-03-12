import streamlit as st
import requests

# --- UI CONFIGURATION ---
# Setting up the page title and layout
st.set_page_config(page_title="Player Churn Predictor", page_icon="🎮", layout="centered")

# --- HEADER SECTION ---
st.title(" 🎮 Game Player Churn Predictor")
st.markdown("Will your player stay or leave? Enter their Day-0 stats below to ask the AI.")
st.divider()

# --- INPUT FORM ---
# We create two columns for a clean, modern look
col1, col2 = st.columns(2)

with col1:
    # Dropdown for the day of the week (0=Monday, 6=Sunday)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected_day_name = st.selectbox("Install Day of Week", options=days)
    install_day = days.index(selected_day_name) # Convert name back to integer for our API

with col2:
    # Number input for how many times they played on the first day
    day_0_sessions = st.number_input("Day 0 Sessions", min_value=0, max_value=100, value=1, step=1)

st.divider()

# --- PREDICTION LOGIC ---
# This button triggers the API call
if st.button("Predict Player Future ", type="primary", use_container_width=True):
    
    # The URL of our running FastAPI server
    API_URL = "http://127.0.0.1:8000/predict"
    
    # The payload (data) we are sending to the brain
    payload = {
        "day_0_sessions": day_0_sessions,
        "install_day_of_week": install_day
    }
    
    try:
        # Send a POST request to our FastAPI backend
        with st.spinner('Asking the AI Model...'):
            response = requests.post(API_URL, json=payload)
            response_data = response.json()
        
        # Display the result with beautiful UI alerts
        if response_data["prediction"] == 1:
            st.error(f" ALERT: {response_data['message']}")
            st.toast('High risk of churn detected!', icon='⚠️')
        else:
            st.success(f" GREAT NEWS: {response_data['message']}")
            st.toast('Player is likely to be loyal.', icon='🎉')
            
    except requests.exceptions.ConnectionError:
        st.warning(" Could not connect to the API. Is your FastAPI server running on port 8000?")