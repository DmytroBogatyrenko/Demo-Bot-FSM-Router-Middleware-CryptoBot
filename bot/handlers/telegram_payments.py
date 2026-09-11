from aiogram import F, Router
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery
 
from bot.config import settings
 
router = Router(name="telegram_payments")

PROVIDER_TOKEN = "PLACEHOLDER_PROVIDER_TOKEN"
 
 
async def send_subscription_invoice(message: Message) -> None:
    prices = [

        LabeledPrice(label="Підписка на 30 днів", amount=10000)
    ]
 
    await message.answer_invoice(
        title="Підписка на бота",
        description="Доступ до всіх функцій на 30 днів",
        payload="subscription_30_days",
        provider_token=PROVIDER_TOKEN,
        currency="UAH",
        prices=prices,
    )
 
 
@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery) -> None:

    await pre_checkout_query.answer(ok=True)
 
 
@router.message(F.successful_payment)
async def process_successful_payment(message: Message) -> None:
    payload = message.successful_payment.invoice_payload
    await message.answer(
        f"Оплату отримано! Активовано: {payload}. Дякую за довіру"
    )