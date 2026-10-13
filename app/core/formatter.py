from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def format_number(value, number_format="id", max_decimals=10):
    number = value if isinstance(value, Decimal) else Decimal(str(value))
    if not number.is_finite():
        return str(number)
    if number == 0:
        return "0"

    decimals = max_decimals
    if decimals != "auto":
        decimals = max(0, min(12, int(decimals)))
        quantum = Decimal(1).scaleb(-decimals)
        try:
            number = number.quantize(quantum, rounding=ROUND_HALF_UP)
        except InvalidOperation:
            return _scientific(number, number_format)
    rendered = format(number, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    if len(rendered.replace("-", "").replace(".", "")) > 24:
        return _scientific(number, number_format)

    integer, separator, fraction = rendered.partition(".")
    sign = ""
    if integer.startswith("-"):
        sign, integer = "-", integer[1:]
    groups = []
    while integer:
        groups.insert(0, integer[-3:])
        integer = integer[:-3]
    thousands, decimal_mark = ((".", ",") if number_format == "id" else (",", "."))
    integer = thousands.join(groups) or "0"
    return sign + integer + (decimal_mark + fraction if separator and fraction else "")


def _scientific(number, number_format):
    mantissa, exponent = format(number, ".8E").split("E")
    mantissa = mantissa.rstrip("0").rstrip(".")
    if number_format == "id":
        mantissa = mantissa.replace(".", ",")
    return mantissa + "E" + exponent
