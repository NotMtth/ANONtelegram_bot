class API:
    def __init__(self, update, context):
        self.update = update
        self.context = context

    def send_message(self, text, reply_markup=None):
        return self.context.bot.send_message(chat_id=self.update.effective_chat.id, text=text,
                                             reply_markup=reply_markup, parse_mode='HTML')

    def send_photo(self, photo, caption, reply_markup=None):
        return self.context.bot.send_photo(chat_id=self.update.effective_chat.id, photo=photo,
                                           caption=caption, reply_markup=reply_markup, parse_mode='HTML')

    # def tx_notify(self, text, reply_markup=None):
    #     return self.context.bot.send_message(chat_id='-1001637689617', text=text,
    #                                          reply_markup=reply_markup, parse_mode='HTML')
    # TODO