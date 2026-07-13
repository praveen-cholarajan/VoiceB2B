from app.conversation.state_machine import StateMachine


class ConversationManager:

    def __init__(self, campaign):

        self.state_machine = StateMachine(campaign)

    # -----------------------------------------
    # Current State Name
    # -----------------------------------------

    def get_current_state(self):

        return self.state_machine.get_current_state()

    # -----------------------------------------
    # Current State Config
    # -----------------------------------------

    def get_state(self):

        return self.state_machine.get_state()

    # -----------------------------------------
    # Next State
    # -----------------------------------------

    def next_state(self):

        return self.state_machine.next_state()

    # -----------------------------------------
    # Go To State
    # -----------------------------------------

    def goto(self, state_name):

        return self.state_machine.goto(state_name)

    # -----------------------------------------
    # Reset
    # -----------------------------------------

    def reset(self):

        self.state_machine.reset()

    # -----------------------------------------
    # Completed
    # -----------------------------------------

    def is_completed(self):

        return self.state_machine.is_completed()