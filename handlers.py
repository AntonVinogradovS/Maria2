import random
from aiogram import types, Router
from aiogram import Dispatcher
from aiogram.filters.command import Command, CommandStart
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F
from database import insert_payment, read_payment_by_id, read_payment, delete_payment_by_id
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from createBot import bot
#from database import insert_data
TEST_TOKEN = '390540012:LIVE:50661'
PRICE1 = types.LabeledPrice(label="Подписка на 1 месяц", amount=555*100)  # в копейках (руб)
PRICE3 = types.LabeledPrice(label="Подписка на 3 месяц", amount=1355*100)  # в копейках (руб)
user_router = Router()
def kb():
    buttons = [
        [types.InlineKeyboardButton(text="Подписка на 1 месяц", callback_data="sub_1_month")],
        [types.InlineKeyboardButton(text="Подписка на 3 месяца", callback_data="sub_3_month")],
        [types.InlineKeyboardButton(text="Подписка на 1 месяц через PayPal", callback_data="sub_pal")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
def kb2(id):
    buttons = [[
        types.InlineKeyboardButton(text="Подтвердить", callback_data=f"good_{id}"),
        types.InlineKeyboardButton(text="Отклонить", callback_data=f"deny"),
    ]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
async def send_message(dp: Dispatcher):
    users = await read_payment()
    # Текущая дата
    current_date = datetime.now().date()

    # Дата, которая находится через три дня от текущей даты
    three_days_later = current_date + timedelta(days=3)
    for user in users:
        payment_date = datetime.strptime(user[1], "%Y-%m-%d").date()
        if payment_date == three_days_later:
            try:
                await bot.send_message(chat_id=user[0], text="До окончании подписки осталось всего 3 дня. Вы можете ее продлить прямо сейчас.", reply_markup=kb())
            except:
                print(user[0])
        if payment_date < current_date:
            
            await bot.ban_chat_member(chat_id='-1002003077509', user_id=user[0])
            await delete_payment_by_id(user[0])
            # try:
            #     await bot.send_message(chat_id=user[0], text=":(")
            # except:
            #     print(':(')

@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(text='Привет! С помощью этого бота ты можешь получить доступ к закрытому каналу <b>Rock&rollный Гуру</b>',parse_mode='HTML', reply_markup=kb())
    #print(message.from_user.id)
    

@user_router.callback_query(F.data == 'sub_1_month')
async def pay_1(callback: types.CallbackQuery):
    await bot.send_invoice(callback.message.chat.id,
                           title="Подписка на канал",
                           description="Активация подписки на 1 месяц",
                           provider_token=TEST_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE1],
                           #start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
    
@user_router.callback_query(F.data == 'sub_3_month')
async def pay_1(callback: types.CallbackQuery):
    await bot.send_invoice(callback.message.chat.id,
                           title="Подписка на канал",
                           description="Активация подписки на 3 месяца",
                           provider_token=TEST_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE3],
                           #start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
    
@user_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    #print("1")

@user_router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    #print(message.successful_payment.total_amount)
    await message.answer('Спасибо за оплату! За 3 дня до окончании подписки я напомню вам!\nhttps://t.me/+F4RTVf_lV-A5YzZi')
    res = await read_payment_by_id(message.from_user.id)
    if message.successful_payment.total_amount == 55500:
        if res == None:
            current_date = datetime.now() + timedelta(days=30)  # Текущая дата плюс один месяц
            print(current_date)
        else:
            #current_date = (datetime.now() + timedelta(days=30)).date() + datetime.strptime(res[1], "%Y-%m-%d").date()
            current_date = datetime.strptime(res[1], "%Y-%m-%d") + timedelta(days=30)
    else:
        if res == None:
            current_date = datetime.now() + timedelta(days=90)  # Текущая дата плюс один месяц
        else:
            current_date = datetime.strptime(res[1], "%Y-%m-%d") + timedelta(days=90)
    
    
    formatted_date = current_date.strftime("%Y-%m-%d")  # Преобразование в строку
    await insert_payment(message.from_user.id, formatted_date)

@user_router.callback_query(F.data == 'sub_pal')
async def pay_pal(callback: types.Message):
    await bot.send_message(chat_id=callback.from_user.id, text="Необходимо произвести оплату в размере 7$ на PayPal по адресу `malinov.yoga@gmail.com` и отправить *скриншот оплаты*.",parse_mode='MarkDown')

@user_router.message(F.photo)
async def mes_photo(message: types.Message):
    print(message.from_user.id)
    if message.chat == 'private':
        await message.answer(text='После проверки я пришлю вам ссылку на канал.')
        await bot.send_photo(chat_id=54787745, photo=message.photo[-1].file_id, reply_markup=kb2(message.from_user.id)) #54787745

@user_router.callback_query(F.data.startswith('good'))
async def pay_good(callback: types.CallbackQuery):
    # print(callback.data.split('_')[1])
    # await bot.send_message(chat_id=callback.data.split('_')[1], text="Спасибо за оплату!\nhttps://t.me/+F4RTVf_lV-A5YzZi")

    us_id = callback.data.split('_')[1]
    await bot.send_message(chat_id=us_id, text ='Спасибо за оплату! За 3 дня до окончании подписки я напомню вам!\nhttps://t.me/+F4RTVf_lV-A5YzZi')
    res = await read_payment_by_id(us_id)
    if res == None:
        current_date = datetime.now() + timedelta(days=30)  # Текущая дата плюс один месяц
        print(current_date)
    else:
        #current_date = (datetime.now() + timedelta(days=30)).date() + datetime.strptime(res[1], "%Y-%m-%d").date()
        current_date = datetime.strptime(res[1], "%Y-%m-%d") + timedelta(days=30)
    
    formatted_date = current_date.strftime("%Y-%m-%d")  # Преобразование в строку
    await insert_payment(us_id, formatted_date)
    await callback.message.delete()

@user_router.callback_query(F.data == 'deny')
async def deny_user(callback: types.CallbackQuery):
    await callback.message.delete()