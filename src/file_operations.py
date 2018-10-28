import csv
import os.path


class CSVOperations():

    def write_csv(data, file_name='../data/registro_total_imoveis.csv',
                  fieldnames=['dia', 'total_imoveis']):

        """ Writes a list of dictionaries into a csv file

        Arguments:

        data -> list of dictionaries that will be writen
        file_name -> the name of the target file
            (default ../data/registro_total_imoveis.csv)
        fieldnames -> list of strings containing the name of the collumns
            (default ['dia', 'total_imoveis'])
        """

        file_exists = os.path.isfile(file_name)

        with open(file_name, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # writes header only once in the file
            if not file_exists:
                writer.writeheader()

            for observation in data:
                writer.writerow(observation)
