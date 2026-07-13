from datetime import datetime


class CustomerMemory:

    def __init__(self):

        # ----------------------------------------
        # Customer Information
        # ----------------------------------------

        self.customer_name = None

        self.business_type = None

        self.connection_count = None

        self.connection_type = None

        self.current_operator = None

        self.existing_vi_customer = None

        self.selected_plan = None

        self.recommended_plan = None

        self.special_offer = False

        # ----------------------------------------
        # Conversation
        # ----------------------------------------

        self.history = []

        self.current_state = "GREETING"

        self.talk_permission = None

        # ----------------------------------------
        # Schedule
        # ----------------------------------------

        self.callback_text = None

        self.pickup_text = None

        # ----------------------------------------
        # Documents
        # ----------------------------------------

        self.required_documents = []

        self.documents_acknowledged = False

        # ----------------------------------------
        # Objections
        # ----------------------------------------

        self.objections = []

        # ----------------------------------------
        # Audit
        # ----------------------------------------

        self.created_at = datetime.now()

    # =====================================================
    # Conversation History
    # =====================================================

    def add_user_message(self, message):

        self.history.append(
            {
                "role": "user",
                "content": message
            }
        )

    def add_ai_message(self, message):

        self.history.append(
            {
                "role": "assistant",
                "content": message
            }
        )

    def last_user_message(self):

        for message in reversed(self.history):

            if message["role"] == "user":

                return message["content"]

        return ""

    # =====================================================
    # Customer Information
    # =====================================================

    def update_customer_name(self, name):

        self.customer_name = name

    def update_connection_count(self, count):

        self.connection_count = count

    def update_connection_type(self, connection_type):

        self.connection_type = connection_type

    def update_current_operator(self, operator):

        self.current_operator = operator

    def update_business_type(self, business_type):

        self.business_type = business_type

    def update_existing_vi_customer(self, value):

        self.existing_vi_customer = value

    def update_selected_plan(self, plan):

        self.selected_plan = plan

    def update_recommended_plan(self, plan):

        self.recommended_plan = plan

    # =====================================================
    # Schedule
    # =====================================================

    def update_callback(self, callback):

        self.callback_text = callback

    def update_pickup(self, pickup):

        self.pickup_text = pickup

    # =====================================================
    # Documents
    # =====================================================

    def set_required_documents(self, documents):

        self.required_documents = documents

    def acknowledge_documents(self):

        self.documents_acknowledged = True

    # =====================================================
    # Objections
    # =====================================================

    def add_objection(self, objection):

        if objection not in self.objections:

            self.objections.append(objection)

    # =====================================================
    # Conversation State
    # =====================================================

    def update_state(self, state):

        self.current_state = state

    # =====================================================
    # Reset Conversation
    # =====================================================

    def reset(self):

        self.__init__()