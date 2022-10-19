<p align="center">
  <img src="images/anon_logo.png" width="350">
</p>


# ANON telegram bot

![Forks](https://img.shields.io/github/forks/NotMtth/ANONtelegram_bot)
![Issues](https://img.shields.io/github/issues-raw/NotMtth/ANONtelegram_bot)

Telegram bot powered by **Python**, **Tor** and **Monero**.

## Dependencies

- Torsocks

- At least python 3.8 (and the libraries in 'requirements.txt')

- Sqlite3

## Installing dependencies

- Torsocks (recommended to build from source): [official installation guide](https://github.com/dgoulet/torsocks#installation)

- Install python and pip from your package manager (should be already installed)

- Sqlite3 should be installed as well, check it by typing the command `sqlite3`
in your terminal

## Deployment

### Edit variables [work in progress]

- `start.sh` variables
https://github.com/NotMtth/ANONtelegram_bot/blob//start.sh#L8-L11

- `bot token settings.py`
https://github.com/NotMtth/ANONtelegram_bot/blob//settings.py#L9-L11

##

### Get monero binaries

- Start the sh file called `monero.sh` in its own folder

##

### Restore wallet from viewkey

- Follow `ìnstructions.txt`

##

### Make it operational

At the end of `ìnstructions.txt` is wrote:

```text
--Bot deployment--

[Remember to change all the variables at line 8 to 11 like: node, node port, wallet name (it's your private viewkey) and wallet password]

-> start it typing 'sh start.sh' to create virtual environment, install dependecies, create database, run the bot and the RPC all at the same time

The RPC doesn't instantly starts, give it some time. It needs to fully load the wallet keys and fire up the server.
```

## Commands

- `/start`, start the bot

- `/help`, help screen to get help

- `/fund`, check new funding proposals

- `/add`, add new funding proposal __[restricted to admins]__

- `/clean`, cleans the whole database __[restricted to admins]__

- `/delete <proposal_name>`, delete a proposal __[restricted to admins]__

- `/donate`, donation screen

## TODO

- ~~Use `tx-notify` to notify every incoming transaction~~

- Make deployment better (working on dockers)

- Improve rounding for shown donated amount in a proposal

- Error handling when writing database (ex: unique data errors etc...)

## Author

- [@NotMtth](https://github.com/NotMtth) - notmtth.xyz

### Donate

- XMR:`4ASpDUymEkgcBBDoqp7HFs2xqiTuddJzbhvHmSVQWdt51mbbtxjMWP4LwvbYk6xqTDNnj9FyvSRGqMvRYxWuKyALJbf8265`

## License

[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
