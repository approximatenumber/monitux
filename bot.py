#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from telegram import Updater, TelegramError, Update
import monitux
import logging
try:
    sys.path.append('.private'); from private_config import ADMIN_ID, TOKEN
except ImportError:
    print("I need ADMIN_ID, TOKEN from .private/config.py!")
    sys.exit(1)

log_file = "bot.log"

logging.basicConfig(level = logging.WARNING,filename=log_file,format='%(asctime)s:%(levelname)s - %(message)s')


def get_cpuload(bot, update):
    message = update.message
    chat_id = message.chat.id
    text = 'Загрузка процессора: %s' % monitux.get_cpuload(interval=0) # "interval" need to be developed
    bot.sendMessage(chat_id=chat_id, text=text)


def get_proclist(bot, update):
    message = update.message
    chat_id = message.chat.id
    text = 'Список процессов:\n%s' % monitux.get_proclist()
    bot.sendMessage(chat_id=chat_id, text=text)


def grep_proc(bot, update, procname):
    message = update.message
    chat_id = message.chat.id
    if monitux.grep_proc(procname) is True:
        text = '%s запущен' % procname
        bot.sendMessage(chat_id=chat_id, text=text)
    elif monitux.grep_proc(procname) is False:
        text = '%s не запущен' % procname
        bot.sendMessage(chat_id=chat_id, text=text)

"""
def main(**args):
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            update_id = echo(bot, update_id)
        except telegram.TelegramError as e:
            # These are network problems with Telegram.
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            elif e.message == "Unauthorized":
                # The user has removed or blocked the bot.
                update_id += 1
            else:
                raise e
        except URLError as e:
            # These are network problems on our end.
            sleep(1)

if __name__ == '__main__':
    main()
"""


def main(**args):
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, workers=2)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.addTelegramCommandHandler("get_cpuload", get_cpuload)
    dp.addTelegramCommandHandler("get_proclist", get_proclist)

#    dp.addErrorHandler(error)

    # Start the Bot and store the update Queue, so we can insert updates
    update_queue = updater.start_polling(poll_interval=1, timeout=5)

    # Start CLI-Loop
    while True:
        text = input()

        # Gracefully stop the event handler
        if text == 'stop':
            updater.stop()
            break

        # else, put the text into the update queue
        elif len(text) > 0:
            update_queue.put(text)  # Put command into queue


if __name__ == '__main__':
    main()