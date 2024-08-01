import aiosqlite
import json

async def creat_table_products():
    async with aiosqlite.connect('chudo larchik.sql') as db:
        await db.execute("CREATE TABLE IF NOT EXISTS products(product TEXT, description TEXT, price TEXT,  contacts TEXT, callback TEXT)")
        await db.commit()

async def creat_table_reservating():
    async with aiosqlite.connect('chudo larchik.sql') as db:
        await db.execute("CREATE TABLE IF NOT EXISTS reservating(product TEXT, id INT, name TEXT)")
        await db.commit()

async def add_product(product, price, description):
    async with aiosqlite.connect('chudo larchik.sql') as db:
        callback = f'{len(product)}{product[len(product)//3:1:-1]}'
        await db.execute(f"INSERT INTO products (product, description, price, callback) VALUES (?, ?, ?, ?)", (product, description, price, callback))
        await db.commit()

async def add_info_in_reservating(product, id, name):
    async with aiosqlite.connect('chudo larchik.sql') as db:
        await db.execute(f"INSERT INTO reservating (product, id, name) VALUES (?, ?, ?)", (product, id, name))
        await db.commit()

async def get_info_from_reservating(id):
    async with aiosqlite.connect('chudo larchik.sql') as db:
        async with db.execute(f"SELECT product FROM reservating WHERE id = {id}") as curs:
            temp = await curs.fetchall()
            list_reservating = []
            for el in temp:
                for e in el:
                    list_reservating.append(e)
            return list_reservating
            
async def add_contacts_reserving(product, list_contacts):
    list_contacts = json.dumps(list_contacts,)
    async with aiosqlite.connect('chudo larchik.sql') as db:
        await db.execute("UPDATE products SET contacts = ? WHERE product = ?", (list_contacts, product))
        await db.commit()

async def get_contacts_reserving(product):
    async with aiosqlite.connect('chudo larchik.sql') as db:
        async with db.execute(f"SELECT contacts FROM products WHERE product = ?", (product,)) as curs:
            list_contacts = await curs.fetchone()
            try:
                list_contacts = json.loads(list_contacts[0])
                return(list_contacts)
            except:
                return []
            
async def get_products():
    async with aiosqlite.connect('chudo larchik.sql') as db:
        async with db.execute(f"SELECT product, callback FROM products") as curs:
            temp = await curs.fetchall()
            dict_products = {}
            for el in temp:
                for i in range(0, len(el), 2):
                    dict_products[el[i]] = el[i + 1]
            return dict_products

async def get_description(callback):
    async with aiosqlite.connect('chudo larchik.sql') as db:
        async with db.execute(f"SELECT price, description FROM products WHERE callback = ?", (callback, )) as curs:
            temp = await curs.fetchall()
            description = []
            for el in temp:
                for e in el:
                    description.append(e)
            return description
        
async def get_info(table):
    async with aiosqlite.connect('chudo larchik.sql') as db:
        async with db.execute(f"SELECT * FROM {table}") as curs:
            return await curs.fetchall()
        
async def delete_product(callback):
    async with aiosqlite.connect('chudo larchik.sql') as db:
        await db.execute(f"DELETE FROM products WHERE callback = ?", (callback,))
        await db.commit()