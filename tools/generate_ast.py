from io import TextIOWrapper
import sys
from typing import List

INDENT = "    "


def define_visitor(file: TextIOWrapper, base_class_name: str, types: List[str]):
    file.write("\n\nclass AstVisitor:\n")

    """
    Output wanted: 

    @visitor(Binary)
    def visit(self, expr):
        return "something"

    @visitor(Grouping)
    def visit(self, expr):
        return "another thing"
    """
    for type in types:
        class_name = type.split(':')[0].strip()
        file.writelines([
            f"{INDENT}@visitor({class_name})\n",
            f"{INDENT}def visit(self, expr):\n",
            f"{INDENT}{INDENT}pass\n\n"
        ])


def define_ast(output_dir: str, base_name: str, types: List[str]):
    path = f"{output_dir}/{base_name.lower()}.py"
    base_class_name = base_name.title().replace(" ", "")

    # Write mode, clears file contents.
    with open(path, 'w') as file:
        file.writelines([
            "import typing\n",
            "from dataclasses import dataclass\n",
            "from decorators.visitor import visitor\n",
            "from _token import Token\n\n\n",
            f"class {base_class_name}:\n",
            f"{INDENT}pass\n",
        ])

        # The AST classes
        for type in types:
            class_name, fields = type.split(':')
            define_type(file, base_class_name,
                        class_name.strip(), fields.strip())

        define_visitor(file, base_class_name, types)


def define_type(file: TextIOWrapper, base_class_name: str, class_name: str, fields: str):
    file.writelines([
        "\n\n"
        "@dataclass(frozen=True)\n",
        f"class {class_name}({base_class_name}):\n"
    ])

    for field in fields.split(", "):
        arg_type, arg_name = field.split(" ")
        file.write(f"{INDENT}{arg_name}: {arg_type}\n")


class GenerateAst:
    def __init__(self) -> None:
        if (len(sys.argv) != 2):
            print('Usage: generate_ast <output directory>')
            sys.exit(64)
        output_dir = sys.argv[1]
        define_ast(output_dir, "Expr", [
            "Binary : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal : typing.Any value",
            "Unary : Token operator, Expr right"
        ])


if __name__ == "__main__":
    GenerateAst()
