import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import link
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '5508024822:AAELlrGvRzyh-Loe5--2e9OQjEeoz7PV0bQ'

yaroslavID = 296143439
arturID = 192150244

currentID = yaroslavID


# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def postData(id):
    rget = requests.get(
        'https://dsbot-4f2a2-default-rtdb.firebaseio.com/clients.json')

    rgetAnswer = rget.json()

    print(rgetAnswer)

    check = False

    for value in rgetAnswer.values():
        print(value["tgid"])
        if value['tgid'] == id:
            check = True

    if check:
        print("Данные не отправляем, клиент уже есть...")
    else:
        r = requests.post(
            'https://dsbot-4f2a2-default-rtdb.firebaseio.com/clients.json', json={"tgid": id})


def getUsers():
    rget = requests.get(
        'https://dsbot-4f2a2-default-rtdb.firebaseio.com/clients.json')
    rgetAnswer = rget.json()
    return rgetAnswer


inline_btn_1 = InlineKeyboardButton(
    '⚜️ DS ⚜️', url="https://t.me/joinchat/SMMtj7Qh26ZHkZUn")
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

# Приветствие


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    postData(message.from_user.id)

    await bot.send_message(message.from_user.id, f"""Приветствуем Вас, в рядах последователей тайного мира наслаждений!
    
Благодарим, что доверяете нам свой комфорт. 

Мы будем напоминать, о предстоящих мероприятиях Dark Secrets, анонсы которых всегда можно посмотреть в нашем основном канале.""", parse_mode="markdown", disable_web_page_preview=True, reply_markup=inline_kb1)


reply_btn_chat = InlineKeyboardButton(
    'Вступить в чат', url="https://t.me/welcomedarksecrets")
reply_btn_event = InlineKeyboardButton(
    'Посетить мероприятие', url="https://t.me/facecontroleds")
echo_reply_markup = InlineKeyboardMarkup(row_width=2).add(
    reply_btn_chat).add(reply_btn_event)


# Просто текст
@dp.message_handler()
async def echo(message: types.Message):
    for value in getUsers().values():
        if value['tgid'] != currentID and currentID == message.from_user.id:
            await bot.send_message(value['tgid'], message.text)
    if message.from_user.id != currentID:
        await bot.send_message(message.from_user.id, "Все интересующие вас вопросы, можете уточнить у нашего менеджера: @MrJamesBrown", reply_markup=echo_reply_markup)


# Текст с фото
@dp.message_handler(content_types=["photo"])
async def echoPhoto(message: types.Message):
    for value in getUsers().values():
        if value['tgid'] != currentID and currentID == message.from_user.id:
            await bot.send_photo(value['tgid'], message.photo[-1].file_id, message.caption)
    if message.from_user.id != currentID:
        await message.reply("Все интересующие вас вопросы, можете уточнить у нашего менеджера: @MrJamesBrown", reply_markup=echo_reply_markup)


# Текст с видео
@dp.message_handler(content_types=["video"])
async def echoPhoto(message: types.Message):
    for value in getUsers().values():
        if value['tgid'] != currentID and currentID == message.from_user.id:
            await bot.send_video(value['tgid'], message.video.file_id, caption=message.caption)
    if message.from_user.id != currentID:
        await message.reply("Все интересующие вас вопросы, можете уточнить у нашего менеджера: @MrJamesBrown", reply_markup=echo_reply_markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
