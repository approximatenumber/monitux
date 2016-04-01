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

def start(bot, update):
    message = update.message
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        text = 'Commands: \n' \
               '/get_cpuload - display current processor loading \n' \
               '/get_proclist - list all processes \n' \
               '/grep_proc <procname1> <procname2>... - search for processname in proclist \n' \
               '/make_top_screenshot - get screenshot of "top" utility \n' \
               '/get_mem_stat - get RAM statistic'
        bot.sendMessage(chat_id=ADMIN_ID, text=text)


def get_mem_stat(bot, update):
    message = update.message
    chat_id = message.chat.id
    text = '%s' % monitux.get_mem_stat()
    bot.sendMessage(chat_id=chat_id, text=text)


def get_temp(bot, update):
    message = update.message
    chat_id = message.chat.id
    text = 'Temperature: %s' % monitux.get_temp()
    bot.sendMessage(chat_id=chat_id, text=text)

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


def get_top_screenshot(bot, update):
    message = update.message
    chat_id = message.chat.id
    screenshot = monitux.get_top_screenshot()
    bot.sendDocument(chat_id=chat_id, document=open(screenshot, 'rb'))


def get_disk_stat(bot, update):
    message = update.message
    chat_id = message.chat.id
    text = '%s' % monitux.get_disk_stat()
    bot.sendMessage(chat_id=chat_id, text=text)


def get_ifconfig_screenshot(bot, update):
    message = update.message
    chat_id = message.chat.id
    screenshot = monitux.get_ifconfig_screenshot()
    bot.sendDocument(chat_id=chat_id, document=open(screenshot, 'rb'))


def grep_proc(bot, update, args):
    message = update.message
    chat_id = message.chat.id
    for procname in args:
        if procname in monitux.grep_proc(procname):
            text = '%s запущен' % procname
        else:
            text = '%s не запущен' % procname
    bot.sendMessage(chat_id=chat_id, text=text)


def main(**args):
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, workers=2)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("get_cpuload", get_cpuload)
    dp.addTelegramCommandHandler("get_mem_stat", get_mem_stat)
    dp.addTelegramCommandHandler("get_disk_stat", get_disk_stat)
    dp.addTelegramCommandHandler("get_proclist", get_proclist)
    dp.addTelegramCommandHandler("grep_proc", grep_proc)
    dp.addTelegramCommandHandler("get_top_screenshot", get_top_screenshot)
    dp.addTelegramCommandHandler("get_ifconfig_screenshot", get_ifconfig_screenshot)
    dp.addTelegramCommandHandler("get_temp", get_temp)

#    dp.addErrorHandler(error)

    # Start the Bot and store the update Queue, so we can insert updates
    update_queue = updater.start_polling(poll_interval=1, timeout=5)

if __name__ == '__main__':
    main()