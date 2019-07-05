import logging
from telegram.ext import Updater, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
import random
import uuid
import os


def check_input(items):
    return len(items) > 1


def shuffle_list(items):
    shuffled = list(items)
    random.shuffle(shuffled)
    return '\n'.join(['{}: {}'.format(i + 1, item) for i, item in enumerate(shuffled)])


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
    items = tuple(query.split())
    results = []
    if check_input(items):
        # pick item from list
        results.append(InlineQueryResultArticle(
            id=uuid.uuid4(),
            title='Randomize',
            description='Happy Baiting :)',
            thumb_url='https://i.imgur.com/O3oeAik.png',
            input_message_content=InputTextMessageContent(pick_and_highlight_item(items), parse_mode='HTML')
        ))

        # shuffle the list
        results.append(InlineQueryResultArticle(
            id=uuid.uuid4(),
            title='Shuffle',
            description='...',
            thumb_url='https://i.imgur.com/CA4eywa.png',
            input_message_content=InputTextMessageContent(shuffle_list(items), parse_mode='HTML')
        ))

    bot.answer_inline_query(update.inline_query.id, results, cache_time=0)


print('Starting bot')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(os.environ.get('LIST_RANDOMIZER_TOKEN'))

inline_query_handler = InlineQueryHandler(answer_inline_query)

updater.dispatcher.add_handler(inline_query_handler)

updater.start_polling()

updater.idle()
