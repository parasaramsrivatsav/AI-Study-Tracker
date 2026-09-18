import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
from storage import load_sessions, load_goals

_model_cache = None

def train_or_get_model():
    global _model_cache
    if _model_cache is not None:
        return _model_cache

    # Synthetic training dataset representing historical student exam readiness outcomes
    # Features: [total_hours, subject_hours, streak_days, avg_productivity, days_to_exam, avg_quiz_score]
    np.random.seed(42)
    n_samples = 300
    
    total_hours = np.random.uniform(10, 120, n_samples)
    subject_hours = total_hours * np.random.uniform(0.15, 0.45, n_samples)
    streak_days = np.random.randint(0, 20, n_samples)
    avg_prod = np.random.uniform(2.5, 5.0, n_samples)
    days_to_exam = np.random.randint(3, 30, n_samples)
    avg_quiz = np.random.uniform(60, 100, n_samples)

    # Readiness percentage calculation formula for realistic target labels
    readiness_target = (
        (subject_hours / 25.0) * 35 +
        (streak_days / 10.0) * 15 +
        (avg_prod / 5.0) * 15 +
        (avg_quiz / 100.0) * 25 +
        (np.clip(20 - days_to_exam, 1, 20) / 20.0) * 10
    ) + np.random.normal(0, 3, n_samples)
    
    y = np.clip(readiness_target, 15, 99)

    X = np.column_stack([total_hours, subject_hours, streak_days, avg_prod, days_to_exam, avg_quiz])

    rf = RandomForestRegressor(n_estimators=50, max_depth=6, random_state=42)
    rf.fit(X, y)
    
    _model_cache = rf
    return rf

def predict_exam_readiness(target_subject=None, days_until_exam=None):
    sessions = load_sessions()
    goals = load_goals()

    if not sessions:
        return {
            "readiness_pct": 25.0,
            "readiness_level": "Needs Improvement",
            "confidence_score": 50,
            "target_subject": target_subject or "General Prep",
            "days_until_exam": days_until_exam or 14,
            "subject_hours": 0.0,
            "total_hours": 0.0,
            "risk_factors": ["No study sessions recorded yet."],
            "recommendations": ["Start logging daily study sessions to activate AI insights."]
        }

    df = pd.DataFrame(sessions)
    total_hours = df['duration'].sum() / 60.0
    streak_days = 5  # default baseline
    avg_prod = df['productivity_rating'].mean()
    avg_quiz = df['quiz_score'].dropna().mean() if 'quiz_score' in df and not df['quiz_score'].dropna().empty else 82.0

    if not target_subject:
        target_subject = goals.get("target_exam", "Machine Learning & Python Final")
    
    # Calculate subject hours
    subj_df = df[df['subject'].str.contains(target_subject, case=False, na=False)]
    if subj_df.empty and ('Machine' in target_subject or 'Python' in target_subject):
        subj_df = df[df['subject'].isin(['Machine Learning', 'Python', 'Pandas'])]
    
    subject_hours = subj_df['duration'].sum() / 60.0 if not subj_df.empty else total_hours * 0.25

    if days_until_exam is None:
        exam_date_str = goals.get("exam_date")
        if exam_date_str:
            try:
                exam_dt = datetime.strptime(exam_date_str, "%Y-%m-%d")
                days_until_exam = max(1, (exam_dt - datetime.now()).days)
            except Exception:
                days_until_exam = 14
        else:
            days_until_exam = 14

    model = train_or_get_model()
    input_features = np.array([[total_hours, subject_hours, streak_days, avg_prod, days_until_exam, avg_quiz]])
    
    predicted_pct = float(model.predict(input_features)[0])
    predicted_pct = round(min(98.5, max(15.0, predicted_pct)), 1)

    # Determine level
    if predicted_pct >= 80:
        level = "High Readiness"
        level_color = "#10b981"  # Emerald
    elif predicted_pct >= 60:
        level = "Moderate Readiness"
        level_color = "#f59e0b"  # Amber
    else:
        level = "Needs Focused Improvement"
        level_color = "#ef4444"  # Red

    # Generate tailored risk factors & recommendations based on feature importance
    risk_factors = []
    recommendations = []

    if subject_hours < 12:
        risk_factors.append(f"Low dedicated time on {target_subject} ({round(subject_hours, 1)} hrs recorded).")
        recommendations.append(f"Allocate at least 2.5 additional hours specifically to {target_subject} topics.")

    if avg_prod < 3.8:
        risk_factors.append(f"Average productivity rating is {round(avg_prod, 1)}/5, indicating potential fatigue or distractions.")
        recommendations.append("Use 25-minute Pomodoro sprints to maintain high focus quality during study sessions.")

    if days_until_exam <= 7 and predicted_pct < 85:
        risk_factors.append(f"Only {days_until_exam} days remaining until exam date.")
        recommendations.append("Prioritize mock practice tests and weak topic revisions over new theoretical material.")

    if not recommendations:
        recommendations.append(f"Excellent progress! Keep maintaining your current study rhythm of 3-4 hours daily for {target_subject}.")
        recommendations.append("Conduct a 30-minute quick formula & core concept review 2 days before the exam.")

    # Feature Importance for Radar Chart visualization
    feature_breakdown = [
        {"feature": "Subject Dedicated Hours", "score": min(100, round((subject_hours / 20.0) * 100))},
        {"feature": "Total Study Volume", "score": min(100, round((total_hours / 50.0) * 100))},
        {"feature": "Study Consistency", "score": min(100, round((streak_days / 7.0) * 100))},
        {"feature": "Productivity Rating", "score": min(100, round((avg_prod / 5.0) * 100))},
        {"feature": "Quiz & Retention Score", "score": min(100, round(avg_quiz))}
    ]

    return {
        "readiness_pct": predicted_pct,
        "readiness_level": level,
        "level_color": level_color,
        "confidence_score": round(min(95.0, 75.0 + (total_hours / 5.0)), 1),
        "target_subject": target_subject,
        "days_until_exam": days_until_exam,
        "subject_hours": round(subject_hours, 1),
        "total_hours": round(total_hours, 1),
        "risk_factors": risk_factors,
        "recommendations": recommendations,
        "feature_breakdown": feature_breakdown
    }
