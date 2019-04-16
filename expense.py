import decimal as dcm


class Expense:
    __PRICE = ' ' + 'price'
    __INTERCITY_PRICE_COEFF = 'intercity price coefficient'
    __ERROR_MESS = "can't be calculated, seem's like problems with rate " \
                   "data. Check it for correctness."
    # Учет только 3х знаков после запятой
    dcm.getcontext().prec = 3

    def __init__(self, transaction, map_table):
        self.transaction = transaction
        self.map_table = map_table
        self.balance = self.__calculate_balance()

    def __get_rate_info(self):
        all_rates = self.map_table[self.transaction.sender]
        for rate in all_rates:
            if rate is not None:
                if rate.conn_date < self.transaction.date:
                    return rate
        return None

    def __get_service_price(self):
        rate_data = self.__get_rate_info().rate_data
        if rate_data is not None:
            key = str(self.transaction.service) + self.__PRICE
            if self.transaction.send_loc == self.transaction.recip_loc:
                return dcm.Decimal(rate_data.get(key))
            else:
                # Домножение на коэффициент межгорода.
                return dcm.Decimal(rate_data.get(key)) \
                    * dcm.Decimal(rate_data.get(self.__INTERCITY_PRICE_COEFF))
        else:
            return -1

    def __calculate_balance(self):
        price = self.__get_service_price()
        if price >= 0:
            return dcm.Decimal(self.transaction.volume) * price
        else:
            return self.__ERROR_MESS

    def __float__(self):
        return float(self.balance)

    def __add__(self, other):
        return float(self.balance) + float(other.balance)

    # Сделать более достойный вывод.
    def __str__(self):
        return f'Balance for service {self.transaction.service} ' \
            f'for user {self.transaction.sender} is {self.balance}$ '
