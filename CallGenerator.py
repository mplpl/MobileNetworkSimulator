from MobileNetwork import MobileNetwork
from ImsiGenerator import ImsiGenerator
import random
import datetime


class CallGenerator(object):

    def __init__(self):
        self.imsis = []
        self.network = None

    def random_imsi(self):
        x = random.randint(0, len(self.imsis) - 1)
        return self.imsis[x].id

    def go(self, from_day: datetime.datetime, days: int, simboxes_count: int, regulars_count: int, pros_count: int,
           semi_pro_count: int, simbox_start_msisdn: int):

        print("Mobile Network Simulator")
        print()
        print("From day: {}".format(from_day))
        print("Number of days: {}".format(days))
        print("Number of regular subscribers: {}".format(regulars_count))
        print("Number of professional subscribers: {}".format(pros_count))
        print("Number of semi-professional subscribers: {}".format(pros_count))
        print("Number of simboxes: {}".format(simboxes_count))
        print("Simbox start MSISDN: {}".format(simbox_start_msisdn))
        print("")

        random.seed()

        self.network = MobileNetwork(from_day=from_day)
        self.imsis = ImsiGenerator(self.network).generate_imsis(simboxes_count, regulars_count,
                                                                pros_count, semi_pro_count, simbox_start_msisdn)
        day = 0

        while day < days:
            minute = 0
            while minute < 1440:
                if minute % 60 == 0:
                    print("Simulating day {} hour {}".format(day + 1, int(minute / 60)))
                for imsi in self.imsis:
                    imsi.progress()
                    if not self.network.is_in_call(imsi.id):
                        should, intern = imsi.should_call(self.network.current_activity_profile())
                        if should:
                            if intern:
                                other_imsi = 0
                                other_msisdn = "+48" + str(random.randint(1, 999999999)).zfill(9)
                            else:
                                other_imsi = imsi.select_other()
                                if other_imsi == -1:
                                    other_imsi = self.random_imsi()
                                other_msisdn = 0
                            self.network.place_call(imsi, other_imsi, other_msisdn)
                            imsi.had_call(0)

                self.network.progress()
                minute += 1
            day += 1

        self.network.summary()





