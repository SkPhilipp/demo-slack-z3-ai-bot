import os

from slack_bolt import App

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
