# 🌧️ Rain Tomorrow Classifier

> An AI-powered weather prediction app that forecasts whether it will rain tomorrow across **49 Australian cities** — built with Random Forest, Streamlit, and Plotly.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?logo=scikitlearn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Overview

**Rain Tomorrow Classifier** is a machine learning project that predicts rainfall for the next day using real Australian Bureau of Meteorology data. Users enter today's weather observations (temperature, humidity, wind, pressure, etc.) and receive an instant AI prediction with probability, a gauge chart, and feature importance analysis.

---

## ✨ Features

- 🔮 **Binary rain prediction** — Yes / No for rain tomorrow
- 📊 **Live probability gauge** — Plotly-powered visual meter
- 🗺️ **49 Australian locations** supported
- 🌡️ **22 weather input features** — temperature, humidity, pressure, wind, and more
- 📈 **Top feature importances** — horizontal bar chart from the trained Random Forest
- 💡 **Key input summary** — metric tiles for the most relevant values
- 🎨 **Premium dark glassmorphism UI** with smooth hover animations

---

## 🗂️ Project Structure

```
tomorrow rain classifier/
│
├── app.py              # Streamlit frontend — prediction UI
├── training.py         # Model training script — data prep, train, evaluate, save
├── weatherAUS.csv      # Raw dataset (~145,000 records)
│
└── model/              # Auto-created after training
    ├── model.pkl           # Trained Random Forest classifier
    ├── scaler.pkl          # StandardScaler for numerical features
    ├── label_encoders.pkl  # LabelEncoders for categorical columns
    ├── target_encoder.pkl  # LabelEncoder for RainTomorrow target
    └── metadata.pkl        # Feature list, metrics, and feature importances
```

---

## 🤖 Model Details

| Property         | Value                          |
|------------------|-------------------------------|
| **Algorithm**    | Random Forest Classifier       |
| **Estimators**   | 200 trees                      |
| **Max Depth**    | 15                             |
| **Class Weight** | Balanced (handles imbalance)   |
| **Train/Test**   | 80% / 20% (stratified split)   |
| **Scaler**       | StandardScaler                 |

### 🔑 Input Features (22 total)

| Type        | Features |
|-------------|----------|
| Numerical   | MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine, WindGustSpeed, WindSpeed9am, WindSpeed3pm, Humidity9am, Humidity3pm, Pressure9am, Pressure3pm, Cloud9am, Cloud3pm, Temp9am, Temp3pm, Month |
| Categorical | Location, WindGustDir, WindDir9am, WindDir3pm, RainToday |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/anushka672/Tomorrow-Rain-Classifier.git
cd Tomorrow-Rain-Classifier
```

### 2. Install dependencies

```bash
pip install streamlit scikit-learn pandas numpy plotly joblib
```

### 3. Train the model

> Make sure `weatherAUS.csv` is present in the project root.

```bash
python training.py
```

This will create all model artifacts in the `model/` folder and print evaluation metrics to the console.

### 4. Launch the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📊 Dataset

| Property      | Detail                                    |
|---------------|-------------------------------------------|
| **Source**    | Bureau of Meteorology — Australia         |
| **File**      | `weatherAUS.csv`                          |
| **Records**   | ~145,000 daily observations               |
| **Locations** | 49 cities across Australia                |
| **Target**    | `RainTomorrow` — Yes / No                 |

---

## 🖼️ App Preview

The Streamlit app features:
- **Sidebar** — Model accuracy, F1 score, ROC-AUC, and model status badge
- **Input form** — Organized sections for location, temperature, humidity, pressure, and wind
- **Predict button** — Runs inference in real time
- **Result card** — Color-coded rain/no-rain box with probability
- **Gauge chart** — Plotly Indicator showing rain probability (0–100%)
- **Feature importance chart** — Top-12 features ranked by importance from the Random Forest

---

## 🛠️ Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| ML Model     | scikit-learn (RandomForestClassifier) |
| Frontend     | Streamlit                           |
| Visualization| Plotly (gauge + bar charts)         |
| Data         | Pandas, NumPy                       |
| Persistence  | joblib                              |
| Styling      | Custom CSS · Glassmorphism · Inter font |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
Built with ❤️ using Random Forest · Streamlit · Plotly<br>
Dataset: Bureau of Meteorology — Australia (weatherAUS)
</div>
