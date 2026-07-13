from typing import Dict


class StateMachine:

    def __init__(self, campaign):

        self.campaign = campaign

        self.states: Dict = campaign.states

        self.current_state = campaign.start_state

    # =====================================================
    # Current State Name
    # =====================================================

    def get_current_state(self) -> str:

        return self.current_state

    # =====================================================
    # Current State Configuration
    # =====================================================

    def get_state(self):

        return self.campaign.get_state(
            self.current_state
        )

    # =====================================================
    # Move Next
    # =====================================================

    def next_state(self):

        next_state = self.campaign.get_next_state(
            self.current_state
        )

        if next_state is not None:

            self.current_state = next_state

        return self.current_state

    # =====================================================
    # Jump To State
    # =====================================================

    def goto(self, state_name):

        if self.campaign.has_state(state_name):

            self.current_state = state_name

        return self.current_state

    # =====================================================
    # Previous State
    # =====================================================

    def previous_state(self):

        for name, state in self.states.items():

            if state.get("next") == self.current_state:

                self.current_state = name

                break

        return self.current_state

    # =====================================================
    # Completed
    # =====================================================

    def is_completed(self):

        return self.campaign.is_last_state(
            self.current_state
        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.current_state = self.campaign.start_state

    # =====================================================
    # Helpers
    # =====================================================

    def has_state(self, state_name):

        return self.campaign.has_state(
            state_name
        )

    def all_states(self):

        return list(self.states.keys())

    def __repr__(self):

        return (
            f"StateMachine("
            f"current_state='{self.current_state}')"
        )