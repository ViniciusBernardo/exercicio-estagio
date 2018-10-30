import time
from bot import UbiPlacesBot


def main():
    bot = UbiPlacesBot()
    last_update_id = None
    while True:
        updates = bot.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = bot.get_last_update_id(updates) + 1
            bot.echo_all(updates)
        time.sleep(1)

if __name__ == '__main__':
    main()
