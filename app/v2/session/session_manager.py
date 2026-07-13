from app.v2.session.call_session import CallSession


class SessionManager:

    def __init__(self):

        self.sessions = {}

    def get_session(self, session_id):

        return self.sessions.get(session_id)

    def create_session(self, phone_number=None):

        session = CallSession(phone_number)

        self.sessions[session.session_id] = session

        return session

    def remove_session(self, session_id):

        if session_id in self.sessions:

            del self.sessions[session_id]

    def total_sessions(self):

        return len(self.sessions)