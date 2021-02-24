import hpfeeds
import json
import sys



def on_message(identifier, channel, payload):

    f = open("data.txt", "a")
    f.write(payload + '\n')



def on_error(payload):
    print(' -> errormessage from server: {0}'.format(payload), file=sys.stderr)



def main():
    hpc = hpfeeds.new('157.245.114.100', 10000, 'HONEYPOT', 'H0N3YP0T4U')

    hpc.subscribe('HONEYPOT')
    hpc.run(on_message, on_error)
    hpc.close()


main()
