"""Hodor meets IRC.

This program implements a funny little chatbot which says, under
certain conditions, "Hodor."  It serves as a simple example of an IRC
bot in python:

* It joins channels when invited
* It replies to private messages
* It (intermittently) speaks in channels when others are speaking
* It also conveniently presents protocol information on stdout.

Requires the irc package, obtainable by typing

    pip install irc

"""

import argparse
import random
import irc.client
import irc.events

def percentx(param):
    val = int(param)
    if val < 0 or val > 100:
        raise argparse.ArgumentTypeError(
            ("%s is invalid; choose an value between 0 and 100.") % val)
    return val

parser = argparse.ArgumentParser(description='Hodor meets IRC.')
parser.add_argument('--server', default='localhost',
                    help='Server to connect to (defaults to localhost)')
parser.add_argument('--port', type=int, default=6667,
                    help='Port to connect to')
parser.add_argument('--nick', default='hodor',
                    help='Nickname to connect with')
parser.add_argument('--probability', type=percentx, default=5,
                    help='Probability to reply in channel per message')
parser.add_argument('--verbose', action='store_true',
                    help='Print to stdout all events')
parser.add_argument('--debug', action='store_true', help='Debug messages')
options = parser.parse_args()

def debug(*args):
    "Prints all arguments, if the debug option is enable."

    if options.debug:
        print ' '.join(map(str, args))


Random = random.Random()
client = irc.client.IRC()
server = client.server()
channellist = []
hodors = ['Hodor'+x for x in ['.', '...', '?', '!']]

# Default event processor
def process_event(connection, event):
    """
    Prints the parameters of the supplied event: type, arguments, source, and target.
    """
    print "{0}: {1} ({2}->{3})".format(event.type, event.arguments, event.source,
                                       event.target)

def pubmsg_handler(connection, event):
    """
    Randomly reply to the pubmsg with "Hodor".
    """
    text = event.arguments[0].lower()
    if 'hodor' in text:
        user = event.source.split('!')[0]
        connection.action(event.target, 'looks at ' + user)
        connection.privmsg(event.target, Random.choice(hodors))
    if Random.random() < options.probability/100.:
        connection.privmsg(event.target, Random.choice(hodors))

def privmsg_handler(connection, event):
    """
    Replies to private message with a hodor.
    """
    server.privmsg(event.source.split('!')[0], Random.choice(hodors))

def invite_handler(connection, event):
    """
    Joins a channel when invited.
    """
    for i in event.arguments:
        server.join(i)

if options.verbose:
    debug('Registering default handler for all messages')
    for v in irc.events.all:
        client.add_global_handler(v, process_event)
else:
    debug('Registering default handler for protocol messages')
    debug(irc.events.protocol)
    for v in irc.events.protocol:
        client.add_global_handler(v, process_event)

client.add_global_handler('pubmsg', pubmsg_handler)
client.add_global_handler('privmsg', privmsg_handler)
client.add_global_handler('invite', invite_handler)
server.connect(options.server, options.port, options.nick)
client.process_forever()
