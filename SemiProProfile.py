from Imsi import Imsi
from Imsi import s_factor
import random


class SemiProImsiProfile(object):

    def generate_imsi(self, id: int):

        activity_factor = random.randint(30, 60) / 100  # 0.4 - 0.8
        mobility_factor = random.randint(0, 50) / 100  # 0 - 0.05
        international_activity_factor = random.randint(0, 20) / 10000  # 0 - 0.002
        social_factor = s_factor(0.1, 0.3)
        location = random.randint(1000, 2000)
        imsi_per_cust = random.randint(1, 60)

        return Imsi(id=id, activity_factor=activity_factor, mobility_factor=mobility_factor,
                    international_activity_factor=international_activity_factor, social_factor=social_factor,
                    initial_location=location, imsi_per_cust=imsi_per_cust, trusted=0)