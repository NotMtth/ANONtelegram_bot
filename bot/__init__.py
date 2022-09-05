from functools import wraps
import settings
from bot.api import API


def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if str(user_id) not in settings.LIST_OF_ADMINS:
            return
        return await func(update, context, *args, **kwargs)

    return wrapped
