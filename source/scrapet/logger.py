from abc import ABC, abstractmethod


class Logger(ABC):
    """Documentation for Logger
    
    """
    def __init__(self):
        super(Logger, self).__init__()
    
    @abstractmethod
    def update_progress(self, percent_complete):
        pass
    
    # Importance is a number from 0-1
    @abstractmethod
    def log_event(self, importance, text):
        pass
