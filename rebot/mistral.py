import json
import os
from enum import Enum
from typing import List, Optional

import requests
from dotenv import load_dotenv


class ChatCompletionMessageRole(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


class ChatCompletionMessage:
    def __init__(self, role: "ChatCompletionMessageRole", content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role.value, "content": self.content}

    def __repr__(self):
        return f"<ChatCompletionMessage(role={self.role}, content={self.content})>"


class ChatCompletionRequest:
    def __init__(self, messages: List["ChatCompletionMessage"],
                 model: str = "mistral-medium",
                 temperature: float = 0.7,
                 top_p: float = 1.0,
                 max_tokens: int = 500,
                 stream: bool = False,
                 safe_prompt: bool = False,
                 random_seed: Optional[int] = None):
        self.model = model
        self.messages = messages
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.stream = stream
        self.safe_prompt = safe_prompt
        self.random_seed = random_seed

    def to_dict(self):
        return {
            "model": self.model,
            "messages": [message.to_dict() for message in self.messages],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "stream": self.stream,
            "safe_prompt": self.safe_prompt,
            "random_seed": self.random_seed,
        }

    def __repr__(self):
        return f"<ChatCompletionRequest(model={self.model}, messages={self.messages}, temperature={self.temperature}, top_p={self.top_p}, max_tokens={self.max_tokens}, stream={self.stream}, safe_prompt={self.safe_prompt}, random_seed={self.random_seed})>"


class ChatCompletionResponseChoice:
    def __init__(self, index: int, message: "ChatCompletionMessage", finish_reason: str):
        self.index = index
        self.message = message
        self.finish_reason = finish_reason

    @staticmethod
    def from_dict(response_dict):
        return ChatCompletionResponseChoice(
            index=response_dict["index"],
            message=ChatCompletionMessage(
                role=ChatCompletionMessageRole(response_dict["message"]["role"]),
                content=response_dict["message"]["content"],
            ),
            finish_reason=response_dict["finish_reason"],
        )

    def __repr__(self):
        return f"<ChatCompletionResponseChoice(index={self.index}, message={self.message}, finish_reason={self.finish_reason})>"


class ChatCompletionResponseUsage:
    def __init__(self, prompt_tokens: int, total_tokens: int, completion_tokens: int):
        self.prompt_tokens = prompt_tokens
        self.total_tokens = total_tokens
        self.completion_tokens = completion_tokens

    @staticmethod
    def from_dict(response_dict):
        return ChatCompletionResponseUsage(
            prompt_tokens=response_dict["prompt_tokens"],
            total_tokens=response_dict["total_tokens"],
            completion_tokens=response_dict["completion_tokens"],
        )

    def __repr__(self):
        return f"<ChatCompletionResponseUsage(prompt_tokens={self.prompt_tokens}, total_tokens={self.total_tokens}, completion_tokens={self.completion_tokens})>"


class ChatCompletionResponse:
    def __init__(self, response_id: str, response_object: str, created: int, model: str, choices: List["ChatCompletionResponseChoice"],
                 usage: "ChatCompletionResponseUsage"):
        self.id = response_id
        self.object = response_object
        self.created = created
        self.model = model
        self.choices = choices
        self.usage = usage

    @staticmethod
    def from_dict(response_dict):
        return ChatCompletionResponse(
            response_id=response_dict["id"],
            response_object=response_dict["object"],
            created=response_dict["created"],
            model=response_dict["model"],
            choices=[ChatCompletionResponseChoice.from_dict(choice) for choice in response_dict["choices"]],
            usage=ChatCompletionResponseUsage.from_dict(response_dict["usage"]),
        )

    def __repr__(self):
        return f"<ChatCompletionResponse(id={self.id}, object={self.object}, created={self.created}, model={self.model}, choices={self.choices}, usage={self.usage})>"


class ChatCompletionClient:
    def __init__(self, token: str = None, base_url: str = "https://api.mistral.ai"):
        if token is None:
            load_dotenv()
            token = os.getenv("MISTRAL_API_KEY")
        self._token = token
        self._base_url = base_url

    def complete(self, request: "ChatCompletionRequest"):
        """
        Refer to https://docs.mistral.ai/api/

        :param request: A ChatCompletionRequest object.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
        print("Sending request to Mistral API...")
        response = requests.post(f"{self._base_url}/v1/chat/completions", headers=headers, data=json.dumps(request.to_dict()))
        response.raise_for_status()
        print("Received response from Mistral API")
        return ChatCompletionResponse.from_dict(response.json())


if __name__ == "__main__":
    client = ChatCompletionClient()
    print(client.complete(ChatCompletionRequest(
        max_tokens=50,
        messages=[
            ChatCompletionMessage(role=ChatCompletionMessageRole.SYSTEM, content="Answer the following within 50 characters:"),
            ChatCompletionMessage(role=ChatCompletionMessageRole.USER, content="Hello, how are you?"),
        ],
    )))
