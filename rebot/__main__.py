import fire
from rebot.main import CLI


def main():
    fire.Fire(component=CLI, name="re-bot")


if __name__ == "__main__":
    main()
