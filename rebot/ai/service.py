from functions import Function, FunctionCatalog, FunctionPackage
from mistral import ChatCompletionClient, ChatCompletionRequest, ChatCompletionMessageRole, ChatCompletionMessage


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

                            Answer ONLY with a function name, provide no explanation and write nothing else.

                            Example:
                            - user: "What is the weather like today?"
                            - you: "search.google"

                            Counterexample, do NOT this:
                            - user: "I wonder what Pandas look like"
                            - you: "I think you should search.google because ..."

                            Example:
                            - user: "Hey bot what's the square root of Pi"
                            - you: "math.solve"

                            Counterexample, do NOT this:
                            - user: "What is 1 + 1?"
                            - you: "math.solve Note: bla bla bla ..."
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

    def complete_arguments(self, query: str, function: Function) -> str:
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
                    content=f"""Your current task is to provide arguments for the function {function.name} to resolve the user's request.

                            Here is the full information about the function:
                            {function.format_full()}

                            Answer ONLY with the arguments for the function, provide no explanation and write nothing else.

                            Example: (in context of search.google)
                            - user: "Hey how do I do python programming?"
                            - you: "'introduction to python programming'"

                            Counterexample, do NOT do this: (in context of search.google)
                            - user: "Hey how do I do python programming?"
                            - you: "Well you should search for 'python programming' because ..."

                            Example: (in context of math.solve)
                            - user: "What is 1 + 1?"
                            - you: "'1 + 1'"

                            Counterexample, do NOT do this: (in context of math.solve)
                            - user: "What is 1 + 1?"
                            - you: "'1 + 1' Note: bla bla bla ..."

                            Provide arguments for the function {function.name}.
                            """
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

        return args


def main():
    def search__google(_):
        print(f"searching google for {_}")

    def math__solve(_):
        print(f"solving {_}")

    function_catalog = FunctionCatalog(
        packages=[
            FunctionPackage(
                name="search",
                functions=[
                    Function(
                        name="google",
                        description="Searches Google for a query",
                        examples="search_google('python programming')",
                        inputs="A string query",
                        outputs="Search results",
                        callback=search__google
                    ),
                ]
            ),
            FunctionPackage(
                name="math",
                functions=[
                    Function(
                        name="solve",
                        description="Solves a mathematical expression with a calculator",
                        examples="math.solve('2 + 2')",
                        inputs="A string expression",
                        outputs="The result of the calculation",
                        callback=math__solve
                    )
                ]
            )
        ]
    )
    function_service = FunctionService(function_catalog)
    function = function_service.complete_function("Who is the president of the United States?")
    args = function_service.complete_arguments("Who is the president of the United States?", function)
    function.callback(args)


if __name__ == "__main__":
    main()
