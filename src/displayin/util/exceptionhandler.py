from abc import ABC, abstractmethod

# Base Class Exception Handler
class ExceptionHandler(ABC):
    def __init__(self, logger=None):
        self.logger = logger
        
    @abstractmethod
    def handle(self, ex: Exception):
        pass
