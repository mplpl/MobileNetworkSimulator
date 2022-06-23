# MobileNetworkSimulator

The tool simulates the network by generating calls for the given time period and with the given number of subscribers. There are 3 categories of subscribers that can be simulated:
* regular subscribers
* semi-pro subscribers (small/medium business customers)
* pro subscribers (huge customers like call-centers etc.)
* sim boxes (used for froud)


Each category is characterised by several attributes (hard-coded in the simulator) that determine subscribed willingness to make a local or international call, move to a different BTS, call his friends vs random numbers, etc. Each subscriber may also have more than one sim card and the probability of that is also determined by the category.

The simulator generates two csv files:
* cdr.csv - each row is a call data record with:
** imsi - sim card unique identifier
** to_imsi - IMSI of the 2nd connection leg or 0 for connection outside of the network (like international)
** to_msisdn - the phone number of the 2nd connection leg (also for international calls)
** start_date - call start date
** start_time - call start time
** duration - call duration in minutes
** type - record type: MO for IMSI that started the call, MT for IMSI that received the call
** location_id - BTS id to which IMSI was connected during the call
* imsi.csv - each row describes one IMSI (sim card):
** imsi - sim card unique identifier
** msisdn - phone number assigned to IMSI
** imsi_per_cust - number of active sim card for the customer
** trusted - is the customer trusted (set for big pro customers)
** is_froud - is the IMSI confirmed froud (sim box)
