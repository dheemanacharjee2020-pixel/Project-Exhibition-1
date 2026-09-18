from flask import Flask, render_template, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import random

app = Flask(__name__)
CORS(app)

# Load the trained models into memory
knn = joblib.load('knn_model.pkl')
rf = joblib.load('rf_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/telemetry', methods=['GET'])
def get_telemetry():
    # 1. Simulate the FOUR new real-time environmental data points
    sim_temp = round(random.uniform(20.0, 40.0), 2)
    sim_humidity = round(random.uniform(40.0, 80.0), 2)
    sim_ph = round(random.uniform(5.5, 7.5), 2)
    sim_rainfall = round(random.uniform(50.0, 200.0), 2)
    
    # 2. Format for Scikit-Learn prediction (Must be exactly 4 items!)
    features = np.array([[sim_temp, sim_humidity, sim_ph, sim_rainfall]])
    
    # 3. Run the AI predictions
    predicted_state = knn.predict(features)[0]
    predicted_volume = round(rf.predict(features)[0], 2)
    
    # 4. Trigger pump based on the new textual label
    pump_status = "ON" if predicted_state == "Dry" else "OFF"
    
    return jsonify({
        "temperature": sim_temp,
        "humidity": sim_humidity,
        "ph": sim_ph,
        "rainfall": sim_rainfall,
        "state": predicted_state,
        "volume_ml": predicted_volume,
        "pump": pump_status
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)