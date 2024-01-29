import logging
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from rebot.ai.functions import FunctionCatalog
from rebot.ai.service import FunctionService
from rebot.db.main import message_exists, message_create
from rebot.fnchat.main import package_chat
from rebot.fnformat.main import package_format
from rebot.fnmath.main import package_math
from rebot.fnsearch.main import package_search

logging.basicConfig(level=logging.INFO)

load_dotenv()

function_catalog = FunctionCatalog(packages=[
    package_search,
    package_math,
    package_format,
    package_chat
])
function_service = FunctionService(function_catalog)

app = App(token=os.getenv("SLACK_BOT_TOKEN"))


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
    function = function_service.complete_function(message["text"])
    args = function_service.complete_inputs(message["text"], function)
    result = function.callback(args)
    say(f"<@{message['user']}> {result}")


def main():
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()


if __name__ == "__main__":
    main()
