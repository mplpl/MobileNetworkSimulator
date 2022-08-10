from Imsi import Imsi
from Imsi import s_factor
import random


class ProImsiProfile(object):

    def generate_imsi(self, id: int, imsi_per_cust: int = 0):

        activity_factor = random.randint(20, 40) / 100  # 0.2 - 0.4
        mobility_factor = random.randint(0, 10) / 1000  # 0 - 0.01
        international_activity_factor = random.randint(0, 20) / 10000  # 0 - 0.002
        social_factor = s_factor(0.1, 0.3)
        location = random.randint(1000, 2000)
        if imsi_per_cust == 0:
            imsi_per_cust = random.randint(50, 300)

        return Imsi(id=id, activity_factor=activity_factor, mobility_factor=mobility_factor,
                    international_activity_factor=international_activity_factor, social_factor=social_factor,
                    initial_location=location, imsi_per_cust=imsi_per_cust, trusted=1)