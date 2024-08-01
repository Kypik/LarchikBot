import json
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

import kb, db
from main import bot
rout = Router()

admins = {2038755799, 2136268830, 980477111}

dict_products = {}

class MyState(StatesGroup):
    waiting_for_new_product = State()
    waiting_for_phone = State()


### Для админов 

@rout.channel_post(F.photo)
async def check_new_post(msg: Message):
    if msg.chat.username == 'chudo_larchik':
        temp = msg.caption.split('\n')
        product = temp[0]
        price = temp[-1]
        description = '\n'.join(temp[1:-1])
        kbn = await kb.product_inline_button()
        await msg.edit_reply_markup(reply_markup=kbn)
        await db.add_product(product, price, description)

@rout.message(Command('admin'))
async def admin(msg: Message):
    if msg.from_user.id in admins:
        await admin_panel(msg)
        
@rout.callback_query(F.data == 'back')
async def back(cb: CallbackQuery):
    if cb.from_user.id in admins:
        await cb.message.delete()
        await admin_panel(cb.message)

@rout.callback_query(F.data == 'show_all')
async def show_all(cb: CallbackQuery):
    if cb.from_user.id in admins:
        await cb.message.delete()
        data = await db.get_info('products')
        lt = []
        kbn = await kb.back_to_panel()
        for el in data:
            if el[-2] is None:
                lt.append(f'Товар - {el[0]}\nПока нет желающих приобрести')
            else:
                temp = json.loads(el[-2])
                lt.append(f'Товар - {el[0]}\nЖелающие приобрести: {', '.join(temp)}')
        if lt == []:
            await cb.message.answer('Сейчас нет товаров', reply_markup=kbn)
        else:
            await cb.message.answer('\n\n'.join(lt), reply_markup=kbn)

@rout.callback_query(F.data == 'show_reservation')
async def show_reservation(cb: CallbackQuery):
    if cb.from_user.id in admins:        
        await cb.message.delete()
        kbn = await kb.back_to_panel()
        try:
            data = await db.get_info('reservating')
            lt = []
            for el in data:
                lt.append(f'{el[0]}: {el[2]} - {el[1]} id')
            await cb.message.answer('\n\n'.join(lt), reply_markup=kbn)
        except:
            await cb.message.answer('Нет резерваций', reply_markup=kbn)

@rout.callback_query(F.data == 'delete_product')
async def select_product_delete(cb: CallbackQuery):
    if cb.from_user.id in admins:
        global dict_products
        await cb.message.delete()
        dict_products = await db.get_products()
        kbn = await kb.delete_product(tuple(dict_products.keys()), tuple(dict_products.values()))
        await cb.message.answer("Выберете товар, который нужно убрать из доступа", reply_markup=kbn)

@rout.callback_query(F.data.endswith('_del'))
async def delete_product(cb: CallbackQuery):
    if cb.from_user.id in admins:
        await cb.message.delete()
        temp = await db.get_description(cb.data[:-4])
        description = temp[0]
        price = temp[-1]
        product = [k for k, v in dict_products.items() if v == cb.data[:-4]]
        kbn = await kb.accept_delete(cb.data[:-4])
        await cb.message.answer(f'{product[0]}\n{description}\n{price}\n\nВы уверены, что хотите удалить этот товар?', reply_markup=kbn)

@rout.callback_query(F.data.startswith('del_'))
async def accept_delete(cb: CallbackQuery):
    if cb.from_user.id in admins:
        await db.delete_product(cb.data[4:])
        await cb.message.delete()
        await admin_panel(cb.message)

@rout.callback_query(F.data == 'new_product')
async def ask_new_product(cb: CallbackQuery, state: FSMContext):
    if cb.from_user.id in admins:
        await cb.message.delete()
        await cb.message.answer('Введите название, описание и цену товара (всё с отступами), которого вы хотите добавить')
        await state.set_state(MyState.waiting_for_new_product)

@rout.message(MyState.waiting_for_new_product)
async def add_new_product(msg: Message, state: FSMContext):
    if msg.from_user.id in admins:
        await state.clear()
        temp = msg.text.split('\n')
        product = temp[0]
        description = '\n'.join(temp[1:-1])
        price = temp[-1]
        kbn = await kb.back_to_panel()
        try:
            await db.add_product(product, price, description)
            await msg.answer(f"{msg.text}\n\nТовар добавлен в список!", reply_markup=kbn)
        except:
            await msg.answer(f"Не удалось добавить товар", reply_markup=kbn)
        

async def admin_panel(msg):
    kbn = await kb.admin_panel()
    await msg.answer("АДМИН ПАНЕЛЬ", reply_markup=kbn)


### Для пользователей 


@rout.message(Command('start'))
async def start(msg: Message, state: FSMContext):
    global dict_products
    await state.clear()
    dict_products = await db.get_products()
    await msg.answer("Привет!✨\nЭто бот для резервации товара🔒\n\nКанал - @chudo_larchik\nПо техническим проблемам - @kkypik", parse_mode=ParseMode.HTML)
    id = msg.from_user.id
    await send_list_products(msg)

async def send_list_products(msg):
    global dict_products
    dict_products = await db.get_products()

    if len(dict_products) == 0:
        await msg.answer("На данный момент нет доступных товаров!😣 Загляните не много позже⏳", parse_mode=ParseMode.HTML)
    else:
        kbn = await kb.list_products(tuple(dict_products.keys()), tuple(dict_products.values()))
        await msg.answer("Выберете товар который хотите зарезервировать", reply_markup=kbn)

@rout.callback_query(F.data.startswith('continue_'))
async def next_list_product(cb: CallbackQuery):
    global dict_products
    c = int(cb.data.split('_')[1])
    dict_products = await db.get_products()
    kbn = await kb.next_list_products(tuple(dict_products.keys()), tuple(dict_products.values()), c)
    await cb.message.edit_reply_markup(reply_markup=kbn)
    
@rout.callback_query(F.data.startswith('previous_'))
async def previous_list_product(cb: CallbackQuery):
    global dict_products
    c = int(cb.data.split('_')[1])
    dict_products = await db.get_products()
    kbn = await kb.previous_list_products(tuple(dict_products.keys()), tuple(dict_products.values()), c)
    await cb.message.edit_reply_markup(reply_markup=kbn)

@rout.callback_query(F.data.endswith('_yes'))
async def get_contact(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    id = cb.from_user.id
    product = [k for k, v in dict_products.items() if v == cb.data[:-4]]
    if id in await db.get_contacts_reserving(product[0]):
        await cb.message.answer("Вы уже зарезервировали этот товар!")
        await send_list_products(cb.message)
    else:
        await db.add_info_in_reservating(product[0], id, cb.from_user.full_name)
        if cb.from_user.username is None:
            await cb.message.answer('Укажите номер телефона для связи')
            await state.set_state(MyState.waiting_for_phone)
        else:
            contact = '@' + cb.from_user.username
            await write_about_resrvation(cb.message, contact, id)
        
@rout.callback_query(F.data == 'нет')
async def back_to_list(cb: CallbackQuery):
    await cb.message.delete()
    await send_list_products(cb.message)

@rout.callback_query()
async def confirm(cb: CallbackQuery):
    global dict_products
    if cb.data in dict_products.values() and cb.data:
        await cb.message.delete()
        temp = await db.get_description(cb.data)
        price = temp[0]
        description = temp[1]
        kbn = await kb.confirm(cb.data)
        product = [k for k, v in dict_products.items() if v == cb.data]
        await cb.message.answer(f'{product[0]}\n{description}\n{price}\n\nВы уверены, что хотите заререзрвировать этот товар?', reply_markup=kbn)

@rout.message(MyState.waiting_for_phone)
async def get_number(msg: Message, state: FSMContext):
    await state.clear()
    contact = msg.text
    await write_about_resrvation(msg, contact, msg.from_user.id)

async def write_about_resrvation(msg, contact, id):
    list_reservating = await db.get_info_from_reservating(id)
    product = list_reservating[-1]
    await msg.answer(f'Товар {product} зарезервирован\n\nСвязь: +7(914)881-32-23 - WhatsApp')
    list_contacts = await db.get_contacts_reserving(product)
    list_contacts.append(contact)
    await db.add_contacts_reserving(product, list_contacts)
    await bot.send_message(chat_id=2038755799, text=f'Пользователь {contact} зарезервировал товар {product}') #


