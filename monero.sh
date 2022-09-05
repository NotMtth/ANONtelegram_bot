#!/bin/bash

G='\033[0;32m'
Y='\033[0;33m'
R='\033[0;31m'
NOCOLOR='\033[0m'

echo "${R}[!] Start in the main folder only [!]${NOCOLOR}"

echo "${Y}[~] downloading monero binaries...${NOCOLOR}"

mkdir monero_wallet

cd monero_wallet/

# in case of compatibility error use an other download link that you can find @ https://github.com/monero-project/monero/releases/tag/v0.18.1.0
wget https://downloads.getmonero.org/cli/monero-linux-x64-v0.18.1.0.tar.bz2

tar -xf monero-linux-x64-v0.18.1.0.tar.bz2

mv monero-x86_64-linux-gnu-v0.18.1.0/monero-wallet-* ./

rm -rf monero-x86_64-linux-gnu-v0.18.1.0

rm monero-linux-x64-v0.18.1.0.tar.bz2

echo "${G}[~] binaries downloaded...${NOCOLOR}"

echo "exiting..."

exit
