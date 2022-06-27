from Imsi import Imsi
from Imsi import s_factor
import random


class SimBoxProfile(object):

    def generate_imsi(self, id: int):

        activity_factor = random.randint(30, 50) / 100  # 0.3 - 0.5
        mobility_factor = random.randint(0, 10) / 10000  # 0 - 0.001
        international_activity_factor = random.randint(0, 10) / 10000  # 0 - 0.001
        social_factor = s_factor(0.1, 0.1)
        location = random.randint(1000, 2000)
        imsi_per_cust = random.randint(50, 300)

        return Imsi(id=id, activity_factor=activity_factor, mobility_factor=mobility_factor,
                    international_activity_factor=international_activity_factor, social_factor=social_factor,
                    initial_location=location, imsi_per_cust=imsi_per_cust, trusted=0)
