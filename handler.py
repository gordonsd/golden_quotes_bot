import re
import configparser
from models import Quote

config = configparser.ConfigParser()
config.read('config.ini')

regexes = [
    re.compile('/start'),
    re.compile('/add_scroll'),
    re.compile('/help'),
    re.compile('/show_wisdom'),
    re.compile('/forget_wisdom'),
    re.compile('@goldest_scrolls_bot')
]


def start_command():
    return config['TEXT']['start_cmd']


def help_command(update):
    if update.effective_chat.type == 'private':
        return config['TEXT']['help_private']
    else:
        return config['TEXT']['help_cmd']


def prepare_quote(update):
    status = None
    if update.message.reply_to_message is not None:
        if any(regex.match(update.message.reply_to_message.text) for regex in regexes):
            status = 'dumb'
        if Quote.get_or_none(Quote.chat_quote == update.message.reply_to_message.text,
                             Quote.chat_id == update.effective_chat.id) is not None:
            status = 'exist'
        if update.message.reply_to_message.from_user.username == config['BOT']['bot_name']:
            status = 'bot'
    if update.message.reply_to_message is None and any(regex.match(update.message.text) for regex in regexes):
        status = 'miss'
    print("YOUR STATUS: {}".format(status))
    return{
        'bot': config['TEXT']['bot_quote'],
        'exist': config['TEXT']['exist_quote'],
        'dumb': config['TEXT']['dumb_quote'],
        'miss': config['TEXT']['miss_quote']
    }.get(status, None)


def add_quote(update):
    if prepare_quote(update) is None:
        new_message = Quote(chat_quote=update.message.reply_to_message.text,
                            chat_id=update.effective_chat.id,
                            chat_name=update.effective_chat.title,
                            user_id=update.message.reply_to_message.from_user.id,
                            user_firstname=update.message.reply_to_message.from_user.first_name,
                            user_lastname=update.message.reply_to_message.from_user.last_name,
                            user_username=update.message.reply_to_message.from_user.username,
                            quote_fromuser_id=update.message.from_user.id,
                            quote_fromuser_firstname=update.message.from_user.first_name,
                            quote_fromuser_lastname=update.message.from_user.last_name,
                            quote_fromuser_username=update.message.from_user.username)
        new_message.save()
        text = config['TEXT']['add_quote']
    else:
        text = prepare_quote(update)
    return text


def delete_quote(update):
    status = None
    text = update.message.text
    if text == ('/forget_wisdom' or '/forget_wisdom@{}'.format(config['BOT']['bot_name'])):
        status = 'empty'
    if update.effective_chat.type == 'private':
        status = 'private'
    text = text.replace('/forget_wisdom@{} '.format(config['BOT']['bot_name']), '')
    text = text.replace('/forget_wisdom@{}'.format(config['BOT']['bot_name']), '')
    text = text.replace('/forget_wisdom ', '')
    text = text.replace('/forget_wisdom', '')
    if status != 'empty' and status != 'private':
        quote = Quote.get_or_none(Quote.chat_id == update.effective_chat.id, Quote.chat_quote == text)
        if quote is not None:
            quote.delete_instance()
            status = 'success'
        if quote is None:
            status = 'fail'
    return {
        'empty': config['TEXT']['empty_delete'],
        'private': config['TEXT']['private_alert'],
        'success': config['TEXT']['success_delete'],
        'fail': config['TEXT']['fail_delete']
    }.get(status, None)


def show_quotes(update):
    if update.effective_chat.type == 'private':
        return config['TEXT']['private_alert']
    if Quote.get_or_none(Quote.chat_id == update.effective_chat.id) is None:
        return config['TEXT']['no_quotes']
    else:
        # pass
        query = Quote.select().where(Quote.chat_id == update.effective_chat.id)
        scroll = list(zip([quote.chat_quote for quote in query], [quote.user_username for quote in query]))
        return get_scroll(scroll)


def get_scroll(scroll):
    list_l = []
    for rec in scroll:
        string = '</code> ©<i>'.join(rec)
        list_l.append(string)
    string = config['TEXT']['scroll_head'] + "\n"
    for i in list_l:
        string += '<code>' + i + "</i>\n\n"
    return string
