# HDFEEDS Docs 


***

## TOC

* [Broker Configuration ](##Broker-Configuration )
    * [Environment-Variables ](###Environment-Variables)
* [Client Configuration](##Client-Configuration)
    * [Publisher](###Publisher)
    * [Subcriber](###Subcriber)

***


## Broker Configuration 

```
version: '2.1'

volumes:
  hpfeeds_userdb: {}

services:
  hpfeeds:
    image: hpfeeds/hpfeeds-broker
    container_name: hpfeeds
    environment:
      HPFEEDS_IDENT_SECRET: 'secret_password'
      HPFEEDS_IDENT_SUBCHANS: 'channel_name'
      HPFEEDS_IDENT_PUBCHANS: 'channel_name'
   
    command:
     - '/app/bin/hpfeeds-broker'
     - '--endpoint=tcp:port=10000'
     - '--auth=env'
    ports:
     - "0.0.0.0:10000:10000"
    
    volumes:
     - hpfeeds_userdb:/app/var

```

The Broker is configured with a .ymal file, and initiated with docker. To start the broker service issue the command 'docker-compose up' from within the directory. 

***

### Environment Variables 

The environment section of the .yml configuration dictates what a parameters the clients need to pass in order to connect to the broker. To understand these a little more it's easier to break them apart. 



**HPFEEDS_IDENT**:

Although 'HPFEEDS' and 'IDENT' represent two different things, you will notice they stay consistent in each environment declaration. 


- HPFEEDS : Represents the service we are using - this should always be HPFEEDS for our purposes

- IDENT : This is the identifier for our Broker. It can have any name you like, ex.  'MYIDENT' 'SOMEIDENT' 


There are three ways you can trail the HPFEED_IDENT portion of the environment variables, these all are followed by a value that is passed in single quotes. 

- SECRET : This will be the password clients use to authenticate to the broker. 

- SUBCHANS : Signifies the name of the channel clients will read from

- PUBCHANS : Signifies the name of the channel clients will write to. 



*There are ways to obfuscate  this password, or the environment variables as a whole by storing them in a database. We will likely want to do this in a prod setting.*  



****

## Client Configuration

There are two ways a client can be used, a Subscriber (one that reads from the broker) and a Publisher (one who writes to the broker). In our examples we are using Python as the language to create these clients.

***

### Publisher 

```python
import asyncio
from hpfeeds.asyncio import ClientSession


async def main():
    async with ClientSession('x.x.x.x', 10000, 'IDENT', 'secret_password') as client:
        client.publish('channel_name', b'{"data": "Hello World"}')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

```

<ins>ClientSession() Arguments</ins>

This function takes 4 arguments  - IP Address of Broker, Port of Broker, Ident Name, Password. 

- **'x.x.x.x'**: This is going to be the IP Address of the broker. In the .yml configuration you will see 0.0.0.0 under the ports section. This means the broker will take on the IP Address of the host it's on - you will want to pass that IP into this function

- **10000** : Again in the ports section you will see :10000 after the 0.0.0.0, this is the port exposed for the broker service. It seems 10000 is the best practice, so we will use that. 

- **'IDENT'**: The middle portion of the environment variable  if you used HPFEEDS_MYBROKER_SECRET instead of HPFEEDS_IDENT_SECRET, you would want to pass 'MYBROKER' here instead. 

- **'secret_password'**: This is the password value set in the .yml file. 

After configuring the required parameters you will initiate  the listener  from the CLI with 

<ins>client.publish() Arguments</ins>

This function  takes in 2 arguments - Channel Name, Data to Publish

- **'channel_name'** : Represents the name declared in the broker .yml file. 

- **b'{"data": "Hello World"}'** : Example JSON post to the Broker. the b value is important as the broker expects data to arrive in byte strings. From there you can configure a JSON object (or whatever datatype you want) that can be parsed by the listeners. 

<ins>Calling the Publisher </ins>



```
python3 client_publish.py
```

***

### Subcriber  


```python

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

```

The subscriber  contains 2 helper functions that are called within the main function. By now it should be clear what values need to be passed into this function, so I will only address the on_message() function below. 

<ins>on_message()</ins>

- identifier : Can be used to identify the server - we aren't using this use. 

- channel : Represents the channel name it heard the message from 

- payload: this is the data that was sent from the publisher. 

This function is where you would define what you want to do with the data, in this example we are simply writing it to a text file, but you could write it to a database if desired. 

<ins>Calling the Subscriber </ins>

```
python3 client_listen.py
```

This process runs in a loop, since we are printing out the payload in the on_message function call we would see this output in the terminal as the publisher makes it's posts. 

```
b'{"data": "Hello World"}'
b'{"data": "Hello World"}'
```