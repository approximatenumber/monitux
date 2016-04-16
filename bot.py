#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from telegram import Updater, TelegramError, Update, ChatAction
import monitux
import logging

try:
    sys.path.append('.private')
    from private_config import ADMIN_ID, TOKEN
except ImportError:
    print("I need ADMIN_ID, TOKEN from .private/config.py!")
    raise SystemExit

log_file = "bot.log"
logging.basicConfig(level = logging.WARNING, filename=log_file, format='%(asctime)s:%(levelname)s - %(message)s')
logging.FileHandler(log_file, mode='w')

help_text = 'Commands: \n' \
           '/cpuload - display current processor loading \n' \
           '/proclist - list all processes \n' \
           '/grep_proc <procname1> <procname2>... - search for processname in proclist \n' \
           '/screenshot_top - get screenshot of "top" utility \n' \
           '/screenshot_ifconfig - get screenshot of "ifconfig" utility \n' \
           '/mem_stat - get RAM statistic \n' \
           '/disk_stat - get storage statistic \n' \
           '/uptime - get uptime \n' \
           '/temp - get temperature \n'


def start(bot, update):
    message = update.message
    chat_id = message.chat.id
    if chat_id == ADMIN_ID:
        bot.sendMessage(chat_id=chat_id, text='Welcome to Monitux! \n %s' % help_text)
    else:
        text='ADMIN_ID and your chat_id (%s) are not the same' % chat_id
        bot.sendMessage(chat_id=chat_id, text=text)
        error(bot, update, text)


def _help(bot, update):
    text = help_text
    bot.sendMessage(chat_id=ADMIN_ID, text=text)


def mem_stat(bot, update):
    mem_stat = monitux.get_mem_stat()
    text = 'total: %s Gb, used: %s Gb, free %s Gb' % (mem_stat[0], mem_stat[1], mem_stat[2])
    bot.sendMessage(chat_id=ADMIN_ID, text=text)


def temp(bot, update):
    text = 'temperature: %s' % monitux.get_temp()
    bot.sendMessage(chat_id=ADMIN_ID, text=text)


def cpuload(bot, update):
    text = 'processor loading: %s %%' % monitux.get_cpuload(interval=0) # "interval" need to be developed
    bot.sendMessage(chat_id=ADMIN_ID, text=text)


def uptime(bot, update):
    uptime = monitux.get_uptime()
    days = uptime.tm_mday - 1 # "time" module return +1
    hours = uptime.tm_hour
    mins = uptime.tm_min
    text = 'uptime: %s days, %s hours, %s minutes' % (days, hours, mins)
    bot.sendMessage(chat_id=ADMIN_ID, text=text)


def proclist(bot, update):
    text = 'process list:\n%s' % monitux.get_proclist()
    bot.sendMessage(chat_id=ADMIN_ID, text=text)


def screenshot_top(bot, update):
    screenshot = monitux.make_screenshot('top -b -n1')
    bot.sendChatAction(chat_id=ADMIN_ID, action=ChatAction.UPLOAD_PHOTO)
    bot.sendDocument(chat_id=ADMIN_ID, document=open(screenshot, 'rb'))


def screenshot_ifconfig(bot, update):
    screenshot = monitux.make_screenshot('ifconfig')
    bot.sendChatAction(chat_id=ADMIN_ID, action=ChatAction.UPLOAD_PHOTO)
    bot.sendDocument(chat_id=ADMIN_ID, document=open(screenshot, 'rb'))


def disk_stat(bot, update):
    text = []
    for dev in monitux.get_disk_stat():
        text.append(("%s on %s: total %s Gb, used %s Gb, free %s Gb" % \
                    (dev[0], dev[1], dev[2], dev[3], dev[4])))
    bot.sendMessage(chat_id=ADMIN_ID, text='\n'.join(text))


def grep_proc(bot, update, args):
    proclist = monitux.get_proclist()
    text = []
    for proc in args:
        if proc in proclist:
            text.append('%s is running' % proc)
        else:
            text.append('%s is not running' % proc)
    bot.sendMessage(chat_id=ADMIN_ID, text='\n'.join(text))

def all_stats(bot, update):
     bot.sendMessage(chat_id=ADMIN_ID, text=monitux.get_all_stats())


def error(bot, update, error):
    logging.warning('Update "%s" caused error:\n "%s"' % (update, error))


def main(**args):
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, workers=2)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("cpuload", cpuload)
    dp.addTelegramCommandHandler("mem_stat", mem_stat)
    dp.addTelegramCommandHandler("disk_stat", disk_stat)
    dp.addTelegramCommandHandler("proclist", proclist)
    dp.addTelegramCommandHandler("grep_proc", grep_proc)
    dp.addTelegramCommandHandler("screenshot_top", screenshot_top)
    dp.addTelegramCommandHandler("screenshot_ifconfig", screenshot_ifconfig)
    dp.addTelegramCommandHandler("temp", temp)
    dp.addTelegramCommandHandler("uptime", uptime)
    dp.addTelegramCommandHandler("help", _help)
    dp.addTelegramCommandHandler("all_stats", all_stats)
    dp.addErrorHandler(error)

    # Start the Bot and store the update Queue, so we can insert updates
    update_queue = updater.start_polling(poll_interval=1, timeout=5)

if __name__ == '__main__':
    main()