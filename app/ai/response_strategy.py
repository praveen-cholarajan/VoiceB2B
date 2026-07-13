class ResponseStrategy:

    # Objection → campaign objection key mapping
    OBJECTION_KEYS = {
        "CURRENT_PROVIDER": "happy_provider",
        "PRICE":            "expensive",
        "NOT_INTERESTED":   "not_interested",
        "BUSY":             "busy_callback",
    }

    def get_strategy(self, state_name, rule_result, memory):

        strategy = {
            "mode": "NORMAL",
            "instruction": ""
        }

        # Handle objections
        if memory.objections:
            strategy["mode"] = "OBJECTION_HANDLE"
            strategy["instruction"] = "Handle the customer's objection, then continue the conversation."

        # Callback state
        elif state_name == "CALLBACK":
            strategy["mode"] = "SCHEDULE"
            strategy["instruction"] = "Schedule a callback at the customer's preferred time."

        # Documents
        elif state_name == "DOCUMENTS":
            strategy["mode"] = "NORMAL"
            strategy["instruction"] = "Explain the required documents clearly."

        # Recommend plan
        elif state_name == "RECOMMEND_PLAN":
            strategy["mode"] = "SELL_MODE"
            strategy["instruction"] = "Recommend the most suitable Vi Business plan based on the customer's profile."

        return strategy

    def decide(self, signal: dict, state: dict, memory, campaign=None):

        intent  = signal.get("intent",  "STATEMENT")
        emotion = signal.get("emotion", "NEUTRAL")
        urgency = signal.get("urgency", "LOW")

        state_name = state.get("title", "") if state else ""

        strategy = {
            "mode":        "NORMAL",
            "instruction": ""
        }

        # =================================================
        # 1. OBJECTION HANDLING (highest priority)
        # =================================================
        objection = getattr(memory, "objection", None)

        if objection:
            obj_key = self.OBJECTION_KEYS.get(objection)
            rebuttal_points = []

            if campaign and obj_key:
                rebuttal_points = campaign.get_objection(obj_key)

            if objection == "BUSY":
                strategy["mode"] = "CALM_REASSURE"
                strategy["instruction"] = (
                    "Customer is busy. Politely acknowledge and ask if you can "
                    "call them back at a convenient time. Do NOT continue the sales pitch."
                )
            elif rebuttal_points:
                strategy["mode"] = "OBJECTION_HANDLE"
                points_text = "\n".join(f"- {p}" for p in rebuttal_points)
                strategy["instruction"] = (
                    f"Customer raised objection: {objection}.\n"
                    f"Use these points to address it empathetically:\n{points_text}\n"
                    f"After addressing the objection, smoothly return to the current goal."
                )
            else:
                strategy["mode"] = "OBJECTION_HANDLE"
                strategy["instruction"] = (
                    f"Customer raised a concern ({objection}). "
                    "Acknowledge it empathetically, provide a brief relevant response, "
                    "then return to the current goal."
                )
            return strategy

        # =================================================
        # 2. NEGATIVE EMOTION
        # =================================================
        if emotion == "NEGATIVE":
            strategy["mode"] = "CALM_REASSURE"
            strategy["instruction"] = (
                "Customer seems unhappy. Be short, calm, and empathetic. Do not sell aggressively."
            )
            return strategy

        # =================================================
        # 3. HIGH URGENCY
        # =================================================
        if urgency == "HIGH":
            strategy["mode"] = "FAST_TRACK"
            strategy["instruction"] = (
                "Be direct and efficient. Skip small talk and move to solution quickly."
            )
            return strategy

        # =================================================
        # 4. SCHEDULING STATES
        # =================================================
        title_upper = state_name.upper()
        if "CALLBACK" in title_upper or "SCHEDULE" in title_upper or "PICKUP" in title_upper:
            strategy["mode"] = "SCHEDULE"
            strategy["instruction"] = (
                "Confirm the date and time the customer provided. "
                "Repeat it back naturally and proceed to close the call."
            )
            return strategy

        # =================================================
        # 5. YES / NO FLOW CONTROL
        # =================================================
        if intent == "YES":
            strategy["mode"] = "TRANSITION"
            strategy["instruction"] = (
                "Customer agreed. Acknowledge briefly and move forward. DO NOT repeat the question."
            )
            return strategy

        if intent == "NO":
            strategy["mode"] = "RESCHEDULE"
            strategy["instruction"] = (
                "Customer is not available. Politely offer a callback at a convenient time."
            )
            return strategy

        # =================================================
        # 6. CUSTOMER QUESTION
        # =================================================
        if intent == "QUESTION":
            strategy["mode"] = "ANSWER_RETURN"
            strategy["instruction"] = (
                "Answer the question briefly and accurately using the information provided, "
                "then return to the current state goal."
            )
            return strategy

        # =================================================
        # 7. PLAN / SALES STATE
        # =================================================
        if any(kw in title_upper for kw in ["PLAN", "RECOMMEND", "BENEFIT"]):
            strategy["mode"] = "SELL_MODE"
            strategy["instruction"] = (
                "Explain the plan benefits naturally. Highlight special offer if applicable. "
                "No aggressive selling — be consultative and helpful."
            )
            return strategy

        # =================================================
        # DEFAULT
        # =================================================
        strategy["mode"] = "NORMAL"
        strategy["instruction"] = "Follow the script for the current state. Stay on goal."

        return strategy