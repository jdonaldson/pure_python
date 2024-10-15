import ast
import inspect

class PurityChecker(ast.NodeVisitor):
    def __init__(self):
        self.is_pure = True
        self.reason = None

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ['append', 'extend', 'insert', 'remove', 'pop', 'clear', 'sort']:
                self.is_pure = False
                self.reason = f"Uses mutating method: {node.func.attr}"
        elif isinstance(node.func, ast.Name):
            if node.func.id in ['print', 'input', 'open']:
                self.is_pure = False
                self.reason = f"Uses I/O function: {node.func.id}"
        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            if node.targets[0].id.startswith('self.'):
                self.is_pure = False
                self.reason = "Modifies object state"
        elif isinstance(node.targets[0], ast.Attribute):
            if node.targets[0].value.id == 'self':
                self.is_pure = False
                self.reason = "Modifies object state"
        self.generic_visit(node)

    def visit_Global(self, node):
        self.is_pure = False
        self.reason = "Uses global variable"

    def visit_Nonlocal(self, node):
        self.is_pure = False
        self.reason = "Uses nonlocal variable"

def is_method_pure(method):
    source = inspect.getsource(method)
    tree = ast.parse(source)
    checker = PurityChecker()
    checker.visit(tree)
    return checker.is_pure, checker.reason

# Example usage
class Example:
    def pure_method(self, a, b):
        return a + b

    def impure_method(self, item):
        self.some_list.append(item)

# # Test the purity checker
# print(is_method_pure(Example.pure_method))
# print(is_method_pure(Example.impure_method))
