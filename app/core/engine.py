import ast
import math
import operator
import re
from decimal import Decimal, DecimalException, DivisionByZero, InvalidOperation, localcontext


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_FUNCTIONS = {
    "sin", "cos", "tan", "asin", "acos", "atan", "log", "ln",
    "sqrt", "abs", "factorial",
}
_PERCENT_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|\([^()]*\))\s*%"
)
_MAX_EXPRESSION_LENGTH = 300
_MAX_POWER = 10000


class CalculationError(ValueError):
    """An expression cannot be safely or mathematically evaluated."""


def _clean_expression(expression):
    if not isinstance(expression, str) or not expression.strip():
        raise CalculationError("Masukkan ekspresi")
    if len(expression) > _MAX_EXPRESSION_LENGTH:
        raise CalculationError("Ekspresi terlalu panjang")
    expression = expression.strip()
    expression = expression.replace(",", ".").replace("×", "*").replace("÷", "/")
    expression = expression.replace("−", "-").replace("^", "**")
    expression = re.sub(r"\b(?:dari|of)\b", "*", expression, flags=re.IGNORECASE)
    expression = _PERCENT_PATTERN.sub(r"percent(\g<value>)", expression)
    return expression


def evaluate(expression, angle_unit="deg", answer=None):
    """Safely evaluate arithmetic and approved scientific functions using Decimal."""
    try:
        tree = ast.parse(_clean_expression(expression), mode="eval")
        with localcontext() as context:
            context.prec = 28
            result = _evaluate_node(tree.body, angle_unit.lower(), answer)
        if not result.is_finite():
            raise CalculationError("Hasil tidak terhingga")
        return result
    except CalculationError:
        raise
    except ZeroDivisionError:
        raise CalculationError("Tidak bisa dibagi nol")
    except (DivisionByZero, InvalidOperation):
        raise CalculationError("Operasi tidak valid")
    except DecimalException:
        raise CalculationError("Operasi tidak valid")
    except (SyntaxError, TypeError, ValueError, OverflowError, MemoryError, RecursionError):
        raise CalculationError("Ekspresi tidak valid")


def _decimal(value):
    return value if isinstance(value, Decimal) else Decimal(str(value))


def _evaluate_node(node, angle_unit, answer):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return Decimal(str(node.value))
    if isinstance(node, ast.Num):
        return Decimal(str(node.n))
    if isinstance(node, ast.Name):
        if node.id == "pi":
            return Decimal(str(math.pi))
        if node.id == "e":
            return Decimal(str(math.e))
        if node.id.lower() == "ans" and answer is not None:
            return _decimal(answer)
        raise CalculationError("Nama atau fungsi tidak dikenal")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](
            _evaluate_node(node.operand, angle_unit, answer)
        )
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate_node(node.left, angle_unit, answer)
        right = _evaluate_node(node.right, angle_unit, answer)
        if isinstance(node.right, ast.Call) and isinstance(node.right.func, ast.Name):
            if node.right.func.id == "percent" and isinstance(node.op, (ast.Add, ast.Sub)):
                right = left * right
        if isinstance(node.op, ast.Pow) and abs(right) > _MAX_POWER:
            raise CalculationError("Pangkat terlalu besar")
        try:
            return _BINARY_OPERATORS[type(node.op)](left, right)
        except (DivisionByZero, InvalidOperation, OverflowError, ZeroDivisionError):
            raise CalculationError("Tidak bisa dibagi nol")
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        name = node.func.id.lower()
        if name == "percent":
            if len(node.args) != 1 or node.keywords:
                raise CalculationError("Ekspresi tidak valid")
            return _evaluate_node(node.args[0], angle_unit, answer) / Decimal(100)
        if name not in _FUNCTIONS or len(node.args) != 1 or node.keywords:
            raise CalculationError("Fungsi tidak dikenal")
        value = _evaluate_node(node.args[0], angle_unit, answer)
        return _evaluate_function(name, value, angle_unit)
    raise CalculationError("Ekspresi tidak valid")


def _evaluate_function(name, value, angle_unit):
    number = float(value)
    if name in ("sin", "cos", "tan"):
        if angle_unit == "deg":
            number = math.radians(number)
        result = getattr(math, name)(number)
    elif name in ("asin", "acos", "atan"):
        result = getattr(math, name)(number)
        if angle_unit == "deg":
            result = math.degrees(result)
    elif name == "ln":
        result = math.log(number)
    elif name == "log":
        result = math.log10(number)
    elif name == "sqrt":
        result = math.sqrt(number)
    elif name == "abs":
        return abs(value)
    else:
        if value < 0 or value != value.to_integral_value() or value > 1000:
            raise CalculationError("Faktorial memerlukan bilangan bulat 0–1000")
        return Decimal(math.factorial(int(value)))
    return Decimal(str(result))
