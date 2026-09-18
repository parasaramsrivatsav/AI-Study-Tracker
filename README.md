# ⚡ AI Study Tracker - Learning Analytics & Exam Readiness Predictor

> An intelligent productivity platform built with **Python**, **Machine Learning (Scikit-Learn)**, **Pandas**, and **JavaScript** to track study hours, analyze learning patterns, and estimate student exam preparedness.

---

## ✨ Features

- 📚 **Study Session Management**: Log subject topics, durations, productivity ratings, and study notes.
- 🤖 **ML-Based Exam Readiness Predictor**: Random Forest model evaluated on cumulative hours, subject balance, consistency streaks, and quiz scores.
- 📈 **Pandas Analytics Engine**: High-level statistical aggregations, 14-day study trends, 24-hour peak productivity detection, and subject time share breakdown.
- ⏱️ **Focus Study Timer**: Live Pomodoro (25m), Deep Work (45m), and Marathon (60m) countdown timer.
- 🎯 **Goal & Consistency Streaks**: Set daily/weekly study targets and monitor streak records.
- 🌙 **Glassmorphism Web Dashboard**: Responsive dark mode design system built with HTML5, CSS3, JavaScript, and Chart.js.

---

## 📂 Project Architecture

```
AI Study Tracker/
├── backend/
│   ├── app.py                 # Flask REST API server & router
│   ├── analytics.py           # Pandas data aggregation & trend detection
│   ├── ml_model.py            # Scikit-Learn ML Exam Readiness Predictor
│   ├── storage.py             # Data persistence manager
│   ├── seed_data.py           # Pre-populates 50+ study logs for demo
│   └── requirements.txt       # Dependencies (Flask, Pandas, Scikit-Learn, NumPy)
├── frontend/
│   ├── index.html             # Dashboard UI layout
│   ├── css/
│   │   └── style.css          # Glassmorphic dark theme stylesheet
│   └── js/
│       ├── app.js             # API integration & SPA routing
│       ├── charts.js          # Chart.js visualization engine
│       └── timer.js           # Pomodoro countdown timer
├── .gitignore
├── run.py                     # Application launcher
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & Install Dependencies
```bash
git clone <your-repository-url>
cd "AI Study Tracker"
pip install -r backend/requirements.txt
```

### 2. Launch Application
```bash
python run.py
```
Open your browser at: `http://localhost:5000`

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, Flask-CORS
- **Machine Learning & Analytics**: Scikit-Learn, Pandas, NumPy, Joblib
- **Frontend**: JavaScript (ES6+), HTML5, CSS3 Glassmorphism, Chart.js
