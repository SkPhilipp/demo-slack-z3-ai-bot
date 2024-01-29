from rebot.ai.functions import FunctionPackage

package_search = FunctionPackage(name="search")


@package_search.registered(
    name="search.google",
    description="Searches Google for a query",
    examples=["""
    user: Can you tell me about Python?
    assistant: python programming
    """],
    inputs="A string query"
)
def search__google(query: str):
    return f"https://lmgtfy.app/?q={query}"
