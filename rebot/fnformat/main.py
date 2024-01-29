from rebot.ai.functions import FunctionPackage

package_format = FunctionPackage(name="format")


@package_format.registered(
    name="format.markdown",
    description="Formats a markdown document",
    examples=["""
    user: Can you make this into markdown? schedule: breakfast at 9, meeting at 10:10, dinner at 1800
    assistant:
    # Schedule
    - 09:00 Breakfast
    - 10:10 Meeting
    - 18:00 Dinner
    """],
    inputs="Markdown document content"
)
def format__markdown(markdown: str):
    # this is a guiding prompt only
    return markdown
