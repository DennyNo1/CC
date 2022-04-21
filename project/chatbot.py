from glob import glob
import time
from tokenize import String
from unicodedata import name
from webbrowser import get
from telegram import Update,InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,CallbackQueryHandler
import random
import configparser
import logging
import redis

global redis1

def main():
    # Load your token and create an Updater for your Bot
    
 
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    global redis1
    redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']))
    global hands
    hands = ['rock', 'paper', 'scissors','quit']
    global emoji
    emoji = {
    'rock': '👊',
    'paper': '✋',
    'scissors': '✌️',
    'quit': '❎'
            }
    #
    db_keys = redis1.keys(pattern='*')
    print((len(db_keys)))
    for single in db_keys:
        chat_id = redis1.get(single).decode("UTF-8")
        print(single.decode("UTF-8"), ": ", chat_id)
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("start", start))
    
    dispatcher.add_handler(CommandHandler('game', game))
    dispatcher.add_handler(CommandHandler('show', show))
    dispatcher.add_handler(CallbackQueryHandler(play))


    # To start the bot:
    updater.start_polling()
    updater.idle()


# writting functionality of the command
def start(update, context):
    user_id = update.message.from_user.id
    global user_last_name
    user_last_name = update.message.from_user.last_name


    message = 'Welcome to the bot'
    path='C:\\Users\\Denny\\Pictures\\头像&图标\\1.jpg'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(path, 'rb'))

def show(update: Update, context: CallbackContext):

    msg = context.args[0]
    n=redis1.get(msg)
    if n is not None:
        n=n.decode('UTF-8')
    w=redis1.get(msg+'win')
    if w is not None:
        w=w.decode('UTF-8')   
    l=redis1.get(msg+'lose')

    if l is not None :
        l=l.decode('UTF-8') 
    d=redis1.get(msg+'draw')
    if d is not None:
        d=d.decode('UTF-8') 

    context.bot.send_message(chat_id=update.effective_chat.id, text='Player {} played the game {} times.Win {} ,lose {}, tie {}.'.
    format(msg,n,w,l,d))
    #format(msg,redis1.get(msg).decode('UTF-8'), redis1.get(win).decode('UTF-8'),redis1.get(lose).decode('UTF-8'),redis1.get(draw).decode('UTF-8') ))

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try: 
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def game(update, bot):
    
    update.message.reply_text('剪刀石頭布！',
        reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(emoji, callback_data = hand) for hand, emoji in emoji.items()
            ]]))

def judge(mine, yours):
    
    if mine == yours:

        return '平手'
    elif (hands.index(mine) - hands.index(yours)) % 3 == 1:

        return '你输了'
    else:

       
        return '你赢了'

def play(update, context):
    try:
        mine = random.choice(hands)
        while mine=='quit':
            mine = random.choice(hands)
    
        yours = update.callback_query.data

        if yours=='quit':
            return

        if mine == yours:
            temp=str(user_last_name)+'draw'
            redis1.incr(temp)
        
        elif (hands.index(mine) - hands.index(yours)) % 3 == 1:
            temp=str(user_last_name)+'lose'
            redis1.incr(temp)
        else:
            temp=str(user_last_name)+'win'
            redis1.incr(temp)
            
        
        update.callback_query.edit_message_text('结果如下')
        context.bot.send_message(chat_id=update.effective_chat.id, text='{}！！！！！因为你出{}，我出{}'.format(judge(mine, yours),emoji[yours], emoji[mine] ))
        redis1.incr(user_last_name)
        time.sleep(0.5)
        update.callback_query.edit_message_text('剪刀石頭布！',
            reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(emoji, callback_data = hand) for hand, emoji in emoji.items()
            ]]))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()