import unittest
from mapping_number_and_rate import MapNumsRatesReader
from rates import RatesTableReader
from billing import Billing


class TestMappingNumbersTariffsMethods(unittest.TestCase):

    # В случае изменения имени файла с тарифами передать его в конструктор
    rates_table = RatesTableReader().rate_table
    mnr_reader = MapNumsRatesReader('number-rate-test.txt', rates_table).map_table

    @staticmethod
    def get_err(ind):
        with open('map_errors.txt', 'r') as err_f:
            error = err_f.readlines()
        return error[ind].rstrip()

    def test_invalid_input_separator(self):
        error = self.get_err(1)
        should_be = 'Please, check your input in line "89090995429:3: ;" ' \
                    'with this information: "invalid literal for int() with ' \
                    'base 10: \' ;\'"'
        self.assertEqual(should_be, error)

    def test_id_is_number(self):
        error = self.get_err(0)
        should_be = 'Please, check your input in line "89090995429:ieieir:2" '\
                    'with this information: "Tariff ID is not a digit!"'
        self.assertEqual(should_be, error)

    def test_number(self):
        error = self.get_err(2)
        should_be = 'Please, check your input in line "kkerjker:2:123" ' \
                    'with this information: "Number is not a digit!"'
        self.assertEqual(should_be, error)

    def test_date_parse_not_fulfilled_with_month_day(self):
        error = self.get_err(3)
        should_be = 'Please, check your input in line "89092:3:2012" with ' \
                    'this information: "function missing required argument ' \
                    '\'month\' (pos 2)"'
        self.assertEqual(should_be, error)

    def test_date_parse_not_fulfilled_with_day(self):
        error = self.get_err(4)
        should_be = 'Please, check your input in line "8909094:2:2012.2" ' \
                    'with this information: "function missing required ' \
                    'argument \'day\' (pos 3)"'
        self.assertEqual(should_be, error)

    def test_date_invalid_parser(self):
        error = self.get_err(5)
        should_be = 'Please, check your input in line "890902:1:2012-2-31" ' \
                    'with this information: "invalid literal for int() with ' \
                    'base 10: \'2012-2-31\'"'
        self.assertEqual(should_be, error)


class TestRatesMethods(unittest.TestCase):

    @staticmethod
    def get_err(filename):
        with open(filename, 'r') as err_f:
            return err_f.read().rstrip()

    def test_extra_field_and_missing_value(self):
        rates_table = RatesTableReader(
            'rates-tests/rates-test-0.txt').rate_table
        error = self.get_err('rates_errors.txt')
        should_be = 'There is no value in column in rate with id 1'
        self.assertEqual(should_be, error)

    def test_missing_field(self):
        rates_table = RatesTableReader(
            'rates-tests/rates-test-1.txt').rate_table
        error = self.get_err('rates_errors.txt')
        should_be = 'There is no column name for not empty column in ' \
                    'rate with id 1'
        self.assertEqual(should_be, error)

    def test_missing_id(self):
        rates_table = RatesTableReader(
            'rates-tests/rates-test-2.txt').rate_table
        error = error = self.get_err('rates_errors.txt')
        should_be = "'id'"
        self.assertEqual(should_be, error)


class TestBillingMethods(unittest.TestCase):

    def initialise_errors():
        with open('log-test.txt', 'r', encoding='utf-8') as f:
            with open('log_errors.txt', 'w', encoding='utf-8') as err_f:
                for line in f:
                    try:
                        Billing.validate_log_line(line.rstrip())
                    except ValueError as error:
                        err_f.write(str(error) + '\n')

    initialise_errors()

    @staticmethod
    def get_err(ind):
        with open('log_errors.txt', 'r', encoding='utf-8') as err_f:
            return err_f.readlines()[ind].rstrip()

    def test_log_invalid_service(self):
        error = self.get_err(0)
        should_be = 'Invalid service in row "cal 20 2018.4.15 ' \
                    'Екатеринбург-Екатеринбург 89090995429 89090995429"'
        self.assertEqual(should_be, error)

    def test_log_invalid_volume(self):
        error = self.get_err(1)
        should_be = 'Volume of service is not a number ' \
                    'in row "net 2k 2018.4.15 Екатеринбург-Екатеринбург' \
                    ' 89090995429 89090995429"'
        self.assertEqual(should_be, error)

    def test_log_invalid_sender_number(self):
        error = self.get_err(2)
        should_be = 'Sender\'s number consist\'s not only of digits in row ' \
                    '"net 20 2018.4.15 Екатеринбург-Екатеринбург ' \
                    'ghrhugr 89090995429"'
        self.assertEqual(should_be, error)

    def test_log_invalid_recipient_number(self):
        error = self.get_err(3)
        should_be = 'Recipient\'s number consist\'s not only of digits in ' \
                    'row "net 20 2018.4.15 Екатеринбург-Екатеринбург ' \
                    '89090995429 k"'
        self.assertEqual(should_be, error)


if __name__ == '__main__':
    unittest.main()
