from enum import Enum

from pyinvoker.usage import Usage

from rebot.extensions.chat_greet import chat_greet_usage
from rebot.extensions.format_markdown import format_markdown_usage
from rebot.extensions.math_z3_solve import math_z3_solve_usage


class CatalogFunction(Enum):
    CHAT_GREET = chat_greet_usage
    FORMAT_MARKDOWN = format_markdown_usage
    MATH_Z3_SOLVE = math_z3_solve_usage


def function_catalog(function: CatalogFunction) -> Usage:
    return function.value


function_catalog_usage = Usage(function_catalog)
function_catalog_usage.example(description="""
user: "Please format this nicely: (...)
""")(function=CatalogFunction.CHAT_GREET.name)

function_catalog_usage.example(description="""
user: "Can you solve x + 1 = 2?"
""")(function=CatalogFunction.MATH_Z3_SOLVE.name)
