from abc import ABC, abstractmethod


class FAQPort(ABC):

    @abstractmethod
    def get_answer(self, question: str) -> str | None:
        pass
