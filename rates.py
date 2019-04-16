import csv


class RatesTableReader:
    def __init__(self, filename='rates.txt', encoding='utf-8',
                 err_filename='rates_errors.txt'):
        self.rate_table = self.__read_table(filename, encoding, err_filename)

    @staticmethod
    def validate_table(table):
        for i in range(1, len(table) + 1):
            if None in table[str(i)]:
                raise ValueError(f'There is no column name for not empty '
                                 f'column in rate with id {i}')
            elif None in table[str(i)].values():
                raise ValueError(f'There is no value in column in rate with '
                                 f'id {i}')

    @staticmethod
    def __read_table(filename, encoding, err_filename):
        with open(filename, 'r', encoding=encoding, newline='') as fin:
            with open(err_filename, 'w') as err_file:
                try:
                    fieldnames = fin.readline().rstrip().lower().split(',')
                    rates = csv.DictReader(fin, fieldnames=fieldnames)
                    rates_table = {row.pop('id'): row for row in rates}
                    RatesTableReader.validate_table(rates_table)
                    return rates_table
                except (ValueError, KeyError) as error:
                    err_file.write(str(error))
                    return None
