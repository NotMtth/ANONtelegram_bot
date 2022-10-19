from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ContextTypes

import bot.main
from bot import restricted
from bot.api import API

from bot.models import Funding, cleanup
from bot.utils import Utils


async def proposal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)
    user_data = context.user_data

    buttons = [
        [InlineKeyboardButton(text=f'+ Edit feature name', callback_data='feature')],
        [InlineKeyboardButton(text=f'+ Edit amount', callback_data='amount')],
        [InlineKeyboardButton(text=f'+ Edit more info', callback_data='info')],
        [InlineKeyboardButton(text=f'✓ Done', callback_data='done')]
    ]

    await api.send_message(f'''
<b>Edit proposal</b>
› Feature: <code>{user_data['name']}</code>
› Amount: <code>{user_data['amount']} XMR</code>
› More info: <code>{user_data['info']}</code>
    ''', reply_markup=InlineKeyboardMarkup(buttons))


@restricted
async def submit_funding_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cleanup(update.effective_user.id)

    proposal = Funding.create(id=update.effective_user.id, feature=None, amount=None, more_info=None)
    proposal.save()
    user_data = context.user_data
    user_data['name'], user_data['amount'], user_data['info'] = None, None, None

    return await proposal_menu(update, context)


@restricted
async def db_cleanup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)

    if Funding.select():
        for proposal in Funding.select():
            Funding.delete().where(Funding.feature == proposal.feature).execute()
        return await api.send_message('Proposals cleaned!')

    await api.send_message('There are no proposals!')


@restricted
async def delete_proposal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)
    feature = update.message.text
    feature = feature.replace('/delete ', '')

    if Funding.select().where(Funding.feature == feature):
        Funding.delete().where(Funding.feature == feature).execute()
        return await api.send_message('Proposal deleted!')

    await api.send_message('Proposal not found!')


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)
    await api.send_message('''<b>Welcome to the ANON feature funding bot!</b>
/help to get more info about the bot and on the commands.

<code>Stay Anon, stay private</code>.     
    ''')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)
    await api.send_message('''<b>Get some help here!</b>
This bot is dedicated to the funding of the ANON Monero wallet.
/fund to check for proposals to fund.
/donate to get donation addresses. 

Made with ♥ by NotMtth / @moneromaxi
    ''')


async def donate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)
    await api.send_message('''<b>Help the project with a donation!</b>
All this funds will go for the wallet development/infrastructure maintaining.

General donation address: <code>42Wocf8sTM1Vqn2qmgC1S1fzoF5oujnJvEeSXde5vcr1WDRuUEPgGbvMN5kV1SaegxVk25cpnvBKsJtigedN1E3aETwpCiV</code>.

Bot dev address: <code>4ASpDUymEkgcBBDoqp7HFs2xqiTuddJzbhvHmSVQWdt51mbbtxjMWP4LwvbYk6xqTDNnj9FyvSRGqMvRYxWuKyALJbf8265</code>
    ''')


async def fund_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = API(update, context)
    from bot.models import Funding

    buttons = []

    for fund in Funding.select():
        if fund.feature and Utils.check_funded(fund.amount, fund.address_index):
            buttons.append([InlineKeyboardButton(text=f'➤ {fund.feature}', callback_data=f'➤{fund.feature}')])

    if not buttons:
        return await api.send_message('<i>Every proposal is funded for now...</i>')

    await api.send_message('<b>Currently active ANON proposals:</b>', reply_markup=InlineKeyboardMarkup(buttons))
