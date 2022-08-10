from SimBoxProfile import SimBoxProfile
from RegularImsiProfile import RegularImsiProfile
from ProImsiProfile import ProImsiProfile
from SemiProProfile import SemiProImsiProfile

from collections import deque


class ImsiGenerator:

    def __init__(self, network):
        self.network = network
        self.imsis = []
        self.last_customer_id = 1000

    def __generate_in_profile(self, profile, count: int, id_start: int, friends: int):

        imsi_id = id_start
        cust_sim_remaining = 0
        currect_customer_imsi_count = -1
        prev = deque()

        for i in range(count):

            if cust_sim_remaining:
                imsi = profile.generate_imsi(id=imsi_id, imsi_per_cust=currect_customer_imsi_count)
            else:
                imsi = profile.generate_imsi(id=imsi_id)
                if imsi.imsi_per_cust > count - i:
                    imsi.imsi_per_cust = count - i
                cust_sim_remaining = imsi.imsi_per_cust
                currect_customer_imsi_count = imsi.imsi_per_cust
                self.last_customer_id += 1

            imsi.customer_id = self.last_customer_id
            cust_sim_remaining -= 1

            if friends:
                for prev_imsi in prev:
                    imsi.add_friends(prev_imsi.id)
                    prev_imsi.add_friends(imsi.id)
                if i >= friends:
                    prev.popleft()
                prev.append(imsi)

            self.imsis.append(imsi)
            self.network.register_imsi(imsi)
            imsi_id += 1

    def generate_imsis(self, simboxes_count: int, regulars_count: int, pros_count: int,
                       semi_pros_count: int, simbox_start_msisdn: int) -> [object]:

        self.__generate_in_profile(SimBoxProfile(), simboxes_count, simbox_start_msisdn, 0)
        self.__generate_in_profile(RegularImsiProfile(), regulars_count, 1000000, 10)
        self.__generate_in_profile(ProImsiProfile(), pros_count, 2000000, 0)
        self.__generate_in_profile(SemiProImsiProfile(), semi_pros_count, 3000000, 0)

        return self.imsis