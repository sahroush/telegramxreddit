from telegram.ext import Updater
import time , requests  , random
tkn = "947964816:AAHVqouGt5Pmm_aCNpDVhA3LpUQSDtN7mag"
updater = Updater(token= tkn , use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi!")
from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="??????????")
from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

from telegram import InlineQueryResultArticle, InputTextMessageContent
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

from telegram.ext import InlineQueryHandler
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)






def makeUrl(afterID, subreddit):
        return subreddit.split('/.json')[0] + "/.json?after={}".format(afterID)
def fetch(sub , x = 0):
    url = makeUrl('', sub)
    subJson = requests.get(url, headers={'User-Agent': 'MyRedditScraper'}).json()
    post = subJson['data']['children']
    if(len(post) < x):
        return(0)
    imageUrl = (post[x]['data']['url'])
    imageTitle = (post[x]['data']['title'])
    if(not('jpg' in imageUrl or 'webm' in imageUrl or 'gif' in imageUrl or 'gifv' in imageUrl or 'png' in imageUrl)):
        return(fetch(sub , x + 1))
    else :
        return(imageUrl , imageTitle)

def latest(update, context):
    sub = ' '.join(context.args).lower()
    try:
        (url  , title ) = fetch("https://www.reddit.com/r/"+ sub)
        context.bot.send_message(chat_id=update.effective_chat.id, text='<a href="'+url+'">'+ "<b>"+title+'</b></a>' , parse_mode = "HTML")
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, couldn't find a pic :( ")


latest_handler = CommandHandler('latest', latest)
dispatcher.add_handler(latest_handler)




def getrecent(sub , context , update):
    url = makeUrl('', sub)
    subJson = requests.get(url, headers={'User-Agent': 'MyRedditScraper'}).json()
    post = subJson['data']['children']
    mark = 0
    for i in range(len(post)):
        imageUrl = (post[i]['data']['url'])
        imageTitle = (post[i]['data']['title'])
        if(('jpg' in imageUrl or 'webm' in imageUrl or 'gif' in imageUrl or 'gifv' in imageUrl or 'png' in imageUrl)):
            mark = 1;
            context.bot.send_message(chat_id=update.effective_chat.id, text='<a href="'+imageUrl+'">'+ "<b>"+imageTitle+'</b></a>' , parse_mode = "HTML")
    return(mark);

def recent(update, context):
    sub = ' '.join(context.args).lower()
    if (getrecent("https://www.reddit.com/r/"+ sub , context , update)):
        sub = 2
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, couldn't find a pic :( ")

recent_handler = CommandHandler('recent', recent)
dispatcher.add_handler(recent_handler)


def rnd(sub , context , update):
    url = makeUrl('', sub)
    subJson = requests.get(url, headers={'User-Agent': 'MyRedditScraper'}).json()
    post = subJson['data']['children']
    mark = 0
    stuff = []
    for i in range(len(post)):
        imageUrl = (post[i]['data']['url'])
        imageTitle = (post[i]['data']['title'])
        if(('jpg' in imageUrl or 'webm' in imageUrl or 'gif' in imageUrl or 'gifv' in imageUrl or 'png' in imageUrl)):
            mark = 1;
            stuff += [[imageUrl , imageTitle]]
    if(mark == 0):
        return(0);
    x = random.randint(0 , len(stuff)-1);
    context.bot.send_message(chat_id=update.effective_chat.id, text='<a href="'+stuff[x][0]+'">'+ "<b>"+stuff[x][1]+'</b></a>' , parse_mode = "HTML")
    return(1);

def rndom(update, context):
    sub = ' '.join(context.args).lower()
    if (rnd("https://www.reddit.com/r/"+ sub , context , update)):
        sub = 2
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, couldn't find a pic :( ")

random_handler = CommandHandler('random', rndom)
dispatcher.add_handler(random_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
