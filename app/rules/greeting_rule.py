import re


class GreetingRule:

    def process(
        self,
        state_name,
        customer_message,
        memory
    ):

        result = {}

        # -----------------------------------------
        # GREETING
        # -----------------------------------------
        # No customer input required.
        # BusinessRuleEngine will auto-transition.
        if state_name == "GREETING":
            return result

        # -----------------------------------------
        # ASK_CUSTOMER_NAME
        # -----------------------------------------
        if state_name == "ASK_CUSTOMER_NAME":

            name = self._extract_name(customer_message)

            if name:

                memory.update_customer_name(name)

                result["customer_name"] = name

            return result

        # -----------------------------------------
        # INTRODUCE_SELF
        # -----------------------------------------
        # No data collection.
        if state_name == "INTRODUCE_SELF":
            return result

        # -----------------------------------------
        # ASK_TALK_TIME
        # -----------------------------------------

        if state_name == "ASK_TALK_TIME":

            msg = customer_message.lower()

            positive = [
                "yes",
                "yeah",
                "yep",
                "sure",
                "okay",
                "ok",
                "go ahead",
                "please continue",
                "continue",
                "tell me",
                "speak"
            ]

            negative = [
                "no",
                "busy",
                "later",
                "call later",
                "not now",
                "another time"
            ]

            if any(word in msg for word in positive):

                memory.talk_permission = True

                result["talk_permission"] = True

            elif any(word in msg for word in negative):

                memory.talk_permission = False

                result["talk_permission"] = False

            return result

        return result

    # ---------------------------------------------------
    # Extract Customer Name
    # ---------------------------------------------------

    def _extract_name(self, text: str):

        if not text:
            return None

        name = text.strip()

        patterns = [

            r"my name is\s+(.*)",

            r"i am\s+(.*)",

            r"i'm\s+(.*)",

            r"this is\s+(.*)",

            r"it is\s+(.*)"
        ]

        lower = name.lower()

        for pattern in patterns:

            match = re.match(pattern, lower)

            if match:

                name = match.group(1)

                break

        name = re.sub(
            r"[^a-zA-Z\s]",
            "",
            name
        ).strip()

        if not name:

            return None

        return " ".join(
            word.capitalize()
            for word in name.split()
        )