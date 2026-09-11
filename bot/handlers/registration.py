from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
 
from bot.handlers.start import show_main_menu
from bot.keyboards import confirmation_keyboard
from bot.states import Registration
 
router = Router(name="registration")
 
 
@router.message(Registration.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:

    name = message.text.strip()
 
    if len(name) < 2:
        await message.answer("Ім'я закоротке, спробуй ще раз:")
        return

    await state.update_data(name=name)
 
    await message.answer(f"Приємно познайомитись, {name}! Скільки тобі років?")
    await state.set_state(Registration.waiting_for_age)
 
 
@router.message(Registration.waiting_for_age)
async def process_age(message: Message, state: FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Введи вік цифрами: ")
        return
 
    age = int(message.text)
    if not (5 <= age <= 100):
        await message.answer("Схоже на помилку. Введи реальний вік:")
        return
 
    await state.update_data(age=age)

    data = await state.get_data()
    await message.answer(
        f"Перевір дані:\nІм'я: {data['name']}\nВік: {data['age']}\n\nВсе вірно?",
        reply_markup=confirmation_keyboard(),
    )
    await state.set_state(Registration.waiting_for_confirmation)
 
 
@router.callback_query(Registration.waiting_for_confirmation, F.data == "confirm_yes")
async def confirm_registration(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

 
    await callback.message.answer(f"Реєстрацію завершено, {data['name']}!")

    await state.clear()
 
    await show_main_menu(callback.message)
    await callback.answer()
 
 
@router.callback_query(Registration.waiting_for_confirmation, F.data == "confirm_no")
async def restart_registration(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.answer("Добре, почнемо заново. Як тебе звати?")
    await state.set_state(Registration.waiting_for_name)
    await callback.answer()
 