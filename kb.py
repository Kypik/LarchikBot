from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def product_inline_button():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Хочу!', url='https://t.me/chudo_larchik_bot'))
    return kb.as_markup()

async def list_products(products, callbacks):
    buttons = []
    for i in range(0, min(len(products), 10), 2):
        if i + 1 < len(products):
            buttons.append([InlineKeyboardButton(text=products[i], callback_data=callbacks[i]),
                            InlineKeyboardButton(text=products[i + 1], callback_data=callbacks[i + 1])])
        else:
            buttons.append([InlineKeyboardButton(text=products[i], callback_data=callbacks[i])])
        
    if len(products) > 10:
        buttons.append([InlineKeyboardButton(text='Дальше', callback_data=f'continue_10')])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def next_list_products(products, callbacks, c):
    buttons = []
    l = min(c + 10, len(products))
    
    for i in range(c, l, 2):
        if i + 1 < len(products):
            buttons.append([InlineKeyboardButton(text=products[i], callback_data=callbacks[i]),
                            InlineKeyboardButton(text=products[i + 1], callback_data=callbacks[i + 1])])
        else:
            buttons.append([InlineKeyboardButton(text=products[i], callback_data=callbacks[i])])

    button = []
    if c >= 10:
        button.append(InlineKeyboardButton(text='Назад', callback_data=f'previous_{c}'))
    if l < len(products):
        button.append(InlineKeyboardButton(text='Дальше', callback_data=f'continue_{l}'))
    
    buttons.append(button)
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def previous_list_products(products, callbacks, c):
    buttons = []
    c -= 10
    l = max(c, 0)
    
    for i in range(l, min(c + 10, len(products)), 2):
        if i + 1 < len(products):
            buttons.append([InlineKeyboardButton(text=products[i], callback_data=callbacks[i]),
                            InlineKeyboardButton(text=products[i + 1], callback_data=callbacks[i + 1])])
        else:
            buttons.append([InlineKeyboardButton(text=products[i], callback_data=callbacks[i])])

    button = []
    if l > 0:
        button.append(InlineKeyboardButton(text='Назад', callback_data=f'previous_{l}'))
    if l + 10 < len(products):
        button.append(InlineKeyboardButton(text='Дальше', callback_data=f'continue_{l + 10}'))
    
    buttons.append(button)
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def confirm(callback):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Да!', callback_data=f'{callback}_yes'))
    kb.add(InlineKeyboardButton(text='Нет...', callback_data="нет"))
    return kb.as_markup()

async def admin_panel():
    buttons = [[InlineKeyboardButton(text='Показать все товары и бронь', callback_data='show_all')],
               [InlineKeyboardButton(text='Показать все резервации', callback_data='show_reservation')],
               [InlineKeyboardButton(text='Удалить товар из списка', callback_data='delete_product')],
               [InlineKeyboardButton(text='Добавить товар', callback_data='new_product')]]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def delete_product(products, callbacks):
    buttons = []
    for i in range(0, 10, 2):
        try:
            buttons.append([InlineKeyboardButton(text=products[i], callback_data=f"{callbacks[i]}_del"),
                            InlineKeyboardButton(text=products[i + 1], callback_data=f"{callbacks[i + 1]}_del")])
            
        except:
            buttons.append([InlineKeyboardButton(text=products[i], callback_data=f"{callbacks[i]}_del")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data='back')])    
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb

async def accept_delete(callback):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Да', callback_data=f'del_{callback}'))
    kb.add(InlineKeyboardButton(text='Нет', callback_data="back"))
    return kb.as_markup()

async def back_to_panel():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text='Назад', callback_data=f'back'))
    return kb.as_markup()