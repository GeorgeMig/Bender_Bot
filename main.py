from curses.panel import bottom_panel
from imaplib import Commands
import random
import telebot, wikipedia, re
from telebot import types

# Загружаем список поговорок
f = open('data/thinks.txt', 'r', encoding='UTF-8')
thinks  = f.read().split('\n')
f.close()

# Создание экземпляра бота
bot = telebot.TeleBot('5416890025:AAGHN2txjpTTzRPMuf-0N8rSCwpdEI7J1Q4')

# Перевод Википедии на русский язык
wikipedia.set_lang("ru")

# Метод очищение текста статей в Википедии и сокращения его размера до 1000 символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'Я хоть и робот, но не всезнайка, Болван. \nСпроси что попроще'

@bot.message_handler(commands=["start"])
def start(m, res=False):
        # Добавляем кнопку
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Сказани чо-нибудь")
        item2 = types.KeyboardButton("Навести справки")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(m.chat.id, 'Здорова, чудик! \nПс.. крч могу навести справки на интересующие тебя темы. Врубаешь? Я же робот в конце концов.. \n\nА еще девочек часто сводят с ума мои фразы. Хочешь проверить? Тогда не промахнись своим жирным пальцем по нужной кнопке.',  reply_markup=markup)

# # Метод обработки команды старт
# @bot.message_handler(commands = ['start'])
# def start (message, res = False):
#     bot.send_message(message.chat.id, '<b>Здорова, чудик! Отправь мне любое слово и я найду его значение на Wikipedia</b>', parse_mode='html')

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Если юзер прислал thinks, выдаем ему случайную цитатку бота
    if message.text.strip() == 'Сказани чо-нибудь':
        answer = random.choice(thinks)
        bot.send_message(message.chat.id, answer) # Отсылаем юзеру сообщение в его чат
    elif message.text.strip() == 'Навести справки':
    # Если юзер прислал иное слово, то бот ему отправит статью из википедии по запросу
        bot.send_message(message.chat.id, 'Напиши чо интересует, а я поищу.')
    else:
        bot.send_message(message.chat.id, getwiki(message.text))
        

# # Метод получения сообщений от юзера и отправка ему статьи
# @bot.message_handler(content_types = ["text"])
# def handle_text(message):
#     bot.send_message(message.chat.id, getwiki(message.text))

print('Server start')
bot.polling(none_stop = True, interval = 0)