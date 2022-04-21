
from telegram.ext import Updater # 更新者
from telegram.ext import CommandHandler, CallbackQueryHandler # 註冊處理器 一般用 回答用
from telegram.ext import MessageHandler, Filters # Filters過濾訊息
from telegram import InlineKeyboardMarkup, InlineKeyboardButton # 互動式按鈕
#import telegram


# 設定 token
token = '5135823339:AAGUcCNQHpFHgVEOYJ51gFDri-I-T3LY9mk'

# 初始化bot
updater = Updater(token=token, use_context=False)


# 設定一個dispatcher(調度器)
dispatcher = updater.dispatcher


# 定義收到訊息後的動作(新增handler)
def start(bot, update): # 新增指令/start
    message = update.message
    chat = message['chat']
    update.message.reply_text(text='HI  ' + str(chat['id']))    
    

def blog(bot, update): # /btc 互動式按鈕
    update.message.reply_text('量化交易中心',
                              reply_markup = InlineKeyboardMarkup([[
                                  InlineKeyboardButton('恩哥Python量化教室', 
                                                       url = 'https://pixnashpython.pixnet.net/blog'),
                                  InlineKeyboardButton('你的網路生活教授Nash', 
                                                       url = 'https://pixnashlife.pixnet.net/blog')
                                  ]])
                              )
qt = {
    'Q1': '你是誰?',
    'Q2': '有新文章嗎?',
    'Q3': '今天會下雨嗎?'
        } 

def question(bot, update):
    update.message.reply_text('你問我答',
        reply_markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(qt, callback_data = name) for name, qt in qt.items()
            ]]))
    
def answer(bot, update):
    yours = update.callback_query.data # 一樣從update中抽取資料
    update.callback_query.edit_message_text(text=yours)


def echo(bot, update): # 其他訊息
    message = update.message
    text = message.text + '  <<< 這個部份我就不太懂了~'
    update.message.reply_text(text=text)
    

# 把handler加入dispatcher()
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('blog', blog))
dispatcher.add_handler(CommandHandler('question', question)) # 問題
dispatcher.add_handler(CallbackQueryHandler(answer)) # 回答問題
dispatcher.add_handler(MessageHandler(Filters.text, echo)) # Filters如果是文字就呼叫start


# 發指定對象訊息
who = '對象ID, '
text = '我是機器人可以問我問題喔!'
dispatcher.bot.send_message(chat_id=who, text=text) # 發送訊息


# 開始運作bot
updater.start_polling()


# 待命 若要停止按Ctrl-C 就好
#updater.idle()


# 離開
#updater.stop()