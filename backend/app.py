import os
import sys

# Ensure user site-packages are accessible
site_pkg = os.path.expanduser(r"~\AppData\Roaming\Python\Python313\site-packages")
if os.path.exists(site_pkg) and site_pkg not in sys.path:
    sys.path.insert(0, site_pkg)

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from storage import load_sessions, add_session, load_goals, save_goals
from seed_data import generate_seed_data
from analytics import get_analytics_summary
from ml_model import predict_exam_readiness

# Initialize seed data if empty
generate_seed_data()

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

# Serve Frontend Pages & Static Assets
@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')

# API Endpoints
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    summary = get_analytics_summary()
    readiness = predict_exam_readiness()
    return jsonify({
        "summary": summary,
        "readiness": readiness,
        "status": "success"
    })

@app.route('/api/sessions', methods=['GET', 'POST'])
def handle_sessions():
    if request.method == 'POST':
        data = request.json or {}
        if not data.get('subject') or not data.get('duration'):
            return jsonify({"error": "Subject and duration are required"}), 400
        
        session = {
            "subject": data.get('subject'),
            "topic": data.get('topic', 'General Study'),
            "duration": int(data.get('duration', 30)),
            "productivity_rating": int(data.get('productivity_rating', 4)),
            "notes": data.get('notes', ''),
            "quiz_score": int(data.get('quiz_score', 85)) if data.get('quiz_score') else 85
        }
        added = add_session(session)
        return jsonify({"message": "Session logged successfully", "session": added}), 201
    
    # GET
    sessions = load_sessions()
    return jsonify({"sessions": list(reversed(sessions))})

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    summary = get_analytics_summary()
    return jsonify(summary)

@app.route('/api/predict-readiness', methods=['POST'])
def predict_readiness_endpoint():
    data = request.json or {}
    target_subject = data.get('target_subject')
    days_until_exam = data.get('days_until_exam')
    if days_until_exam:
        try:
            days_until_exam = int(days_until_exam)
        except ValueError:
            days_until_exam = 14

    res = predict_exam_readiness(target_subject=target_subject, days_until_exam=days_until_exam)
    return jsonify(res)

@app.route('/api/goals', methods=['GET', 'POST'])
def handle_goals():
    if request.method == 'POST':
        data = request.json or {}
        current_goals = load_goals()
        current_goals.update(data)
        save_goals(current_goals)
        return jsonify({"message": "Goals updated successfully", "goals": current_goals})
    
    return jsonify(load_goals())

@app.route('/api/insights', methods=['GET'])
def get_insights():
    summary = get_analytics_summary()
    readiness = predict_exam_readiness()
    
    insights = []
    
    # High-level productivity insight
    if summary['avg_productivity'] >= 4.0:
        insights.append({
            "type": "positive",
            "title": "High Focus Consistency",
            "description": f"Your average productivity rating is {summary['avg_productivity']}/5 across {summary['total_sessions']} sessions. Peak study time detected between 10 AM - 2 PM."
        })
    else:
        insights.append({
            "type": "warning",
            "title": "Productivity Dip Detected",
            "description": f"Average rating is {summary['avg_productivity']}/5. Try scheduling shorter 45-minute blocks with 10-minute active breaks."
        })

    # Subject distribution insight
    if summary['weak_subjects']:
        weak_list = ", ".join(summary['weak_subjects'])
        insights.append({
            "type": "action",
            "title": "Subject Allocation Gap",
            "description": f"Subjects needing attention: {weak_list}. Consider allocating your next 2 study blocks here."
        })

    # ML Readiness insight
    insights.append({
        "type": "ml",
        "title": f"Exam Readiness Prediction: {readiness['readiness_pct']}%",
        "description": f"Based on historical data for {readiness['target_subject']}, your estimated readiness is {readiness['readiness_level']}."
    })

    return jsonify({"insights": insights, "recommendations": readiness['recommendations']})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"AI Study Tracker Backend running at http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
