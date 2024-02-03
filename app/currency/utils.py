from decimal import Decimal, ROUND_DOWN


def to_2_places_decimal(value: [str, int, float]) -> Decimal:
    if isinstance(value, float):
        # Convert float to string to avoid floating-point precision issues, like this:
        #  Decimal(50.01) -> Decimal('50.00999999999999801048033987171947956085205078125')
        value = str(value)
    return Decimal(value).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
