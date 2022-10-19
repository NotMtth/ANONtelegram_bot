from bot.main import application, start_handler, help_handler, fund_handler, submit_funding_handler, \
    feature_handler, amount_handler, info_handler, done_handler, fund_menu_handler, fund_back_menu_handler, \
    donate_handler, cleanup_handler, delete_handler


def _setup_database():
    import peewee
    import bot.models
    for m in peewee.Model.__subclasses__():
        m.create_table()


if __name__ == '__main__':
    _setup_database()

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(fund_handler)
    application.add_handler(submit_funding_handler)
    application.add_handler(cleanup_handler)
    application.add_handler(delete_handler)
    application.add_handler(donate_handler)

    application.add_handler(feature_handler)
    application.add_handler(amount_handler)
    application.add_handler(info_handler)
    application.add_handler(done_handler)
    application.add_handler(fund_menu_handler)
    application.add_handler(fund_back_menu_handler)

    application.run_polling()
