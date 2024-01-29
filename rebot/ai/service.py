import re
from typing import Optional

from rebot.ai.functions import Function, FunctionCatalog
from rebot.ai.mistral import ChatCompletionClient, ChatCompletionRequest, ChatCompletionMessageRole, ChatCompletionMessage


class FunctionService:
    def __init__(self, catalog: FunctionCatalog,
                 completion_client: ChatCompletionClient = ChatCompletionClient()):
        self.function_catalog: FunctionCatalog = catalog
        self.completion_client: ChatCompletionClient = completion_client

    def parse_answer(self, text: str) -> Optional[str]:
        answer_pattern = r'---ANSWER---\s*(.*?)\s*---NOTES---'
        answer_match = re.search(answer_pattern, text, re.DOTALL)
        return answer_match.group(1) if answer_match else None

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
                    content=f"""Your are given the following function list and must select one of them which you think is most likely to resolve the user's query.

                            ## Function List

                            {self.function_catalog.format_basic()}

                            ## Examples
                            
                            ### Example 1
                            - user: What is the weather like today?
                            - assistant: search.google

                            ### Example 2
                            - user: Hey bot what's the square root of Pi
                            - assistant: math.solve

                            Your answer must be in the following format:
                    
                            ---ANSWER---
                            WRITE FUNCTION NAME HERE
                            ---NOTES---
                            Note: Any additional comments you would like to provide.
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

        function_name = self.parse_answer(function_name)

        function = self.function_catalog.lookup(function_name)
        if not function:
            raise Exception(f"No function found with name '{function_name}'")

        return function

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
