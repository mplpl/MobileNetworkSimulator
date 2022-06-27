from collections import namedtuple
from Imsi import Imsi
import random
import datetime

call_record = namedtuple('call_record', ['imsi', 'msisdn', 'to_imsi', 'to_msisdn', 'start_time', 'duration', 'location'])


class MobileNetwork(object):

    def __init__(self, from_day: datetime.datetime):

        self.minute = 0
        self.calls = []
        self.in_call = set()
        self.calls_generated = 0
        self.international_calls_generated = 0
        self.total_calls_duration = 0
        self.busy_calls = 0
        self._cdr_header_printed = False
        self._imsi_header_printed = False
        self.agg_cdrs = {}
        self.imsis = {}
        self.start_timestamp = from_day
        self.now = self.start_timestamp

    class AggCdr(object):

        def __init__(self):
            self.totLenMT = 0
            self.callCountMT = 0
            self.totLenMO = 0
            self.callCountMO = 0
            self.totLenIntern = 0
            self.callCountIntern = 0
            self.msisdns = set()
            self.locations = set()

        def update(self, len: int, type: str, intern: bool, msisdn: str, location: int):
            if type == "MT":
                self.totLenMT += len
                self.callCountMT += 1
            else:
                self.totLenMO += len
                self.callCountMO += 1
            if intern:
                self.totLenIntern += len
                self.callCountIntern += 1
            self.msisdns.add(msisdn)
            self.locations.add(location)

    def current_activity_profile(self):

        wd = self.now.weekday()

        if wd == 0:
            mod = 1.2
        elif wd == 1:
            mod = 1.3
        elif wd == 2:
            mod = 1.3
        elif wd == 3:
            mod = 1.5
        elif wd == 4:
            mod = 1.4
        elif wd == 5:
            mod = 0.6
        else:
            mod = 0.4

        if self.minute < 360:  # 6am
            return 0.05 * mod

        if self.minute < 480:  # 8am
            return 0.15 * mod

        if self.minute < 600:  # 10am
            return 0.2 * mod

        if self.minute < 720:  # 12am
            return 0.25 * mod

        if self.minute < 840:  # 14am
            return 0.3 * mod

        if self.minute < 1020:  # 5pm
            return 0.35 * mod

        if self.minute < 1200:  # 8pm
            return 0.3 * mod

        if self.minute < 1260:  # 9pm
            return 0.2 * mod

        if self.minute < 1320:  # 10pm
            return 0.15 * mod

        return 0.1 * mod

    def is_in_call(self, imsi: int):

        return imsi in self.in_call

    def __call_duration(self):
        return random.randint(1, 5) * random.randint(1, 5)

    f3 = open("imsi.csv", "w")

    def register_imsi(self, imsi: Imsi):
        self.imsis[imsi.id] = imsi
        if not self._imsi_header_printed:
            print("imsi,msisdn,imsi_per_cust,trusted,is_fraud", file=self.f3)
            self._imsi_header_printed = True
        print("{},{},{},{},{}".format(imsi.id, imsi.msisdn, imsi.imsi_per_cust, imsi.trusted,
                                      0 if imsi.id < 9000000 else 1), file=self.f3)

    def place_call(self, imsi: Imsi, to_imsi_id: int, to_msisdn: str):

        if to_imsi_id != 0 and self.is_in_call(to_imsi_id):
            self.busy_calls += 1
            return

        if imsi.id == to_imsi_id:
            self.busy_calls += 1
            return

        duration = self.__call_duration()
        to_imsi = None
        if to_imsi_id != 0:
            to_imsi = self.imsis.get(to_imsi_id)
            to_msisdn = to_imsi.msisdn

        self.calls.append(call_record(imsi.id, imsi.msisdn, to_imsi_id, to_msisdn, self.now, duration, imsi.location))
        self.in_call.add(imsi.id)
        if to_imsi_id != 0:
            self.in_call.add(to_imsi_id)
        self.calls_generated += 1
        self.total_calls_duration += duration
        if to_imsi_id == 0:
            self.international_calls_generated += 1

        acdr = self.agg_cdrs.get(imsi.id, MobileNetwork.AggCdr())
        acdr.update(duration, "MO", to_imsi_id == 0, to_msisdn, imsi.location)
        self.agg_cdrs[imsi.id] = acdr
        if to_imsi_id != 0:
            acdr = self.agg_cdrs.get(to_imsi_id, MobileNetwork.AggCdr())
            acdr.update(duration, "MT", False, imsi.id, to_imsi.location)
            self.agg_cdrs[to_imsi_id] = acdr

    def progress(self):

        self.minute += 1
        if self.minute >= 1440:
            self.minute = 0
        self.now += datetime.timedelta(minutes=1)

        new_calls = []

        for call in self.calls:
            if call.start_time + datetime.timedelta(minutes=call.duration) < self.now:
                self.add_cdr(imsi=call.imsi, to_imsi=call.to_imsi, to_msisdn=call.to_msisdn,
                             start_time=call.start_time, duration=call.duration,
                             type="MO", location=call.location)
                if call.to_imsi > 0:
                    to_imsi = self.imsis.get(call.to_imsi)
                    self.add_cdr(imsi=call.to_imsi, to_imsi=call.imsi, to_msisdn=call.msisdn,
                                 start_time=call.start_time, duration=call.duration,
                                 type="MT", location=to_imsi.location)
                    self.in_call.remove(call.to_imsi)
                self.in_call.remove(call.imsi)
            else:
                new_calls.append(call)

        self.calls = new_calls

    f = open("cdr.csv", "w")

    def add_cdr(self, imsi: int, to_imsi: str, to_msisdn: str, start_time: datetime, duration: int,
                type: str, location: int):
        if not self._cdr_header_printed:
            print("imsi,to_imsi,to_msisdn,start_date,start_time,duration,type,location_id", file=self.f)
            self._cdr_header_printed = True
        sdate = start_time.strftime("%Y-%m-%d")
        stime = start_time.strftime("%H:%M:%S")
        print("{},{},{},{},{},{},{},{}".format(imsi, to_imsi, to_msisdn, sdate, stime, duration, type, location),
              file=self.f)

    f2 = open("agg_cdr.csv", "w")

    def summary(self):

        print("\nNumber of calls: {}".format(self.calls_generated))
        print("Number of international calls: {}".format(self.international_calls_generated))
        print("Busy calls: {}".format(self.busy_calls))
        print("Total calls duration: {}".format(self.total_calls_duration))

        print("imsi,"
              "mo_call_duration,"
              "mo_call_count,"
              "mo_avg_call_duration,"
              "mt_call_duration,"
              "mt_call_count,"
              "mt_avg_call_duration,"
              "intern_call_duration,"
              "intern_call_count,"
              "intern_avg_call_duration,"
              "msisdns_called,"
              "msisdns_to_all_call,"
              "intern_to_all_calls,"
              "MO_calls_to_MT_calls,"
              "locations,"
              "MT_calls_to_locations,", file=self.f2)

        for imsi, acrd in self.agg_cdrs.items():
            print("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
                imsi,
                acrd.totLenMO,
                acrd.callCountMO,
                acrd.totLenMO/acrd.callCountMO if acrd.callCountMO > 0 else 0,
                acrd.totLenMT,
                acrd.callCountMT,
                acrd.totLenMT/acrd.callCountMT if acrd.callCountMT > 0 else 0,
                acrd.totLenIntern,
                acrd.callCountIntern,
                acrd.totLenIntern / acrd.callCountIntern if acrd.callCountIntern > 0 else 0,
                len(acrd.msisdns),
                len(acrd.msisdns) / (acrd.callCountMO + acrd.callCountMT) if acrd.callCountMO + acrd.callCountMT > 0 else 0,
                acrd.callCountIntern / (acrd.callCountMO + acrd.callCountMT) if acrd.callCountMO + acrd.callCountMT > 0 else 0,
                acrd.callCountMO / acrd.callCountMT if acrd.callCountMT > 0 else 0,
                len(acrd.locations),
                acrd.callCountMT / len(acrd.locations) if len(acrd.locations) > 0 else 0),
            file=self.f2)

