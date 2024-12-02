import json
import random

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
    bot.send_message(message.chat.id, "Edu English Bot, Команды: /help /learn [цифра сколько слов нужно изучить] /addword [слово по англ] [слово по русс] , Автор: @kidroier")

@bot.message_handler(commands=["learn"])
def handle_learn(message): # /learn 5
    user_words = user_data.get(str(message.chat.id), {})

    try:
        words_number = int(message.text.split()[1])
        ask_translation(message.chat.id, user_words, words_number)
    except IndexError:
       bot.send_message(message.chat.id, "Команда вводиться вот так: /learn [цифра сколько слов нужно изучить]")  # Обработка ошибки Out of range!!!!  $

    except Exception as a:
        print(type(a).__name__, a)


def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id, f"Напиши перевод слова {word}")

        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left)
    else:
        bot.send_message(chat_id, "Вы все изучили!")

def check_translation(message, translation, words_left):
    user_translation = message.text.strip().lower()
    if user_translation == translation.lower():
        bot.send_message(message.chat.id, "Правильно! молодец!")
        words_left -= 1
    else:
        bot.send_message(message.chat.id, f"Неправильно! Правильный перевод {translation}")
        words_left -= 1
    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left)


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
