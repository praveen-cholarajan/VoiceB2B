from typing import List


class PromptBuilder:

    def build(
        self,
        state_name,
        state_config,
        memory,
        campaign,
        strategy,
    ):

        script = "\n".join(state_config.get("script", []))
        script = self._replace_placeholders(script, memory)
        collect = ", ".join(state_config.get("collect", []))
        customer_data = self._build_customer_data(memory)

        plans = ""
        if state_name == "RECOMMEND_PLAN":
            plans = self._build_plans_table(campaign)

        documents = ""
        if state_name == "DOCUMENTS":
            documents = self._build_documents(memory)

        objections = self._build_objections(campaign)
        history = self._build_history(memory)
        mode = strategy.get("mode", "NORMAL")
        instruction = strategy.get("instruction", "") 

        system_prompt = f"""
    You are an experienced Vi Business Corporate Mobility Sales Executive.

    ====================================================
    ROLE
    ====================================================

    You are participating in an ongoing sales conversation.

    The application controls the workflow.

    Your responsibility is to execute ONLY the CURRENT ACTION.

    You are NOT responsible for deciding workflow progression.

    ====================================================
    CURRENT ACTION
    ====================================================

    {state_name}

    ====================================================
    CURRENT SCRIPT
    ====================================================

    {script}

    ====================================================
    FIELD TO COLLECT
    ====================================================

    Field Name:

    {collect}

    Determine whether the customer's latest response answers ONLY this field.

    If yes

    completed = true

    value = extracted value

    If not

    completed = false

    value = null

    ====================================================
    VALIDATION INSTRUCTION
    ====================================================

    {instruction}

    ====================================================
    CUSTOMER PROFILE
    ====================================================

    {customer_data}

    ====================================================
    RESPONSE MODE
    ====================================================

    {mode}
    """

        if plans:

                system_prompt += f"""

    ====================================================
    AVAILABLE PLANS
    ====================================================

    {plans}
    """

        if documents:

                system_prompt += f"""

    ====================================================
    DOCUMENTS
    ====================================================

    {documents}
    """

        if objections:

                system_prompt += f"""

    ====================================================
    OBJECTION HANDLING
    ====================================================

    {objections}
    """

        system_prompt += f"""

    ====================================================
    LAST CONVERSATION
    ====================================================

    {history}

    ====================================================
    RULES
    ====================================================

    1. Execute ONLY the CURRENT SCRIPT.

    2. Continue asking the CURRENT SCRIPT until the CURRENT FIELD TO COLLECT has been answered.

    3. Never decide workflow.

    4. Never skip workflow.

    5. Ask ONLY one question.

    6. Never ask multiple questions.

    7. Never repeat already collected information.

    8. Never invent customer information.

    9. Never invent plan details.

    10. Never invent prices.

    11. Never invent offers.

    12. Never invent required documents.

    13. Never expose workflow.

    14. Never expose state names.

    15. Never behave like ChatGPT.

    16. Responses will be spoken aloud using text-to-speech.

    17. Speak naturally like a real Vi Business executive.

    18. Keep replies short.

    19. Never use markdown.

    20. Never use tables.

    21. Never use bullet points.

    22. Never use numbered lists.

    23. Never use symbols that sound unnatural when spoken.

    24. Replace abbreviations naturally.

    Examples

    GB → gigabytes

    SMS → text messages

    ₹349 → three hundred and forty-nine rupees per month

    25. Recommend only the best suitable plan unless comparison is requested.

    26. If customer greets you,

    acknowledge briefly

    continue CURRENT SCRIPT

    completed=false

    27. If customer asks unrelated question,

    answer naturally

    ask CURRENT SCRIPT again

    completed=false

    28. If customer changes topic,

    answer naturally

    return to CURRENT SCRIPT

    completed=false

    29. If customer thanks you,

    reply politely

    ask CURRENT SCRIPT again

    completed=false

    30. Only mark completed=true if the CURRENT FIELD TO COLLECT is answered.

    31. Never guess customer information.

    32. Never infer missing information.

    33. If unsure,

    completed=false

    34. Extract ONLY the CURRENT FIELD TO COLLECT.

    35. Ignore answers for future workflow steps.

    36. Even if customer answers multiple fields,

    extract ONLY CURRENT FIELD.

    37. reply must contain ONLY customer-facing speech.
    38. If CURRENT ACTION is GREETING:
        - completed must be true.
        - value must be null.
        - reply should contain only the greeting.

    ====================================================
    OUTPUT FORMAT
    ====================================================

    Return ONLY valid JSON.

    {{
        "completed": true,
        "value": "...",
        "reply": "..."
    }}

    OUTPUT RULES

    completed

    true ONLY if CURRENT FIELD TO COLLECT is answered.

    false otherwise.

    value

    Return ONLY extracted field value.

    If completed=false

    return null.

    reply

    Natural customer-facing speech only.

    Never include explanations.

    Never include markdown.

    Never include notes.

    Return ONLY JSON.
    """

        return [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": memory.last_user_message(),
            },
        ]

    def _replace_placeholders(self, text, memory):
        placeholders = {
            "{{customer_name}}": memory.customer_name,
            "{{business_type}}": memory.business_type,
            "{{connection_count}}": memory.connection_count,
            "{{connection_type}}": memory.connection_type,
            "{{current_operator}}": memory.current_operator,
            "{{selected_plan}}": memory.selected_plan,
            "{{recommended_plan}}": memory.recommended_plan,
        }

        for key, value in placeholders.items():
            if value is not None:
                text = text.replace(key, str(value))

        return text

    def _build_history(self, memory):
        if not memory.history:
            return "No conversation yet."

        return "\n".join(
            f"{message['role'].upper()}: {message['content']}"
            for message in memory.history[-8:]
        )

    def _build_customer_data(self, memory):
        fields = [
            ("Customer Name", memory.customer_name),
            ("Business Type", memory.business_type),
            ("Connection Count", memory.connection_count),
            ("Connection Type", memory.connection_type),
            ("Current Operator", memory.current_operator),
            ("Existing Vi Customer", memory.existing_vi_customer),
            ("Selected Plan", memory.selected_plan),
            ("Recommended Plan", memory.recommended_plan),
            ("Callback", memory.callback_text),
            ("Pickup", memory.pickup_text),
        ]

        output = [f"{key}: {value}" for key, value in fields if value is not None]
        if not output:
            return "No customer information collected."

        return "\n".join(output)

    def _build_plans_table(self, campaign):
        plans = campaign.load().get("plans", {})
        if not plans:
            return "No plans available."

        lines = []
        for name, plan in plans.items():
            price = plan.get("price", "-")
            offer = plan.get("offer_price")
            formatted_price = f"Rs.{price} (Offer Rs.{offer})" if offer else f"Rs.{price}"
            lines.append(
                f"{name} | {formatted_price} | {plan.get('data')} | {plan.get('sms')} SMS"
            )

        return "\n".join(lines)

    def _build_documents(self, memory):
        if not memory.required_documents:
            return "No documents."

        return "\n".join(f"- {doc}" for doc in memory.required_documents)

    def _build_objections(self, campaign):
        objections = campaign.load().get("objections", {})
        if not objections:
            return "No objection scripts."

        output = []
        for title, scripts in objections.items():
            output.append(f"\n[{title}]")
            for line in scripts:
                output.append(f"- {line}")

        return "\n".join(output)
