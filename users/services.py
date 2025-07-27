import stripe
from forex_python.converter import CurrencyRates
from config import settings

stripe.api_key = settings.STRIPE_API_KEY

def convert_rub_to_usd(amount):
    """Конвертирует рубли в доллары"""
    # c = CurrencyRates()
    # rate = c.get_rate('RUB', 'USD') # Сервис не работает, оставлю заглушку
    rate = 0.01257
    return int(amount * rate)


def create_stripe_product(name):
    """Создает продукт в Stripe"""

    return stripe.Product.create(name=name)

def create_stripe_price(amount, product_id, currency='usd'):
    """Создает цену"""
    return stripe.Price.create(
        currency=currency,
        unit_amount=amount * 100,
        product=product_id
    )

def create_stripe_session(price_id):
    """Создает сессию"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
