scikit-learn==1.6.1
pandas==2.2.2
numpy==2.0.2
joblib==1.4.2

// ===== Hospital Heart Disease Prediction: front-end logic =====
// 1. Asks the API (GET) which fields the model needs and builds the form.
// 2. Sends the filled-in form to the API (POST) and shows the result.

const API_URL = "/api/predict";

const statusBox = document.getElementById("status");
const form = document.getElementById("predict-form");
const fieldsBox = document.getElementById("fields");
const submitBtn = document.getElementById("submit-btn");
const resultCard = document.getElementById("result");
const resultIcon = document.getElementById("result-icon");
const resultLabel = document.getElementById("result-label");
const resultProb = document.getElementById("result-prob");
const barFill = document.getElementById("bar-fill");

// ---------- Step 1: build the form from the model's schema ----------
async function loadForm() {
  try {
    const response = await fetch(API_URL);
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Server error");
    }
    buildFields(data.features);
    statusBox.hidden = true;
    form.hidden = false;
  } catch (error) {
    showStatus("Could not load the form. " + error.message, true);
  }
}

function buildFields(features) {
  fieldsBox.innerHTML = "";

  features.forEach((feature) => {
    const wrapper = document.createElement("div");
    wrapper.className = "field";

    const label = document.createElement("label");
    label.htmlFor = "f-" + feature.name;
    label.textContent = feature.label;
    wrapper.appendChild(label);

    let input;

    if (feature.type === "categorical") {
      input = document.createElement("select");
      const placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = "Select…";
      input.appendChild(placeholder);

      feature.options.forEach((option) => {
        const opt = document.createElement("option");
        opt.value = option;
        opt.textContent = option;
        input.appendChild(opt);
      });
    } else {
      input = document.createElement("input");
      input.type = "number";
      input.step = feature.step;
      input.value = feature.default;
      input.inputMode = "decimal";

      const hint = document.createElement("span");
      hint.className = "hint";
      hint.textContent = "Typical range: " + feature.min + " to " + feature.max;
      wrapper.appendChild(input);
      wrapper.appendChild(hint);
    }

    input.id = "f-" + feature.name;
    input.name = feature.name;
    input.required = true;

    if (feature.type === "categorical") {
      wrapper.appendChild(input);
    }

    fieldsBox.appendChild(wrapper);
  });
}

// ---------- Step 2: send the values and show the answer ----------
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  const inputs = {};
  new FormData(form).forEach((value, key) => {
    inputs[key] = value;
  });

  submitBtn.disabled = true;
  submitBtn.textContent = "Predicting…";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ inputs }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Prediction failed");
    }
    showResult(data);
  } catch (error) {
    resultCard.hidden = true;
    showStatus("Prediction failed. " + error.message, true);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Predict";
  }
});

form.addEventListener("reset", () => {
  resultCard.hidden = true;
  statusBox.hidden = true;
});

function showResult(data) {
  statusBox.hidden = true;

  const positive = data.prediction === 1;
  const percent = Math.round(data.probability * 1000) / 10;

  resultCard.hidden = false;
  resultCard.classList.toggle("positive", positive);
  resultCard.classList.toggle("negative", !positive);
  resultIcon.textContent = positive ? "!" : "✓";
  resultLabel.textContent = data.label;
  resultProb.textContent = "Probability of heart disease: " + percent + "%";

  // Restart the bar animation from zero
  barFill.style.width = "0%";
  requestAnimationFrame(() => {
    barFill.style.width = percent + "%";
  });

  resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function showStatus(message, isError) {
  statusBox.textContent = message;
  statusBox.classList.toggle("error", Boolean(isError));
  statusBox.hidden = false;
}

loadForm();

/* ===== Hospital theme: clean white, medical teal and blue ===== */
:root {
  --primary: #0b6e99;
  --primary-dark: #084f70;
  --accent: #14a3a3;
  --bg: #f2f7fa;
  --card: #ffffff;
  --text: #1c2b36;
  --muted: #5b6b78;
  --border: #d8e3ea;
  --danger: #c0392b;
  --danger-bg: #fdecea;
  --success: #1e8a5a;
  --success-bg: #e6f6ee;
  --radius: 12px;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: "Segoe UI", system-ui, -apple-system, Roboto, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.5;
}

.container {
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
  padding: 0 20px;
}

/* ===== Header ===== */
.site-header {
  background: linear-gradient(90deg, var(--primary-dark), var(--primary));
  color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  padding-bottom: 14px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.25rem;
  font-weight: 700;
}

.brand small {
  display: block;
  font-size: 0.72rem;
  font-weight: 400;
  opacity: 0.85;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.brand-icon {
  width: 36px;
  height: 36px;
  padding: 6px;
  border-radius: 8px;
  background: #fff;
  color: var(--primary);
}

.badge {
  font-size: 0.8rem;
  padding: 5px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.35);
}

/* ===== Hero ===== */
.hero {
  padding: 36px 0 18px;
}

.hero h1 {
  margin: 0 0 8px;
  font-size: 2rem;
  color: var(--primary-dark);
}

.hero p {
  margin: 0;
  max-width: 640px;
  color: var(--muted);
}

/* ===== Cards ===== */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-top: 4px solid var(--accent);
  border-radius: var(--radius);
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 14px rgba(11, 110, 153, 0.08);
}

.card h2 {
  margin: 0 0 18px;
  font-size: 1.2rem;
  color: var(--primary-dark);
}

/* ===== Form ===== */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 18px 20px;
}

.field label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.9rem;
  font-weight: 600;
}

.field input,
.field select {
  width: 100%;
  padding: 10px 12px;
  font-size: 1rem;
  color: var(--text);
  background: #fbfdfe;
  border: 1px solid var(--border);
  border-radius: 8px;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.field input:focus,
.field select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(11, 110, 153, 0.18);
}

.field input:user-invalid,
.field select:user-invalid {
  border-color: var(--danger);
}

.hint {
  display: block;
  margin-top: 4px;
  font-size: 0.75rem;
  color: var(--muted);
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 26px;
  flex-wrap: wrap;
}

.btn {
  padding: 11px 26px;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s, transform 0.05s;
}

.btn:active { transform: translateY(1px); }

.btn-primary {
  background: var(--primary);
  color: #fff;
}

.btn-primary:hover { background: var(--primary-dark); }

.btn-primary:disabled {
  background: #8fb7c9;
  cursor: not-allowed;
}

.btn-secondary {
  background: #eaf1f5;
  color: var(--primary-dark);
  border: 1px solid var(--border);
}

.btn-secondary:hover { background: #dce8ef; }

/* ===== Status message ===== */
.status {
  padding: 12px 14px;
  border-radius: 8px;
  background: #eaf4f9;
  color: var(--primary-dark);
}

.status.error {
  background: var(--danger-bg);
  color: var(--danger);
}

.status[hidden] { display: none; }

/* ===== Result ===== */
.result-head {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 18px;
}

.result-icon {
  flex: none;
  width: 56px;
  height: 56px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
}

.result-label {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
}

.result-prob {
  margin: 2px 0 0;
  color: var(--muted);
}

.result.positive { border-top-color: var(--danger); }
.result.positive .result-icon { background: var(--danger); }
.result.positive .result-label { color: var(--danger); }
.result.positive .bar-fill { background: var(--danger); }

.result.negative { border-top-color: var(--success); }
.result.negative .result-icon { background: var(--success); }
.result.negative .result-label { color: var(--success); }
.result.negative .bar-fill { background: var(--success); }

.bar {
  height: 14px;
  border-radius: 999px;
  background: #e5edf2;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  width: 0;
  border-radius: 999px;
  transition: width 0.6s ease;
}

.bar-caption {
  margin: 8px 0 0;
  font-size: 0.8rem;
  color: var(--muted);
}

/* ===== Footer ===== */
.site-footer {
  margin-top: 10px;
  padding: 22px 0;
  background: #e4edf2;
  color: var(--muted);
  font-size: 0.85rem;
}

.site-footer p { margin: 0; }

/* ===== Small screens ===== */
@media (max-width: 600px) {
  .hero h1 { font-size: 1.6rem; }
  .badge { display: none; }
  .card { padding: 18px; }
}

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

{
  "functions": {
    "api/predict.py": {
      "includeFiles": "model/**",
      "maxDuration": 30
    }
  }
}

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hospital Heart Disease Prediction</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <header class="site-header">
    <div class="container header-inner">
      <div class="brand">
        <svg class="brand-icon" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M10 3h4v7h7v4h-7v7h-4v-7H3v-4h7z" fill="currentColor"/>
        </svg>
        <span>CardioCare <small>Hospital Diagnostics</small></span>
      </div>
      <span class="badge">AI Screening Tool</span>
    </div>
  </header>

  <main class="container">

    <section class="hero">
      <h1>Heart Disease Risk Prediction</h1>
      <p>Enter the patient details below. The trained machine learning model will estimate whether heart disease is likely.</p>
    </section>

    <section class="card">
      <h2>Patient Information</h2>
      <div id="status" class="status" role="status">Loading form…</div>

      <form id="predict-form" novalidate hidden>
        <div id="fields" class="grid"></div>
        <div class="actions">
          <button type="submit" id="submit-btn" class="btn btn-primary">Predict</button>
          <button type="reset" id="reset-btn" class="btn btn-secondary">Clear</button>
        </div>
      </form>
    </section>

    <section id="result" class="card result" hidden aria-live="polite">
      <h2>Prediction Result</h2>
      <div class="result-head">
        <div id="result-icon" class="result-icon"></div>
        <div>
          <p id="result-label" class="result-label"></p>
          <p id="result-prob" class="result-prob"></p>
        </div>
      </div>
      <div class="bar"><div id="bar-fill" class="bar-fill"></div></div>
      <p class="bar-caption">Model estimated probability of heart disease</p>
    </section>

  </main>

  <footer class="site-footer">
    <div class="container">
      <p><strong>Disclaimer:</strong> This tool is a student machine learning project for learning purposes only. It is not a medical device and must not replace advice from a qualified doctor.</p>
    </div>
  </footer>

  <script src="script.js"></script>
</body>
</html>

"""Vercel serverless function that connects the website to the trained model.

GET  /api/predict  -> returns the list of form fields the model needs
POST /api/predict  -> returns the prediction for the values sent by the form
"""

from http.server import BaseHTTPRequestHandler
import json
import os

import joblib
import pandas as pd

# model/heart_model.joblib sits one folder above this api/ folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "heart_model.joblib")

_artifact = None  # the model is loaded once and reused


def get_artifact():
    global _artifact
    if _artifact is None:
        _artifact = joblib.load(MODEL_PATH)
    return _artifact


class handler(BaseHTTPRequestHandler):
    # ---------- helpers ----------
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ---------- GET: tell the website which fields to show ----------
    def do_GET(self):
        try:
            artifact = get_artifact()
            self._send_json(200, {
                "features": artifact["schema"],
                "target": artifact["target"],
            })
        except Exception as error:
            self._send_json(500, {"error": f"Could not load the model: {error}"})

    # ---------- POST: make a prediction ----------
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            inputs = payload.get("inputs", {})

            artifact = get_artifact()
            schema = artifact["schema"]

            row = {}
            missing = []
            for feature in schema:
                value = inputs.get(feature["name"])
                if value is None or value == "":
                    missing.append(feature["label"])
                    continue
                if feature["type"] == "number":
                    row[feature["name"]] = float(value)
                else:
                    row[feature["name"]] = str(value)

            if missing:
                self._send_json(400, {"error": "Missing values: " + ", ".join(missing)})
                return

            frame = pd.DataFrame([row], columns=[f["name"] for f in schema])
            model = artifact["model"]

            prediction = int(model.predict(frame)[0])
            positive_index = list(model.classes_).index(1)
            probability = float(model.predict_proba(frame)[0][positive_index])

            label = "Heart disease likely" if prediction == 1 else "No heart disease detected"
            self._send_json(200, {
                "prediction": prediction,
                "label": label,
                "probability": probability,
            })

        except ValueError as error:
            self._send_json(400, {"error": f"Invalid input: {error}"})
        except Exception as error:
            self._send_json(500, {"error": f"Prediction error: {error}"})

# Hospital Heart Disease Classification App

A machine learning web application that predicts whether a patient is likely to have heart disease, based on clinical information entered into a web form.

**Live app:** _add your Vercel link here_
**GitHub repository:** https://github.com/gyedustephen70-svg/hospital-classification-app

> **Disclaimer:** This is a student project for learning purposes. It is not a medical device and must not replace advice from a qualified doctor.

## How it works

1. A classification model (Random Forest, built with Scikit-Learn) is trained on a heart disease dataset of 500 patient records. The target column is `heart_disease`.
2. Categorical columns are encoded with one-hot encoding inside a Scikit-Learn `Pipeline`, so the model accepts raw form values.
3. The trained pipeline is saved as `model/heart_model.joblib`.
4. The website (`index.html`, `style.css`, `script.js`) builds a form from the model's field list and sends the values to `api/predict.py`.
5. The Python API loads the model, predicts, and returns the result (heart disease likely or not, plus a probability) to the page.

## Project structure

```
hospital-classification-app/
├── index.html          # Web page
├── style.css           # Hospital-style design
├── script.js           # Interactive prediction form
├── api/
│   └── predict.py      # Serverless API connecting the site to the model
├── model/
│   └── heart_model.joblib   # Trained model (created in Google Colab)
├── requirements.txt    # Python libraries
├── vercel.json         # Vercel deployment configuration
└── README.md           # Documentation
```

## Technologies used

- Python, Scikit-Learn, Pandas, NumPy, Joblib
- HTML, CSS, JavaScript
- Google Colab (model training)
- GitHub (code hosting) and Vercel (deployment)

## Model evaluation

Add your results here after training in Colab:

| Metric | Score |
|--------|-------|
| Accuracy | |
| Precision | |
| Recall | |
| F1-score | |
| ROC-AUC | |

## Run it yourself

1. Train the model in Google Colab and download `heart_model.joblib`.
2. Put it inside the `model/` folder.
3. Install the libraries: `pip install -r requirements.txt`
4. Deploy to Vercel (import this repository), or test locally with the Vercel CLI: `vercel dev`

## API

- `GET /api/predict` returns the form fields the model expects.
- `POST /api/predict` accepts `{"inputs": {"field": "value", ...}}` and returns `{"prediction": 0 or 1, "label": "...", "probability": 0.0-1.0}`.

## Author

[@gyedustephen70-svg](https://github.com/gyedustephen70-svg) (add your full name and index number here)
