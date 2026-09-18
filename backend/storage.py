import os
import json
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SESSIONS_FILE = os.path.join(DATA_DIR, 'sessions.json')
GOALS_FILE = os.path.join(DATA_DIR, 'goals.json')

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_sessions():
    ensure_data_dir()
    if not os.path.exists(SESSIONS_FILE):
        return []
    try:
        with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_sessions(sessions):
    ensure_data_dir()
    with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)

def add_session(session):
    sessions = load_sessions()
    if 'id' not in session:
        session['id'] = len(sessions) + 1
    if 'timestamp' not in session:
        session['timestamp'] = datetime.now().isoformat()
    sessions.append(session)
    save_sessions(sessions)
    return session

def load_goals():
    ensure_data_dir()
    default_goals = {
        "daily_target_hours": 4.0,
        "weekly_target_hours": 25.0,
        "target_exam": "Machine Learning & Python Final",
        "exam_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
        "target_readiness_pct": 85
    }
    if not os.path.exists(GOALS_FILE):
        save_goals(default_goals)
        return default_goals
    try:
        with open(GOALS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # fill missing defaults if any
            for k, v in default_goals.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception:
        return default_goals

def save_goals(goals):
    ensure_data_dir()
    with open(GOALS_FILE, 'w', encoding='utf-8') as f:
        json.dump(goals, f, indent=2, ensure_ascii=False)
