from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the trained model
with open(r"C:\Users\pc\OneDrive\Documents\vendor\anomaly_model.pkl", "rb") as f:

    model = pickle.load(f)

# Sample encoder setup (in real app, this should match training)
le = LabelEncoder()
le.classes_ = ['vendor_1', 'vendor_2', 'vendor_3']  # replace with your actual vendors

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            rating = float(request.form["rating"])
            account_age = int(request.form["account_age"])
            hour = int(request.form["hour"])
            vendor_id = request.form["vendor_id"]

            vendor_encoded = le.transform([vendor_id])[0]
            input_df = pd.DataFrame([[rating, account_age, hour, vendor_encoded]],
                                     columns=["rating", "account_age", "hour", "vendor_encoded"])
            pred = model.predict(input_df)[0]
            prediction = "Anomalous" if pred == -1 else "Normal"
        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
