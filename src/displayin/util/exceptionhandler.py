from abc import ABC, abstractmethod

# Base Class Exception Handler
class ExceptionHandler(ABC):

    @abstractmethod
    def handle(self, ex: Exception):
        pass
