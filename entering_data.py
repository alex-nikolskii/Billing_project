import argparse


class EnteredData:
    def __init__(self, namespace):
        self.log_file = namespace.log_file
        self.rate_file = namespace.rate_file
        self.map_num_rate = namespace.map_num_rate
        self.log_enc = namespace.log_enc
        self.rate_enc = namespace.rate_enc
        self.mnr_enc = namespace.mnr_enc
        self.service_filter = namespace.service
        self.volume_filter = namespace.volume
        self.filter_with_date = namespace.date
        self.send_loc_filter = namespace.sender_loc
        self.recp_loc_filter = namespace.recp_loc
        self.send_nums_filter = namespace.numbers_to_group_sender
        self.recp_nums_filter = namespace.numbers_to_group_recipient
        self.all_users = namespace.all_users
        self.detailed_bill = namespace.detailed_bill


def create_argument_parser():
    description = 'This program is for automatic bill calculations\n\n'
    epilog = (
        'Exit code "0" - Successfully ended.\n'
        'Exit code "1" - Exception during the working with the file. '
        'Check filename\'s\n\n'
        'November 2018, Ural Federal University'
    )
    parser_help = 'Displays help information on this program.\n\n'
    log_data_help = 'Logs data will be read for the calculation'
    rates_file_help = 'Rates information will be read for calculation'
    map_nums_rates_help = 'The correspondence of the number ' \
                          'and rate ID will be used in the program'
    date_help = 'Enter a date to filter the bill.'
    all_users_help = 'Display bill for all numbers in log file'
    detailed_bill_help = 'Displays whole information about bill'
    senders_nums_help = "Enter nums to filter transactions with sender's " \
                        "number and see there bill"
    recipients_nums_help = "Enter nums to see transactions with recipient's " \
                           "numbers and see there bill"
    service_help = 'Calculate bill filtered with service'
    log_enc_help = 'Defines log file encoding'
    rate_enc_help = 'Defines rate file encoding'
    mnr_enc_help = 'Defines map numbers and rates files encoding'
    sender_location_help = 'Enter to filter transactions with sender location'
    recipient_location_help = 'Enter to filter transactions with ' \
                              'recipient location'
    volume_help = 'Filter log with this amount of volume'

    parser = argparse.ArgumentParser(
        prog='Billing',
        description=description,
        epilog=epilog,
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter
    )
    param_group = parser.add_argument_group(
        title='Launch params'
    )
    param_group.add_argument(
        '--help', '-h',
        action='help',
        help=parser_help
    )
    param_group.add_argument(
        '--log-file', '-l',
        type=str,
        help=log_data_help,
        required=True
    )
    param_group.add_argument(
        '--rate-file', '-r',
        type=str,
        help=rates_file_help,
        required=True
    )
    param_group.add_argument(
        '--map-num-rate', '-mnr',
        type=str,
        help=map_nums_rates_help,
        required=True
    )
    param_group.add_argument(
        '--log-enc', '-le',
        type=str,
        help=log_enc_help,
        default='utf-8'
    )
    param_group.add_argument(
        '--rate-enc', '-re',
        type=str,
        help=rate_enc_help,
        default='utf-8'
    )
    param_group.add_argument(
        '--mnr-enc', '-me',
        type=str,
        help=mnr_enc_help,
        default='utf-8'
    )
    param_group.add_argument(
        '--service', '-s',
        type=str,
        help=service_help
    )
    param_group.add_argument(
        '--volume', '-v',
        type=str,
        help=volume_help
    )
    param_group.add_argument(
        '--date', '-d',
        type=str,
        help=date_help,
    )
    param_group.add_argument(
        '--sender-loc', '-sl',
        type=str,
        help=sender_location_help
    )
    param_group.add_argument(
        '--recp-loc', '-rl',
        type=str,
        help=recipient_location_help
    )
    param_group.add_argument(
        '--numbers-to-group-sender', '-ns',
        nargs='+',
        help=senders_nums_help
    )
    param_group.add_argument(
        '--numbers-to-group-recipient', '-nr',
        nargs='+',
        help=recipients_nums_help
    )
    param_group.add_argument(
        '--detailed-bill', '-db',
        action="store_true",
        help=detailed_bill_help
    )
    param_group.add_argument(
        '--all-users', '-a',
        action="store_true",
        help=all_users_help
    )

    return parser


def input_data():
    parser = create_argument_parser()
    namespace = parser.parse_args()

    return EnteredData(namespace)

