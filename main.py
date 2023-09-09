from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import Database

from config import TOKEN_API, ADMIN, CHANEL_ID

import pygame

pygame.init()

db = Database("Database/db")

LINKS = {}  # Словарь с ссылками и челами, которые их отправили

send_vote_kb = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
send_vote_kb.row(types.InlineKeyboardButton(text="Предложить опрос"))

admin_kb = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                     one_time_keyboard=True)

admin_kb.row(types.InlineKeyboardButton(text="/help"))
admin_kb.row(types.InlineKeyboardButton(text="Пожарная тревога"))
admin_kb.row(types.InlineKeyboardButton(text="Террорист в школе"))

add_admin_kb = InlineKeyboardMarkup(row_width=2)

approve_admin = InlineKeyboardButton(text='Назначить',
                                     callback_data='like_admin')

disapprove_admin = InlineKeyboardButton(text='Не назначать',
                                        callback_data='dislike_admin')

add_admin_kb.add(approve_admin, disapprove_admin)

approve_vote_kb = InlineKeyboardMarkup(row_width=2)

approve_vote = InlineKeyboardButton(text='Одобрить',
                                    callback_data='like')

disapprove_vote = InlineKeyboardButton(text='Не одобрить',
                                       callback_data='dislike')

approve_vote_kb.add(approve_vote, disapprove_vote)

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        admins = db.get_admins()
        for admin in admins:
            ADMIN.append(str(*admin))

        if message.chat.type == 'private':
            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id)
            if message.from_user.id not in ADMIN:
                await bot.send_message(message.from_user.id, text='Дорбро пожаловать в нашего бота!\n\n'
                                                                  'Вы можете отправить нашему боту ссылку на ваш опрос')

                await bot.send_sticker(chat_id=message.from_user.id,
                                       sticker='CAACAgIAAxkBAAEKQZNk_H0cnP8JG6m3Las9Jo0ISaTYaQACkBUAArTlyUvP28AHDr-D6TAE')
            elif message.from_user.id in ADMIN:
                await message.answer('Дорбро пожаловать в нашего бота!\n\nВы Админинстратор!👨🏻‍💻\n\n'
                                     'Вам доступны следущие команды:\n\n'
                                     'sendall текст   -> Сделает рассылку с вашим текстом всем пользователям бота \n\n'
                                     'add_admin id    -> Добавит Администратора\n\n'
                                     'delete_admin    -> Удалит Администратора\n\n'
                                     'Так-же вам доступна клавиатура для объявления пожарной/терраристической тревоги',
                                     reply_markup=admin_kb)

                await bot.send_sticker(chat_id=message.from_user.id,
                                       sticker='CAACAgIAAxkBAAEKQZNk_H0cnP8JG6m3Las9Jo0ISaTYaQACkBUAArTlyUvP28AHDr-D6TAE')

    except Exception:
        print('Ошибка')


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    try:
        admins = db.get_admins()
        for admin in admins:
            ADMIN.append(str(*admin))

        if message.from_user.id in ADMIN:
            await message.answer('Вы Админинстратор!👨🏻‍💻\n\n'
                                 'Вам доступны следущие команды:\n\n'
                                 'sendall текст   -> Сделает рассылку с вашим текстом всем пользователям бота \n\n'
                                 'add_admin id    -> Добавит Администратора\n\n'
                                 'delete_admin    -> Удалит Администратора\n\n'
                                 'Так-же вам доступна клавиатура для объявления пожарной/терраристической тревоги',
                                 reply_markup=admin_kb)

        elif message.from_user.id not in ADMIN:
            await bot.send_message(message.from_user.id, text='Дорбро пожаловать в нашего бота!\n\n'
                                                              'Вы можете отправить нашему боту ссылку на ваш опрос')

    except Exception:
        print('Ошибка в help')


@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    try:
        if message.chat.type == 'private':

            admins = db.get_admins()
            for admin in admins:
                ADMIN.append(str(*admin))

            if message.from_user.id in ADMIN:
                text = message.text[9:]
                users = db.get_users()
                for row in users:
                    try:  # Для проверки заблокал ли чел бота или нет
                        if row[0] not in ADMIN:
                            await bot.send_message(row[0], text)
                            if int(row[1]) != 1:
                                print('Зашёл в иф')
                                db.set_active(row[0], 1)
                    except:
                        db.set_active(row[0], 0)
                await bot.send_message(message.from_user.id, text='Расслыка успешна произошла')

    except Exception:
        print('Ошибка в sendall')


@dp.message_handler(commands=['add_admin'])
async def add_admin(message: types.Message):
    try:
        if message.chat.type == 'private':
            text = message.text[11:]

            admins = db.get_admins()
            for admin in admins:
                ADMIN.append(str(*admin))

            if text.isdigit() and message.from_user.id in ADMIN:
                link.LAST_ADMIN = text
                link.LAST_USER_ID = message.from_user.id
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f'Сделать пользователя {text} Администратором?',
                                       reply_markup=add_admin_kb)

                print('Добавление Админа')
            else:
                await bot.send_message(message.from_user.id, text='У вас недостаточно прав')

    except Exception:
        print('Ошибка в add_admin')


@dp.message_handler(commands=['delete_admin'])
async def delete_admin(message: types.Message):
    try:
        if message.chat.type == 'private':

            admins = db.get_admins()
            for admin in admins:
                ADMIN.append(str(*admin))

            if message.from_user.id in ADMIN:
                text = message.text[14:]
                print(text)
                clear_admin_list = []
                admins = db.get_admins()
                for admin in admins:
                    clear_admin_list.append(str(*admin))
                print(clear_admin_list)
                if text in clear_admin_list:
                    db.delete_admin(text)
                else:
                    await bot.send_message(message.from_user.id, text='Админ с этим id не был найден')
            else:
                await bot.send_message(message.from_user.id, text='У вас недостаточно прав')

    except Exception:
        print('Ошибка в delete_admin')


@dp.message_handler()
async def base(message: types.Message):
    try:
        admins = db.get_admins()
        for admin in admins:
            ADMIN.append(str(*admin))

        if message.text == 'Пожарная тревога' and message.from_user.id in ADMIN:
            pygame.mixer.music.load('sounds/fire.mp3')
            pygame.mixer.music.play(0)

        if message.text == 'Террорист в школе' and message.from_user.id in ADMIN:
            pygame.mixer.music.load('sounds/terrorist.mp3')
            pygame.mixer.music.play(0)

        if "http" in message.text and "forms" in message.text and ADMIN:

            links = db.get_link()
            clear_links = []
            for element in links:
                clear_links.append(*element)
            if len(set(clear_links)) > 1:
                await message.reply(
                    text='Ваш опрос не отправился Администратору, т.к у него на рассмотринии уже есть опрос!\n\n '
                         'Попробуйте чуть позже')

            else:
                link.LAST_MESSAGE = message.text
                link.LAST_USER_ID = message.from_user.id

                db.add_link(link.LAST_MESSAGE, message.from_user.id)

                await message.reply(text='Ваш опрос отправился на рассмотрение Администратору!')
                if message.from_user.username is not None:
                    await bot.send_message(chat_id=ADMIN[0],
                                           text=f"@{message.from_user.username}\n\n" + link.LAST_MESSAGE,
                                           reply_markup=approve_vote_kb)
                else:
                    await bot.send_message(chat_id=ADMIN[0],
                                           text=f"Не смог узнать username Пользователя\n\n" + link.LAST_MESSAGE,
                                           reply_markup=approve_vote_kb)

        elif message.text != "Предложить опрос" and not (
                message.text.isdigit() and message.from_user.id in ADMIN) and not (
                message.text == 'Пожарная тревога' and message.from_user.id in ADMIN) and not (
                message.text == 'Террорист в школе' and message.from_user.id in ADMIN) and not (
                "http" in message.text and "forms" in message.text and ADMIN):
            print('Я вас не понял')

        print(LINKS)

    except Exception:
        print('Ошибка в base')


class Link:
    def __init__(self):
        self.LAST_MESSAGE = 'Не пусто'
        self.LAST_ADMIN = 'Не пусто'
        self.LAST_USER_ID = 88005553535


@dp.callback_query_handler()
async def callback_approve(callback: types.CallbackQuery):
    try:
        print(callback.message.from_id)
        if callback.data == 'like':
            await bot.send_message(chat_id=CHANEL_ID, text=link.LAST_MESSAGE)
            await callback.message.delete()
            await db.set_link('Пусто')
        elif callback.data == 'dislike':
            await bot.send_message(chat_id=link.LAST_USER_ID,
                                   text='Админ отклонил ваш опрос')  # Отправляет челу message Что опрос не прошёл
            await callback.message.delete()
            await db.set_link('Пусто')

        if callback.data == 'like_admin':
            db.add_admin(link.LAST_ADMIN)
            await callback.message.delete()
        elif callback.data == 'dislike_admin':
            await callback.message.delete()

    except Exception:
        print('Ошибка в callback_approve')


if __name__ == "__main__":
    link = Link()
    executor.start_polling(dp, skip_updates=True)
