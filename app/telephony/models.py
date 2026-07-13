from dataclasses import dataclass


@dataclass
class CallRequest:

    phone_number: str

    customer_name: str = ""

    campaign: str = "vi_business"


@dataclass
class CallResponse:

    success: bool

    call_id: str = ""

    message: str = ""