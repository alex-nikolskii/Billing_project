import entering_data as ed
from billing import Billing


def main(entered_data):
        bill = Billing(
            log_f_name=entered_data.log_file,
            rate_f_name=entered_data.rate_file,
            map_f_name=entered_data.map_num_rate,
            log_f_enc=entered_data.log_enc,
            rates_f_enc=entered_data.rate_enc,
            map_f_enc=entered_data.mnr_enc,
            group_service=entered_data.service_filter,
            group_volume=entered_data.volume_filter,
            group_date=entered_data.filter_with_date,
            group_senders_location=entered_data.send_loc_filter,
            group_recipients_location=entered_data.recp_loc_filter,
            group_senders=entered_data.send_nums_filter,
            group_recipients=entered_data.recp_nums_filter,
            group_all=entered_data.all_users,
            det_bill=entered_data.detailed_bill
        )
        print(bill)


if __name__ == '__main__':
    main(ed.input_data())

