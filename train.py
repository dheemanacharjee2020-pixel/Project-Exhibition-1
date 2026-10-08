import csv
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
import joblib

file_path = 'agriculture_data.csv'

# Rainfall thresholds used to derive the soil-moisture state
DRY_LIMIT = 80.0
WET_LIMIT = 150.0


def soil_state(rain):
    """Derive the soil-moisture state from rainfall."""
    if rain < DRY_LIMIT:
        return "Dry"
    elif rain > WET_LIMIT:
        return "Oversaturated"
    return "Optimal"


X, y_class, y_reg = [], [], []

# Read data without pandas (column 5, the crop name, is not used)
with open(file_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        temp, hum, ph, rain = float(row[0]), float(row[1]), float(row[2]), float(row[3])
        label = soil_state(rain)

        X.append([temp, hum, ph, rain])
        y_class.append(label)  # Target 1 (classification): soil state for KNN

        # Target 2 (regression): water volume for Random Forest
        volume = max(0.0, (WET_LIMIT - rain) * 2.5) if label == "Dry" else 0.0
        y_reg.append(volume)

X = np.array(X)
y_class = np.array(y_class)
y_reg = np.array(y_reg)

print("Samples:", len(X))
for s in ("Dry", "Optimal", "Oversaturated"):
    print(s, int((y_class == s).sum()))

# Train the state trigger (KNN classification)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y_class)

# Train the volume predictor (Random Forest regression)
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y_reg)

# Export models
joblib.dump(knn, 'knn_model.pkl')
joblib.dump(rf, 'rf_model.pkl')

print("Models successfully trained and exported!")
