import asyncio
import logging
import os
from telebot.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types, Router
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
import json
import Admin
from filters import IsAdmin
logging.basicConfig(level=logging.INFO)
bot = Bot(token="token")
dp = Dispatcher()
router = Router()

async def main():
    dp.include_routers(Admin.router)
    await dp.start_polling(bot)

class Message_to_group(StatesGroup):
    help_input = State()
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="FAQ", callback_data="faq")
    builder.button(text="Помогите", callback_data="HELP")
    keyboard = builder.as_markup()
    hello_user = "⚙️Вы написали в поддержку компании ООО 'Тмыв бабла' \n⌨️Выберите нужную вам опцию"
    await message.answer(hello_user, reply_markup=keyboard)
@dp.callback_query(F.data == "menu")
async def menu(callback:CallbackQuery, state:FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="FAQ", callback_data="faq")
    builder.button(text="Помогите", callback_data="HELP")
    keyboard = builder.as_markup()
    await callback.message.edit_text("⚙️Вы написали в поддержку компании ООО 'Тмыв бабла' \n⌨️Выберите нужную вам опцию",reply_markup = keyboard)
    return await state.clear()
@dp.callback_query(F.data == "faq")
async def with_puree(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Вернуться", callback_data="menu")
    keyboard = builder.as_markup()
    await callback.message.edit_text("🔄Если сайт не работает - перезагрузите ваш компьютер.\n⚙️Если FAQ оказалась недостаточной, просто напишите 'помогите' и отправьте запрос о помощи в поддержку", reply_markup=keyboard)

@dp.callback_query(F.data == "HELP")
async def without_puree(callback: CallbackQuery,state:FSMContext):
    builder = InlineKeyboardBuilder()
    builder.button(text="Вернуться", callback_data="menu")
    keyboard = builder.as_markup()
    await callback.message.edit_text("⚠️Подробно опишите вашу проблему. \n✉️Можете прикрепить ссылки на изображения проблем, которые случились при работе с сайтом. \n📱Укажите контакты, по которым можно с вами связаться и в ближайшее время с вами свяжется наш администратор", reply_markup=keyboard)
    global schet
    schet += 1
    return await state.set_state(Message_to_group.help_input)
schet = 0
@dp.message(Message_to_group.help_input)
async def obrabotka_zaprosa(message: types.Message, state: FSMContext ):
    text = message.text
    data = await state.get_data()
    if text != "Стоп":
        await message.reply("📥Сохранено, напишите 'Стоп', чтобы отправить всю информацию")
        mass = data.get("message_saved", [])
        mass.append(text)
        await state.update_data(message_saved = mass)
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text="Вернуться", callback_data="menu")
        keyboard = builder.as_markup()
        await message.reply("📤Отправлено", reply_markup=keyboard)
        mass = data.get("message_saved")
        textfromuser = "\n".join(mass)
        username = message.from_user.username
        spisok = {
            "ID": schet,
            "text": textfromuser,
            "name": username
        }
        if os.path.exists("bdbd.json") and os.path.getsize("bdbd.json") > 0:
            with open("bdbd.json", 'r') as file:
                bata = json.load(file)
        else:
            bata = []
        bata.append(spisok)
        with open('bdbd.json', 'w') as file:
            json.dump(bata, file, indent=4)
        print(bata)
        print(schet)
        await state.clear()
        await bot.send_message(-4681080381, "Отправили новый запрос о помощи, чтобы просмотреть его, откройте бота и напишите /admin    " + "\nИмя пользователя: @" + message.from_user.username)
        #await bot.send_message(-4681080381, messageforgroup + "\nИмя пользователя: @" + message.from_user.username) Второй способ

if __name__ == "__main__":
    asyncio.run(main())
