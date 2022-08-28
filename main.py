import types
import telebot

TOKEN = None
with open('token.txt') as f:
    TOKEN=f.read().strip()
bot = telebot.TeleBot(TOKEN)

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
