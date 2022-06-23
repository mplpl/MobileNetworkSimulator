from CallGenerator import CallGenerator
import argparse
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mobile Network Simulator')
    parser.add_argument('--from-day', help='The first day YYYY-MM-DD', required=False,
                        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
    parser.add_argument('--days', help='Number of days simulated', required=True, type=int)
    parser.add_argument('--sub', help='Number of regular subscribers', required=True, type=int)
    parser.add_argument('--pro', help='Number of professional subscribers', required=True, type=int)
    parser.add_argument('--spro', help='Number of semi-professional subscribers', required=True, type=int)
    parser.add_argument('--simbox', help='Number of simboxes', required=True, type=int)

    args = parser.parse_args()

    from_day = args.from_day if args.from_day is not None else datetime.datetime(year=2022, month=6, day=6, hour=0,
                                                                                 minute=0, second=0)

    CallGenerator().go(from_day=from_day, days=args.days, simboxes_count=args.simbox,
                       regulars_count=args.sub, pros_count=args.pro, semi_pro_count=args.spro)
