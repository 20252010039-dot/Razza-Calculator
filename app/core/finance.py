from decimal import Decimal


def discount_vat(price, discount_percent, vat_percent):
    price = Decimal(str(price))
    discount = Decimal(str(discount_percent))
    vat = Decimal(str(vat_percent))
    if price < 0 or discount < 0 or vat < 0:
        raise ValueError("Nilai tidak boleh negatif")
    savings = price * discount / Decimal(100)
    discounted_price = price - savings
    final_price = discounted_price * (Decimal(1) + vat / Decimal(100))
    return {
        "savings": savings,
        "discounted_price": discounted_price,
        "vat_amount": final_price - discounted_price,
        "final_price": final_price,
    }
