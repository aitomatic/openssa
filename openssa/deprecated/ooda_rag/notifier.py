from abc import ABC, abstractmethod
from typing import Any, Dict


class Notifier(ABC):
    @abstractmethod
    def notify(self, event: str, data: Dict[str, Any]) -> None:
        """Send a notification with event type and data."""
        pass


class SimpleNotifier(Notifier):
    def notify(self, event: str, data: Dict[str, Any]) -> None:
        print(f"Event: {event}, Data: {data}")


class EventTypes:
    MAINTASK = "ooda-maintask"
    MAIN_PROBELM_STATEMENT = "ooda-main-problem-statement"
    NOTIFICATION = "notification"
    SUBTASK = "ooda-subtask"
    SUBTASK_BEGIN = "ooda-subtask-begin"
    TASK_RESULT = "task_result"
    SWICTH_MODE = "switch_mode"
