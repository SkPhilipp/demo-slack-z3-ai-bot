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
    def __init__(self, name: str, functions: list["Function"]):
        self.name: str = name
        self.functions: list["Function"] = functions

    def format_basic(self):
        formatted = f""
        for index, function in enumerate(self.functions):
            formatted += f"- {self.name}.{function.format_basic()}\n"
        return formatted

    def format_full(self):
        return self.format_basic()

    def lookup(self, name: str) -> Optional["Function"]:
        for function in self.functions:
            if f"{self.name}.{function.name}" == name:
                return function


class Function:
    def __init__(self, name: str,
                 description: str,
                 examples: str,
                 inputs: str,
                 outputs: str,
                 callback: callable):
        self.name: str = name
        self.description: str = description
        self.examples: str = examples
        self.inputs: str = inputs
        self.outputs: str = outputs
        self.callback: callable = callback

    def format_basic(self):
        return f"{self.name} -- \"{self.description}\""

    def format_full(self):
        return f"""
        {self.name}
        
        {self.description}

        Examples:
        {self.examples}
        
        Inputs:
        {self.inputs}
        Outputs:
        {self.outputs}
        """
