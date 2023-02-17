from os import environ
from dotenv import load_dotenv
import telebot

load_dotenv(".env")

API_KEY = environ['API_KEY']

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.reply_to(message, "Hello!")


@bot.message_handler(commands=['start', 'song'])
def start(message):
    bot.send_message(message.chat.id, "Hello!, I'm Miku Hatsune, I'm a bot that sends you a random song from my library, just type /song and I'll send you one!")
def song(message):
    bot.send_message(message.chat.id, "Here's a song for you!")


def get_song_from_youtube():
    pass


bot.polling()