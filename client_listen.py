import hpfeeds
import json
import sys



def on_message(identifier, channel, payload):

    f = open("data.txt", "a")
    f.write(str(payload) + '\n')
    print(payload)



def on_error(payload):
    print(' -> errormessage from server: {0}'.format(payload), file=sys.stderr)



def main():
    hpc = hpfeeds.new('x.x.x.x', 10000, 'IDENT', 'secret_password')

    hpc.subscribe('channel_name')
    hpc.run(on_message, on_error)
    hpc.close()


main()
