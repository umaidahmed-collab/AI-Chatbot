"""
Stripe Products and Pricing Configuration

This module defines the product tiers and pricing information for the AI Chatbot application.
Products are mapped to Stripe product IDs, and prices are mapped to Stripe price IDs.
"""

from typing import Dict, List, Optional, TypedDict


class ProductMetadata(TypedDict):
    """Type definition for product metadata"""
    name: str
    description: str
    features: List[str]


class PriceMetadata(TypedDict):
    """Type definition for price metadata"""
    product_id: str
    amount: int  # Amount in cents
    currency: str
    interval: str  # 'month', 'year', or 'one_time'
    interval_count: int


# Product definitions with metadata
# In production, these IDs should be replaced with actual Stripe product IDs
STRIPE_PRODUCTS: Dict[str, ProductMetadata] = {
    "prod_free": {
        "name": "Free Tier",
        "description": "Basic chatbot functionality for individual users",
        "features": [
            "Basic AI chat",
            "Up to 50 messages per month",
            "1 document upload",
            "Community support"
        ]
    },
    "prod_basic": {
        "name": "Basic",
        "description": "Enhanced features for regular users",
        "features": [
            "Advanced AI chat",
            "Up to 500 messages per month",
            "10 document uploads",
            "Email support",
            "Chat history export"
        ]
    },
    "prod_pro": {
        "name": "Pro",
        "description": "Professional plan for power users",
        "features": [
            "Advanced AI chat with GPT-4",
            "Unlimited messages",
            "50 document uploads",
            "Priority support",
            "Chat history export",
            "Advanced analytics",
            "Custom AI model fine-tuning"
        ]
    },
    "prod_enterprise": {
        "name": "Enterprise",
        "description": "Custom solutions for organizations",
        "features": [
            "All Pro features",
            "Unlimited document uploads",
            "Dedicated account manager",
            "Custom integrations",
            "SSO authentication",
            "SLA guarantee",
            "On-premise deployment option"
        ]
    }
}


# Price definitions with pricing information
# In production, these IDs should be replaced with actual Stripe price IDs
STRIPE_PRICES: Dict[str, PriceMetadata] = {
    "price_free": {
        "product_id": "prod_free",
        "amount": 0,
        "currency": "usd",
        "interval": "month",
        "interval_count": 1
    },
    "price_basic_monthly": {
        "product_id": "prod_basic",
        "amount": 999,  # $9.99
        "currency": "usd",
        "interval": "month",
        "interval_count": 1
    },
    "price_basic_yearly": {
        "product_id": "prod_basic",
        "amount": 9999,  # $99.99 (save ~17%)
        "currency": "usd",
        "interval": "year",
        "interval_count": 1
    },
    "price_pro_monthly": {
        "product_id": "prod_pro",
        "amount": 2999,  # $29.99
        "currency": "usd",
        "interval": "month",
        "interval_count": 1
    },
    "price_pro_yearly": {
        "product_id": "prod_pro",
        "amount": 29999,  # $299.99 (save ~17%)
        "currency": "usd",
        "interval": "year",
        "interval_count": 1
    },
    "price_enterprise": {
        "product_id": "prod_enterprise",
        "amount": 99999,  # $999.99
        "currency": "usd",
        "interval": "month",
        "interval_count": 1
    }
}


def get_product_by_id(product_id: str) -> Optional[ProductMetadata]:
    """
    Retrieve product metadata by product ID.

    Args:
        product_id: The Stripe product ID

    Returns:
        ProductMetadata if found, None otherwise

    Example:
        >>> product = get_product_by_id("prod_basic")
        >>> print(product["name"])
        'Basic'
    """
    return STRIPE_PRODUCTS.get(product_id)


def get_price_by_id(price_id: str) -> Optional[PriceMetadata]:
    """
    Retrieve price metadata by price ID.

    Args:
        price_id: The Stripe price ID

    Returns:
        PriceMetadata if found, None otherwise

    Example:
        >>> price = get_price_by_id("price_basic_monthly")
        >>> print(price["amount"] / 100)  # Convert cents to dollars
        9.99
    """
    return STRIPE_PRICES.get(price_id)


def get_prices_for_product(product_id: str) -> List[Dict[str, PriceMetadata]]:
    """
    Retrieve all prices associated with a product.

    Args:
        product_id: The Stripe product ID

    Returns:
        List of price dictionaries with price_id as key

    Example:
        >>> prices = get_prices_for_product("prod_basic")
        >>> len(prices)
        2  # monthly and yearly
    """
    return [
        {price_id: price}
        for price_id, price in STRIPE_PRICES.items()
        if price["product_id"] == product_id
    ]


def format_price(amount: int, currency: str = "usd") -> str:
    """
    Format price amount for display.

    Args:
        amount: Price amount in cents
        currency: Currency code (default: "usd")

    Returns:
        Formatted price string

    Example:
        >>> format_price(2999)
        '$29.99'
    """
    currency_symbols = {
        "usd": "$",
        "eur": "€",
        "gbp": "£"
    }
    symbol = currency_symbols.get(currency.lower(), currency.upper())
    return f"{symbol}{amount / 100:.2f}"


def get_all_products() -> Dict[str, ProductMetadata]:
    """
    Retrieve all available products.

    Returns:
        Dictionary of all products
    """
    return STRIPE_PRODUCTS


def get_all_prices() -> Dict[str, PriceMetadata]:
    """
    Retrieve all available prices.

    Returns:
        Dictionary of all prices
    """
    return STRIPE_PRICES
