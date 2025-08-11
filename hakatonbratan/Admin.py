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
router = Router()

class Helper(StatesGroup):
    Helper_input= State()
    Delete_input=State()
admin_ids = {1427364974}
@router.message(Command("admin"), IsAdmin())
async def Is_user_admin(message: types.Message, state:FSMContext):
        Hello_admin = "Здравствуйте администратор"
        builder = InlineKeyboardBuilder()
        builder.button(text ="Режим удаления", callback_data="startdelete")
        builder.button(text ="Просмотреть запросы",callback_data="check")
        builder.button(text ="Выйти", callback_data="deadmin")
        keyboard = builder.as_markup()  # это InlineKeyboardMarkup
        await message.answer(Hello_admin, reply_markup=keyboard)
        return await state.set_state(Helper.Helper_input)

@router.callback_query(F.data == "back")
async def Is_user_admin(callback: CallbackQuery, state: FSMContext):
    Hello_admin = "Здравствуйте администратор"
    builder = InlineKeyboardBuilder()
    builder.button(text="Режим удаления", callback_data="startdelete")
    builder.button(text="Просмотреть запросы", callback_data="checkall")
    builder.button(text="Выйти", callback_data="deadmin")
    keyboard = builder.as_markup()
    await callback.message.edit_text(Hello_admin, reply_markup=keyboard)
    return await state.set_state(Helper.Helper_input)
@router.callback_query(F.data.startswith("deadmin"))
async def set_deleter(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы вышли из режима администратора")
    await callback.message.delete()
@router.callback_query(F.data.startswith("startdelete"))
async def set_deleter(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Теперь вы в режиме удаления запросов")
    builder = InlineKeyboardBuilder()
    with open("bdbd.json", 'r') as file:
        data = json.load(file)
    ids = [item["ID"] for item in data]
    for num_element in range(len(data)):
        id = int(data[num_element]["ID"])
        builder.button(text=str(id), callback_data=f"delete_{id}")
    builder.button(text="вернуться", callback_data=f"back")
    keyboard = builder.as_markup()
    await callback.message.edit_text("Выберите айди, который необходимо удалить", reply_markup = keyboard)
    await state.set_state(Helper.Delete_input)

@router.callback_query(F.data.startswith("checkall"))
async def checkall(callback: CallbackQuery):
    print("nogga")
    builder = InlineKeyboardBuilder()
    with open("bdbd.json", 'r') as file:
        data = json.load(file)
    for num_element in range(len(data)):
        id = int(data[num_element]["ID"])
        builder.button(text=str(id), callback_data=f"check_{id}")
    builder.button(text="вернуться", callback_data=f"back")
    keyboard = builder.as_markup()
    await callback.message.edit_text("Выберите айди, который хотите просмотеть", reply_markup = keyboard)

@router.callback_query(F.data.startswith("check_"))
async def checkthatshitbro(callback:CallbackQuery):
    idtocheck = int(callback.data.split("_")[-1])
    print(idtocheck)
    username = ""
    response_text = ""
    with open("bdbd.json", "r") as file:
        data = json.load(file)
    for num_element in range(len(data)):
        print(data[num_element]["ID"])
        if int(data[num_element]["ID"]) == idtocheck:
            whattocheck = data[num_element]
            username = whattocheck.get("name")
            response_text = whattocheck.get("text")
            print(whattocheck)
        else:
            print(idtocheck, int(data[num_element]["ID"]))
    builder = InlineKeyboardBuilder()
    builder.button(text="вернуться", callback_data=f"checkall")
    keyboard = builder.as_markup()
    await callback.message.edit_text(f"Имя: {"@" + username}\nТекст: {response_text}",reply_markup = keyboard)
@router.callback_query(F.data.startswith("quit"), Helper.Delete_input)
async def quit_delete(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы вышли из режима удаления запросов, чтобы вернуться, напишите /deleter ")
    return await state.clear()

@router.callback_query(F.data.startswith("delete_"), Helper.Delete_input)
async def delete_id(callback: CallbackQuery):
    idtodelete = callback.data.split("_")[-1]
    try:
            Id_To_Delete = int(idtodelete)
            print(Id_To_Delete)
            with open("bdbd.json", "r") as file:
                data = json.load(file)
            for num_element in range(len(data)):
                if data[num_element]["ID"] == Id_To_Delete:
                    whattodelete = data[num_element]
            data.remove(whattodelete)
            with open('bdbd.json', 'w') as file:
                json.dump(data, file, indent=4)
            await callback.answer (f"запись с ID {Id_To_Delete} успешно удалена. Чтобы выйти из режима удаления напишите /dedeleter")
            builder = InlineKeyboardBuilder()
            with open("bdbd.json", 'r') as file:
                data = json.load(file)
            ids = [item["ID"] for item in data]
            for num_element in range(len(data)):
                id = int(data[num_element]["ID"])
                builder.button(text=str(id), callback_data=f"delete_{id}")
            builder.button(text="вернуться", callback_data=f"back")
            keyboard = builder.as_markup()
            await callback.message.edit_text("Выберите айди, который необходимо удалить", reply_markup=keyboard)

    except (IndexError, ValueError):
            await callback.answer("Неверный формат команды. Используйте 'delete: <айди записи>', или введённого айди не существует")


