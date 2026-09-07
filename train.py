import csv
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Ensure your Kaggle CSV is named exactly 'agriculture_data.csv'
file_path = 'agriculture_data.csv'
X, y_class, y_reg = [], [], []

# Fallback: Generates synthetic CSV if your Kaggle file is missing or misnamed
if not os.path.exists(file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Moisture", "Temp", "Humidity", "Status", "Volume"])
        for _ in range(200):
            m, t, h = np.random.uniform(10, 60), np.random.uniform(20, 40), np.random.uniform(30, 80)
            status = "Dry" if m < 30 else ("Oversaturated" if m > 50 else "Optimal")
            vol = max(0, (40 - m) * 10) if status == "Dry" else 0
            writer.writerow([m, t, h, status, vol])

# Read data without pandas
with open(file_path, 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip headers
    for row in reader:
        X.append([float(row[0]), float(row[1]), float(row[2])])
        y_class.append(row[3])
        y_reg.append(float(row[4]))

X = np.array(X)
y_class = np.array(y_class)
y_reg = np.array(y_reg)

# Train the state trigger and volume predictor
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y_class)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y_reg)

# Export models
joblib.dump(knn, 'knn_model.pkl')
joblib.dump(rf, 'rf_model.pkl')
print("Models successfully trained and exported!")