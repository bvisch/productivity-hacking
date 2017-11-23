from liblo import *

import sys
import time
import csv

data = { 'fft0': [], 'fft1': [], 'fft2': [], 'fft3': [] }

class MuseServer(ServerThread):

    #listen for messages on port 5000
    def __init__(self):
        ServerThread.__init__(self, 5000)
        self.packet = { 'fft0': [], 'fft1': [], 'fft2': [], 'fft3': [] }
        self.garbage = False

    @make_method('/muse/elements/blink', 'i')
    def blink_callback(self, path, args):
        print("blink" + str(args))
        if args[0] == 1:
            self.garbage = True


    @make_method('/muse/elements/jaw_clench', 'i')
    def clench_callback(self, path, args):
        print("clench" + str(args))
        if args[0] == 1:
            self.garbage = True


    #receive fft data
    @make_method('/muse/elements/raw_fft0', 'f'*129)
    def fft0_callback(self, path, args):
        print("1")
        self.packet['fft0'].append(args)

    @make_method('/muse/elements/raw_fft1', 'f'*129)
    def fft1_callback(self, path, args):
        print("2")
        self.packet['fft1'].append(args)

    @make_method('/muse/elements/raw_fft2', 'f'*129)
    def fft2_callback(self, path, args):
        print("3")
        self.packet['fft2'].append(args)

    @make_method('/muse/elements/raw_fft3', 'f'*129)
    def fft3_callback(self, path, args):
        print("4")
        self.packet['fft3'].append(args)

        if not self.garbage:
            data['fft0'].append(self.packet['fft0'])
            data['fft1'].append(self.packet['fft1'])
            data['fft2'].append(self.packet['fft2'])
            data['fft3'].append(self.packet['fft3'])
            self.packet = { 'fft0': [], 'fft1': [], 'fft2': [], 'fft3': [] }
        else:
            self.garbage = False



try:
    server = MuseServer()
except ServerError as err:
    print(str(err))
    sys.exit()


#wait 1 minute
print('Waiting 1 minute before data collection')
time.sleep(60)

#collect data for 10 minutes
print('Collecting data')
server.start()
time.sleep(600)
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
