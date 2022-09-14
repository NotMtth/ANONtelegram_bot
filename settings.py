import os
from decimal import Decimal

from dotenv import load_dotenv

load_dotenv()

cwd = os.path.dirname(os.path.realpath(__file__))

TOKEN = os.environ.get('TOKEN')  # bot token

DATABASE = os.path.join(cwd, "db.sqlite3")

RPC = os.environ.get('RPC', '127.0.0.1')
RPC_PORT = os.environ.get('RPC_PORT', 28088)
PROXY = 'socks5://127.0.0.1:9050'

LIST_OF_ADMINS = os.environ.get('ADMINS').split(',')

SPECIAL_CHARS = os.environ.get('SPECIAL_CHARS', '[@_!#$%^&*()<>?/\|}{~:]')

PICO_XMR = os.environ.get('PICO_XMR', Decimal(0.000000000001))

ANON_GROUP = os.environ.get('ANON_GROUP')

MONERO_CHAN = 'https://www.monerochan.art/commissions/mememe_bikini.gif'
