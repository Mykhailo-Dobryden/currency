from decimal import Decimal
import pytest

from currency.utils import to_2_places_decimal


@pytest.mark.parametrize("value, expected", [(1, Decimal('1.00')),
                                             (10, Decimal('10.00')),
                                             (10.1, Decimal('10.10')),
                                             (10.10, Decimal('10.10')),
                                             (10.73, Decimal('10.73')),
                                             (12.34567898, Decimal('12.34')),
                                             (123.4567898, Decimal('123.45')),
                                             (50.01, Decimal('50.01')),
                                             (37.5252, Decimal('37.52')),
                                             ('10.73', Decimal('10.73')),
                                             ('10', Decimal('10.00')),
                                             ('10.0', Decimal('10.00')),
                                             ('10.00', Decimal('10.00')),

                                             ])
def test_to_2_places_decimal(value, expected):
    assert to_2_places_decimal(value) == expected
