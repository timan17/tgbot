# Импортирование библиотек(Telegram API) и JSON(для разбора ответа)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests, json
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext


# Получение ответа от сервера по URL в формате JSON
def getURLDog():
    # Получение ответа от сервера по URL в формате JSON
    contents = requests.get('https://random.dog/woof.json').json()
    # Получение URL картинки по 'url' ключу
    url = contents['url']
    return url


def getURLQuote():
    # Получение рандомного ответа ввиде json-цитаты
    response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    data = response.json()
    return data['quote']


def start(sefl, update: Update, context: CallbackContext) -> None:
    """Функция отправки меню бота пользователю.

    Функция закрепреляет к каждой кнопке меню специальный идентификатор и
    отправляет меню из кнопок пользователю.
    """

    keyboard = [
        [
            # Присваиваем каждому меню коллбэк идентификатор
            InlineKeyboardButton("Dog", callback_data='1'),
            InlineKeyboardButton("Quote", callback_data='2'),
            InlineKeyboardButton("Weather", callback_data='3')
        ],
        [InlineKeyboardButton("Help!", callback_data='4')],
    ]
    # Определяем что ответ пользователю будет меню ввиде обьектов InlineKeyboardButton
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отвечаем пользователю сообщение ввиде меню
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


# Обрабатываем нажатие определенной кнопки меню
def button(sefl, update: Update, context: CallbackContext) -> None:
    """Функция обработчик нажатий кнопок.

    Функция обрабатывает нажания кнопок пользователем в окне телеграмма.
    Обработка основана на использовании идентификаторов кнопок.
    """

    # Присываииваем контекст
    query = update.callback_query
    query.answer()
    # Взываем ту или иную функцию по проверки коллбэк идентификатора
    if query.data == "1":
        sefl.dog(update, context)
    if query.data == "2":
        sefl.quote(update, context)
    if query.data == "3":
        context.bot.send_message(chat_id=update.effective_chat.id, text="/weather country_name")
    if query.data == "4":
        help(update, context)


# Функция help отвечает справкой пользователю
def help(update: Update, context: CallbackContext):
    """Функция отправки справки пользователю.

    Функция отправляет справку по командам бота.
    """

    helpMessage = ""
    # Открываем файл спарвки
    with open("test.txt", 'r') as fileObject:
        for sentence in fileObject:
            helpMessage += sentence
    # Высылаем справку
    context.bot.send_message(chat_id=update.effective_chat.id, text=helpMessage)


def getWeatherResponse(city):
    # API ключ получаем на сайте провайдера прогноза погоды
    API = "6cae83bb26e34737a7ae627581f34e92"
    URL = "http://api.openweathermap.org/data/2.5/weather?"
    # Формируем конечный URL адрес
    complete_url = URL + "appid=" + API + "&q=" + city
    # Далем запрос
    response = requests.get(complete_url)
    # Конвертируем ответ в JSON
    x = response.json()
    return x


def getWeather(update, context):
    # Проверка аргумента(Города), если аргумента нет, высылаем справку
    if len(context.args) == 0:
        return "/weather location_name\n\nMust has arguments."
    # Получаем город из запроса
    cityName = " ".join(context.args)
    x = getWeatherResponse(cityName)
    # Разбираем JOSN ответ
    if x["cod"] != "404":
        y = x["main"]
        # Сохраняем температуру
        current_temperature = y["temp"]
        # Сохраняем погоду и описание
        z = x["weather"]
        weather_description = z[0]["description"]
        result = "Current temperature: " + str(current_temperature) + "\n" \
                                                                      "Description: " + str(weather_description) + "\n"
        return result
    else:
        return "City is not found"


def weather(update, context):
    """Функция отправки прогноза погоды.

    Функция отправляет прогноз погода по указанному городу пользователю.
    Данна функция требует api-ключ. Функция проверяет наличия аргумента указания названия
    города.
    """

    text = update.effective_message.text
    # Получаем погоду по городу
    response = getWeather(update, context)
    # Отсылаем ответ пользователю
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def echo(update: Update, context: CallbackContext):
    """Функция отправки эхо-сообщения пользователю

    Функция отправляет обратно тоже самое сообщение которое пользователь послал
    боту.
    """

    update.message.reply_text(update.message.text)


def dog(update, context):
    """Функция отправки картинки собаки

    Функция использует запрос к серверу для получения случайных картинок собак и
    отправки их пользователю. Запрос не требует API-ключ.
    Пользователю отправляется URL-адрес картинки.
    """

    response = getURLDog()
    chat_id = update.effective_chat.id
    # Отсылаем ответ пользователю с фото собаки
    context.bot.send_photo(chat_id=chat_id, photo=response)


def quote(update: Update, context: CallbackContext):
    """Функция отправки пользователю цитаты

    Функция использует запрос к серверу для генирации случайных цитат и
    отправки их пользователю. Запрос не требует API-ключ.
    """

    quoteText = getURLQuote()
    # Отсылаем ответ пользователю с цитатой в теле сообщения
    context.bot.send_message(chat_id=update.effective_chat.id, text=quoteText)
    # update.message.reply_text(data['quote'])


def main(sefl):
    """Функция точка входа бота.

    Функция закрпеляет команды отправляемые пользователем к обработчикам ввиде
    функций. Использует API-ключ доступа.
    """
    # Ключ API для работы бота. Получае из Bot-father
    updater = Updater('5091308511:AAHFVzStrznzMvea4Pjj5L4ba7-8TthcHGo')
    # Создаем дейсптечер для принятия от телеграма сообщения в нашу программу
    dp = updater.dispatcher
    # Привязываем команды которые будет отсылать пользователь к нашим функциям
    # Команда start - запускает меню бота (/start)
    dp.add_handler(CommandHandler('start', sefl.start))
    dp.add_handler(CallbackQueryHandler(sefl.button))
    # Команда запускает отсылку рандомной собаки (/dog)
    dp.add_handler(CommandHandler('dog', sefl.dog))
    # Команда запускает отсылку циатыт пользователю
    dp.add_handler(CommandHandler('quote', sefl.quote))
    # Команда запускает отсылку справки пользователю
    dp.add_handler(CommandHandler('help', help))
    # Команда запускает отсылку прогноза погода пользователю
    dp.add_handler(CommandHandler('weather', sefl.weather))
    # Перенаправляем запрос пользователю обратно пользователю
    dp.add_handler(MessageHandler(Filters.text, sefl.echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
