import unittest
from unittest import mock
from unittest.mock import patch
from Bot import *

class BotTests(unittest.TestCase):
    @mock.patch("Bot.getURLQuote")
    def test_quote(self, mock_get_url_quote):
        update = unittest.mock.Mock()
        context = unittest.mock.Mock()
        mock_get_url_quote.return_value = "I like IT"
        update.message.text = 'I like IT'
        update.effective_chat.id = 3
        quote(update, context)
        context.bot.send_message.assert_called_with(chat_id=update.effective_chat.id, text=update.message.text)

    def test_echo(self):
        update = unittest.mock.Mock()
        context = unittest.mock.Mock()
        update.message.text = 'echo test'
        echo(update, context)
        update.message.reply_text.assert_called_with(update.message.text)

    @mock.patch("Bot.getWeather")
    def test_weather(self, mock_getWeatherResponse):
        update = unittest.mock.Mock()
        context = unittest.mock.Mock()
        mock_getWeatherResponse.return_value = "Cloud, 221F"
        update.message.text = 'Cloud, 221F'
        update.effective_chat.id = 3
        weather(update, context)
        context.bot.send_message.assert_called_with(chat_id=update.effective_chat.id, text=update.message.text)

    @mock.patch("Bot.getURLDog")
    def test_dog(self, mock_getURLDog):
        update = unittest.mock.Mock()
        context = unittest.mock.Mock()
        mock_getURLDog.return_value = "some url address"
        update.message.text = 'some url address'
        update.effective_chat.id = 3
        dog(update, context)
        context.bot.send_photo.assert_called_with(chat_id=update.effective_chat.id, photo=update.message.text)
