import uuid
from datetime import datetime

from app.conversation.conversation_orchestrator import ConversationOrchestrator


class CallSession:

    def __init__(self, phone_number=None):

        self.session_id = str(uuid.uuid4())

        self.phone_number = phone_number

        self.started_at = datetime.now()

        self.last_activity = datetime.now()

        self.orchestrator = ConversationOrchestrator()

    def process(self, customer_message: str):

        self.last_activity = datetime.now()

        return self.orchestrator.process(customer_message)