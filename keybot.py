import telebot
import random
from telebot import types
import string
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


class UserState:
    def __init__(self):
        self.state = 'start'
        self.password_length = None
        self.users = {}


user_state = UserState()


def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def save_users(users):
    with open('users.txt', 'w', encoding='utf-8') as f:
        for user_id, passwords in users.items():
            f.write(f'User ID: {user_id}\n')
            f.write('Passwords:\n')
            for password in passwords:
                f.write(f'{password}\n')
            f.write('\n')


def load_users():
    users = {}
    with open('users.txt', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        user_id = None
        for line in lines:
            if line.startswith('User ID:'):
                user_id = line.split(':')[1].strip()
                users[user_id] = []
            elif line.startswith('Passwords:'):
                continue
            else:
                password = line.strip()
                users[user_id].append(password)
    return users


@bot.message_handler(commands=['start'])
def start(message):
    user_state.users = load_users()
    user_id = str(message.from_user.id)
    if user_id not in user_state.users:
        user_state.users[user_id] = []
        save_users(user_state.users)
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton('Сгенерировать пароль')
    markup.row(button)
    bot.send_message(message.chat.id, 'Привет! Я бот для генерации случайного пароля. Нажми на кнопку ниже, '
                                      'чтобы получить пароль.', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Сгенерировать пароль' and user_state.state == 'start')
def handle_button(message):
    user_state.state = 'choose_length'
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton("Длина пароля 10 символов")
    button2 = types.KeyboardButton("Длина пароля 12 символов")
    button3 = types.KeyboardButton("Длина пароля 16 символов")
    button4 = types.KeyboardButton("Напиши свой вариант пароля(длину)")
    button5 = types.KeyboardButton("Выйти из диалога")
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)
    bot.send_message(message.chat.id, "Выбери длину пароля или напиши свой вариант длины или нажми 'Выйти из диалога':",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: user_state.state == 'choose_length')
def process_length_step(message):
    if message.text == 'Выйти из диалога':
        user_state.state = 'start'
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Вы вышли из диалога.', reply_markup=markup)
    else:
        try:
            if message.text.isdigit():
                length = int(message.text)
                if length <= 0:
                    raise ValueError
            else:
                length = int(message.text.split()[2])
            user_state.password_length = length
            password = generate_password(length)
            bot.send_message(message.chat.id, f"Сгенерированный пароль: {password}")
            user_id = str(message.from_user.id)
            user_state.users[user_id].append(password)
            save_users(user_state.users)
            markup = types.ReplyKeyboardMarkup()
            button = types.KeyboardButton('Сгенерировать другой пароль')
            markup.row(button)
            bot.send_message(message.chat.id, 'Хочешь сгенерировать другой пароль?', reply_markup=markup)
            user_state.state = 'generate_another'
        except (ValueError, IndexError):
            bot.send_message(message.chat.id,
                             "Вы должны выбрать один из вариантов, используя кнопки, или напишите свой вариант длины "
                             "пароля.")


@bot.message_handler(func=lambda message: user_state.state == 'generate_another')
def handle_generate_another(message):
    if message.text == 'Выйти из диалога':
        user_state.state = 'start'
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Вы вышли из диалога.', reply_markup=markup)
    else:
        user_state.state = 'choose_length'
        markup = types.ReplyKeyboardMarkup()
        button1 = types.KeyboardButton("Длина пароля 10 символов")
        button2 = types.KeyboardButton("Длина пароля 12 символов")
        button3 = types.KeyboardButton("Длина пароля 16 символов")
        button4 = types.KeyboardButton("Напиши свой вариант пароля(длину)")
        button5 = types.KeyboardButton("Выйти из диалога")
        markup.row(button1, button2)
        markup.row(button3, button4)
        markup.row(button5)
        bot.send_message(message.chat.id,
                         "Выбери другую длину пароля или напиши свой вариант длины или нажми 'Выйти из диалога': ",
                         reply_markup=markup)


bot.infinity_polling()
