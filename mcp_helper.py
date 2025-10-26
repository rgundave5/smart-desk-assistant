from datetime import datetime
from db import Session
from models import SessionModel, EmotionModel
import requests

def start_session(params):
    db_session = Session()
    new_session = SessionModel()
    db_session.add(new_session)
    db_session.commit()
    session_id = new_session.session_id
    started_at = new_session.started_at
    db_session.close()
    return {"session_id": session_id, "started_at": started_at.isoformat()}

def stop_session(params):
    session_id = params.get("session_id")
    db_session = Session()
    session_obj = db_session.query(SessionModel).filter_by(session_id=session_id).first()
    if session_obj:
        session_obj.ended_at = datetime.utcnow()
        db_session.commit()
    ended_at = session_obj.ended_at if session_obj else None
    db_session.close()
    return {"session_id": session_id, "ended_at": ended_at.isoformat() if ended_at else None}

def send_emotion_data(params):

    raw_clip = params.get("raw_clip")  # Example: base64 or file URL of the clip

    # Call Imentiv Emotion API
    # Replace 'YOUR_IMENTIV_ENDPOINT' and add authentication headers as needed
    response = requests.post(
        "https://api.imentiv.ai/emotion",  
        json={"clip": raw_clip},
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )

    emotion_result = response.json().get("emotion")

    # Now store the emotion result in your DB using your ORM as usual
    session_id = params.get("session_id")
    timestamp = params.get("timestamp")

    session_id = params.get("session_id")
    emotion = params.get("emotion")
    timestamp = params.get("timestamp")  # Should be in ISO or datetime format

    db_session = Session()
    emotion_entry = EmotionModel(session_id=session_id, emotion=emotion, timestamp=timestamp)
    db_session.add(emotion_entry)
    db_session.commit()
    db_session.close()
    return {"status": "ok"}

def get_productivity_level(params):
    session_id = params.get("session_id")
    db_session = Session()
    emotions = db_session.query(EmotionModel.emotion).filter_by(session_id=session_id).all()
    db_session.close()
    emotions_list = [e[0] for e in emotions]
    focus_score = emotions_list.count("focused") / max(len(emotions_list), 1)
    return {"productivity": focus_score}