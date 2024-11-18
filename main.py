import settings
import telebot

token = settings.TOKEN

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Пиши сюда только с большой буквы!!! (by Kidroier)")

@bot.message_handler(commands=["description"])
def handle_start(message):
    bot.send_message(message.chat.id, "Я тестовый бот, но я уже могу отвечать на доступные вам вопросы!")

@bot.message_handler(commands=["questions"])
def handle_start(message):
    bot.send_message(message.chat.id, "(Все запросы писать с большой буквы!!!) Что в скобках писать не нужно!!! Доступные запросы: 1. Как тебя (то есть бота) зовут? ; 2. ...")



@bot.message_handler(func= lambda message: True)
def handler_all(message):
    if message.text == "Как тебя зовут?":
        bot.send_message(message.chat.id, "У меня пока нет имени, но можешь меня называть своим ботом :)")

if __name__ == "__main__":
    bot.polling(none_stop=True)
