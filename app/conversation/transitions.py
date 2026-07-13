"""
Conversation Transition Rules

This module decides the next state based on:

1. Current State
2. Extracted Customer Information

The LLM NEVER decides the conversation flow.
"""

from typing import Dict, Optional


class TransitionManager:

    def __init__(self, campaign):

        self.campaign = campaign

    # ---------------------------------------------------------
    # Get Next State
    # ---------------------------------------------------------

    def get_next_state(
        self,
        current_state: str,
        extracted: Dict
    ) -> Optional[str]:

        state = self.campaign["states"][current_state]

        transition = state.get("next")

        # -----------------------------------
        # Simple Transition
        # -----------------------------------

        if isinstance(transition, str):
            return transition

        # -----------------------------------
        # Branch Transition
        # -----------------------------------

        if not isinstance(transition, dict):
            return None

        # GREETING
        if current_state == "ASK_TALK_TIME":

            if extracted.get("talk_permission") is True:
                return transition["yes"]

            return transition["no"]

        # -----------------------------------

        if current_state == "ASK_CONNECTION_TYPE":

            value = extracted.get("connection_type", "").lower()

            if value == "port":
                return transition["port"]

            return transition["new"]

        # -----------------------------------

        if current_state == "EXISTING_CUSTOMER":

            if extracted.get("existing_vi_customer") is True:
                return transition["yes"]

            return transition["no"]

        return None

    # ---------------------------------------------------------
    # Validate
    # ---------------------------------------------------------

    def is_valid_state(self, state_name):

        return state_name in self.campaign["states"]

    # ---------------------------------------------------------

    def available_states(self):

        return list(self.campaign["states"].keys())