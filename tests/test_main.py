from rebot.main import CLI


def test_cli():
    cli = CLI(name="World")
    answer = cli.hello()
    assert answer == "Hello World"
