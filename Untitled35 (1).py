#!/usr/bin/env python
# coding: utf-8

# In[5]:


import gradio as gr
import pickle
import pandas as pd
import mysql.connector
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

# ---------- DB Connection ----------
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="cat123",
    database="byte5"
)
cursor = db.cursor()

# ---------- Star Rating Map ----------
star_map = {
    "1 ⭐": 1.0,
    "2 ⭐": 2.0,
    "3 ⭐": 3.0,
    "4 ⭐": 4.0,
    "5 ⭐": 5.0
}

# ---------- Load model ----------
with open("anomaly_model.pkl", "rb") as f:
    model = pickle.load(f)

# ---------- Label Encoder (must match model training) ----------
le = LabelEncoder()
le.classes_ = ['vendor_1', 'vendor_2', 'vendor_3']

# ---------- Prediction Function ----------
def predict_and_store(rating_str):
    try:
        rating = star_map[rating_str]
        vendor_id = 'vendor_1'  # static for now
        vendor_encoded = le.transform([vendor_id])[0]

        # Fetch latest user_id
        cursor.execute("SELECT user_id, created_at FROM users ORDER BY user_id DESC LIMIT 1")
        user_row = cursor.fetchone()
        user_id, user_created = user_row
        user_created = pd.to_datetime(user_created)
        now = pd.to_datetime(datetime.now())
        account_age = (now - user_created).days
        hour = now.hour

        # Predict
        input_df = pd.DataFrame([[rating, account_age, hour, vendor_encoded]],
                                columns=["rating", "account_age", "hour", "vendor_encoded"])
        prediction = model.predict(input_df)[0]
        label = "🔴 Anomalous" if prediction == -1 else "🟢 Normal"

        # Insert review into DB
        insert_query = """
        INSERT INTO reviews (user_id, vendor_id, rating, review_text, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, 1, rating, label, now))
        db.commit()

        # === Simulated Anomaly Detection ===
        flagged_users = {4, 5, 6, 10} if prediction == -1 else set()

        if flagged_users:
            # Simulate suspension (in real setup, update DB here)
            suspend_msg = f"⛔ Flagged Users: {flagged_users}\n⏳ Users account suspended for 24 hours"
        else:
            suspend_msg = "✅ No anomalies detected. No account suspended."

        return f"{label}\n\n{suspend_msg}"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ---------- Gradio UI ----------
interface = gr.Interface(
    fn=predict_and_store,
    inputs=gr.Radio(
        choices=list(star_map.keys()),
        label="Rating (Stars)",
        value="5 ⭐"
    ),
    outputs=gr.Textbox(label="Prediction"),
    title="Vendor Review Anomaly Detector",
    description="Select rating to detect anomaly. Data is stored and used for future learning."
)

interface.launch()


# In[ ]:




