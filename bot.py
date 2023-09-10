import telebot
from telebot import types
bot = telebot.TeleBot('6592342960:AAHxdaDACU-zERBDa2Y4E3IsMtvR4ZfXSI0')

@bot.message_handler(commands = ['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помошник!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Как зайти на мой github??')
        btn2 = types.KeyboardButton('Познакомиться с этим кодом')
        btn3 = types.KeyboardButton('Советы по оформлению публикации')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота
        
    elif message.text == 'Как зайти на мой github?':
      bot.send_message(message.from_user.id, 'Вы просто переходите по' + '[ссылке](https://github.com/kruglovbogL)', parse_mode='Markdown')

    elif message.text == 'Познакомиться с этим кодом':
      bot.send_message(message.from_user.id, 'Познакомиться с этим кодом вы можете по ' + '[ссылке](https://github.com/kruglovbogL/Telegram_bot)', parse_mode='Markdown')

def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Наш сайт', url='https://vk.com/kruglovbog/')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на сайт", reply_markup = markup)

@bot.message_handler(commands = ['launguage'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🇷🇺 Русский")
    btn2 = types.KeyboardButton('🇬🇧 English')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)



bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть