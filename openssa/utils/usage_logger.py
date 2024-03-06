from abc import ABC, abstractmethod
from datetime import datetime, timezone
from openai.resources.chat.completions import ChatCompletion


# Abstract Logger
class AbstractUsageLogger(ABC):
    @abstractmethod
    def log_usage(self, **kwargs):
        pass


# Basic Logger
class BasicUsageLogger(AbstractUsageLogger):
    def log_usage(self, **kwargs):
        user_id = kwargs.get("user", "openssa")
        result = kwargs.get("result", {})
        if isinstance(result, ChatCompletion):
            model = result.model
            utc_date_time = datetime.fromtimestamp(result.created, tz=timezone.utc)
            completion_tokens = result.usage.completion_tokens
            prompt_tokens = result.usage.prompt_tokens
            total_tokens = result.usage.total_tokens
            token_info = f"input tokens: {completion_tokens}, ouput tokens: {prompt_tokens}, total: {total_tokens}"
            print(
                f"model: {model}, utc-timestamp: {utc_date_time}, user: {user_id}, {token_info}"
            )
        else:
            print(f"user_id: {user_id}, result: {result}")


# DB Logger (Placeholder for actual implementation)
# class DBUsageLogger(AbstractUsageLogger):
#     def log_usage(self, **kwargs):
#         pass
