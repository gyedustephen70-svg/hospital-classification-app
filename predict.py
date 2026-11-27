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
