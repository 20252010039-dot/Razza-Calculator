import unittest
from decimal import Decimal

from app.core.finance import discount_vat
from app.core.formatter import format_number
from app.core.units import convert


class FeatureTests(unittest.TestCase):
    def test_number_formatting(self):
        self.assertEqual(format_number(Decimal("1234567.89")), "1.234.567,89")
        self.assertEqual(format_number(Decimal("1234567.89"), "intl"), "1,234,567.89")

    def test_temperature_conversion(self):
        self.assertEqual(convert(0, "Suhu", "Celsius", "Fahrenheit"), Decimal(32))
        self.assertEqual(convert(32, "Suhu", "Fahrenheit", "Celsius"), Decimal(0))

    def test_length_conversion(self):
        self.assertEqual(convert(1, "Panjang", "Kilometer", "Meter"), Decimal(1000))

    def test_discount_and_vat(self):
        result = discount_vat(100, 10, 11)
        self.assertEqual(result["savings"], Decimal(10))
        self.assertEqual(result["final_price"], Decimal("99.90"))


if __name__ == "__main__":
    unittest.main()
