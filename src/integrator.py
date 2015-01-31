__author__ = 'dibyo'

from datetime import datetime as dt, timezone


class Message(object):
    """
    Data arrives as a set of messages.  This defines the message
    interface.
    """
    def __init__(self, message):
        self.message = message
        self.timestamp = dt.now(tz=timezone.utc)

    def __eq__(self, other: Message):
        """
        Two messages are equal if they have the same message
        :param other: the other message to be considered
        :return:
        """
        return self.message == other.message


