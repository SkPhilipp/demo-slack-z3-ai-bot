from typing import Optional


class FunctionCatalog:
    def __init__(self, packages: list["FunctionPackage"]):
        self.packages: list["FunctionPackage"] = packages

    def format_basic(self):
        formatted = f""
        for index, package in enumerate(self.packages):
            formatted += f"{package.format_full()}\n"
        return formatted

    def format_full(self):
        return self.format_basic()

    def lookup(self, name: str) -> Optional["Function"]:
        for package in self.packages:
            function = package.lookup(name)
            if function:
                return function


class FunctionPackage:
    def __init__(self, name: str, functions: list["Function"] = None):
        self.name: str = name
        if functions is None:
            functions = []
        self.functions: list["Function"] = functions

    def registered(self,
                   name: str,
                   description: str,
                   examples: list[str] = None,
                   counter_examples: list[str] = None,
                   inputs: str = "string"):
        if examples is None:
            examples = []
        if counter_examples is None:
            counter_examples = []

        def decorator(function):
            function = Function(
                callback=function,
                name=name,
                description=description,
                examples=examples,
                counter_examples=counter_examples,
                inputs=inputs
            )
            self.functions.append(function)
            return function

        return decorator

    def format_basic(self):
        formatted = f""
        for index, function in enumerate(self.functions):
            formatted += f"- {function.format_basic()}\n"
        return formatted

    def format_full(self):
        return self.format_basic()

    def lookup(self, name: str) -> Optional["Function"]:
        for function in self.functions:
            if function.name == name:
                return function


class Function:
    def __init__(self,
                 callback: callable,
                 name: str,
                 description: str,
                 examples: list[str],
                 counter_examples: list[str],
                 inputs: str):
        self.name: str = name
        self.description: str = description
        self.examples: list[str] = examples
        self.counter_examples: list[str] = counter_examples
        self.inputs: str = inputs
        self.callback: callable = callback

    def format_basic(self):
        return f"{self.name} -- \"{self.description}\""

    def format_full(self):
        examples = ""
        for index, example in enumerate(self.examples):
            examples += f"""
            ### Example {index + 1}:
            {example}
            \n
            """
        examples += "\n"

        for index, counter_example in enumerate(self.counter_examples):
            examples += f"""            
            ### Counterexample {index + 1}, do NOT do this:
            {counter_example}
            \n
            """
        examples += "\n"

        return f"""
        # {self.name}
        {self.description}:

        ## Input
        {self.inputs}

        ## Examples and counterexamples        
        {examples}
        """

    def format_prompt(self):
        return f"""You are given the following function for which you must provide an input to respond to the user.

        ---
        {self.format_full()}        
        ---     

        Your answer must be in the following format:

        ---ANSWER---
        WRITE INPUT HERE
        ---NOTES---
        Note: Any additional comments you would like to provide.
        """
