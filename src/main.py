from datetime import date
from request import Fetch
from file_operations import CSVOperations

URL = 'https://api.ubiplaces.com.br/is/imoveis?exibir=12&pagina=1'

if __name__ == '__main__':
    total_imoveis = Fetch.make_request('GET', URL, 'total_imoveis')

    observation = [{'dia': str(date.today()), 'total_imoveis': total_imoveis}]

    CSVOperations.write_csv(observation)
