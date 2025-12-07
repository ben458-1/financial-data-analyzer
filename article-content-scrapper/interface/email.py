from abc import ABC, abstractmethod


class EmailInterface(ABC):
    @abstractmethod
    def get_subject(self, context: dict) -> str:
        pass

    @abstractmethod
    def get_template_name(self) -> str:
        pass

    @abstractmethod
    def prepare_context(self, raw_data: dict) -> dict:
        pass
