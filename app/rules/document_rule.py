from app.rules.base_rule import BaseRule


class DocumentRule(BaseRule):

    STATES = [
        "ASK_BUSINESS_TYPE",
        "DOCUMENTS"
    ]

    BUSINESS_TYPES = {
        "private_limited": [
            "private limited",
            "pvt ltd",
            "private ltd",
            "limited company",
            "ltd company"
        ],
        "partnership": [
            "partnership",
            "partnership firm",
            "partner firm"
        ],
        "proprietorship": [
            "proprietorship",
            "proprietor",
            "sole proprietor",
            "sole proprietorship",
            "individual business"
        ]
    }

    def __init__(self, campaign):
        self.campaign = campaign

    def can_handle(self, state_name):
        return state_name in self.STATES

    def process(
        self,
        state_name,
        customer_message,
        memory
    ):
        extracted = {}
        
        # Always try to extract business type
        business_type = self.extract_business_type(customer_message)
        if business_type:
            memory.business_type = business_type
            extracted["business_type"] = business_type
            docs = self.load_documents(business_type)
            memory.required_documents = docs
            extracted["required_documents"] = docs
            return extracted

        if state_name == "DOCUMENTS":
            extracted["required_documents"] = memory.required_documents
            return extracted

        return extracted

    def extract_business_type(self, text):
        text = text.lower()
        for business_type, keywords in self.BUSINESS_TYPES.items():
            for keyword in keywords:
                if keyword in text:
                    return business_type
        return None

    def load_documents(self, business_type):
        return self.campaign.get_documents(business_type)
