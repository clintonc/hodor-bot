hodor-bot
=========

Hodor meets IRC.

This program implements a funny little chatbot which says, under
certain conditions, "Hodor."  It serves as a simple example of an IRC
bot in python:

* It joins channels when invited
* It replies to private messages
* It (intermittently) speaks in channels when others are speaking
* It also conveniently presents protocol information on stdout.

Requires the irc package, obtainable by typing

    pip install irc

