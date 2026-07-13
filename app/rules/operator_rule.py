import re

from app.rules.base_rule import BaseRule


class OperatorRule(BaseRule):

    STATES = [
        "ASK_OPERATOR"
    ]

    OPERATORS = {
        "jio": [
            "jio",
            "reliance jio",
            "jio telecom"
        ],
        "airtel": [
            "airtel",
            "bharti airtel"
        ],
        "bsnl": [
            "bsnl",
            "bharat sanchar nigam"
        ],
        "vi": [
            "vi",
            "vodafone",
            "idea",
            "vodafone idea"
        ]
    }

    def can_handle(self, state_name):
        return state_name in self.STATES

    def process(
        self,
        state_name,
        customer_message,
        memory
    ):
        extracted = {}
        operator = self.extract_operator(customer_message)
        if operator:
            memory.current_operator = operator
            extracted["current_operator"] = operator
        return extracted

    def extract_operator(self, text):
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", " ", text)
        for operator, keywords in self.OPERATORS.items():
            for keyword in keywords:
                if keyword in text:
                    return operator
        return None
