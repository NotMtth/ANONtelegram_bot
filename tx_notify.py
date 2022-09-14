from telegram.ext import ApplicationBuilder

import asyncio
import settings

application = ApplicationBuilder().token(settings.TOKEN).proxy_url(settings.PROXY).build()


async def tx_notify():
    return await application.bot.send_animation(chat_id=settings.ANON_GROUP, animation=settings.MONERO_CHAN,
                                                caption='Some Monero got donated, here is a happy Monero-Chan!')


if __name__ == '__main__':
    asyncio.run(tx_notify())

    # thanks to iTzVirtual for the quick fix :D
