from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
 
 
def confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Так, все вірно", callback_data="confirm_yes")
    builder.button(text="Почати заново", callback_data="confirm_no")
    builder.adjust(2)
    return builder.as_markup()
 
 
def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Оформити підписку", callback_data="buy_subscription")
    builder.button(text="Про бота", callback_data="about")
    builder.adjust(1)
    return builder.as_markup()
 
 
def subscription_plans_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="7 днів — 3 USDT", callback_data="plan_7_3")
    builder.button(text="30 днів — 10 USDT", callback_data="plan_30_10")
    builder.adjust(1)
    return builder.as_markup()
 