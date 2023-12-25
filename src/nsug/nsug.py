import os
import sys
import re
import argparse
from langchain.globals import set_llm_cache
from langchain.llms import OpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.cache import InMemoryCache

set_llm_cache(InMemoryCache())


def check_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("Environment variable not set: OPENAI_API_KEY")


def read_code_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            code = file.read().strip()
        if not code:
            raise ValueError("File is empty")
        return code
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    except IOError as e:
        raise IOError("Error reading file: " + str(e))


def find_name_in_code(code, variable):
    pattern = r"(?<=[\n\s\t])" + re.escape(variable) + r"(?=[\(\[: =])"
    if not re.search(pattern, code):
        raise ValueError(f"Name '{variable}' not found in code")
    return True


def run(code, name, max):
    output_parser = CommaSeparatedListOutputParser()
    format_instructions = output_parser.get_format_instructions()
    llm = OpenAI(temperature=0)
    prompt = FewShotPromptTemplate(
        examples=[
            {
                "code": """def foo(str):
    print("Hello " + str + "!!")""",
                "name": "foo",
                "max": 5,
                "output": "printGreeting, sayHello, greetWithName, displayHelloMessage, outputGreeting",
            }
        ],
        example_prompt=PromptTemplate(
            template="input1:\n{code}\n\ninput2:\n{name}\n\ninput3:\n{max}\n\noutput:\n{output}\n",
            input_variables=["code", "name", "max", "output"],
        ),
        prefix="Please analyze input1 below and suggest a better naming of input2 as it appears in the code, taking into account the context. Please provide input3 suggestions. "
        + format_instructions,
        suffix="input1:\n{code}\n\ninput2:\n{name}\n\ninput3:\n{max}\n\noutput:",
        input_variables=["code", "name", "max"],
    )
    output = llm(prompt.format(code=code, name=name, max=max))
    items = output_parser.parse(output)
    for item in items:
        print(item)


def main():
    parser = argparse.ArgumentParser(description="nsug: a tool for suggesting better names for variables, functions, and methods in code.")
    parser.add_argument("--code", "-c", type=str, default="code.txt", help="path to the code file")
    parser.add_argument("--name", "-n", type=str, required=True, help="name of the variable, function, or method to suggest names for")
    parser.add_argument("--max", "-m", type=int, default=5, help="maximum number of suggestions to return")
    args = parser.parse_args()

    try:
        check_openai_api_key()
        code = read_code_from_file(args.code)
        find_name_in_code(code, args.name)
        run(code, args.name, args.max)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
