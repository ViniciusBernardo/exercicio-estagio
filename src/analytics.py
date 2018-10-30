from datetime import date
from file_operations import CSVOperations
from request import Fetch

TO_LIST_FUNCTIONS = lambda x: list(x)


class Analytic():

    file_operator = CSVOperations()

    URL = 'https://api.ubiplaces.com.br/is/imoveis?exibir=12&pagina=1'

    def fetch_data_api(self):
        total_imoveis = Fetch.make_request('GET', self.URL, 'total_imoveis')

        self.file_operator.write_csv({
            'dia': str(date.today()),
            'total_imoveis': total_imoveis}
        )
        return total_imoveis

    def analyse_past_days(self):
        csv_data = self.file_operator.read_csv(
            file_handler=TO_LIST_FUNCTIONS)

        if not csv_data[-1]['dia'] == str(date.today()):
            self.fetch_data_api()
            csv_data = self.file_operator.read_csv(
                file_handler=TO_LIST_FUNCTIONS)

        yesterday_total_imoveis = int(csv_data[-2]['total_imoveis'])
        today_total_imoveis = int(csv_data[-1]['total_imoveis'])
        variation = (yesterday_total_imoveis/today_total_imoveis - 1)*100

        if variation > 0:
            variation_type = 'Aumento de'

        elif variation < 0:
            variation_type = 'Queda de'

        else:
            variation_type = 'Estabilizado em'

        data = {
            'yesterday': csv_data[-2]['dia'],
            'yesterday_total_imoveis': yesterday_total_imoveis,
            'today': csv_data[-1]['dia'],
            'today_total_imoveis': today_total_imoveis,
            'variation': variation,
            'variation_type': variation_type,
        }

        return data
