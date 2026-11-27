# ===== Run this in ONE Google Colab cell =====
# It trains the heart disease model and saves model/heart_model.joblib,
# which the website (api/predict.py) needs.

import os
import joblib
import numpy
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# ---------- 1. EDIT THESE THREE LINES ----------
CSV_PATH = "heart_disease.csv"   # the exact name of your uploaded csv file
TARGET = "heart_disease"         # the column you are predicting
DROP_COLUMNS = []                # ID-like columns to ignore, e.g. ["patient_id"]
# -----------------------------------------------

df = pd.read_csv(CSV_PATH).drop(columns=DROP_COLUMNS).dropna()

# Make the target 0 / 1 (works for 0/1 or Yes/No style columns)
y = df[TARGET]
if y.dtype == "object" or y.dtype == "bool":
    y = (
        y.astype(str).str.strip().str.lower()
        .isin(["1", "yes", "y", "true", "positive", "present"])
        .astype(int)
    )
y = y.astype(int)

X = df.drop(columns=[TARGET])

# Split columns into text (categorical) and number columns
cat_cols = X.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
num_cols = [c for c in X.columns if c not in cat_cols]
X[cat_cols] = X[cat_cols].astype(str)

# Pipeline = encode categories + Random Forest, saved together
pipeline = Pipeline([
    ("prep", ColumnTransformer(
        [("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)],
        remainder="passthrough",
    )),
    ("model", RandomForestClassifier(n_estimators=200, random_state=42)),
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
pipeline.fit(X_train, y_train)

# Evaluation (copy these numbers into your report and README)
pred = pipeline.predict(X_test)
proba = pipeline.predict_proba(X_test)[:, 1]
print("Accuracy:", round(accuracy_score(y_test, pred), 4))
print("ROC-AUC :", round(roc_auc_score(y_test, proba), 4))
print(classification_report(y_test, pred))

# Describe each form field so the website can build itself
schema = []
for col in X.columns:
    label = col.replace("_", " ").title()
    if col in cat_cols:
        schema.append({
            "name": col, "label": label, "type": "categorical",
            "options": sorted(X[col].unique().tolist()),
        })
    else:
        is_int = pd.api.types.is_integer_dtype(X[col])
        schema.append({
            "name": col, "label": label, "type": "number",
            "min": float(X[col].min()) if not is_int else int(X[col].min()),
            "max": float(X[col].max()) if not is_int else int(X[col].max()),
            "step": 1 if is_int else "any",
            "default": round(float(X[col].median()), 1) if not is_int else int(X[col].median()),
        })

os.makedirs("model", exist_ok=True)
joblib.dump({"model": pipeline, "schema": schema, "target": TARGET}, "model/heart_model.joblib")
print("\nSaved model/heart_model.joblib")

# Paste these exact versions into requirements.txt on GitHub
print("\n--- requirements.txt lines ---")
print(f"scikit-learn=={sklearn.__version__}")
print(f"pandas=={pd.__version__}")
print(f"numpy=={numpy.__version__}")
print(f"joblib=={joblib.__version__}")

# Download the model to your computer
from google.colab import files
files.download("model/heart_model.joblib")
