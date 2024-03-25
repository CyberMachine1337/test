import telebot
from telebot import types

bot = telebot.TeleBot("6968339719:AAHmYAJqC7jYztl0UYT8ZwRs1NOd_5GGcGc")
user_state = {}
questions = ["Вопрос 1: ...", "Вопрос 2: ...", "Вопрос 3: ..."]
user_stats = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_state[chat_id] = {"state": "start", "current_question": 0}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Прохождение опроса')
    item2 = types.KeyboardButton('Просмотр личной статистики')
    item3 = types.KeyboardButton('Создание вопроса')
    item4 = types.KeyboardButton('Удаление вопроса')
    item5 = types.KeyboardButton('Просмотр общей статистики')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Прохождение опроса')
def quiz(message):
    chat_id = message.chat.id
    user_state[chat_id] = {"state": "answering_question", "current_question": 0}
    user_stats[chat_id] = {"Да": 0, "Нет": 0}
    send_question(chat_id)

@bot.message_handler(func=lambda message: message.text == 'Просмотр личной статистики')
def personal_stats(message):
    chat_id = message.chat.id
    stats = user_stats.get(chat_id, {})
    stat_message = f"Личная статистика:\nДа: {stats.get('Да', 0)}\nНет: {stats.get('Нет', 0)}"
    bot.send_message(chat_id, stat_message)

@bot.message_handler(func=lambda message: message.text == 'Создание вопроса')
def create_question(message):
    chat_id = message.chat.id
    if chat_id == 830388125:
        bot.send_message(chat_id, "Введите новый вопрос:")
        user_state[chat_id] = "waiting_for_question"
    else:
        bot.send_message(chat_id, "У вас нет прав администратора")

@bot.message_handler(func=lambda message: message.text == 'Удаление вопроса')
def delete_question(message):
    chat_id = message.chat.id
    if chat_id == 830388125:
        bot.send_message(chat_id, "Выберите номер вопроса для удаления:")
        user_state[chat_id] = "waiting_for_question_number"
    else:
        bot.send_message(chat_id, "У вас нет прав администратора")

@bot.message_handler(func=lambda message: message.text == 'Просмотр общей статистики')
def overall_stats(message):
    chat_id = message.chat.id
    if chat_id == 830388125:
        bot.send_message(chat_id, "Общая статистика: ...")
    else:
        bot.send_message(chat_id, "У вас нет прав администратора")

def send_question(chat_id):
    question_number = user_state[chat_id]["current_question"]
    bot.send_message(chat_id, questions[question_number])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Да')
    item2 = types.KeyboardButton('Нет')
    markup.add(item1, item2)
    bot.send_message(chat_id, "Ответьте на вопрос:", reply_markup=markup)

@bot.message_handler(func=lambda message: user_state.get(message.chat.id, {}).get("state") == "answering_question")
def answer_question(message):
    chat_id = message.chat.id
    answer = message.text
    user_stats[chat_id][answer] = user_stats[chat_id].get(answer, 0) + 1
    user_state[chat_id]["current_question"] += 1
    if user_state[chat_id]["current_question"] < len(questions):
        send_question(chat_id)
    else:
        bot.send_message(chat_id, "Опрос завершен. Спасибо за участие!")

@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "waiting_for_question")
def handle_new_question(message):
    chat_id = message.chat.id
    new_question = message.text
    bot.send_message(chat_id, "Новый вопрос успешно добавлен!")

@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == "waiting_for_question_number")
def handle_question_number(message):
    chat_id = message.chat.id
    question_number = message.text
    bot.send_message(chat_id, "Вопрос успешно удален!")


bot.polling()