import json
import settings
import telebot

token = settings.TOKEN

bot = telebot.TeleBot(token)

with open("user_data.json", "r", encoding="utf-8") as file:
    user_data = json.load(file)

@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Edu English (by @kidroier)")

@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, "Edu English Bot, Комманды: /help /questions , Автор: @kidroier")

@bot.message_handler(commands=["learn"])
def handle_learn(message):
    bot.send_message(message.chat.id, user_data)

@bot.message_handler(commands=["addword"])
def handle_addword(message):
    global user_data
    chat_id = message.chat.id
    user_dict = user_data.get(chat_id, {})

    words = message.text.split()[1:]
    if len(words) == 2:
        word, translation = words[0].lower(), words[1].lower()
        user_dict[word] = translation

        user_data[chat_id] = user_dict

        with open("user_data.json", "w", encoding="utf-8") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)
        bot.send_message(chat_id, f"Слово {word} добавлено в словарь.")
    else:
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте ещё раз")

if __name__ == "__main__":
    bot.polling(none_stop=True)
