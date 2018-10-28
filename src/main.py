import time
from datetime import date
from request import Fetch
from file_operations import CSVOperations
from bot import UbiPlacesBot

URL = 'https://api.ubiplaces.com.br/is/imoveis?exibir=12&pagina=1'

def main():
    bot = UbiPlacesBot()
    last_update_id = None
    while True:
        updates = bot.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = bot.get_last_update_id(updates) + 1
            bot.echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    #total_imoveis = Fetch.make_request('GET', URL, 'total_imoveis')

    #observation = [{'dia': str(date.today()), 'total_imoveis': total_imoveis}]

    #CSVOperations.write_csv(observation)
    main()
