import json
import logging
import re
from dataclasses import dataclass

from dotenv import load_dotenv
from pyinvoker.context import ContextDescriptors
from pyinvoker.markdown import MarkdownFormatter

from rebot.extensions.function_catalog import function_catalog_usage
from rebot.mistral import ChatCompletionRequest, ChatCompletionMessageRole, ChatCompletionMessage, ChatCompletionClient

logging.basicConfig(level=logging.INFO)

load_dotenv()


@dataclass
class UserContext:
    message: str


context_descriptors = ContextDescriptors()
context_descriptors.describe(UserContext, lambda ctx: ctx.message, description="The user's message which to act on.")

usage = function_catalog_usage
formatter = MarkdownFormatter()
context = UserContext("Hey man")
markdown_usage = formatter.format_usage(context_descriptors, [context], usage)
markdown_request = formatter.format_request([context], usage)
request = ChatCompletionRequest(
    messages=[
        ChatCompletionMessage(
            role=ChatCompletionMessageRole.SYSTEM,
            content="""
You are an AI assistant that helps users determine inputs for their highly specific task. Refer to the function's documentation, examples and context for help.
You must always answer with inputs to the best of your ability, refer to the context if you don't know what to write. Provide a single answer only.
"""
        ),
        ChatCompletionMessage(
            role=ChatCompletionMessageRole.SYSTEM,
            content=markdown_usage
        ),
        ChatCompletionMessage(
            role=ChatCompletionMessageRole.USER,
            content=markdown_request
        ),
    ]
)
client = ChatCompletionClient()
response = client.complete(request)
response_text = response.choices[0].message.content if response.choices else None


def extract_code_blocks(text):
    pattern = r"```(json)?(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    groups = [match[1] for match in matches]
    return json.loads(groups[0]) if groups else None


code_blocks = extract_code_blocks(response_text)
print(code_blocks)
