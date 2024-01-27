import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
app = App(token=os.getenv("SLACK_BOT_TOKEN"))


@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")


def main():
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()


if __name__ == "__main__":
    main()
