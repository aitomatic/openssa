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
    NOTIFICATION = "notification"
    SUBTASK = "ooda-subtask"
    MAINTASK = "ooda-maintask"
    EXECUTING = "executing"
    TASK_RESULT = "task_result"

# Example usage:
# notifier = SimpleNotifier()
# notifier.notify(EventTypes.NOTIFICATION, {"message": "Task completed successfully"})
