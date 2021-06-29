import os
import logging
import handler
from telegram.ext import Updater, CommandHandler

DEBUG = True

token = os.environ.get('GOLDEN_QUOTE_TOKEN')

FORMAT = '%(asctime)-15s  %(levelname)-8s %(message)s'

matches = ["/start", "/add_scroll", "/help", "/show_wisdom", "/forget_wisdom"]

bot_username = 'goldest_scrolls_bot'

if DEBUG:
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
else:
    logging.basicConfig(filename='golden_quotes.log', format=FORMAT, level=logging.INFO)

print('BOT STARTED...')


class Bot:
    def __init__(self, token):
        self.token = token
        self.updater = Updater(token, use_context=True)

    def join(self):
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('add_scroll', self.add_command))
        dp.add_handler(CommandHandler('help', self.help_me))
        dp.add_handler(CommandHandler('show_wisdom', self.show_command))
        dp.add_handler(CommandHandler('forget_wisdom', self.del_command))
        self.updater.start_polling()
        self.updater.idle()

    def start(self, update, context):
        # TODO: registration and chat info at first join
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=handler.start_command(),
                                 parse_mode='Markdown')

    def help_me(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=handler.help_command(update),
                                 parse_mode='Markdown')

    def add_command(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=handler.add_quote(update))

    def del_command(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=handler.delete_quote(update))

    def show_command(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=handler.show_quotes(update),
                                 parse_mode='Markdown')


bot = Bot(token)
bot.join()
