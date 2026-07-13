import re


class ObjectionRule:

    """
    Detect customer objections.

    IMPORTANT BEHAVIOR:
    - This rule does NOT change the conversation state.
    - It only stores the objection in memory.
    - The ResponseStrategy will pick it up and inject objection-handling
      instructions into the prompt so the LLM addresses it, then
      the flow continues from the same state.
    - Objection is cleared after one turn of handling.
    """

    def __init__(self):

        # Patterns that trigger soft objection handling (stay in state)
        self.patterns = {

            "NOT_INTERESTED": [
                r"not interested",
                r"no thanks",
                r"don't want",
                r"no need",
                r"not required",
                r"not looking"
            ],

            "BUSY": [
                r"busy",
                r"call later",
                r"not now",
                r"in a meeting",
                r"driving"
            ],

            "PRICE": [
                r"expensive",
                r"too costly",
                r"price is high",
                r"cheaper",
                r"discount",
                r"reduce the price"
            ],

            "CURRENT_PROVIDER": [
                r"happy with (?:jio|airtel|bsnl|current)",
                r"already using (?:jio|airtel|bsnl)",
                r"using jio",
                r"using airtel",
                r"using bsnl",
                r"satisfied with current"
            ]

        }

    # --------------------------------------------------

    def can_handle(self, state_name):
        # Objections can happen in ANY state
        return True

    # --------------------------------------------------

    def process(self, state_name, customer_message, memory):

        message = customer_message.lower()

        for objection, patterns in self.patterns.items():

            for pattern in patterns:

                if re.search(pattern, message):

                    memory.objection = objection

                    # Return minimal dict – DO NOT trigger state change
                    return {"objection": objection}

        # No objection detected; clear any stale objection
        return {}