import telebot
from telebot import types
bot = telebot.TeleBot('YOUR_TOKEN')

URL = "https://api.telegram.org/botYOUR_TOKENs/" % BOT_TOKEN
MyURL = "https://example.com/hook"

api = requests.Session()
application = tornado.web.Application([
    (r"/", Handler),
])

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    try:
        set_hook = api.get(URL + "setWebhook?url=%s" % MyURL)
        if set_hook.status_code != 200:
            logging.error("Can't set hook: %s. Quit." % set_hook.text)
            exit(1)
        application.listen(8888)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        signal_term_handler(signal.SIGTERM, None)

class Handler(tornado.web.RequestHandler):
        def post(self):
            try:
                logging.debug("Got request: %s" % self.request.body)
                update = tornado.escape.json_decode(self.request.body)
                message = update['message']
                text = message.get('text')
                if text:
                    logging.info("MESSAGE\t%s\t%s" % (message['chat']['id'], text))

                    if text[0] == '/':
                        command, *arguments = text.split(" ", 1)
                        response = CMD.get(command, not_found)(arguments, message)
                        logging.info("REPLY\t%s\t%s" % (message['chat']['id'], response))
                        send_reply(response)
            except Exception as e:
                logging.warning(str(e))
               
def send_reply(response):
    if 'text' in response:
        api.post(URL + "sendMessage", data=response)
        
def help_message(arguments, message):
    response = {'chat_id': message['chat']['id']}
    result = ["Hey, %s!" % message["from"].get("first_name"),
              "\rI can accept only these commands:"]
    for command in CMD:
        result.append(command)
    response['text'] = "\n\t".join(result)
    return response

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

@bot.message_handler(commands=['server'])
def send_server(message):
    try:
        # по этому пути на сервере лежит скрипт сбора информации по статусу сервера
        call(["/root/scrps/status.sh"])
        # читает файл с результатами выполнения скрипта
        status = open("/root/scrps/status.txt", "rb").read()
        bot.send_message(message.chat.id, status, parse_mode="Markdown")
    except Exception as e:
        logger.exception(str(e))
        bot.send_message(message.chat.id, "Ошибка при получении статуса сервера. Подробности в журнале.")

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
