import re
from typing import Optional

from rebot.ai.functions import Function, FunctionCatalog
from rebot.ai.mistral import ChatCompletionClient, ChatCompletionRequest, ChatCompletionMessageRole, ChatCompletionMessage


class FunctionService:
    def __init__(self, catalog: FunctionCatalog,
                 completion_client: ChatCompletionClient = ChatCompletionClient()):
        self.function_catalog: FunctionCatalog = catalog
        self.completion_client: ChatCompletionClient = completion_client

    def _remove_quotes(self, message: str) -> str:
        """
        Removes quotes from the beginning and end of a string

        :param message:
        :return:
        """
        quotes = ["\"", "'"]
        if message[0] in quotes and message[-1] in quotes:
            return message[1:-1]
        return message

    def complete_function(self, query: str) -> Function:
        """
        Generates a function associated with resolving a given user query.

        :param query:
        :return:
        """
        request = ChatCompletionRequest(
            messages=[
                ChatCompletionMessage(
                    role=ChatCompletionMessageRole.SYSTEM,
                    content=f"""Your current task is to select the function most likely to resolve the user's request.

                            The following functions are available:
                            {self.function_catalog.format_basic()}

                            Answer exclusively with a function name.
                            Provide no explanation.

                            Example:
                            - user: "What is the weather like today?"
                            - you: "search.google" (PERFECT ANSWER)

                            Counterexample:
                            - user: "I wonder what Pandas look like"
                            - you: "I think you should search.google because ..." (WRONG; should have answered "search.google")

                            Example:
                            - user: "Hey bot what's the square root of Pi"
                            - you: "math.solve" (PERFECT ANSWER)

                            Counterexample:
                            - user: "What is 1 + 1?"
                            - you: "math.solve Note: As an AI bla bla bla ..." (WRONG; should have answered "math.solve")

                            Counterexample:
                            - user: "Given x > 100 and x < 10 what is a possible value for x?"
                            - you: "math.solve Note: This answer is bla bla bla" (WRONG; should have answered "math.solve")
                            """
                ),
                ChatCompletionMessage(
                    role=ChatCompletionMessageRole.USER,
                    content=query
                ),
            ]
        )

        response = self.completion_client.complete(request)
        function_name_choices = response.choices
        function_name = function_name_choices[0].message.content if function_name_choices else None
        if not function_name:
            raise Exception("No function name provided in the response")

        function = self.function_catalog.lookup(function_name)
        if not function:
            raise Exception(f"No function found with name '{function_name}'")

        return function

    def parse_answer(self, text: str) -> Optional[str]:
        answer_pattern = r'---ANSWER---\s*(.*?)\s*---NOTES---'
        answer_match = re.search(answer_pattern, text, re.DOTALL)
        return answer_match.group(1) if answer_match else None

    def complete_inputs(self, query: str, function: Function) -> str:
        """
        Generates arguments for a given function to resolve a given user query.

        :param query:
        :param function:
        :return:
        """
        request = ChatCompletionRequest(
            messages=[
                ChatCompletionMessage(
                    role=ChatCompletionMessageRole.SYSTEM,
                    content=function.format_prompt()
                ),
                ChatCompletionMessage(
                    role=ChatCompletionMessageRole.USER,
                    content=query
                ),
            ]
        )

        response = self.completion_client.complete(request)
        args_choices = response.choices
        args = args_choices[0].message.content if args_choices else None
        if not args:
            raise Exception("No arguments provided in the response")

        return self.parse_answer(args)
