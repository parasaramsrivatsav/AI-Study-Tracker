import random
from datetime import datetime, timedelta
from storage import load_sessions, save_sessions

SUBJECTS = [
    {"name": "Python", "color": "#3776AB", "topics": ["Decorators", "Asyncio", "Generators", "OOP Principles", "Multiprocessing"]},
    {"name": "Machine Learning", "color": "#FF6F61", "topics": ["Random Forest", "Gradient Boosting", "Feature Engineering", "Model Evaluation", "Neural Networks"]},
    {"name": "Pandas", "color": "#150458", "topics": ["DataFrames", "GroupBy & Aggregations", "Merging & Joins", "Time Series Analysis", "Missing Data Handling"]},
    {"name": "JavaScript", "color": "#F7DF1E", "topics": ["Async/Await & Promises", "DOM Manipulation", "Event Loop", "ES6+ Features", "Closures & Scope"]},
    {"name": "Data Structures", "color": "#4CAF50", "topics": ["Trees & Graphs", "Dynamic Programming", "Sorting Algorithms", "Heaps", "Hash Tables"]},
    {"name": "System Design", "color": "#9C27B0", "topics": ["Caching & Redis", "Database Sharding", "Load Balancing", "Microservices", "REST API Design"]}
]

def generate_seed_data(days=30):
    sessions = load_sessions()
    if len(sessions) >= 20:
        return  # Data already exists

    generated = []
    end_date = datetime.now()
    session_id = 1

    for day_offset in range(days - 1, -1, -1):
        current_date = end_date - timedelta(days=day_offset)
        # 1 to 3 sessions per day
        num_sessions = random.choices([1, 2, 3], weights=[30, 50, 20])[0]
        
        # Skip some days to make streak realistic
        if day_offset in [24, 18, 11, 4] and random.random() < 0.6:
            continue

        for _ in range(num_sessions):
            subj = random.choice(SUBJECTS)
            topic = random.choice(subj["topics"])
            duration = random.choice([30, 45, 60, 75, 90, 120])
            rating = random.choices([3, 4, 5], weights=[20, 50, 30])[0]
            
            # Random hour between 8 AM and 10 PM
            hour = random.randint(8, 21)
            minute = random.choice([0, 15, 30, 45])
            timestamp = current_date.replace(hour=hour, minute=minute, second=0).isoformat()

            generated.append({
                "id": session_id,
                "subject": subj["name"],
                "topic": topic,
                "duration": duration,  # minutes
                "productivity_rating": rating,  # 1-5 scale
                "notes": f"Reviewed {topic} concepts and practiced exercises.",
                "timestamp": timestamp,
                "quiz_score": random.randint(70, 98)
            })
            session_id += 1

    save_sessions(generated)
    print(f"Generated {len(generated)} seed study sessions.")

if __name__ == "__main__":
    generate_seed_data()
