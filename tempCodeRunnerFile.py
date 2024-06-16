@bot.message_handler(commands=['stop'])
def stop(message):
    bot.stop_polling()