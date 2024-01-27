import os
from slack_bolt.adapter.socket_mode import SocketModeHandler

from rebot.main import app


def main():
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


if __name__ == "__main__":
    main()
