from liblo import *

import sys
import time
import csv

data = { 'fft0': [], 'fft1': [], 'fft2': [], 'fft3': [] }

class MuseServer(ServerThread):
    #listen for messages on port 5000
    def __init__(self):
        ServerThread.__init__(self, 5000)

    #receive fft data
    @make_method('/muse/elements/raw_fft0', 'f'*129)
    def fft0_callback(self, path, args):
        data['fft0'].append(args)

    @make_method('/muse/elements/raw_fft1', 'f'*129)
    def fft1_callback(self, path, args):
        data['fft1'].append(args)

    @make_method('/muse/elements/raw_fft2', 'f'*129)
    def fft2_callback(self, path, args):
        data['fft2'].append(args)

    @make_method('/muse/elements/raw_fft3', 'f'*129)
    def fft3_callback(self, path, args):
        data['fft3'].append(args)



try:
    server = MuseServer()
except ServerError as err:
    print(str(err))
    sys.exit()



#wait 10 minutes
print('Waiting 10 minutes before data collection')
time.sleep(600)

#collect data for 20 minutes
print('Collecting data')
server.start()
time.sleep(1200)
server.stop()

#save to csv
print('Saving data')
# size = len(min(data.values(), key=len))

data_csv = list(zip(*data.values()))
# data_csv = [[item for sublist in row for item in sublist] for row in data_csv]

filename = sys.argv[1]
with open(filename + '.csv', 'w') as savefile:
    wr = csv.writer(savefile)
    wr.writerows(data_csv)
