#!/bin/bash

G='\033[0;32m'
Y='\033[0;33m'
R='\033[0;31m'
NOCOLOR='\033[0m'

NODE='' # onion address is preferred
PORT='' # most common stagenet ports: 38089, 38081 | most common mainnet ports: 18089, 18081
WALLET='' # aka your private viewkey
PASSWORD=' ' # wallet key file password

echo "${R}[!] Start in the main folder only [!]${NOCOLOR}"

python3 -m venv venv

echo "${Y}[~] installing requirements...${NOCOLOR}"

venv/bin/python -m pip install -r requirements.txt

echo "${G}[+] requirements installed!${NOCOLOR}"

echo "${Y}[~] creating database...${NOCOLOR}"

sqlite3 db.sqlite3 .databases

echo "${G}[+] database created!${NOCOLOR}"

echo "${Y}[~] starting wallet and RPC...${NOCOLOR}"

screen -dmS anon_bot

screen -S anon_bot -X stuff 'venv/bin/python run.py\n'

echo "${G}[+] bot started!${NOCOLOR}"

screen -dmS anon_rpc

screen -S anon_rpc -X stuff 'cd monero_wallet/\n'

#stagenet recommended (remove --stagenet for mainnet use)
# remove `torsocks` at the beginning if you want to use a standard node 
screen -S anon_rpc -X stuff "torsocks ./monero-wallet-rpc --stagenet --daemon-address=${NODE}:${PORT} --untrusted-daemon --rpc-bind-port 28088 --disable-rpc-login --wallet-file ${WALLET}.keys --password '${PASSWORD}'\n"

echo "${G}[+] rpc started${NOCOLOR}"

echo "${G}[+] all done!${NOCOLOR}"

echo "exiting..."

exit
