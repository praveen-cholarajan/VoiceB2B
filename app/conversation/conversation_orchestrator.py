from sympy import true

from app.ai.llm_service import LLMService
from app.ai.prompt_builder import PromptBuilder
from app.ai.response_strategy import ResponseStrategy
from app.campaign.campaign_loader import CampaignLoader
from app.customer.customer_memory import CustomerMemory
from app.rules.business_rule_engine import BusinessRuleEngine
from datetime import datetime
from zoneinfo import ZoneInfo

# class ConversationOrchestrator:
#     def __init__(self):
#         self.campaign = CampaignLoader("vi_business")
#         self.memory = CustomerMemory()
#         self.prompt_builder = PromptBuilder()
#         self.rule_engine = BusinessRuleEngine(self.campaign)
#         self.strategy = ResponseStrategy()
#         self.llm = LLMService()

#     def start(self):
#          # Current time in India (IST)
#         current_time = datetime.now(ZoneInfo("Asia/Kolkata"))
#         current_hour = current_time.hour
#         # Set initial conversation state
#         self.memory.reset()
#         self.memory.update_state("GREETING") 

#         if 5 <= current_hour < 12:
#             greeting = "Hello! Good morning."
#         elif 12 <= current_hour < 17:
#             greeting = "Hello! Good afternoon."
#         elif 17 <= current_hour < 21:
#             greeting = "Hello! Good evening."
#         else:
#             greeting = "Hello!"

#         self.memory.add_ai_message(greeting)
#          # Move to first workflow state
#         self.memory.update_state("ASK_CUSTOMER_NAME")

#         return greeting
    
#     def process(self, customer_message: str):

#         # ----------------------------------------
#         # Save customer message
#         # ----------------------------------------

#         if customer_message:
#             self.memory.add_user_message(customer_message)

#         print("\n===================================")
#         print("Customer :", customer_message)
#         print("Current State :", self.memory.current_state)

#         # ----------------------------------------
#         # Current State
#         # ----------------------------------------

#         state_name = self.memory.current_state
#         state = self.campaign.get_state(state_name)

#         # ----------------------------------------
#         # STEP 1
#         # Validate previous question
#         # ----------------------------------------

#         if state_name == "ASK_CUSTOMER_NAME":

#             # First interaction after greeting
#             completed = True
#             value = customer_message.strip()

#         else:

#             validation_messages = self.prompt_builder.build_validation_prompt(
#                 state_name=state_name,
#                 state_config=state,
#                 memory=self.memory,
#                 campaign=self.campaign,
#             )

#             validation = self.llm.validate(validation_messages)

#             print("\nValidation :", validation)

#             completed = validation.get("completed", False)
#             value = validation.get("value")
        

#         # ----------------------------------------
#         # STEP 2
#         # Save value
#         # ----------------------------------------

#         if completed:

#             collect = state.get("collect")

#             print("Collected :", collect)
#             print("Value :", value)

#             if collect == "customer_name":
#                 self.memory.update_customer_name(value)

#             elif collect == "connection_count":
#                 self.memory.update_connection_count(value)

#             elif collect == "connection_type":
#                 self.memory.update_connection_type(value)

#             elif collect == "current_operator":
#                 self.memory.update_current_operator(value)

#             elif collect == "business_type":
#                 self.memory.update_business_type(value)

#             elif collect == "selected_plan":
#                 self.memory.update_selected_plan(value)

#             # ----------------------------------------
#             # STEP 3
#             # Business Rules
#             # ----------------------------------------

#             rule_result = self.rule_engine.process(
#                 state_name=state_name,
#                 customer_message=customer_message,
#                 memory=self.memory
#             )

#             print("Rule Result :", rule_result)

#             if rule_result.get("move_next"):

#                 next_state = rule_result.get("next_state")

#                 if next_state:

#                     self.memory.update_state(next_state)

#                     print("Moved To :", next_state)

#         else:
#             rule_result = {}    
#             print("Current question not completed.")

#         # ----------------------------------------
#         # STEP 4
#         # Build prompt for CURRENT state
#         # ----------------------------------------

#         state_name = self.memory.current_state
#         state = self.campaign.get_state(state_name)

#         strategy = self.strategy.get_strategy(
#             state_name=state_name,
#             rule_result=rule_result,
#             memory=self.memory
#         )
#         print("strategy :", strategy)
#         conversation_messages = self.prompt_builder.build(
#             state_name=state_name,
#             state_config=state,
#             memory=self.memory,
#             campaign=self.campaign,
#             strategy=strategy
#         ) 
#         # ----------------------------------------
#         # STEP 5
#         # Generate reply ONLY
#         # ----------------------------------------

#         reply = self.llm.generate(conversation_messages)

#         print("\nAI :", reply)

#         self.memory.add_ai_message(reply)

#         return {
#             "reply": reply,
#             "state": self.memory.current_state,
#             "memory": {
#                 "customer_name": self.memory.customer_name,
#                 "connection_count": self.memory.connection_count,
#                 "connection_type": self.memory.connection_type,
#                 "current_operator": self.memory.current_operator,
#                 "business_type": self.memory.business_type,
#                 "selected_plan": self.memory.selected_plan,
#             },
#         }




class ConversationOrchestrator:

    def __init__(self):

        self.campaign = CampaignLoader("vi_business")
        self.memory = CustomerMemory()

        self.prompt_builder = PromptBuilder()
        self.rule_engine = BusinessRuleEngine(self.campaign)
        self.llm = LLMService()

    # =====================================================
    # Start Conversation
    # =====================================================

    def start(self):

        self.memory.reset()

        current_hour = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).hour

        if 5 <= current_hour < 12:
            greeting = "Hello! Good morning."
        elif 12 <= current_hour < 17:
            greeting = "Hello! Good afternoon."
        elif 17 <= current_hour < 21:
            greeting = "Hello! Good evening."
        else:
            greeting = "Hello!"

        first_state = "ASK_CUSTOMER_NAME"

        self.memory.update_state(first_state)

        first_question = self.campaign.get_state(first_state)["script"]

        reply = f"{greeting} {first_question}"

        self.memory.add_ai_message(reply)

        return reply

    # =====================================================
    # Process Customer Message
    # =====================================================

    def process(self, customer_message: str):

        print("\n======================================")
        print("Customer :", customer_message)

        self.memory.add_user_message(customer_message)

        state_name = self.memory.current_state
        state = self.campaign.get_state(state_name)

        print("Current State :", state_name)

        # ----------------------------------------
        # STEP 1
        # Validate customer response
        # ----------------------------------------

        validation_prompt = self.prompt_builder.build_validation_prompt(
            state_name=state_name,
            state_config=state,
            memory=self.memory,
            campaign=self.campaign
        )

        validation = self.llm.validate(validation_prompt)

        print("Validation :", validation)

        completed = validation["completed"]
        value = validation["value"]
        

        # ----------------------------------------
        # STEP 2
        # If answer is valid
        # ----------------------------------------

        if completed:

            self.save_value(
                state["collect"],
                value
            )

            rule_result = self.rule_engine.process(
                state_name=state_name,
                customer_message=customer_message,
                memory=self.memory
            )

            print("Rule Result :", rule_result)

            if rule_result.get("move_next"):

                self.memory.update_state(
                    rule_result["next_state"]
                )

        else:

            print("Customer has NOT answered current question.")

        # ----------------------------------------
        # STEP 3
        # Current state after rules
        # ----------------------------------------

        state_name = self.memory.current_state 
        state = self.campaign.get_state(state_name) 
        strategy = self.strategy.get_strategy(state_name=state_name,
                                               rule_result=rule_result,
                                                 memory=self.memory) 
        print("strategy :", strategy) 
        conversation_messages = self.prompt_builder.build(state_name=state_name, 
                                                          state_config=state, 
                                                          memory=self.memory, 
                                                          campaign=self.campaign, 
                                                          strategy=strategy )

        # ----------------------------------------
        # STEP 4
        # Final Reply
        # ----------------------------------------
        reply = self.llm.generate(conversation_messages) 

        self.memory.add_ai_message(reply)

        print("Reply :", reply)

        return {
            "reply": reply,
            "state": self.memory.current_state,
            "memory": {
                "customer_name": self.memory.customer_name,
                "business_type": self.memory.business_type,
                "connection_count": self.memory.connection_count,
                "connection_type": self.memory.connection_type,
                "current_operator": self.memory.current_operator,
                "selected_plan": self.memory.selected_plan,
            }
        }

    # =====================================================
    # Save Collected Value
    # =====================================================

    def save_value(self, collect, value):

        if not collect:
            return

        print(f"Saving [{collect}] = {value}")

        if collect == "customer_name":
            self.memory.update_customer_name(value)

        elif collect == "connection_count":
            self.memory.update_connection_count(value)

        elif collect == "connection_type":
            self.memory.update_connection_type(value)

        elif collect == "current_operator":
            self.memory.update_current_operator(value)

        elif collect == "business_type":
            self.memory.update_business_type(value)

        elif collect == "selected_plan":
            self.memory.update_selected_plan(value)