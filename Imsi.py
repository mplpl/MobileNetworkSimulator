import random
from collections import namedtuple

s_factor = namedtuple('s_factor', ['friends', 'half_friends'])

taken_msisdns = set()

class Imsi(object):

    def __init__(self, id, activity_factor, mobility_factor, international_activity_factor,
                 social_factor, initial_location, imsi_per_cust, trusted):

        self.id = id
        self.activity_factor = activity_factor
        self.mobility_factor = mobility_factor
        self.international_activity_factor = international_activity_factor
        self.social_factor = social_factor
        self.location = initial_location
        self.friends = []
        self.half_friends = []
        self.__last_move_dir = -1
        msisdn = str(random.randint(1, 999999999)).zfill(9)
        while msisdn in taken_msisdns:
            msisdn = str(random.randint(1, 999999999)).zfill(9)
        self.msisdn = msisdn
        self.imsi_per_cust = imsi_per_cust
        self.trusted = trusted

    def add_friends(self, friend):
        self.friends.append(friend)

    def should_call(self, net_activity_factor):

        x = random.random()
        should = x < net_activity_factor * self.activity_factor
        intern = x < self.international_activity_factor * self.activity_factor
        return should, intern

    def had_call(self, imsi):
        #if imsi > 0 and imsi not in self.half_friends:
        #    self.half_friends.append(imsi)
        pass

    def select_other(self):

        x = random.random()
        if len(self.friends) > 0 and x < self.social_factor.friends:
            y = random.randint(0, len(self.friends) - 1)
            return self.friends[y]
        if len(self.half_friends) > 0 and x < self.social_factor.half_friends:
            y = random.randint(0, len(self.half_friends) - 1)
            return self.half_friends[y]
        return -1

    def progress(self):
        self.__last_move_dir *= -1
        if random.random() < self.mobility_factor:
            self.location += self.__last_move_dir

