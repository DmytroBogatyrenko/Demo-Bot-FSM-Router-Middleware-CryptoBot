import asyncio
import logging
 
import aiohttp
from aiogram import F, Router
from aiogram.types import CallbackQuery
 
from bot.config import settings
from bot.keyboards import subscription_plans_keyboard
 
router = Router(name="payments")
logger = logging.getLogger(__name__)
 
CRYPTO_PAY_API_URL = "https://pay.crypt.bot/api"
 
 
async def create_invoice(amount: str, asset: str = "USDT") -> dict:
    headers = {"Crypto-Pay-API-Token": settings.CRYPTO_PAY_TOKEN}
    payload = {
        "asset": asset,
        "amount": amount,
        "description": "Оплата підписки в demo-боті",
    }
 
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{CRYPTO_PAY_API_URL}/createInvoice", headers=headers, json=payload
        ) as response:
            data = await response.json()
 
    if not data.get("ok"):

        logger.error("Помилка створення інвойса CryptoBot: %s", data)
        raise RuntimeError(f"Не вдалось створити інвойс: {data}")
 
    return data["result"]
 
 
async def check_invoice_paid(invoice_id: int) -> bool:
    headers = {"Crypto-Pay-API-Token": settings.CRYPTO_PAY_TOKEN}
    params = {"invoice_ids": str(invoice_id)}
 
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{CRYPTO_PAY_API_URL}/getInvoices", headers=headers, params=params
        ) as response:
            data = await response.json()
 
    if not data.get("ok"):
        return False
 
    invoices = data["result"]["items"]
    if not invoices:
        return False
 
    return invoices[0]["status"] == "paid"
 
 
@router.callback_query(F.data == "buy_subscription")
async def show_plans(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "Обери тариф:", reply_markup=subscription_plans_keyboard()
    )
    await callback.answer()
 
 
@router.callback_query(F.data.startswith("plan_"))
async def process_plan_selection(callback: CallbackQuery) -> None:

    _, days, price = callback.data.split("_")
 
    await callback.message.answer("Створюю рахунок на оплату, зачекай")
 
    try:
        invoice = await create_invoice(amount=price)
    except RuntimeError:
        await callback.message.answer(
            "Не вдалось створити рахунок. Спробуй пізніше або напиши адміну"
        )
        await callback.answer()
        return
 
    pay_url = invoice["pay_url"]
    invoice_id = invoice["invoice_id"]
 
    await callback.message.answer(
        f"Рахунок створено на {price} USDT за {days} днів підписки\n"
        f"Оплати за посиланням: {pay_url}\n\n"
        "Після оплати я автоматично видам доступ протягом хвилини"
    )
    await callback.answer()

    asyncio.create_task(
        wait_for_payment(callback.from_user.id, invoice_id, callback.bot)
    )
 
 
async def wait_for_payment(user_id: int, invoice_id: int, bot) -> None:

    for _ in range(60):
        await asyncio.sleep(5)
        if await check_invoice_paid(invoice_id):
            await bot.send_message(
                user_id, "Оплату отримано! Підписку активовано"
            )
            # Тут у реальному проєкті: запис у БД про активну підписку
            # await activate_subscription(user_id, days)
            return
 
    await bot.send_message(
        user_id, "Час очікування оплати вичерпано. Спробуй ще раз /start"
    )
 