import csv
import os.path


IDENTITY_FUNCTION = lambda x : x


class CSVOperations():

    def read_csv(self, file_name='../data/registro_total_imoveis.csv',
                 file_handler=IDENTITY_FUNCTION):

        with open(file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return file_handler(reader)

    def write_csv(self, data, file_name='../data/registro_total_imoveis.csv',
                  fieldnames=['dia', 'total_imoveis']):

        """ Writes a list of dictionaries into a csv file

        Arguments:

        data -> list of dictionaries that will be writen
        file_name -> the name of the target file
            (default ../data/registro_total_imoveis.csv)
        fieldnames -> list of strings containing the name of the collumns
            (default ['dia', 'total_imoveis'])
        """

        # Read all the data of the csv file
        csv_data = self.read_csv(file_handler=(lambda x: list(x)))

        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            # check if the day of the data is already in the file.
            # If true, change the total from the old file with the new one
            # else, just append the new data
            if csv_data and data['dia'] == csv_data[-1]['dia']:
                csv_data[-1]['total_imoveis'] = data['total_imoveis']
            else:
                csv_data.append(data)

            for row in csv_data:
                writer.writerow(row)
