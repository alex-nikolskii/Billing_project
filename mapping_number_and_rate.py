from collections import defaultdict
import datetime as dt
import personal_inf as p_inf


class MapNumsRatesReader:
    def __init__(self, filename, rate, encoding='utf-8',
                 err_filename='map_errors.txt'):
        self.map_table = self.read_map_num_id(filename, rate, encoding,
                                              err_filename)

    @staticmethod
    def validate_values(record):
        try:
            # Стоит ли писать тесты на это?
            row = record.strip().split(':')
            number, rate_id, _conn_date = row
            if not number.isdigit():
                raise ValueError('Number is not a digit!')
            elif not rate_id.isdigit():
                raise ValueError('Tariff ID is not a digit!')
            # date = year, month, day
            conn_date = dt.date(*[int(e) for e in _conn_date.split('.')])
            return number, rate_id, conn_date
        except (ValueError, TypeError) as error:
            raise error

    @staticmethod
    def sort(inf_list):
        for elem in inf_list:
            inf_list[elem].sort()
        return inf_list

    @staticmethod
    def read_map_num_id(filename, rate, encoding='utf-8',
                        err_filename='map_errors.txt'):
        with open(filename, 'r', encoding=encoding) as fin:
            rates_numbers = defaultdict(list)
            with open(err_filename, 'w', encoding='utf-8') as er:
                for line in fin:
                    try:
                        line = line.rstrip()
                        valid_line = MapNumsRatesReader.validate_values(line)
                    except (ValueError, TypeError) as error:
                        err = f'Please, check your input in line "{line}" ' \
                            f'with this information: "{error}"\n'
                        er.write(err)
                        valid_line = None

                    if valid_line is not None:
                        inf = p_inf.PersonalInformation(*valid_line, rate)
                        rates_numbers[inf.number].append(inf)
                    # Сортировка по дате подключения тарифа
                rates_numbers = MapNumsRatesReader.sort(rates_numbers)
            return rates_numbers
