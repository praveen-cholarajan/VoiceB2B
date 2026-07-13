import re

from app.rules.base_rule import BaseRule


class ScheduleRule(BaseRule):

    """
    Handles CALLBACK and SCHEDULE_VISIT states.

    Extracts preferred date/time text from customer messages.
    Stores both the raw text and parsed values in memory.
    """

    STATES = [
        "CALLBACK",
        "SCHEDULE_VISIT"
    ]

    TIME_PATTERNS = [
        r"\d{1,2}\s*(?:am|pm|AM|PM)",         # "3 PM", "10AM"
        r"\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?",  # "3:00 PM"
        r"\d{1,2}:\d{2}",                      # "15:00"
        r"morning|afternoon|evening|night",
        r"after\s+lunch|after\s+dinner",
        r"noon|midnight"
    ]

    DATE_PATTERNS = [
        r"today", r"tomorrow", r"day after tomorrow",
        r"monday|tuesday|wednesday|thursday|friday|saturday|sunday",
        r"\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?",    # 4/7, 4-7-2026
        r"\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*"
    ]

    def can_handle(self, state_name):
        return state_name in self.STATES

    def process(self, state_name, customer_message, memory):

        extracted = {}
        text = customer_message.strip()

        # Store raw preference text
        date_str = self._extract_date(text)
        time_str = self._extract_time(text)

        if state_name == "CALLBACK":
            memory.callback_text = text
            extracted["callback_text"] = text
            if date_str:
                memory.callback_date = date_str
                extracted["callback_date"] = date_str
            if time_str:
                memory.callback_time = time_str
                extracted["callback_time"] = time_str

        elif state_name == "SCHEDULE_VISIT":
            memory.pickup_text = text
            extracted["pickup_text"] = text
            if date_str:
                memory.pickup_date = date_str
                extracted["pickup_date"] = date_str
            if time_str:
                memory.pickup_time = time_str
                extracted["pickup_time"] = time_str

        return extracted

    # --------------------------------------------------

    def _extract_time(self, text):
        msg = text.lower()
        for pattern in self.TIME_PATTERNS:
            match = re.search(pattern, msg, re.IGNORECASE)
            if match:
                return match.group().strip()
        return None

    def _extract_date(self, text):
        msg = text.lower()
        for pattern in self.DATE_PATTERNS:
            match = re.search(pattern, msg, re.IGNORECASE)
            if match:
                return match.group().strip()
        return None
