#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, Handler)

import logging
import requests
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

API_KEY, SELECT, CPF, EMAIL, TELEFONE = range(5)


API_KEY_VALUE = ''
CPF_VALUE = ''
EMAIL_VALUE = ''
PHONE_VALUE = ''


def card_generator(json):

    a = open('src/lead.js', 'r')

    print(json)


    text = a.read()
    image = json.get('images')[0] if json.get('images') else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
    text = text.replace('imagem_lead', image)
    text = text.replace('nome', json.get('nome', ''))
    text = text.replace('email', json.get('email', ''))
    text = text.replace('lead_score', str(json.get('lead_score', '0')))
    text = text.replace('profissao', json.get('profissao', ''))
    text = text.replace('empresa', json.get('local', ''))
    text = text.replace('idade', json.get('idade', ''))
    text = text.replace('city', json.get('cidade', ''))
    text = text.replace('telefone', '|'.join(json.get('telefones', '')))

    a.close()

    b = open('src/lead1.js', 'w')
    b.write(text)
    b.close()
    print(text)

    os.system("""repng "./src/lead1.js" -f ubicard.png --width 512 --height 600 --css ./src/semantic.css --out-dir src/images/""")


def start(bot, update):
    user = update.message.from_user
    logger.info("User %s initiated conversation.", user.first_name)
    update.message.reply_text(
        'Olá, preciso que você me forneça sua chave de API do quidata.com.br para começarmos'
    )

    return API_KEY


def restart_global_variables():
    global CPF_VALUE
    global EMAIL_VALUE
    global PHONE_VALUE

    CPF_VALUE, EMAIL_VALUE, PHONE_VALUE = '', '', ''


def api_key(bot, update):
    global API_KEY_VALUE
    user = update.message.from_user
    logger.info("API KEY of %s: %s", user.first_name, update.message.text)
    API_KEY_VALUE = update.message.text
    update.message.reply_text('/search')

    return ConversationHandler.END


def search(bot, update):
    reply_keyboard = [['cpf', 'email', 'telefone']]

    user = update.message.from_user
    logger.info("User %s initiated a search", user.first_name)
    update.message.reply_text(
        'Selecione o parametro de consulta',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return SELECT

def select_search_parameter(bot, update):
    user = update.message.from_user

    if update.message.text == 'cpf':
        logger.info("User %s selected cpf", user.first_name)
        update.message.reply_text(
            'Fornceça o cpf', reply_markup=ReplyKeyboardRemove())
        return CPF

    elif update.message.text == 'email':
        logger.info("User %s selected email", user.first_name)
        update.message.reply_text(
            'Fornceça o email', reply_markup=ReplyKeyboardRemove())
        return EMAIL

    elif update.message.text == 'telefone':
        logger.info("User %s selected telefone", user.first_name)
        update.message.reply_text(
            'Fornceça o telefone', reply_markup=ReplyKeyboardRemove())
        return TELEFONE


def make_request(update):
    headers = { 'Authorization' : 'Bearer {}'.format(API_KEY_VALUE) }
    url = ""
    if CPF_VALUE:
        url = "https://api.ubicity.com.br/ub/moving?large=true&cpf={}&range=eco".format(CPF_VALUE)

    elif EMAIL_VALUE:
        url = "https://api.ubicity.com.br/ub/moving?large=true&email={}&range=eco".format(EMAIL_VALUE)

    elif PHONE_VALUE:
        url = "https://api.ubicity.com.br/ub/moving?large=true&telefone={}&range=eco".format(PHONE_VALUE)
    update.message.reply_text('Acessando API na url {}'.format(url))

    r = requests.get(url, headers = headers)

    logger.info("CPF of the user {}".format(url))

    card_generator(r.json())

    a = open('./src/images/ubicard.png', 'rb')

    update.message.reply_photo(a)

    return update


def cpf(bot, update):
    global CPF_VALUE
    user = update.message.from_user
    logger.info("CPF of the user {}: {}".format(user.first_name, update.message.text))
    CPF_VALUE = update.message.text

    update = make_request(update)

    restart_global_variables()

    return ConversationHandler.END


def email(bot, update):
    global EMAIL_VALUE
    user = update.message.from_user
    logger.info("EMAIL of the user {}: {}".format(user.first_name, update.message.text))
    EMAIL_VALUE = update.message.text

    update = make_request(update)

    restart_global_variables()

    return ConversationHandler.END


def telefone(bot, update):
    global PHONE_VALUE
    user = update.message.from_user
    logger.info("PHONE of the user {}: {}".format(user.first_name, update.message.text))
    PHONE_VALUE = update.message.text

    update = make_request(update)

    restart_global_variables()

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    TOKEN = "663551182:AAGECxo5uVIDF_Phurd2R--KEaxGCxCtItE"
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            API_KEY: [MessageHandler(Filters.text, api_key)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    conv_handler_2 = ConversationHandler(
        entry_points=[CommandHandler('search', search)],

        states={
            SELECT: [RegexHandler('^(cpf|email|telefone)$', select_search_parameter)],
            CPF: [RegexHandler('^(\w{3}.?\w{3}.?\w{3}-?\w{2})$', cpf)],
            EMAIL: [RegexHandler('^(.*@\w+.\w+)$', email)],
            TELEFONE: [RegexHandler('^([+]\d{13})$', telefone)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler_2)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
