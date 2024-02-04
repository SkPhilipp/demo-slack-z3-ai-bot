from pyinvoker.usage import Usage


def chat_greet(greet: str):
    return greet


chat_greet_usage = Usage(chat_greet)
chat_greet_usage.example(description="""
user: "Hey bot guy"
""")(expression="""
Hello!
""")
