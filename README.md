🛡️ FraudGuard — Real-Time Credit Card Fraud Detection System
A complete ML + AI-powered system for fraud monitoring, analysis, and insights.

*Overview

-FraudGuard is an end-to-end fraud detection dashboard that combines:
-Machine Learning Models (XGBoost, Autoencoders, Isolation Forest)
-Rule-Based Risk Boosting
-Generative AI Suggestions using Gemini 2.5 Flash
-Real-Time Visualization & Monitoring
-Bulk Transaction Risk Scanning
-Modern Mint–Teal UI Design
-This project is perfect for fintech applications, fraud analytics, and portfolio demonstration.

*Live Demo


*Key Features
(1) Real-Time Live Stream Fraud Detection

    Generates live transactions every second

    Detects anomalies with ML + rule boosting

    Color-coded risk levels (Low / Medium / High)

    Beautiful Plotly line chart for trending risk

(2) Manual Risk Testing

    Enter:

    Transaction Amount

    Hour (1–12 + AM/PM)

    Get:

    Risk %

    Allow/Block Decision

    Gemini-powered suggestions for unsafe cases

(3) Bulk Transaction Scanner

    Upload multiple formats:

    CSV

    Excel (XLSX)

    JSON

    Parquet

    Feather

    Outputs:

    Risk Score

    Decision

    Level

    AI Suggestions

    Downloadable results

    Live Preview

(4) AI Suggestions Using Gemini

    Uses gemini-2.5-flash for:

    Tailored fraud prevention tips

    Transaction safety recommendations

(5) Modern Fintech UI

    Custom Mint–Teal Theme:

    Gradient headings

    Glass-card style

    Clean spacing

    Responsive & elegant

*Machine Learning Models Used

    FraudGuard uses multiple ML approaches:

    ~ XGBoost Classifier
    ~ Autoencoder Reconstruction Error
    ~ Isolation Forest
    ~ Ensemble Risk Model (Top-3 weighted)
    ~ Rule Boosting based on:

    High amount

    Night-time transactions

    Behavioral deviations

    Final output:
        Risk < 30%  → LOW RISK  
        Risk 30–70% → MEDIUM RISK  
        Risk > 70%  → HIGH RISK  

*Folder Structure

FraudGuard/
│
├── app.py
├── requirements.txt
│
├── models/
│   ├── PRODUCTION_MODEL_R.pkl
│   └── scaled_features.pkl
│
├── data/
│   └── creditcard.csv (optional)
│
├── notebooks/
│   ├── EDA.ipynb
│   └── training.ipynb
│
├── output/
│   ├── PR curves, charts, analysis images
│
├── .streamlit/
│   └── secrets.toml
│
└── README.md

*Installation & Usage

(1)Install Dependencies

pip install -r requirements.txt

(2)Add Gemini API Key

Create:

.streamlit/secrets.toml

Add:

[gemini]
api_key = "YOUR_API_KEY"

(3)Run the App
streamlit run app.py