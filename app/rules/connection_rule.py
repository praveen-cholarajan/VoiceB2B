import re

from app.rules.base_rule import BaseRule


class ConnectionRule(BaseRule):

    STATES = [
        "ASK_CONNECTION_COUNT",
        "ASK_CONNECTION_TYPE"
    ]

    NEW_KEYWORDS = [
        "new",
        "new connection",
        "fresh",
        "new sim",
        "new sims"
    ]

    PORT_KEYWORDS = [
        "port",
        "mnp",
        "porting",
        "switch",
        "transfer"
    ]

    def can_handle(self, state_name):
        return state_name in self.STATES

    def process(
        self,
        state_name,
        customer_message,
        memory
    ):
        extracted = {}
        text = customer_message.lower().strip()

        # Always try to extract connection count
        count = self.extract_connection_count(text)
        if count is not None:
            memory.connection_count = count
            extracted["connection_count"] = count

        # Always try to extract connection type
        if any(word in text for word in self.PORT_KEYWORDS):
            memory.connection_type = "port"
            extracted["connection_type"] = "port"
        elif any(word in text for word in self.NEW_KEYWORDS):
            memory.connection_type = "new"
            extracted["connection_type"] = "new"

        return extracted

    def extract_connection_count(self, text):
        match = re.search(r"\d+", text)
        if match:
            return int(match.group())
        return None
