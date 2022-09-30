from io import TextIOWrapper
import sys
from typing import List

INDENT = "    "


def define_ast(output_dir: str, base_name: str, types: List[str]):
    path = f"{output_dir}/{base_name.lower()}.py"
    base_class_name = base_name.title().replace(" ", "")

    # Write mode, clears file contents.
    with open(path, 'w') as file:
        file.writelines([
            "from abc import abstractclassmethod\n",
            "import typing\n",
            "from dataclasses import dataclass\n",
            "from _token import Token\n"
        ])

        if base_class_name != "Expr":
            file.write("from expr import Expr\n")
        file.write('\n\n')

        file.writelines([
            f"class {base_class_name}:\n",
            f"{INDENT}@abstractclassmethod\n",
            f"{INDENT}def accept() -> typing.Any:\n",
            f"{INDENT}{INDENT}pass\n",
        ])

        # The AST classes
        for type in types:
            class_name, fields = type.split(':')
            define_type(file, base_class_name,
                        class_name.strip(), fields.strip())

            file.writelines([
                f"\n{INDENT}def accept(self, visitor):\n",
                f"{INDENT}{INDENT}return visitor.visit(self)\n"
            ])


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
            "Assign : Token name, Expr value",
            "Binary : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal : typing.Any value",
            "Logical : Expr left, Token operator, Expr right",
            "Unary : Token operator, Expr right",
            "Variable : Token name"
        ])

        define_ast(output_dir, "Stmt", [
            "Block : typing.List[Stmt] statements",
            "Expression : Expr expression",
            "If : Expr condition, Stmt then_branch, Stmt else_branch",
            "Print : Expr expression",
            "Var : Token name, Expr initializer"
        ])


if __name__ == "__main__":
    GenerateAst()
