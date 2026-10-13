from decimal import Decimal


UNITS = {
    "Panjang": {
        "Meter": Decimal("1"), "Kilometer": Decimal("1000"),
        "Sentimeter": Decimal("0.01"), "Milimeter": Decimal("0.001"),
        "Inci": Decimal("0.0254"), "Kaki": Decimal("0.3048"),
        "Mil": Decimal("1609.344"),
    },
    "Berat": {
        "Kilogram": Decimal("1"), "Gram": Decimal("0.001"),
        "Miligram": Decimal("0.000001"), "Ton": Decimal("1000"),
        "Pound": Decimal("0.45359237"), "Ons": Decimal("0.1"),
    },
    "Volume": {
        "Liter": Decimal("1"), "Mililiter": Decimal("0.001"),
        "Meter kubik": Decimal("1000"), "Galon (US)": Decimal("3.785411784"),
        "Cangkir (US)": Decimal("0.2365882365"),
    },
    "Luas": {
        "Meter persegi": Decimal("1"), "Kilometer persegi": Decimal("1000000"),
        "Hektare": Decimal("10000"), "Kaki persegi": Decimal("0.09290304"),
        "Acre": Decimal("4046.8564224"),
    },
    "Waktu": {
        "Detik": Decimal("1"), "Menit": Decimal("60"),
        "Jam": Decimal("3600"), "Hari": Decimal("86400"),
        "Minggu": Decimal("604800"),
    },
    "Kecepatan": {
        "Meter/detik": Decimal("1"), "Kilometer/jam": Decimal("0.2777777777777778"),
        "Mil/jam": Decimal("0.44704"), "Knot": Decimal("0.5144444444444444"),
    },
    "Data": {
        "Byte (B)": Decimal("1"), "Kilobyte (KB)": Decimal("1000"),
        "Megabyte (MB)": Decimal("1000000"), "Gigabyte (GB)": Decimal("1000000000"),
        "Kibibyte (KiB)": Decimal("1024"), "Mebibyte (MiB)": Decimal("1048576"),
        "Gibibyte (GiB)": Decimal("1073741824"),
    },
    "Suhu": {"Celsius": None, "Fahrenheit": None, "Kelvin": None},
}


def convert(value, category, source, target):
    number = Decimal(str(value))
    if category == "Suhu":
        celsius = number
        if source == "Fahrenheit":
            celsius = (number - 32) * Decimal(5) / Decimal(9)
        elif source == "Kelvin":
            celsius = number - Decimal("273.15")
        if target == "Fahrenheit":
            return celsius * Decimal(9) / Decimal(5) + 32
        if target == "Kelvin":
            return celsius + Decimal("273.15")
        return celsius
    return number * UNITS[category][source] / UNITS[category][target]
