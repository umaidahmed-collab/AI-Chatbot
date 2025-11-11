"""
Stripe utility functions for currency formatting and amount conversions.

This module provides helper functions for working with Stripe amounts,
which are always represented in the smallest currency unit (e.g., cents for USD).
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Union


def cents_to_dollars(cents: int) -> Decimal:
    """
    Convert cents to dollars.

    Args:
        cents: Amount in cents (smallest currency unit)

    Returns:
        Decimal: Amount in dollars with 2 decimal places

    Example:
        >>> cents_to_dollars(1299)
        Decimal('12.99')
    """
    return Decimal(cents) / Decimal('100')


def dollars_to_cents(dollars: Union[float, Decimal, str]) -> int:
    """
    Convert dollars to cents.

    Args:
        dollars: Amount in dollars (can be float, Decimal, or string)

    Returns:
        int: Amount in cents (smallest currency unit)

    Example:
        >>> dollars_to_cents(12.99)
        1299
        >>> dollars_to_cents("12.99")
        1299
    """
    decimal_amount = Decimal(str(dollars))
    cents = (decimal_amount * Decimal('100')).quantize(
        Decimal('1'),
        rounding=ROUND_HALF_UP
    )
    return int(cents)


def get_currency_symbol(currency_code: str) -> str:
    """
    Get the currency symbol for a given currency code.

    Args:
        currency_code: ISO 4217 currency code (e.g., 'USD', 'EUR', 'GBP')

    Returns:
        str: Currency symbol or the currency code if symbol not found

    Example:
        >>> get_currency_symbol('USD')
        '$'
        >>> get_currency_symbol('EUR')
        '€'
    """
    currency_symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥',
        'CNY': '¥',
        'CHF': 'CHF',
        'CAD': 'C$',
        'AUD': 'A$',
        'NZD': 'NZ$',
        'INR': '₹',
        'BRL': 'R$',
        'MXN': 'MX$',
        'KRW': '₩',
        'SGD': 'S$',
        'HKD': 'HK$',
        'SEK': 'kr',
        'NOK': 'kr',
        'DKK': 'kr',
        'PLN': 'zł',
        'THB': '฿',
        'IDR': 'Rp',
        'MYR': 'RM',
        'ZAR': 'R',
        'PHP': '₱',
        'TWD': 'NT$',
    }

    return currency_symbols.get(currency_code.upper(), currency_code.upper())


def format_amount(
    cents: int,
    decimal_places: int = 2,
    thousands_separator: str = ','
) -> str:
    """
    Format an amount in cents to a dollar display format.

    Args:
        cents: Amount in cents (smallest currency unit)
        decimal_places: Number of decimal places to display (default: 2)
        thousands_separator: Character to use for thousands separator (default: ',')

    Returns:
        str: Formatted amount string (e.g., '1,299.99')

    Example:
        >>> format_amount(1299)
        '12.99'
        >>> format_amount(1234567)
        '12,345.67'
        >>> format_amount(1000, decimal_places=0)
        '10'
    """
    dollars = cents_to_dollars(cents)

    # Format with specified decimal places
    format_string = f"{{:,.{decimal_places}f}}"
    formatted = format_string.format(float(dollars))

    # Replace comma with custom thousands separator if needed
    if thousands_separator != ',':
        formatted = formatted.replace(',', thousands_separator)

    return formatted


def format_currency(
    cents: int,
    currency_code: str = 'USD',
    include_symbol: bool = True,
    decimal_places: int = 2,
    thousands_separator: str = ','
) -> str:
    """
    Format an amount with currency symbol.

    Args:
        cents: Amount in cents (smallest currency unit)
        currency_code: ISO 4217 currency code (default: 'USD')
        include_symbol: Whether to include currency symbol (default: True)
        decimal_places: Number of decimal places to display (default: 2)
        thousands_separator: Character to use for thousands separator (default: ',')

    Returns:
        str: Formatted currency string (e.g., '$12.99', '€1,234.56')

    Example:
        >>> format_currency(1299, 'USD')
        '$12.99'
        >>> format_currency(1234567, 'EUR')
        '€12,345.67'
        >>> format_currency(1000, 'GBP', decimal_places=0)
        '£10'
        >>> format_currency(1299, 'USD', include_symbol=False)
        '12.99'
    """
    amount_str = format_amount(
        cents,
        decimal_places=decimal_places,
        thousands_separator=thousands_separator
    )

    if include_symbol:
        symbol = get_currency_symbol(currency_code)

        # For most currencies, symbol goes before the amount
        # Special cases where symbol goes after can be added here
        suffix_currencies = {'CHF'}

        if currency_code.upper() in suffix_currencies:
            return f"{amount_str} {symbol}"
        else:
            return f"{symbol}{amount_str}"

    return amount_str
