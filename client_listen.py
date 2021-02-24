import hpfeeds

import sys



def on_message(identifier, channel, payload):

    print('on message')
    print(identifier, payload)


def on_error(payload):
    print(' -> errormessage from server: {0}'.format(payload), file=sys.stderr)



def main():
    hpc = hpfeeds.new('localhost', 10000, 'james', 'secret')

    hpc.subscribe('mychan')
    hpc.run(on_message, on_error)
    hpc.close()


main()
