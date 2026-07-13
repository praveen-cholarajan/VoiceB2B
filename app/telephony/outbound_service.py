from abc import ABC, abstractmethod

from app.telephony.models import CallRequest, CallResponse


class OutboundService(ABC):

    @abstractmethod
    def make_call(
        self,
        request: CallRequest
    ) -> CallResponse:
        pass