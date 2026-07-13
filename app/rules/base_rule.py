from abc import ABC, abstractmethod


class BaseRule(ABC):
    """
    Base class for all conversation rules.

    Every rule should:
    1. Check whether it can handle the current state.
    2. Extract structured information.
    3. Update memory.
    4. Return extracted fields.
    """

    @abstractmethod
    def can_handle(self, state_name: str) -> bool:
        """
        Return True if this rule can process the current state.
        """
        pass

    @abstractmethod
    def process(
        self,
        customer_message: str,
        memory
    ) -> dict:
        """
        Process customer message.

        Returns example:

        {
            "customer_name": "Ravi",
            "talk_permission": True
        }
        """
        pass