import telebot

API_KEY = ''
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm your Recipe Bot. You can ask me for recipes by typing /recipe")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Type /recipe followed by ingredients to get a recipe suggestion!")

bot.polling()