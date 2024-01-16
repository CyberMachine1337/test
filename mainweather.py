import datetime
import requests
import telebot
from config import open_weather_token, tg_bot_token

bot = telebot.TeleBot(tg_bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Напиши мне название города и я пришлю сводку погоды")


@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text
    code_to_smile = {
        "Clear": "Ясно ☀️",
        "Clouds": "Облачно ☁️",
        "Rain": "Дождь 🌧",
        "Drizzle": "Морось 🌧",
        "Thunderstorm": "Гроза ⛈",
        "Snow": "Снег ❄️",
        "Mist": "Туман 🌫"
    }
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно"
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        response = (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                    f"Погода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n"
                    f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                    f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                    f"Хорошего дня!")
        bot.reply_to(message, response)
    except Exception as ex:
        print(ex)
        bot.reply_to(message, "Проверьте название города")


bot.polling()
