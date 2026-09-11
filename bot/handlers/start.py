from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
 
from bot.keyboards import main_menu_keyboard
from bot.states import Registration
 
router = Router(name="start")
 
 
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:

    await state.clear()
 
    await message.answer(
        f"Привіт, {message.from_user.full_name}!\n\n"
    )

    await state.set_state(Registration.waiting_for_name)
 
 
@router.callback_query(F.data == "about")
async def show_about(callback: CallbackQuery) -> None:

    await callback.message.answer(
        "Це демо-бот з курсу FSM + Router + Middleware + оплата через CryptoBot"
    )
    await callback.answer()
 
 
async def show_main_menu(message: Message) -> None:

    await message.answer("Головне меню:", reply_markup=main_menu_keyboard())
 