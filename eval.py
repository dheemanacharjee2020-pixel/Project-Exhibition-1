import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, mean_absolute_error,
                             mean_squared_error, r2_score)

file_path = 'agriculture_data.csv'
DRY_LIMIT = 80.0
WET_LIMIT = 150.0


def soil_state(rain):
    if rain < DRY_LIMIT:
        return "Dry"
    elif rain > WET_LIMIT:
        return "Oversaturated"
    return "Optimal"


X, y_class, y_reg = [], [], []
with open(file_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        temp, hum, ph, rain = float(row[0]), float(row[1]), float(row[2]), float(row[3])
        label = soil_state(rain)
        X.append([temp, hum, ph, rain])
        y_class.append(label)
        y_reg.append(max(0.0, (WET_LIMIT - rain) * 2.5) if label == "Dry" else 0.0)

X, y_class, y_reg = np.array(X), np.array(y_class), np.array(y_reg)
print("Total samples:", len(X))
for s in ("Dry", "Optimal", "Oversaturated"):
    print(" ", s, int((y_class == s).sum()))

# 80/20 split, fixed random state so results can be repeated
Xtr, Xte, yc_tr, yc_te, yr_tr, yr_te = train_test_split(
    X, y_class, y_reg, test_size=0.2, random_state=42)
print("Train:", len(Xtr), " Test:", len(Xte))

# KNN classifier
knn = KNeighborsClassifier(n_neighbors=3).fit(Xtr, yc_tr)
pred_c = knn.predict(Xte)
print("\n--- KNN CLASSIFIER ---")
print("Accuracy:", round(accuracy_score(yc_te, pred_c) * 100, 2), "%")
print(classification_report(yc_te, pred_c, digits=4))
print("Confusion matrix (rows = actual, columns = predicted; order: Dry, Optimal, Oversaturated)")
print(confusion_matrix(yc_te, pred_c, labels=["Dry", "Optimal", "Oversaturated"]))

# Random Forest regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42).fit(Xtr, yr_tr)
pred_r = rf.predict(Xte)
print("\n--- RANDOM FOREST REGRESSOR ---")
print("MAE :", round(mean_absolute_error(yr_te, pred_r), 4))
print("RMSE:", round(mean_squared_error(yr_te, pred_r) ** 0.5, 4))
print("R2  :", round(r2_score(yr_te, pred_r), 5))
