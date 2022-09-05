import random
import sqlite3
import types
import telebot

TOKEN = None
with open('token.txt') as f:
    TOKEN = f.read().strip()
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

comments_for_right_answers = ['Правильно!', 'Верно!', 'Молодец! 😉', 'Вау, это правильный ответ! 🔥',
                              'Совершенно верно!', 'Класс, все верно!', 'Отлично! 👍', 'Все верно!',
                              'Да, так держать! 💪']

comments_for_incorrect_answers = ['Попробуй еще раз', 'Не совсем...',
                                  'Не совсем так. Сделай еще попытку 😉']

#functions for queries
def execute_one_query(query):
    cursor.execute(query)
    result = cursor.fetchone()
    return result

def execute_many_queries(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#start
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
           f'А этот бот поможет вам в этом. Удачи! ' \
           f'И главное помните, что заниматься нужно ежедневно хотя бы по 5 минут 😉' \
           f'Выбери любую команду в меню, чтобы начать обучение 👇'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

#main commands (menu)
@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()
    if get_message_bot == 'рандомное слово':
        select_words = "SELECT eng, rus FROM english_words ORDER BY RANDOM() LIMIT 1"
        words = execute_one_query(select_words)
        final_message = f"{words[0]} - {words[1]}"
        bot.send_message(message.chat.id, final_message, parse_mode='html')

    elif get_message_bot == '10 рандомных слов':
        select_words = "SELECT eng, rus FROM english_words ORDER BY RANDOM() LIMIT 10"
        words = execute_many_queries(select_words)
        final_message = ""
        for word in words:
            final_message += f"{word[0]} - {word[1]} \n"
        bot.send_message(message.chat.id, final_message, parse_mode='html')

    elif get_message_bot == 'потренироваться (rus-eng)':
        select_words = "SELECT eng, rus FROM english_words ORDER BY RANDOM() LIMIT 1"
        words = execute_one_query(select_words)
        rus_word = f"{words[1]}"
        msg = bot.send_message(message.chat.id, rus_word, parse_mode='html')
        bot.register_next_step_handler(msg, verify_rus_eng_answer, words)

    elif get_message_bot == 'потренироваться (eng-rus)':
        select_words = "SELECT eng, rus FROM english_words ORDER BY RANDOM() LIMIT 1"
        words = execute_one_query(select_words)
        eng_word = f"{words[0]}"
        msg = bot.send_message(message.chat.id, eng_word, parse_mode='html')
        bot.register_next_step_handler(msg, verify_eng_rus_answer, words)
    else:
        bot.send_message(message.chat.id, 'Выбери команду из списка 👇', parse_mode='html')

#train rus-eng
def get_rus_eng_answer(message, select_words):
    get_words = select_words
    msg = bot.send_message(message.chat.id, get_words[1], parse_mode='html')
    bot.register_next_step_handler(msg, verify_rus_eng_answer, get_words)

def verify_rus_eng_answer(message, verify_words):
    get_words = verify_words
    if message.text.strip().lower() == get_words[0]:
        bot.send_message(message.chat.id, random.choice(comments_for_right_answers), parse_mode='html')
    elif message.text.strip().lower() == 'рандомное слово':
        mess(message)
    elif message.text.strip().lower() == '10 рандомных слов':
        mess(message)
    elif message.text.strip().lower() == 'потренироваться (rus-eng)':
        mess(message)
    elif message.text.strip().lower() == 'потренироваться (eng-rus)':
        mess(message)
    else:
        bot.send_message(message.chat.id, random.choice(comments_for_incorrect_answers), parse_mode='html')
        get_rus_eng_answer(message, get_words)

#train eng-rus
def get_eng_rus_answer(message, select_words):
    get_words = select_words
    msg = bot.send_message(message.chat.id, get_words[0], parse_mode='html')
    bot.register_next_step_handler(msg, verify_eng_rus_answer, get_words)

def verify_eng_rus_answer(message, verify_words):
    get_words = verify_words
    if message.text.strip().lower() in get_words[1].split(sep=','):
        bot.send_message(message.chat.id, random.choice(comments_for_right_answers), parse_mode='html')
    elif message.text.strip().lower() == 'рандомное слово':
        mess(message)
    elif message.text.strip().lower() == '10 рандомных слов':
        mess(message)
    elif message.text.strip().lower() == 'потренироваться (rus-eng)':
        mess(message)
    elif message.text.strip().lower() == 'потренироваться (eng-rus)':
        mess(message)
    else:
        bot.send_message(message.chat.id, random.choice(comments_for_incorrect_answers), parse_mode='html')
        get_eng_rus_answer(message, get_words)

bot.polling(none_stop=True)