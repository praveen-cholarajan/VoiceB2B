from app.ai.llm_service import LLMService
from app.ai.prompt_builder import PromptBuilder
from app.ai.response_strategy import ResponseStrategy
from app.campaign.campaign_loader import CampaignLoader
from app.customer.customer_memory import CustomerMemory
from app.rules.business_rule_engine import BusinessRuleEngine
from datetime import datetime
from zoneinfo import ZoneInfo

class ConversationOrchestrator:
    def __init__(self):
        self.campaign = CampaignLoader("vi_business")
        self.memory = CustomerMemory()
        self.prompt_builder = PromptBuilder()
        self.rule_engine = BusinessRuleEngine(self.campaign)
        self.strategy = ResponseStrategy()
        self.llm = LLMService()

    def start(self):
         # Current time in India (IST)
        current_time = datetime.now(ZoneInfo("Asia/Kolkata"))
        current_hour = current_time.hour
        # Set initial conversation state
        self.memory.reset()
        self.memory.update_state("GREETING") 

        if 5 <= current_hour < 12:
            greeting = "Hello! Good morning."
        elif 12 <= current_hour < 17:
            greeting = "Hello! Good afternoon."
        elif 17 <= current_hour < 21:
            greeting = "Hello! Good evening."
        else:
            greeting = "Hello!"

        self.memory.add_ai_message(greeting)
        return greeting
    
    def process(self, customer_message: str):

        if customer_message:
            self.memory.add_user_message(customer_message)

        state_name = self.memory.current_state
        state = self.campaign.get_state(state_name)

        print("\n===================================")
        print("Current State :", state_name)
        print("Customer      :", customer_message)

        strategy = self.strategy.get_strategy(
            state_name=state_name,
            rule_result={},
            memory=self.memory,
        )

        print("Strategy :", strategy)

        messages = self.prompt_builder.build(
            state_name=state_name,
            state_config=state,
            memory=self.memory,
            campaign=self.campaign,
            strategy=strategy,
        )

        print("\nGenerating AI Response...")

        ai_result = self.llm.generate(messages)

        print("LLM Result :", ai_result)

        completed = ai_result.get("completed", False)
        value = ai_result.get("value")
        reply = ai_result.get("reply", "")

        # --------------------------------------
        # Update Memory
        # --------------------------------------

        if completed:

            collect = state.get("collect")

            print("Collected Field :", collect)
            print("Collected Value :", value)

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

            next_state = state.get("next_state")

            if next_state:

                print("Moving to Next State :", next_state)

                self.memory.update_state(next_state)

                state_name = next_state

        else:

            print("Current question not answered. Staying in :", state_name)

        self.memory.add_ai_message(reply)

        return {
            "reply": reply,
            "state": self.memory.current_state,
            "memory": {
                "customer_name": self.memory.customer_name,
                "connection_count": self.memory.connection_count,
                "connection_type": self.memory.connection_type,
                "current_operator": self.memory.current_operator,
                "business_type": self.memory.business_type,
                "selected_plan": self.memory.selected_plan,
            },
        }
