from app.rules.greeting_rule import GreetingRule
from app.rules.connection_rule import ConnectionRule
from app.rules.operator_rule import OperatorRule
from app.rules.plan_rule import PlanRule
from app.rules.document_rule import DocumentRule
from app.rules.objection_rule import ObjectionRule
from app.rules.schedule_rule import ScheduleRule
from app.nlp.signal_detector import SignalDetector


class BusinessRuleEngine:

    def __init__(self, campaign):

        self.campaign = campaign

        self.signal_detector = SignalDetector()

        self.objection_rule = ObjectionRule()

        # State-specific rules
        self.rules = {

            "GREETING": GreetingRule(),
            
            "ASK_CUSTOMER_NAME": GreetingRule(),
            
            "INTRODUCE_SELF": GreetingRule(),

            "ASK_TALK_TIME": GreetingRule(),

            "CALLBACK": ScheduleRule(),

            "ASK_CONNECTION_COUNT": ConnectionRule(),

            "ASK_CONNECTION_TYPE": ConnectionRule(),

            "ASK_OPERATOR": OperatorRule(),

            "PLAN_INTRO": PlanRule(),

            "RECOMMEND_PLAN": PlanRule(),

            "EXISTING_CUSTOMER": PlanRule(),

            "ASK_BUSINESS_TYPE": DocumentRule(campaign),

            "DOCUMENTS": DocumentRule(campaign),

            "SCHEDULE_VISIT": ScheduleRule(),
        }

    # =====================================================
    # MAIN PROCESS
    # =====================================================

    def process(self, state_name, customer_message, memory):

        signal = self.signal_detector.detect(customer_message)

        result = {
            "completed": False,
            "move_next": False,
            "next_state": None,
            "intent": signal.get("intent"),
            "emotion": signal.get("emotion"),
            "urgency": signal.get("urgency"),
            "extracted": {}
        }

        # -------------------------------------------------
        # 1. Objection Detection (does NOT change state)
        # -------------------------------------------------
        objection = self.objection_rule.process(
            state_name=state_name,
            customer_message=customer_message,
            memory=memory
        )

        if objection:
            result["extracted"].update(objection)
            # Objection is stored in memory; ResponseStrategy handles it.
            # We do NOT return early here – flow continues normally.
            # The LLM will handle the objection and stay in the same state.
            return result

        # -------------------------------------------------
        # 2. Get state-specific rule
        # -------------------------------------------------
        rule = self.rules.get(state_name)

        if rule:
            extracted = rule.process(
                state_name=state_name,
                customer_message=customer_message,
                memory=memory
            )
            if extracted:
                result["extracted"].update(extracted)

        # -------------------------------------------------
        # 3. Get state config
        # -------------------------------------------------
        state_config = self.campaign.get_state(state_name)

        if not state_config:
            return result

        transitions = state_config.get("transitions", state_config.get("next", {}))

        # -------------------------------------------------
        # 4. Build effective intent for transition matching
        # -------------------------------------------------
        intent = signal.get("intent")

        # --- GREETING: confirm person → YES goes to ASK_TALK_TIME ---
        # -------------------------------------------------
        # GREETING
        # -------------------------------------------------
        if state_name == "GREETING":

            result["move_next"] = True
            result["completed"] = True
            result["next_state"] = "ASK_CUSTOMER_NAME"

            return result


        # -------------------------------------------------
        # ASK CUSTOMER NAME
        # -------------------------------------------------
        elif state_name == "ASK_CUSTOMER_NAME":

            # GreetingRule already extracts and stores the name
            if memory.customer_name:

                result["move_next"] = True
                result["completed"] = True
                result["next_state"] = "INTRODUCE_SELF"

            return result


        # -------------------------------------------------
        # INTRODUCE SELF
        # -------------------------------------------------
        elif state_name == "INTRODUCE_SELF":

            # No input required from customer.
            # After AI introduces itself, move to the next state.

            result["move_next"] = True
            result["completed"] = True
            result["next_state"] = "ASK_TALK_TIME"

            return result


        # -------------------------------------------------
        # ASK TALK TIME
        # -------------------------------------------------
        elif state_name == "ASK_TALK_TIME":
            if memory.talk_permission is True:
                intent = "yes"
            elif memory.talk_permission is False:
                intent = "no"

        # --- ASK_CONNECTION_COUNT: count captured → move next ---
        elif state_name == "ASK_CONNECTION_COUNT":
            if memory.connection_count is not None:
                result["move_next"] = True
                result["completed"] = True
                next_s = transitions if isinstance(transitions, str) else transitions.get("next", "ASK_CONNECTION_TYPE")
                result["next_state"] = next_s
                return result

        # --- ASK_CONNECTION_TYPE: type captured ---
        elif state_name == "ASK_CONNECTION_TYPE":
            if memory.connection_type:
                intent = memory.connection_type.lower()

        # --- ASK_OPERATOR: operator captured → move to PLAN_INTRO ---
        elif state_name == "ASK_OPERATOR":
            if memory.current_operator:
                result["move_next"] = True
                result["completed"] = True
                result["next_state"] = transitions if isinstance(transitions, str) else "PLAN_INTRO"
                return result

        # --- PLAN_INTRO: always move next (no collect required) ---
        elif state_name == "PLAN_INTRO":
            result["move_next"] = True
            result["completed"] = True
            result["next_state"] = transitions if isinstance(transitions, str) else "RECOMMEND_PLAN"
            return result

        # --- RECOMMEND_PLAN: move next on YES/acceptance ---
        elif state_name == "RECOMMEND_PLAN":
            if intent in ("YES", "yes") or any(
                w in customer_message.lower() for w in [
                    "yes", "okay", "ok", "sounds good", "fine", "agree", "that's good", "perfect"
                ]
            ):
                result["move_next"] = True
                result["completed"] = True
                result["next_state"] = transitions if isinstance(transitions, str) else "EXISTING_CUSTOMER"
                return result

        # --- EXISTING_CUSTOMER: branch on yes/no ---
        elif state_name == "EXISTING_CUSTOMER":
            if memory.existing_vi_customer is True:
                intent = "yes"
            elif memory.existing_vi_customer is False:
                intent = "no"

        # --- EXISTING_PROCESS: always move to SCHEDULE_VISIT ---
        elif state_name == "EXISTING_PROCESS":
            result["move_next"] = True
            result["completed"] = True
            result["next_state"] = transitions if isinstance(transitions, str) else "SCHEDULE_VISIT"
            return result

        # --- ASK_BUSINESS_TYPE: type captured → DOCUMENTS ---
        elif state_name == "ASK_BUSINESS_TYPE":
            if memory.business_type:
                result["move_next"] = True
                result["completed"] = True
                result["next_state"] = transitions if isinstance(transitions, str) else "DOCUMENTS"
                return result

        # --- DOCUMENTS: only move next when customer acknowledges ---
        elif state_name == "DOCUMENTS":
            # Customer must explicitly acknowledge (ok, understood, got it)
            ack_words = [
                "ok", "okay", "understood", "got it", "noted", "sure",
                "alright", "fine", "yes", "yeah", "thanks", "thank you"
            ]
            msg_lower = customer_message.lower()
            if any(w in msg_lower for w in ack_words):
                memory.documents_acknowledged = True
                result["move_next"] = True
                result["completed"] = True
                result["next_state"] = transitions if isinstance(transitions, str) else "SCHEDULE_VISIT"
                return result

        # --- SCHEDULE_VISIT: pickup_text captured → CLOSING ---
        elif state_name == "SCHEDULE_VISIT":
            if memory.pickup_text:
                result["move_next"] = True
                result["completed"] = True
                result["next_state"] = transitions if isinstance(transitions, str) else "CLOSING"
                return result

        # --- CALLBACK: callback_text captured → END ---
        elif state_name == "CALLBACK":
            if memory.callback_text:
                result["move_next"] = True
                result["completed"] = True
                result["next_state"] = transitions if isinstance(transitions, str) else "END"
                return result

        # --- CLOSING: move to END ---
        elif state_name == "CLOSING":
            result["move_next"] = True
            result["completed"] = True
            result["next_state"] = transitions if isinstance(transitions, str) else "END"
            return result

        # -------------------------------------------------
        # 5. Transition matching (YES/NO branches)
        # -------------------------------------------------
        # -------------------------------------------------
        # Transition matching
        # -------------------------------------------------
        print("State:", state_name)
        print("Signal Intent:", signal.get("intent"))
        print("Intent:", intent)
        print("Transitions:", transitions)

        if isinstance(transitions, dict):

            key = intent.lower() if intent else ""
            print("Transitions key :", key)
            print("Transitions 1:", transitions[key])
            if key in transitions:

                result["move_next"] = True
                result["completed"] = True
                result["next_state"] = transitions[key]

                return result

        elif isinstance(transitions, str):
            print("Transitions 2:", transitions)
            result["move_next"] = True
            result["completed"] = True
            result["next_state"] = transitions

            return result