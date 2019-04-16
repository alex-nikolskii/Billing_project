class PersonalInformation:
    def __init__(self, number, tariff_id, conn_date, rate):
        self.number = number
        self.conn_date = conn_date
        self.rate_data = self.__get_rate_data(rate, tariff_id)

    @staticmethod
    def __get_rate_data(rate, tariff_id):
        if rate:
            return rate.get(tariff_id)
        else:
            return None

    # Для реализации сортировки
    def __lt__(self, other):
        return self.conn_date > other.conn_date

    def __str__(self):
        return f'Personal information for subscriber "{self.number}":\n' \
               f'connection date — {self.conn_date}; ' \
               f'rate data — {self.rate_data}\n'
