import telebot 
import requests
import random
import string
from main import generate_mail

from telebot import types  

API = 'https://www.1secmail.com/api/v1/'
bot = telebot.TeleBot('6944257036:AAF6bbOAw_Cc2DQGB0sRGIvop6LZOw-v5iI')
domain_list = ["1secmail.com", "1secmail.org", "1secmail.net", "wwjmp.com", "esiix.com", "xojxe.com", "yoggm.com"]
domain = random.choice(domain_list)
username = generate_mail()
mail = f'{username}@{domain}'

@bot.message_handler(commands=['start'])                                
def start(message):
    bot.send_message(message.chat.id, "Hello there")



@bot.message_handler(commands=['generate'])
def create_mail(message):
    bot.send_message(message.chat.id, f'[ * ] Your postal address: {mail}')



@bot.message_handler(command=['check'])
def check(message):
    req_link = f'{API}?action=getMessages&login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
    r = requests.get(req_link).json()
    length = len(r)
    if length == 0:
        bot.send_message(message.chat.id,'[INFO] There are no new messages in the mail yet.')
    else:
        id_list = []
        
        for i in r:
            for k, v in i.items():
                if k == 'id':
                    id_list.append(v)
        bot.send_message(message.chat.id,f'[INFO] You have {length} new message!')


@bot.message_handler(command=['stop'])
def stop(message):
    bot.stop_polling()

bot.polling(none_stop=True)
