import telebot
import random
import requests
from main import generate_mail, checkMail, deleteMail, domain 
from telebot import types

API = 'https://www.1secmail.com/api/v1/'
bot = telebot.TeleBot('token')

generated_mail = ''

#function to start the bot
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #keyboard in the telegram
    item1 = types.KeyboardButton('/Generate')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Hello! I am a bot that can generate and check mail addresses. Choose an option:', reply_markup=markup)

#function to generate email address
@bot.message_handler(commands=['Generate'])
def create_mail(message):
    global generated_mail    #global variable
    username = generate_mail()
    domain_list = ["1secmail.com", "1secmail.org", "1secmail.net", "wwjmp.com", "esiix.com", "xojxe.com", "yoggm.com"]
    domain = random.choice(domain_list)

    generated_mail = f'{username}@{domain}'  

    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('/Check')
    item2 = types.KeyboardButton('/Delete')
    markup1.add(item1, item2)

    bot.send_message(message.chat.id, f'Your generated mail address: {generated_mail}')
    bot.send_message(message.chat.id, 'Choose an option:', reply_markup=markup1)

#function to check mail
@bot.message_handler(commands=['Check'])
def check_mail_handler(message):
    global generated_mail  
    if generated_mail == '':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('/Generate')
        markup2.add(item1)
        bot.send_message(message.chat.id, '[INFO] You have not generated a mail address yet. Please generate a mail address first!', reply_markup=markup2)

    else:    
        jsonFile = checkMail(mail=generated_mail)  
        length = len(jsonFile)
        if length == 0:
            bot.send_message(message.chat.id, f'[INFO] There are no new messages in the mail yet.')
        else:
            id_list = []

            for i in jsonFile:
                for k, v in i.items():
                    if k == 'id':
                        id_list.append(v)

            bot.send_message(message.chat.id, f'[INFO] You have {length} new message!')
            for i in id_list:
                read_msg = f'{API}?action=readMessage&login={generated_mail.split("@")[0]}&domain={generated_mail.split("@")[1]}&id={i}'
                r = requests.get(read_msg).json()

                sender = r.get('from')
                subject = r.get('subject')
                date = r.get('date')
                content = r.get('textBody')

                bot.send_message(message.chat.id, f'Sender: {sender}\nTo: {generated_mail}\nSubject: {subject}\nDate: {date}\nContent: {content}')

#function to delete email address
@bot.message_handler(commands=['Delete'])
def delete_mail_handler(message):
    global generated_mail  
    if generated_mail == '':
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('/Generate')
        markup2.add(item1)
        bot.send_message(message.chat.id, '[INFO] You have not generated a mail address yet. Please generate a mail address first!', reply_markup=markup2)

    else:
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('/Generate')
        markup2.add(item1)
        deleteMail(generated_mail)
        bot.send_message(message.chat.id, f'[INFO] Mail {generated_mail} has been deleted!', reply_markup=markup2)


bot.polling(none_stop=True)
