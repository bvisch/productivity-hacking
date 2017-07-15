from liblo import *

import sys
import select
import time
from sklearn import neural_network

regressor = neural_network.MLPRegressor(solver='lbfgs', max_iter=1000)

concentration = []
# data = {'low': [], 'delta': [], 'theta': [], 'alpha': [], 'beta': [], 'gamma': []}
data = {'delta': [], 'theta': [], 'alpha': [], 'beta': [], 'gamma': []}

class MuseServer(ServerThread):
    #listen for messages on port 5000
    def __init__(self):
        ServerThread.__init__(self, 5000)

    #receive accelrometer data
    @make_method('/muse/elements/experimental/concentration', 'f')
    def concentration_callback(self, path, args):
        concentration.append(args[0])


    # @make_method('/muse/elements/low_freqs_absolute', 'ffff')
    # def low_freqs_absolute_callback(self, path, args):
    #     data['low'].append(args)

    @make_method('/muse/elements/delta_relative', 'ffff')
    def delta_relative_callback(self, path, args):
        data['delta'].append(args)


    @make_method('/muse/elements/theta_relative', 'ffff')
    def theta_relative_callback(self, path, args):
        data['theta'].append(args)

    @make_method('/muse/elements/alpha_relative', 'ffff')
    def alpha_relative_callback(self, path, args):
        data['alpha'].append(args)

    @make_method('/muse/elements/beta_relative', 'ffff')
    def beta_relative_callback(self, path, args):
        data['beta'].append(args)

    @make_method('/muse/elements/gamma_relative', 'ffff')
    def gamma_relative_callback(self, path, args):
        data['gamma'].append(args)

    #handle unexpected messages
    # @make_method(None, None)
    # def fallback(self, path, args, types, src):
        # import pdb; pdb.set_trace()
        # print "Unknown message \
        # \n\t Source: '%s' \
        # \n\t Address: '%s' \
        # \n\t Types: '%s ' \
        # \n\t Payload: '%s'" \
        # % (src.url, path, types, args)

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0)
    for selected in i:
        if selected == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False

def stage1():
    global data, counts, concentration
    while 1:
        time.sleep(1)
        if heardEnter():
            import pdb; pdb.set_trace()
            X = list(zip(*data.values()))
            X = [[item for subsublist in sublist for item in subsublist] for sublist in X]
            y = concentration[:len(X)]
            regressor.fit(X,y)
            # data = {'low': [], 'delta': [], 'theta': [], 'alpha': [], 'beta': [], 'gamma': []}
            data = {'delta': [], 'theta': [], 'alpha': [], 'beta': [], 'gamma': []}
            concentration = []
            break

def stage2():
    global data, counts, concentration
    print("starting stage 2")
    while 1:
        time.sleep(1)
        # rows = list(zip(*data.values()))
        # x = [item for sublist in rows[-1] for item in sublist]
        size = len(data['delta'])
        x = [*data['delta'][size-1], *data['theta'][size-1], *data['alpha'][size-1], *data['beta'][size-1], *data['gamma'][size-1]]
        y = concentration[size-1]
        if len(x) == 20:
            print(regressor.predict([x]), y)

try:
    server = MuseServer()
except ServerError as err:
    # print str(err)
    import pdb; pdb.set_trace()
    sys.exit()

server.start()

if __name__ == "__main__":
    stage1()
    stage2()
