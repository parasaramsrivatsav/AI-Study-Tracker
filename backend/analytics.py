import os
import sys

site_pkg = os.path.expanduser(r"~\AppData\Roaming\Python\Python313\site-packages")
if os.path.exists(site_pkg) and site_pkg not in sys.path:
    sys.path.insert(0, site_pkg)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from storage import load_sessions, load_goals

def get_analytics_summary():
    sessions = load_sessions()
    goals = load_goals()
    
    if not sessions:
        return {
            "total_hours": 0,
            "total_sessions": 0,
            "avg_session_minutes": 0,
            "avg_productivity": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "daily_target_hours": goals.get("daily_target_hours", 4.0),
            "daily_progress_pct": 0,
            "subject_breakdown": [],
            "daily_trend": [],
            "hourly_distribution": [],
            "weak_subjects": [],
            "strong_subjects": []
        }
    
    df = pd.DataFrame(sessions)
    df['dt'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['dt'].dt.strftime('%Y-%m-%d')
    df['hour'] = df['dt'].dt.hour
    df['duration_hours'] = df['duration'] / 60.0

    # Basic KPI Metrics
    total_hours = round(df['duration_hours'].sum(), 1)
    total_sessions = int(len(df))
    avg_session_min = round(df['duration'].mean(), 1)
    avg_productivity = round(df['productivity_rating'].mean(), 2)

    # Calculate Streaks
    unique_dates = sorted(df['date'].unique(), reverse=True)
    today_str = datetime.now().strftime('%Y-%m-%d')
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    current_streak = 0
    check_date = datetime.now().date()
    
    # Check if studied today or yesterday to maintain active streak
    if today_str in unique_dates or yesterday_str in unique_dates:
        # iterate back
        d_set = set(unique_dates)
        curr = datetime.now().date() if today_str in unique_dates else (datetime.now() - timedelta(days=1)).date()
        while curr.strftime('%Y-%m-%d') in d_set:
            current_streak += 1
            curr -= timedelta(days=1)

    # Longest streak calculation
    longest_streak = 0
    temp_streak = 0
    all_dates_asc = pd.to_datetime(pd.Series(unique_dates)).sort_values()
    if not all_dates_asc.empty:
        prev = None
        for d in all_dates_asc:
            if prev is None or (d - prev).days == 1:
                temp_streak += 1
            else:
                temp_streak = 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
            prev = d

    # Daily target progress today
    today_hours = round(df[df['date'] == today_str]['duration_hours'].sum(), 1)
    daily_target = goals.get("daily_target_hours", 4.0)
    daily_progress_pct = min(100, round((today_hours / daily_target) * 100, 1)) if daily_target > 0 else 0

    # Subject Breakdown
    subj_group = df.groupby('subject').agg(
        total_hours=('duration_hours', 'sum'),
        session_count=('duration', 'count'),
        avg_rating=('productivity_rating', 'mean'),
        avg_quiz=('quiz_score', 'mean')
    ).reset_index()

    subj_group['total_hours'] = subj_group['total_hours'].round(1)
    subj_group['avg_rating'] = subj_group['avg_rating'].round(2)
    subj_group['avg_quiz'] = subj_group['avg_quiz'].fillna(80).round(1)
    subj_group['share_pct'] = ((subj_group['total_hours'] / total_hours) * 100).round(1)

    subject_breakdown = subj_group.sort_values(by='total_hours', ascending=False).to_dict(orient='records')

    # Weak & Strong Subjects Identification
    subj_group_sorted = subj_group.sort_values(by='total_hours')
    weak_subjects = subj_group_sorted.head(2)['subject'].tolist()
    strong_subjects = subj_group.sort_values(by='total_hours', ascending=False).head(2)['subject'].tolist()

    # Daily Study Trend (Last 14 Days)
    fourteen_days_ago = datetime.now() - timedelta(days=13)
    date_range = pd.date_range(start=fourteen_days_ago.strftime('%Y-%m-%d'), end=today_str)

    daily_df = df.groupby('date')['duration_hours'].sum().reindex(date_range.strftime('%Y-%m-%d'), fill_value=0).reset_index()
    daily_df.columns = ['date', 'hours']
    daily_df['hours'] = daily_df['hours'].round(1)
    # Format dates to short display string like "Sep 15"
    daily_df['label'] = pd.to_datetime(daily_df['date']).dt.strftime('%b %d')
    daily_trend = daily_df.to_dict(orient='records')

    # Hourly Distribution (Peak Productivity Hours)
    hourly_df = df.groupby('hour')['duration_hours'].sum().reindex(range(24), fill_value=0).reset_index()
    hourly_df.columns = ['hour', 'hours']
    hourly_df['hours'] = hourly_df['hours'].round(1)
    hourly_distribution = hourly_df.to_dict(orient='records')

    return {
        "total_hours": total_hours,
        "total_sessions": total_sessions,
        "avg_session_minutes": avg_session_min,
        "avg_productivity": avg_productivity,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "today_hours": today_hours,
        "daily_target_hours": daily_target,
        "daily_progress_pct": daily_progress_pct,
        "subject_breakdown": subject_breakdown,
        "daily_trend": daily_trend,
        "hourly_distribution": hourly_distribution,
        "weak_subjects": weak_subjects,
        "strong_subjects": strong_subjects
    }
