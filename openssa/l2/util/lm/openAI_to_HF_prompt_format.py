from __future__ import annotations

from typing import Dict, List, Union

from typing import Literal

# from easyllm.schema.base import ChatMessage
from pydantic import BaseModel

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "function", "system"]
    content: str

def build_llama3_prompt(messages: Union[List[Dict[str, str]], str]) -> str:
    """
    Uses LLama 2 chat tokens (`[INST]`) to create a prompt, learn more in the [Hugging Face Blog on how to prompt Llama 2](https://huggingface.co/blog/llama2#how-to-prompt-llama-2). If a `Message` with an unsupported `role` is passed, an error will be thrown.

    Args:
        messages (:obj:`List[ChatMessage]`): The messages to use for the completion.

    """

    start_prompt = "<s>[INST] "
    end_prompt = " [/INST]"
    conversation = []

    if isinstance(messages, str):
        messages = [ChatMessage(content=messages, role="user")]
    elif isinstance(messages[0], dict):
        messages = [ChatMessage(**message) for message in messages]
    for index, message in enumerate(messages):
        if message.role == "user":
            conversation.append(message.content.strip())
        elif message.role == "assistant":
            conversation.append(f" [/INST] {message.content} </s><s>[INST] ")
        elif message.role == "function":
            raise ValueError("Llama 3 does not support function calls.")
        elif message.role == "system" and index == 0:
            conversation.append(f"<<SYS>>\n{message.content}\n<</SYS>>\n\n")
        else:
            raise ValueError(f"Invalid message role: {message.role}")

    return start_prompt + "".join(conversation) + end_prompt
