from rebot.ai.functions import FunctionPackage

package_chat = FunctionPackage(name="chat")


@package_chat.registered(
    name="chat.greet",
    description="Greets a user",
    examples=["""
    user: Hey bot guy
    assistant: Hello!
    """],
    inputs="A message for the user"
)
def chat__greet(greet: str):
    # this is a guiding prompt only
    return greet
