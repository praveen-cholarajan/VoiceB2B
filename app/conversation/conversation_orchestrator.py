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

        rule_result = self.rule_engine.process(
            state_name=state_name,
            customer_message=customer_message,
            memory=self.memory,
        )
        print("Rule Result :", rule_result)

        if rule_result.get("move_next"):
            next_state = rule_result["next_state"]
            print("Next State :", next_state)

            self.memory.update_state(next_state)
            state_name = next_state
            state = self.campaign.get_state(state_name)

        strategy = self.strategy.get_strategy(
            state_name=state_name,
            rule_result=rule_result,
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
        reply = self.llm.generate(messages)
        print("AI :", reply)

        self.memory.add_ai_message(reply)

        return {
            "reply": reply,
            "state": state_name,
            "memory": {
                "customer_name": self.memory.customer_name,
                "connection_count": self.memory.connection_count,
                "connection_type": self.memory.connection_type,
                "current_operator": self.memory.current_operator,
                "business_type": self.memory.business_type,
                "selected_plan": self.memory.selected_plan,
            },
        }
