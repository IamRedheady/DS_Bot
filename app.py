import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5508024822:AAELlrGvRzyh-Loe5--2e9OQjEeoz7PV0bQ'


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


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    postData(message.from_user.id)
    await message.reply("""Приветствуем Вас, в рядах последователей тайного мира наслаждений!
    
Благодарим, что доверяете нам свой комфорт. 

Мы будем напоминать, о предстоящих мероприятиях Dark Secrets, анонсы которых всегда можно посмотреть в нашем основном канале:

https://t.me/joinchat/SMMtj7Qh26ZHkZUn""")


# @dp.message_handler()
# async def echo(message: types.Message):

#     await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
