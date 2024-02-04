from pyinvoker.usage import Usage


def format_markdown(markdown: str):
    return markdown


format_markdown_usage = Usage(format_markdown)
format_markdown_usage.example(description="""
user: "Can you make this into markdown? schedule: breakfast at 9, meeting at 10:10, dinner at 1800"
""")(expression="""
# Schedule
- 09:00 Breakfast
- 10:10 Meeting
- 18:00 Dinner
""")
