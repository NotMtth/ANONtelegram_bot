import qrcode
import settings
from bot.rpc import wallet
from decimal import Decimal
import io


class Utils:

    @staticmethod
    def gen_qrcode(data) -> io.BytesIO:
        qr_img = qrcode.make(data)
        buff = io.BytesIO()
        qr_img.save(buff)
        return buff

    @staticmethod
    def check_name(name: str):
        for char in range(len(name)):
            if name[char] in settings.SPECIAL_CHARS:
                return True
        return False

    @staticmethod
    def from_atomic(amount):
        return Decimal(amount) * settings.PICO_XMR

    @staticmethod
    def get_funded_balance(address_index):
        funds = wallet.balance(0, [address_index])['per_subaddress']
        balance = list(funds[0].values())[
                                    (
                                        list(funds[0].keys())
                                    ).index('balance')
                                ]

        balance = Utils.from_atomic(balance)

        if balance == 0E-92:
            balance = 0

        return balance

    @staticmethod
    def check_funded(amount, address_index):
        balance = Utils.get_funded_balance(address_index)

        if balance >= amount:
            return False
        return True
