import logging
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, \
    Update, Bot
import random
import uuid
import os


def check_input(items):
    return len(items) > 1


def shuffle_list(items):
    shuffled = list(items)
    random.shuffle(shuffled)
    # return '\n'.join(['{}: {}'.format(i + 1, item) for i, item in enumerate(shuffled)])
    return '\n'.join(shuffled)


def pick_and_highlight_item(items):
    pick = random.randrange(0, len(items))
    print('Picked {}', pick)
    return '\n'.join([
        item if i != pick
        else '<b>Baited: {}</b>'.format(item)
        for i, item in enumerate(items)
    ])


def answer_inline_query(bot, update):
    print('Received inline query...')
    query = update.inline_query.query
    if not query:
        print('query failed')
        return
    # split the query string into a list of items
    items = tuple(query.split())
    results = []
    # check if there are at least two items in the list
    if check_input(items):
        # an inline query only supports a few answer formats (stickers, gifs, articles, ...)
        # the article format is the best fit for our needs, since it's the only one,
        # where the displayed text can be customized.

        # when a user selects an article the bot can send a text message (InputTextMessageContent),
        # to the chat

        # the bot currently supports two options: picking a random item from a list and shuffling the list

        # picking a random item
        results.append(InlineQueryResultArticle(
            id=uuid.uuid4(),
            title='Randomize',
            description='Happy Baiting :)',
            thumb_url='https://i.imgur.com/O3oeAik.png',
            input_message_content=InputTextMessageContent(pick_and_highlight_item(items), parse_mode='HTML')
        ))


        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Shuffle", callback_data="1234")]])
        # shuffling the list
        results.append(InlineQueryResultArticle(
            id=uuid.uuid4(),
            title='Shuffle',
            description='...',
            reply_markup=reply_markup,
            thumb_url='https://i.imgur.com/CA4eywa.png',
            input_message_content=InputTextMessageContent(shuffle_list(items), parse_mode='HTML')
        ))

    bot.answer_inline_query(update.inline_query.id, results, cache_time=0)


def answer_shuffle_callbackquery(bot, update, update_queue, chat_data, job_queue, user_data):
    print(update)
    print(bot, update_queue, chat_data, job_queue)




def set_up_inline_handler(updater):
    inline_query_handler = InlineQueryHandler(answer_inline_query)
    updater.dispatcher.add_handler(inline_query_handler)


def set_up_shuffle_button_callback_handler(updater):
    shuffle_button_callback_handler = CallbackQueryHandler(answer_shuffle_callbackquery,
                                                           pass_update_queue=True,
                                                           pass_job_queue=True,
                                                           pattern=None,
                                                           pass_groups=True,
                                                           pass_groupdict=True,
                                                           pass_user_data=True,
                                                           pass_chat_data=True)
    updater.dispatcher.add_handler(shuffle_button_callback_handler)


def init():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(os.environ.get('LIST_RANDOMIZER_TOKEN'))

    # set up handlers
    set_up_inline_handler(updater)
    set_up_shuffle_button_callback_handler(updater)

    updater.start_polling()
    updater.idle()


init()
