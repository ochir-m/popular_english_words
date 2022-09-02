import sqlite3
import types
import telebot

TOKEN = None
with open('token.txt') as f:
    TOKEN = f.read().strip()
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

#functions for queries
def execute_one_query(query):
    cursor.execute(query)
    result = cursor.fetchone()
    return result

def execute_many_queries(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    random = types.KeyboardButton('Рандомное слово')
    random_10 = types.KeyboardButton('10 рандомных слов')
    train_rus = types.KeyboardButton('Потренироваться (rus-eng)')
    train_eng = types.KeyboardButton('Потренироваться (eng-rus)')

    markup.add(random, random_10, train_rus, train_eng)

    mess = f'Привет! 2 000 английских слов покрывают примерно 80-90% устной речи. Это означает, что запомнив всего ' \
           f'2 000 слов, вы сможете с легкостью поддерживать общение на повседневные темы. ' \
           f'Изучая всего по 10 слов в день, вы сможете освоить все 2 000 слов примерно за полгода. ' \
           f'А этот бот поможет вам в этом. Удачи! И главное помните, что заниматься нужно ежедневно хотя бы по 5 минут 😉' \
           f'Выбери любую команду в меню, чтобы начать обучение 👇'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()
    if get_message_bot == 'рандомное слово':
        select_words = "SELECT eng, rus FROM english_words ORDER BY RANDOM() LIMIT 1"
        words = execute_one_query(select_words)
        final_message = f"{words[0]} - {words[1]}"

    elif get_message_bot == '10 рандомных слов':
        select_words = "SELECT eng, rus FROM english_words ORDER BY RANDOM() LIMIT 10"
        words = execute_many_queries(select_words)
        final_message = ""
        for word in words:
            final_message += f"{word[0]} - {word[1]} \n"

    elif get_message_bot == 'потренироваться (rus-eng)':
        final_message = 'тренировка 1'
    elif get_message_bot == 'потренироваться (eng-rus)':
        final_message = 'тренировка 2'

    else:
        final_message = 'Выбери команду из списка 👇'
    bot.send_message(message.chat.id, final_message, parse_mode='html')

bot.polling(none_stop=True)