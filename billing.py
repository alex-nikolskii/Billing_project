from rates import RatesTableReader
from mapping_number_and_rate import MapNumsRatesReader
import datetime as dt
import transaction as tr
import expense as ex


class Billing:
    # Передача входных аргументов командной строки
    def __init__(self, log_f_name, rate_f_name, map_f_name='number-rate.txt',
                 log_f_enc='utf-8', rates_f_enc='utf-8', map_f_enc='utf-8',
                 group_service=None, group_volume=None, group_date=None,
                 group_senders_location=None, group_recipients_location=None,
                 group_senders=None, group_recipients=None, group_all=False,
                 det_bill=False):
        self.rate_table = RatesTableReader(rate_f_name, rates_f_enc).rate_table
        self.map_num_rate = MapNumsRatesReader(map_f_name, self.rate_table,
                                               map_f_enc).map_table
        self.bill = self.create_bill(log_f_name, log_f_enc, group_service,
                                     group_volume, group_date,
                                     group_senders_location,
                                     group_recipients_location,
                                     group_senders, group_recipients,
                                     group_all)
        self.det_bill = det_bill

    @staticmethod
    def validate_log_line(row):
        try:
            possible_services = {'sms', 'net', 'call'}
            record = row.strip().split()
            service, volume, _date, location, sender, recipient = record
            if not volume.isdigit():
                raise ValueError(f'Volume of service is not a number in row '
                                 f'"{row}"')
            elif not sender.isdigit():
                raise ValueError(
                    f"Sender's number consist's not only of digits "
                    f"in row \"{row}\"")
            elif not recipient.isdigit():
                raise ValueError(
                    f"Recipient's number consist's not only of digits"
                    f" in row \"{row}\"")
            elif service not in possible_services:
                raise ValueError(f'Invalid service in row "{row}"')
            date = dt.date(*[int(e) for e in _date.split('-')])
            return service, volume, date, location, sender, recipient
        except ValueError as error:
            raise error

    def create_expense(self, transaction):
        return ex.Expense(transaction, self.map_num_rate)

    @staticmethod
    def group_by(transaction, group_service, group_volume, group_date,
                 group_senders_location, group_recipients_location,
                 group_senders, group_recipients, group_all):

        if group_service is not None and transaction.service in group_service:
            return transaction

        elif group_volume is not None and transaction.volume == group_volume:
            return transaction

        # Дата в формате YYYY-MM-DD
        elif group_date is not None and str(transaction.date) == group_date:
            return transaction

        elif group_senders_location is not None and transaction.send_loc == \
                group_senders_location.lower():
            return transaction

        elif group_recipients_location is not None and transaction.recip_loc\
                == group_recipients_location.lower():
            return transaction

        elif group_senders is not None \
                and (transaction.sender in group_senders):
            return transaction

        elif group_recipients is not None and transaction.recipient \
                in group_recipients:
            return transaction

        elif group_all:
            return transaction

    def create_bill(self, log_f_name, log_f_enc,
                    group_service=None,
                    group_volume=None,
                    group_date=None,
                    group_senders_location=None,
                    group_recipients_location=None,
                    group_senders=None,
                    group_recipients=None,
                    group_all=False):

        with open(log_f_name, 'r', encoding=log_f_enc) as log_file:
            with open('log_errors.txt', 'w', encoding='utf-8') as err_file:
                res = []
                for line in log_file:
                    try:
                        valid_line = self.validate_log_line(line)
                    except ValueError as error:
                        err = f'Please, check your input in line "{line}" ' \
                            f'with this information: "{error}"\n'
                        err_file.write(err)
                        valid_line = None

                    if valid_line is not None:
                        transaction = tr.Transaction(*valid_line)
                        if self.group_by(transaction, group_service,
                                         group_volume, group_date,
                                         group_senders_location,
                                         group_recipients_location,
                                         group_senders, group_recipients,
                                         group_all):
                            res.append(self.create_expense(transaction))
                return sum(list(map(float, res))), res

    def __str__(self):
        if self.det_bill:
            expenses = '\n'.join(list(map(str, self.bill[1])))
            res_str = f"Bill for the services consists of following " \
                f"expenses:\n\n{expenses}\n\nIt's price is: {self.bill[0]}"
            return res_str
        else:
            return f'Billing for the services is the following: {self.bill[0]}'
