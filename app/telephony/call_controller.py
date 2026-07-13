from app.v2.session.session_manager import SessionManager


class CallController:

    def __init__(self):

        self.session_manager = SessionManager()

    def start_call(
        self,
        phone_number
    ):

        session = self.session_manager.create_session(phone_number)

        return session