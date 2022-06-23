# MobileNetworkSimulator

The tool simulates the network by generating calls for the given time period and with the given number of subscribers. There are 3 categories of subscribers that can be simulated:
- regular subscribers
- semi-pro subscribers (small/medium business customers)
- pro subscribers (huge customers like call-centers etc.)
- sim boxes (used for fraud)

Each category is characterised by several attributes (hard-coded in the simulator) that determine subscriber willingness to make a local or international call, move to a different BTS, call his friends vs random numbers, etc. Each subscriber may also have more than one sim card and the probability of that is also determined by the category.

The simulator generates two csv files:
- cdr.csv - each row is a call data record with:
  - imsi - sim card unique identifier
  - to_imsi - IMSI of the 2nd connection leg or 0 for connection outside of the network (like international)
  - to_msisdn - the phone number of the 2nd connection leg (also for international calls)
  - start_date - call start date
  - start_time - call start time
  - duration - call duration in minutes
  - type - record type: MO for IMSI that started the call, MT for IMSI that received the call
  - location_id - BTS id to which IMSI was connected during the call
- imsi.csv - each row describes one IMSI (sim card):
  - imsi - sim card unique identifier
  - msisdn - phone number assigned to IMSI
  - imsi_per_cust - number of active sim card for the customer
  - trusted - is the customer trusted (set for big pro customers)
  - is_fraud - is the IMSI confirmed fraud (sim box)

## Running the tool

The tool requires python3 to run.

```
$ python3 main.py -h
usage: main.py [-h] --from-day FROM_DAY --days DAYS --sub SUB --pro PRO
               --spro SPRO --simbox SIMBOX

Mobile Network Simulator

optional arguments:
  -h, --help           show this help message and exit
  --from-day FROM_DAY  The first day YYYY-MM-DD
  --days DAYS          Number of days simulated
  --sub SUB            Number of regular subscribers
  --pro PRO            Number of professional subscribers
  --spro SPRO          Number of semi-professional subscribers
  --simbox SIMBOX      Number of simboxes
``` 

Examples:

Simulating a network with 100000 subscribers (90000 regular, 6000 pro, 3000 semi-pro, and 1000 sim boxes) for 7 days starting from 2022-06-06
```
python3 main.py --from 2022-06-06 --days 7 --sub 90000 --pro 6000 --spro 3000 --sim 1000
```
