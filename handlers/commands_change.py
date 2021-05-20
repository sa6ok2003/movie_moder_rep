from aiogram import types
from misc import dp, bot
import sqlite3
from .sqlit import proverka_channel_admin, obnovatrafika_adminam, obnovatrafika_adminam2,obnovatrafika_adminam1,cheak_traf,obnovatrafika,reg_admin,proverka_admina,proverka_status_admina
from .callbak_data import obnovlenie
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class r_traf(StatesGroup):
    tr1 = State()
    tr2 = State()
    tr3 = State()


@dp.message_handler(commands=['change'])
async def admin_kaw(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    bat_3 = types.InlineKeyboardButton(text='Настроить каналы', callback_data='level3')
    bat_2 = types.InlineKeyboardButton(text='Настроить каналы', callback_data='level2')
    bat_1 = types.InlineKeyboardButton(text='Настроить канал', callback_data='level1')

    a = '@'+message.from_user.username
    flag = proverka_admina(a) #1 - Если админ, 0 - если не админ
    if flag == 1:
        stat = proverka_status_admina(a) #Проверка статуса
        if int(stat) == 0:
            await bot.send_message(chat_id=message.chat.id,text='Вы зашли в админ панель.\nВаш статус <b>:Уровень 0</b>')

        if int(stat) == 1:
            cha = proverka_channel_admin('@' + message.chat.username)  # Cписок всех каналов пользователя
            markup.add(bat_1)
            await bot.send_message(chat_id=message.chat.id,text='Ваш статус <b>:Уровень 1</b>\n\n'
                                                                'Вам доступен канал для редактирования\n\n'
                                                                'Список настроеных каналов (Если стоит 0, значит каналы еще не настроены) :\n\n'
                                                                f'<b>1. {cha[1]}\n\n'
                                                                f'ПЕРЕД РЕДАКТИРОВАНИЕМ КАНАЛОВ ОБЯЗАТЕЛЬНО ДАЙ БОТУ АДМИНКУ В НИХ!</b>', reply_markup=markup,parse_mode='html')

        if int(stat) == 2:
            cha = proverka_channel_admin('@' + message.chat.username)  # Cписок всех каналов пользователя
            print(cha)
            markup.add(bat_2)
            await bot.send_message(chat_id=message.chat.id,text='Ваш статус <b>:Уровень 2</b>\n\n'
                                                                'Вам доступны 2 канала для редактирования\n\n'
                                                                'Список настроеных каналов (Если стоит 0, значит каналы еще не настроены) :\n\n'
                                                                f'1. {cha[1]}\n'
                                                                f'2. {cha[2]}\n\n'
                                                                f'<b>ПЕРЕД РЕДАКТИРОВАНИЕМ КАНАЛОВ ОБЯЗАТЕЛЬНО ДАЙ БОТУ АДМИНКУ В НИХ!</b>', reply_markup=markup,parse_mode='html')

        if int(stat) == 3:
            cha = proverka_channel_admin('@' + message.chat.username)  # Cписок всех каналов пользователя
            markup.add(bat_3)
            await bot.send_message(chat_id=message.chat.id,text='Ваш статус <b>:Уровень 3</b>\n\n'
                                                                'Вам доступны все 3 канала для редактирования\n\n'
                                                                'Список настроеных каналов (Если стоит 0, значит каналы еще не настроены) :\n\n'
                                                                f'1. {cha[0]}\n'
                                                                f'2. {cha[1]}\n'
                                                                f'3. {cha[2]}\n\n'
                                                                f'<b>ПЕРЕД РЕДАКТИРОВАНИЕМ КАНАЛОВ ОБЯЗАТЕЛЬНО ДАЙ БОТУ АДМИНКУ В НИХ!</b>', reply_markup=markup,parse_mode='html')


# Обработка 3 лвла

@dp.callback_query_handler(text='level3') # Изменение каналов, на которые нужно подписаться
async def baza12342(call: types.callback_query):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Введите список из трех новых каналов\n\n'
                                                      '<b>Список каналов вводи в строчку, пример:\n'
                                                      '@channel1 @channel2 @channel3</b>',parse_mode='html',reply_markup=markup)
    await r_traf.tr1.set()

@dp.message_handler(state=r_traf.tr1, content_types='text')
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    mas = message.text.split()
    if (len(mas) == 3 and mas[0][0] == '@' and mas[1][0] == '@' and mas[2][0] == '@'):
        # Список новых каналов
        channel1 = mas[0][1:]
        channel2 = mas[1][1:]
        channel3 = mas[2][1:]

        try:
            obnovatrafika_adminam(channel1,channel2,channel3,"@"+message.from_user.username)# Внесение новых каналов в базу данных
            await bot.send_message(chat_id=message.chat.id,text='Успешно')
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await state.finish()
        except:
            await bot.send_message(chat_id=message.chat.id,text='Неудачно')
            await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
            await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id, text='Неудачно')
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await state.finish()


# Обработка 2 лвла

@dp.callback_query_handler(text='level2')  # Изменение каналов, на которые нужно подписаться
async def baza123424324(call: types.callback_query):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Введите список из двух новых каналов\n\n'
                                                      '<b>Список каналов вводи в строчку, пример:\n'
                                                      '@channel1 @channel2</b>', parse_mode='html',reply_markup=markup)
    await r_traf.tr2.set()


@dp.message_handler(state=r_traf.tr2, content_types='text')
async def traf_obnovlenie2(message: types.Message, state: FSMContext):
    mas = message.text.split()
    if (len(mas) == 2 and mas[0][0] == '@' and mas[1][0] == '@'):

        # Список новых каналов
        channel2 = mas[0][1:]
        channel3 = mas[1][1:]

        try:
            obnovatrafika_adminam2(channel2, channel3,"@" + message.from_user.username)  # Внесение новых каналов в базу данных
            await bot.send_message(chat_id=message.chat.id, text='Успешно')
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await state.finish()
        except:
            await bot.send_message(chat_id=message.chat.id,text='Неудачно')
            await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
            await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id, text='Неудачно')
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await state.finish()

# Обработка 1 лвла

@dp.callback_query_handler(text='level1')  # Изменение каналов, на которые нужно подписаться
async def baza1234243234324(call: types.callback_query):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Введите свой канал\n\n'
                                                      '<b>Пример:\n'
                                                      '@channel1</b>', parse_mode='html',reply_markup=markup)
    await r_traf.tr3.set()


@dp.message_handler(state=r_traf.tr3, content_types='text')
async def traf_obnovlenie1(message: types.Message, state: FSMContext):
    mas = message.text.split()
    if (len(mas) == 1 and mas[0][0] == '@'):

        # Список новых каналов
        channel2 = mas[0][1:]

        obnovatrafika_adminam1(channel2,"@" + message.from_user.username)  # Внесение новых каналов в базу данных