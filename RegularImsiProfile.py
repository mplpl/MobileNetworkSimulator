from Imsi import Imsi
from Imsi import s_factor
import random


class RegularImsiProfile(object):

    def generate_imsi(self, id: int):

        activity_factor = random.randint(0, 10) / 1000 # 0 - 0.01
        mobility_factor = random.randint(0, 20) / 100  # 0 - 0.2
        international_activity_factor = random.randint(0, 20) / 10000  # 0 - 0.02
        social_factor = s_factor(0.5, 0.3)
        location = random.randint(1000, 2000)
        imsi_per_cust = 1 if random.random() < 0.8 else random.randint(2, 10)

        return Imsi(id=id, activity_factor=activity_factor, mobility_factor=mobility_factor,
                    international_activity_factor=international_activity_factor, social_factor=social_factor,
                    initial_location=location, imsi_per_cust=imsi_per_cust, trusted=0)
