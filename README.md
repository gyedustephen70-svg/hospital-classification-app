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
