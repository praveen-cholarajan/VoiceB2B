from typing import List


class PromptBuilder:
    def build(
        self,
        state_name: str,
        state_config: dict,
        memory,
        campaign,
        strategy,
    ) -> List[dict]:
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

====================================================
CURRENT ACTION
====================================================

{state_name}

====================================================
SCRIPT
====================================================

{script}

====================================================
FIELD TO COLLECT
====================================================

{collect}

====================================================
CUSTOMER PROFILE
====================================================

{customer_data}

====================================================
RESPONSE MODE
====================================================

{mode}

Instruction:

{instruction}
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

2. CURRENT SCRIPT is the next unanswered action.

3. Ask ONLY one question.

4. Never ask two questions.

5. Never repeat answered questions.

6. Never skip workflow.

7. Never invent plan details.

8. Never invent prices.

9. Never invent documents.

10. Never behave like ChatGPT.

11. Never restart conversation.

12. If customer greets you,
briefly acknowledge and continue CURRENT SCRIPT.

13. If customer asks unrelated question,
answer shortly and immediately continue CURRENT SCRIPT.

14. Keep response under 40 words.

15. Sound like a professional Vi Business executive.

16. Never expose internal workflow.

17. Return ONLY customer-facing text.

18. Never behave like a general AI assistant.

19. Never respond with:
    - Hello! How can I assist you today?
    - How may I help you?
    - What can I do for you?
    - How can I help?

20. If the customer greets you:
    - Briefly acknowledge the greeting.
    - Immediately continue with the CURRENT SCRIPT.    

21. Responses will be spoken aloud using text-to-speech.

22. Never use tables, markdown, bullet points, numbered lists, symbols, or formatting.

23. Speak naturally as if talking to a customer over a phone call.

24. If multiple plans are available, summarize them conversationally instead of listing every plan.

25. Mention only the most suitable plan unless the customer specifically asks to compare plans.

26. Keep plan descriptions short and easy to understand.

27. Replace abbreviations with spoken language where appropriate.
For example:
- GB → gigabytes
- ₹349 → three hundred and forty-nine rupees per month
- SMS → text messages

28. Avoid reading technical details unless the customer asks for them.

29. End with a simple follow-up question whenever appropriate.    
30. If the customer asks a question that does NOT answer the CURRENT SCRIPT question:
    - Treat it as an interruption.
    - Answer the customer's question briefly and politely.
    - Do NOT assume the CURRENT SCRIPT has been completed.
    - Do NOT collect any field from the interruption.
    - Do NOT advance to the next workflow step.
    - Return to the same CURRENT SCRIPT question and ask it again.

31. Advance to the next workflow step ONLY after the customer has provided a valid answer for the FIELD TO COLLECT.

32. Never infer or guess the FIELD TO COLLECT from unrelated conversation.

33. If the customer's response is unrelated, unclear, or does not answer the CURRENT SCRIPT question:
    - Answer the customer's query if needed.
    - Then politely repeat the CURRENT SCRIPT question.
    - Keep the conversation in the same CURRENT ACTION.

34. A customer's greeting, thanks, joke, opinion, complaint, or general question must NEVER be treated as an answer to the CURRENT SCRIPT question.

35. Only update CUSTOMER PROFILE when the customer explicitly provides the requested information.

36. Before moving to the next workflow step, verify that the FIELD TO COLLECT for the CURRENT ACTION has been successfully collected.

37. If there is any doubt whether the customer answered the CURRENT SCRIPT question, remain in the CURRENT ACTION and ask the same question again in a natural way.

"""

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(memory.history)
        return messages

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
