import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, filters, ContextTypes, \
    CallbackQueryHandler, MessageHandler

import settings
from bot import commands
from bot.models import Funding, db
from bot.api import API
from bot.rpc import wallet
from bot.utils import Utils
from bot import restricted

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

application = ApplicationBuilder().token(settings.TOKEN).proxy_url(settings.PROXY).build()
start_handler = CommandHandler('start', commands.start_command)
help_handler = CommandHandler('help', commands.help_command)
fund_handler = CommandHandler('fund', commands.fund_command)
submit_funding_handler = CommandHandler('add', commands.submit_funding_command)
donate_handler = CommandHandler('donate', commands.donate_command)

GET_FEATURE, GET_AMOUNT, GET_INFO = range(1, 4)
SHOWING_MENU, CLOSING, BACK = range(4, 7)
END = ConversationHandler.END


@restricted
async def compile_proposal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)

    await update.callback_query.message.delete()

    await update.callback_query.answer()
    await api.send_message(f'Type new {update.callback_query.data}:')

    if update.callback_query.data == 'feature':
        return GET_FEATURE
    elif update.callback_query.data == 'amount':
        return GET_AMOUNT
    else:
        return GET_INFO


async def name_feature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)
    user_data = context.user_data

    feature_name = update.message.text

    if Utils.check_name(feature_name):
        await api.send_message('Name should not contain any special chars!')
        raise ValueError('Special chars in name!')

    user_data['name'] = feature_name

    await api.send_message('Feature named changed!')

    await commands.proposal_menu(update, context)

    return END


async def change_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)
    user_data = context.user_data

    new_amount = update.message.text

    try:
        new_amount = float(new_amount)
    except ValueError as e:
        await api.send_message('Invalid amount!')
        raise e

    user_data['amount'] = new_amount

    await api.send_message('Amount changed!')

    await commands.proposal_menu(update, context)

    return END


async def change_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)
    user_data = context.user_data

    new_info = update.message.text

    user_data['info'] = new_info

    await api.send_message('Info changed!')

    await commands.proposal_menu(update, context)

    return END


@restricted
async def close_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):  # done button in prosal menu
    api = API(update, context)

    await update.callback_query.answer()
    await update.callback_query.message.delete()

    user_data = context.user_data
    feature_name, amount, more_info = user_data['name'], user_data['amount'], user_data['info']

    if user_data['name'] is None:
        await api.send_message('Feature name must be filled!')

        await commands.proposal_menu(update, context)

        raise Exception('Empty feature name!')

    elif user_data['amount'] is None:

        await api.send_message('Amount must be filled!')

        await commands.proposal_menu(update, context)

        raise Exception('Empty amount!')

    sub = wallet.new_address(0)

    sub_address, address_index = sub['address'], sub['address_index']

    current_row = Funding.select().where(Funding.id == update.effective_user.id).order_by(Funding.time.desc()).get()
    with db.atomic():
        current_row.feature = feature_name
        current_row.amount = amount
        current_row.more_info = more_info
        current_row.sub_address = sub_address
        current_row.address_index = address_index
        current_row.save()

    await api.send_message('Proposal closed and submitted!')

    return END


async def fund_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)

    await update.callback_query.answer()
    await update.callback_query.message.delete()

    feature = update.callback_query.data[1:]
    fund = Funding.select().where(Funding.feature == feature).get()

    buttons = [[InlineKeyboardButton(text=f'Back ⮨', callback_data=f'back')]]

    qr_code = Utils.gen_qrcode(fund.sub_address)

    # print(round(fund.))

    await api.send_photo(qr_code.getvalue(), caption=f'''
Feature: <b>{fund.feature}</b>
Amount: <b>{Utils.get_funded_balance(fund.address_index)} of {fund.amount} XMR</b>
More info: <b>{fund.more_info}</b>
Address: <code>{fund.sub_address}</code>
    ''', reply_markup=InlineKeyboardMarkup(buttons))

    return END


async def fund_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):  # back to fund main menu
    await update.callback_query.answer()
    await update.callback_query.message.delete()

    await commands.fund_command(update, context)

    return END


feature_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(compile_proposal, pattern='^feature$')
    ],
    states={
        GET_FEATURE: [
            MessageHandler(filters.TEXT, name_feature)
        ]
    },
    fallbacks=[]
)

amount_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(compile_proposal, pattern='^amount$')
    ],
    states={
        GET_AMOUNT: [
            MessageHandler(filters.TEXT, change_amount)
        ]
    },
    fallbacks=[]
)

info_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(compile_proposal, pattern='^info$')
    ],
    states={
        GET_INFO: [
            MessageHandler(filters.TEXT, change_info)
        ]
    },
    fallbacks=[]
)

done_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(close_conv, pattern='^done$')
    ],
    states={},
    fallbacks=[]
)

fund_menu_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(fund_info, pattern='^➤')
    ],
    states={},
    fallbacks=[]
)

fund_back_menu_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(fund_menu, pattern='^back')
    ],
    states={},
    fallbacks=[]
)
