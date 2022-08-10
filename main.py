from CallGenerator import CallGenerator
import argparse
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mobile Network Simulator')
    parser.add_argument('--from-day', help='The first day YYYY-MM-DD', required=True,
                        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    parser.add_argument('--days', help='Number of days simulated', required=True, type=int)
    parser.add_argument('--sub', help='Number of regular subscribers', required=True, type=int)
    parser.add_argument('--pro', help='Number of professional subscribers', required=True, type=int)
    parser.add_argument('--spro', help='Number of semi-professional subscribers', required=True, type=int)
    parser.add_argument('--simbox', help='Number of simboxes', required=True, type=int)
    parser.add_argument('--simbox_start_msisdn', help='First simboxes MSISDN',
                        required=False, type=int, default=9000000,
                        metavar="[900000-999999]")

    args = parser.parse_args()

    if args.simbox_start_msisdn < 9000000 or args.simbox_start_msisdn > 9999999:
        print("Wrong value of simbox_start_msisdn - must be in [9000000, 9999999] range.")
        exit(1)

    CallGenerator().go(from_day=args.from_day, days=args.days, simboxes_count=args.simbox,
                       regulars_count=args.sub, pros_count=args.pro, semi_pro_count=args.spro,
                       simbox_start_msisdn=args.simbox_start_msisdn)
