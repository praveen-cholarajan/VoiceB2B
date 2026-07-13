from app.rules.base_rule import BaseRule


class PlanRule(BaseRule):

    STATES = [
        "PLAN_INTRO",
        "RECOMMEND_PLAN",
        "EXISTING_CUSTOMER"
    ]

    # All available plans ordered by price
    PLANS = [
        ("Business Plus 349", 30,  349),
        ("Business Plus 399", 40,  399),
        ("Business Plus 449", 60,  449),
        ("Business Plus 549", 100, 549),
        ("Business Plus 899", 175, 899),
    ]

    def can_handle(self, state_name):
        return state_name in self.STATES

    def process(self, state_name, customer_message, memory):

        extracted = {}
        text = customer_message.lower()

        # -------------------------------------------------
        # EXISTING_CUSTOMER – detect yes/no
        # -------------------------------------------------
        if state_name == "EXISTING_CUSTOMER":

            if any(x in text for x in [
                "yes", "already", "existing", "using vi", "have vi", "vi customer"
            ]):
                memory.existing_vi_customer = True
                extracted["existing_vi_customer"] = True

            elif any(x in text for x in [
                "no", "new", "don't have", "do not have", "never", "not a vi"
            ]):
                memory.existing_vi_customer = False
                extracted["existing_vi_customer"] = False

            return extracted

        # -------------------------------------------------
        # RECOMMEND_PLAN – recommend based on count & budget
        # -------------------------------------------------
        if state_name == "RECOMMEND_PLAN":

            plan = self._recommend_plan(memory, text)
            memory.selected_plan = plan
            extracted["selected_plan"] = plan

            # Special offer flag (10+ connections)
            count = memory.connection_count or 0
            if count >= 10:
                memory.special_offer = True
                extracted["special_offer"] = True
            else:
                memory.special_offer = False
                extracted["special_offer"] = False

            return extracted

        return extracted

    # -------------------------------------------------
    # Plan recommendation logic
    # -------------------------------------------------

    def _recommend_plan(self, memory, text):

        count = memory.connection_count or 0

        # If customer mentions a specific data need, try to match
        if "175" in text or "large" in text or "heavy" in text or "maximum" in text:
            return "Business Plus 899"
        if "100" in text:
            return "Business Plus 549"
        if "60" in text or "medium" in text:
            return "Business Plus 449"
        if "40" in text:
            return "Business Plus 399"

        # Default: 10+ connections → special 349 offer; else 399
        if count >= 10:
            return "Business Plus 349"
        return "Business Plus 399"
