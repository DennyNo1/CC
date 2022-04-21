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

    #定义游戏所需变量
    global hands
    hands = ['rock', 'paper', 'scissors','quit']
    global emoji
    emoji = {
    'rock': '👊',
    'paper': '✋',
    'scissors': '✌️',
    'quit': '❎'
            }
    
    #查看下数据库里数据总数和每一对数据（可删）
    db_keys = redis1.keys(pattern='*')
    print((len(db_keys)))
    for single in db_keys:
        chat_id = redis1.get(single).decode("UTF-8")
        print(single.decode("UTF-8"), ": ", chat_id)
    
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    #三个命令
    dispatcher.add_handler(CommandHandler("start", start))   
    dispatcher.add_handler(CommandHandler('game', game))
    dispatcher.add_handler(CommandHandler('show', show))
    dispatcher.add_handler(CallbackQueryHandler(play))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def start(update, context):
    global user_last_name
    user_last_name = update.message.from_user.last_name#只储存玩家的姓
    message = 'Welcome to the bot. Attention: Every time you want to play the game, you need to input /start before. Then you inpunt /game to start game. And /show lastname for score of player.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
def show(update: Update, context: CallbackContext):

    msg = context.args[0]
    n=redis1.get(msg)
    if n is not None:
        n=n.decode('UTF-8')
    w=redis1.get(msg+'win')
    if w is not None:
        w=w.decode('UTF-8')
        int_w=int(w)   
    l=redis1.get(msg+'lose')
    if l is not None :
        l=l.decode('UTF-8') 
        int_l=int(l)
    d=redis1.get(msg+'draw')
    if d is not None:
        d=d.decode('UTF-8') 
    
    if int_l>=1:
        wr=int_w/(int_w+int_l)
    elif int_w>0:
        wr=1
        
        
    context.bot.send_message(chat_id=update.effective_chat.id, text='Player {} played the game {} times.Win {} ,lose {}, tie {}. Win rate is {}.'.
    format(msg,n,w,l,d,wr))

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
  
