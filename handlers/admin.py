from aiogram import types
from misc import dp, bot
import sqlite3
from .sqlit import info_members, reg_one_channel, reg_channels,del_one_channel,cheak_traf,obnovatrafika,reg_admin,list_adminov
from .callbak_data import obnovlenie
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 678623761 #Бекир
ADMIN_ID_4 = 941730379 #Джейсон

ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3, ADMIN_ID_4]

class reg(StatesGroup):
    name = State()
    fname = State()

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()


class del_user(StatesGroup):
    del_name = State()
    del_fname = State()

class reg_trafik(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_admink(StatesGroup):
    adm1 = State()
    adm2 = State()

@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_e = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_j = types.InlineKeyboardButton(text='Скачать базу', callback_data='baza')
        bat_setin = types.InlineKeyboardButton(text='Настройка трафика', callback_data='settings')
        bat_modern = types.InlineKeyboardButton(text='Права администраторов', callback_data='but_adm')
        markup.add(bat_a,bat_e,bat_j)
        markup.add(bat_setin)
        markup.add(bat_modern)
        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)

# Урезанные админы
@dp.callback_query_handler(text='but_adm')
async def but_adm12(call: types.callback_query):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup = types.InlineKeyboardMarkup()
    bat_1 = types.InlineKeyboardButton(text='Список админов', callback_data='cheack_admin')
    bat_2 = types.InlineKeyboardButton(text='Изменить | Добавить ', callback_data='add_admin')
    bat_3 = types.InlineKeyboardButton(text='Выход', callback_data='c3')
    markup.add(bat_1,bat_2)
    markup.add(bat_3)

    await bot.send_message(chat_id=call.message.chat.id,text='Панель управления урезанной админкой',reply_markup=markup)

@dp.callback_query_handler(text='c3')
async def add_adm333(call: types.callback_query):
    await bot.delete_message(call.message.chat.id,message_id=call.message.message_id)


@dp.callback_query_handler(text='cheack_admin')
async def add_adm335646453(call: types.callback_query):
    adm = list_adminov()
    kol = adm[1] # Количество админов
    arr = adm[0]

    massiv = []

    for i in arr:
        a,b,c,d,e,w = map(str,i)
        massiv.append(a + ' ' + b + ' ' + w)

    lis = ("\n\n".join(massiv))
    messa = (f"<b>Количество учеников: {kol}\n</b>"
               f"Пары <b>Юзер - Канал - Статус</b>:\n\n"
               f"{lis}")
    await bot.send_message(chat_id=call.message.chat.id,text=messa,parse_mode='html')


@dp.callback_query_handler(text='add_admin')
async def add_adm12(call: types.callback_query,state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    q = await bot.send_message(call.message.chat.id, text='Что бы изменить права текущего админа или добавить нового, вводи :\n\n'
                                                      '@namechannel-@username-0\n'
                                                      '<b>Вводи без пробелов!\n\n'
                                                      '0 - Разрешено работать\n'
                                                      '1 - Разрешено менять 1 канал\n'
                                                      '2 - Разрешено менять 2 канала\n'
                                                      '3 - Разрешено менять 3 канала\n\n'
                                                      '9 - Удалить из админов</b>',parse_mode='html',reply_markup=markup)
    await state.update_data(mess1=q.message_id)
    await reg_admink.adm1.set()


@dp.message_handler(state=reg_admink.adm1, content_types='text')
async def adm_obnovlenie(message: types.Message, state: FSMContext):
    try:
        array = message.text.split('-')
        channel_osnov = array[0]
        username = array[1]
        status = array[2]

        if array[2] != '9': #Если не равно 9, то регистрируем в списке разрешенных
            reg_one_channel(array[0]) #Регистрация канала в списке
            reg_admin(channel_osnov,username,status)

        else:
            reg_admin(channel_osnov, username, status)
            del_one_channel(channel_osnov) # Удаление из разрешенных

        await bot.send_message(chat_id=message.chat.id,text='Успешно')
        data = await state.get_data()
        mess1 = data['mess1']
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=mess1)
        await state.finish()

    except:
        data = await state.get_data()
        mess1 = data['mess1']
        await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=mess1)
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()

# НАСТРОЙКА ТРАФИКА
@dp.callback_query_handler(text='settings')
async def baza12(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ИЗМЕНИТЬ КАНАЛЫ⚙️', callback_data='change_trafik')
    markup_traf.add(bat_a)
    list = cheak_traf()
    await bot.send_message(call.message.chat.id, text=f'Список активный каналов на данный момент:\n\n'
                                                      f'1. @{list[0]}\n'
                                                      f'2. @{list[1]}\n'
                                                      f'3. @{list[2]}\n\n'
                                                      f'<b>Внимание! Первый по счету канал , должен быть обязательно с кино-тематикой</b>\n'
                                                      f'Для изменения жми кнопку',parse_mode='html',reply_markup=markup_traf)


@dp.callback_query_handler(text='change_trafik') # Изменение каналов, на которые нужно подписаться
async def baza12342(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Введите новый список каналов\n<b>ПЕРВЫЙ КАНАЛ ДОЛЖЕН БЫТЬ ОБЯЗАТЕЛЬНО С КИНО-ТЕМАТИКОЙ!</b>\n\n'
                                                      'Список каналов вводи в строчку, пример:\n'
                                                      '@channel1 @channel2 @channel3',parse_mode='html',reply_markup=markup)
    await reg_trafik.traf1.set()


@dp.message_handler(state=reg_trafik.traf1, content_types='text')
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    mas = message.text.split()
    if (len(mas) == 3 and mas[0][0] == '@' and mas[1][0] == '@' and mas[2][0] == '@'):
        # Список новых каналов
        channel1 = mas[0][1:]
        channel2 = mas[1][1:]
        channel3 = mas[2][1:]

        obnovatrafika(channel1,channel2,channel3) # Внесение новых каналов в базу данных
        obnovlenie()
        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. ТЕбе необходимо снова зайти в админ панель и выбрать нужный пункт.'
                                                            'Сообщение со списком каналом мне отсылать сейчас бессмыслено - я тебя буду игнорить, поэтому делай по новой все')
        await state.finish()



@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    a = open('server.db','rb')
    await bot.send_document(chat_id=call.message.chat.id, document=a)


############################  DELITE CHANNEL  ###################################
@dp.callback_query_handler(text='delite_channel')
async def del_channel(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь название канала для удаления в формате\n'
                                                 '@name_channel')
    await del_user.del_name.set()


@dp.message_handler(state=del_user.del_name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    check_dog = message.text[:1]
    if check_dog != '@':
        await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
    else:
        await state.finish()
        del_one_channel(message.text)
        await bot.send_message(message.chat.id, 'Удаление завершено')


############################  REG ONE CHANNEL  ###################################
@dp.callback_query_handler(text='new_channel')  # АДМИН КНОПКА Добавления нового трафика
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь название нового канала в формате\n'
                                                 '@name_channel')
    await reg.name.set()


@dp.message_handler(state=reg.name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    check_dog = message.text[:1]
    if check_dog != '@':
        await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
    else:
        reg_one_channel(message.text)
        await bot.send_message(message.chat.id, 'Регистрация успешна')
        await state.finish()


################################    REG MANY CHANNELS    ###########################

@dp.callback_query_handler(text='new_channels')  # АДМИН КНОПКА Добавления новые телеграмм каналы
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь список каналов в формате\n'
                                                 '@name1 @name2 @name3 ')
    await reg.fname.set()


@dp.message_handler(state=reg.fname, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Каналы зарегистрированы')
    reg_channels(message.text)
    await state.finish()

#####################################################################################


@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    a = info_members() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')


########################  Рассылка  ################################

@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.st_name.set()


@dp.callback_query_handler(text='otemena',state="*")
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.delete_message(call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()


@dp.message_handler(state=st_reg.st_name,content_types=['text','photo','video','video_note'])
async def fname_step(message: types.Message, state: FSMContext):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time").fetchall()
    bad = 0
    good = 0
    await bot.send_message(message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await message.copy_to(i[0])
            good += 1
        except:
            bad += 1

    await bot.send_message(
        message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################