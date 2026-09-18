import csv
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Ensure your Kaggle CSV is named exactly 'agriculture_data.csv'
file_path = 'agriculture_data.csv'
X, y_class, y_reg = [], [], []

# Fallback: Generates synthetic CSV matching your new 5-column format
if not os.path.exists(file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        # Updated Headers
        writer.writerow(["temperature", "humidity", "ph", "rainfall", "label"])
        for _ in range(200):
            temp = round(np.random.uniform(20.0, 40.0), 2)
            hum = round(np.random.uniform(40.0, 80.0), 2)
            ph = round(np.random.uniform(5.5, 7.5), 2)
            rain = round(np.random.uniform(50.0, 200.0), 2)
            
            # Assign a mock categorical label based on rainfall
            if rain < 80:
                label = "Dry"
            elif rain > 150:
                label = "Oversaturated"
            else:
                label = "Optimal"
                
            writer.writerow([temp, hum, ph, rain, label])

# Read data without pandas
with open(file_path, 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip headers
    for row in reader:
        # 1. Extract the 4 features for X
        temp = float(row[0])
        hum = float(row[1])
        ph = float(row[2])
        rain = float(row[3])
        label = row[4]
        
        X.append([temp, hum, ph, rain])
        
        # 2. Extract Target 1 (Classification): The text label for KNN
        y_class.append(label)
        
        # 3. Synthesize Target 2 (Regression): Water Volume for Random Forest
        # Because the Regressor needs a number, we calculate volume based on rainfall
        volume = max(0.0, (150.0 - rain) * 2.5) if label == "Dry" else 0.0
        y_reg.append(volume)

# Convert standard Python lists to NumPy arrays
X = np.array(X)
y_class = np.array(y_class)
y_reg = np.array(y_reg)

# Train the state trigger (KNN Classification)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y_class)

# Train the volume predictor (Random Forest Regression)
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y_reg)

# Export models
joblib.dump(knn, 'knn_model.pkl')
joblib.dump(rf, 'rf_model.pkl')
print("Models successfully trained and exported!")