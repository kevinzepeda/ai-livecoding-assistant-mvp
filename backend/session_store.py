# Simple memory store
session_history = {}

def get_session(session_code):
    return session_history.get(session_code, [])

def store_message(session_code, role, content):
    if session_code not in session_history:
        session_history[session_code] = []
    session_history[session_code].append({"role": role, "content": content})
