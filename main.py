import telebot
from  telebot import  types
import resp_base
import random
import datetime
import os

pagesize=7
allow_perelistivanie=False
dynamic_date=False
perm_date=str(datetime.date(2023,3,10))

with open('token.txt', 'r') as file:
    token = file.readline()
botik=telebot.TeleBot(token)

pd=resp_base.podrobnosti
pdb=resp_base.podrobnosti_bad

with open('admins.txt','r') as file:
    host=file.readline()[:-1]
    admins=(file.readline().split(';'))

rand_spisok_rating_chanse=[]
rand_spisok_rating=[]
with open('rating.txt','r') as file:
    rf=file.readlines()
    for i in rf[0].split(';'):
        rand_spisok_rating_chanse.append(int(i))
    for i in rf[1].split(';'):
        rand_spisok_rating.append(int(i))

pagenum=0
def listik(message):
    global pagesize,allow_perelistivanie,pd,pagenum,pdb,perm_date,rand_spisok_rating_chanse,rand_spisok_rating
    chance=4
    if pagenum<datetime.date.today().day:
        markup = types.InlineKeyboardMarkup(row_width=1)
        pagenum+=1
        if allow_perelistivanie:
            random.shuffle(pd)
            for i in range(1,pagesize+1):
                otzivlist = resp_base.otziv.split(';')
                if rand_spisok_rating_chanse[i]<=chance:
                    otzivlist[0]=str(rand_spisok_rating[i])+(otzivlist[0])[-3:]
                otzivdate=otzivlist[1]
                if dynamic_date:
                    otzivdate=otzivdate[:-2]+str(datetime.date.today().day-pagenum)
                else:
                    otzivdate=perm_date
                buttontext=otzivlist[0]+' | '+otzivdate
                btn=types.InlineKeyboardButton(buttontext, callback_data=str(i)+'#'+buttontext)
                markup.add(btn)
            btn=types.InlineKeyboardButton('>>>',callback_data='page')
            markup.add(btn)
            botik.send_message(message.chat.id,'Отзывы пользователей,\nпо 5 случайных на день',reply_markup=markup)
            random.shuffle(pd)
            random.shuffle(pdb)
        else:
            for i in range(pagesize):
                otzivlist=resp_base.otziv.split(';')
                if rand_spisok_rating_chanse[i]<=chance:
                    otzivlist[0]=str(rand_spisok_rating[i])+(otzivlist[0])[-3:]
                otzivdate=otzivlist[1]
                if dynamic_date:
                    otzivdate=otzivdate[:-2]+str(datetime.date.today().day-pagenum)
                else:
                    otzivdate=perm_date
                buttontext=otzivlist[0]+' | '+otzivdate
                btn=types.InlineKeyboardButton(buttontext,callback_data=str(i)+'#'+buttontext)
                markup.add(btn)
            botik.send_message(message.chat.id, 'Отзывы пользователей', reply_markup=markup)
    else:
        botik.send_message(message.chat.id, 'Доступная база отзывов кончилась')

@botik.message_handler(commands=['start'])
def hi(message):
    with open('userlog.txt','a') as file:
        file.write(f'{datetime.datetime.now()};{message.from_user.first_name};{message.from_user.last_name};{message.from_user.username};{message.from_user.id}\n')
        file.close()
    print(f'{message.from_user.first_name}\n{message.from_user.last_name}\n{message.from_user.username}\n{message.from_user.id}\n')
    if str(message.from_user.id)==host:
        botik.send_message(message.chat.id,'Распознан аккаунт создателя')
        markup=types.ReplyKeyboardMarkup()
        btn=types.KeyboardButton('Отзывы')
        markup.add(btn)
        btn=types.KeyboardButton('stop')
        markup.add(btn)
        btn=types.KeyboardButton('/start')
        markup.add(btn)
        btn=types.KeyboardButton('print_from_base')
        markup.add(btn)
        btn=types.KeyboardButton('regen')
        markup.add(btn)
        botik.send_message(message.chat.id,'Здравствуйте, сэр',reply_markup=markup)
    elif str(message.from_user.id) in admins:
        botik.send_message(message.chat.id,'Распознан аккаунт уполномоченного')
        markup=types.ReplyKeyboardMarkup()
        btn=types.KeyboardButton('Отзывы')
        markup.add(btn)
        btn=types.KeyboardButton('stop')
        markup.add(btn)
        botik.send_message(message.chat.id,'Приветствую',reply_markup=markup)
    else:
        markup=types.InlineKeyboardMarkup(row_width=2)
        btn=types.InlineKeyboardButton('Отзывы', callback_data='page')
        markup.add(btn)
        botik.send_message(message.chat.id,f'Здарова, {message.from_user.first_name}!',reply_markup=markup)

@botik.message_handler(content_types=['text'])
def txt(message):
    if message.text=='Отзывы':
        listik(message)
    global admins
    if message.text=='stop':
        if str(message.from_user.id) in admins:
            botik.send_message(message.chat.id,'Бот отключён')
            os.kill(os.getpid(),1337)
        else:
            botik.send_message(message.chat.id,'Недостаточно полномочий, ваш id:\n'+str(message.from_user.id))
    if message.text[:16]=='print_from_base':
        if str(message.from_user.id)==host:
            msg=''
            for i in resp_base.podrobnosti:
                msg+=(i+'\n\n')
            botik.send_message(message.chat.id,msg)
    if message.text[:4]=='cmd ':
        if str(message.from_user.id)==host:
            print(message.text[4:])
            os.system(message.text[4:])
    if message.text[:9]=='pagesize ':
        global pagesize
        pagesize=int(message.text[9:])
    if message.text[:21]=='allow_perelistivanie ':
        global allow_perelistivanie
        if message.text[21:]=='t':
            allow_perelistivanie=True
        else:
            allow_perelistivanie=False
    if message.text[:13]=='dynamic_date ':
        global dynamic_date
        allow_perelistivanie=bool(message.text[13:])
    if message.text[:10]=='perm_date ':
        global perm_date
        dta=message.text[10:].split('.')
        perm_date=str(datetime.date(int(dta[2]),int(dta[1]),int(dta[0])))
    if message.text=='regen':
        os.popen('python rategen.py')
        global rand_spisok_rating_chanse,rand_spisok_rating
        with open('rating.txt','r') as file:
            rf=file.readlines()
            for i in rf[0].split(';'):
                rand_spisok_rating_chanse.append(int(i))
            for i in rf[1].split(';'):
                rand_spisok_rating.append(int(i))
        botik.send_message(message.chat.id,'Шансы и рейтинг сгенерированы заново')

@botik.callback_query_handler(func=lambda call: True)
def cback(call):
    if call.message:
        if call.data=='page':
            listik(call.message)
        else:
            cdl=call.data.split('#')
            otzivlist=cdl[1].split(' | ')
            global pd,pdb
            if otzivlist[0].split('/')[0]=='10':
                msg='Рейтинг '+otzivlist[0]+'\nДата '+otzivlist[1]+'\nКомментарий: \n'+pd[int(cdl[0])]
            else:
                msg='Рейтинг '+otzivlist[0]+'\nДата '+otzivlist[1]+'\nКомментарий: \n'+pdb[int(cdl[0])]
            botik.send_message(call.message.chat.id,msg)

botik.polling(none_stop=True)
