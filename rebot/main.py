import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from pyinvoker.context import ContextDescriptors
from pyinvoker.markdown import MarkdownFormatter
from pyinvoker.usage import Usage
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from rebot.ai.mistral import ChatCompletionRequest, ChatCompletionMessageRole, ChatCompletionMessage, ChatCompletionClient
from rebot.db.main import message_exists, message_create
from rebot.extensions.function_catalog import function_catalog_usage

logging.basicConfig(level=logging.INFO)

load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@dataclass
class UserContext:
    message: str


context_descriptors = ContextDescriptors()
context_descriptors.describe(UserContext, lambda ctx: ctx.message, description="The user's message which to act on.")


def complete(message: str, usage: Usage) -> str:
    formatter = MarkdownFormatter()
    context = UserContext(message)
    markdown_usage = formatter.format_usage(context_descriptors, [context], usage)
    markdown_request = formatter.format_request([context], usage)
    request = ChatCompletionRequest(
        messages=[
            ChatCompletionMessage(
                role=ChatCompletionMessageRole.SYSTEM,
                content=markdown_usage
            ),
            ChatCompletionMessage(
                role=ChatCompletionMessageRole.USER,
                content=markdown_request
            ),
            ChatCompletionMessage(
                role=ChatCompletionMessageRole.USER,
                content="Please provide the input in JSON format."
            ),
        ]
    )
    client = ChatCompletionClient()
    response = client.complete(request)
    response_text = response.choices[0].message.content if response.choices else None
    if not response_text:
        raise Exception("No arguments provided in the response")

    return response_text


@app.event("message")
def event_message(body, say, logger):
    if "bot_id" in body["event"]:
        return

    logger.info(f"observed message: {body}")


@app.event("app_mention")
def event_test(body, say, logger):
    # check that the message is not from any bot
    if "bot_id" in body["event"]:
        return

    message_id = body["event"]["client_msg_id"]
    if message_exists(message_id):
        logger.info(f"message already observed: {message_id}")
        return
    else:
        message_create(message_id)

    logger.info(f"observed mention: {body}")
    message = body["event"]
    message_text = message["text"]

    print("message_text: ", message_text)
    result = complete(message_text, function_catalog_usage)
    print("result: ", result)

    say(f"<@{message['user']}> {result}")


def main():
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()


if __name__ == "__main__":
    main()
