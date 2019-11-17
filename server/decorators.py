# pylint: disable=C0114

from .database import clear_data
from .channel import channels_create
from .auth import auth_register


def setup_data(user_num=0, channel_num=0, creators=None, public=None):
    """
    Decorator that sets up data for use in testing. Takes a number of
    users and channels to create and gives them generic names ("user1",
    "user2", etc.).

    By default all channels are created as public channels. To make
    channels private you must provide a list to the public argument in
    the form [a1, a2, ..., an] for all n channels where each element is
    True (for public channels) or False (for private channels).

    Similarly by default channels are created by the first user created
    to specify a creator provide a list to the creators keyword
    argument of the form [a1, a2, ... an] for all n channels where each
    number is the user who created the channel. (Indexing begins at 0 so
    if a channel is created by the second user created you would supply
    1).
    """

    def decorator(function):
        def wrapper():
            clear_data()

            creator_order = []
            public_order = []

            if creators is None:
                creator_order = [0] * channel_num
            else:
                creator_order = creators

            if public is None:
                public_order = [True] * channel_num
            else:
                public_order = public

            users = {}
            channels = {}

            for i in range(user_num):
                first = f'user{i + 1}'
                last = f'last{i + 1}'
                email = f'{first}@valid.com'
                password = f"{i + 1}" * 6

                users[i] = auth_register(email, password, first, last)

            for i in range(channel_num):
                channels[i] = channels_create(users[creator_order[i]]["token"],
                                              f"Channel {i + 1}",
                                              public_order[i])

            return function(users, channels)
        return wrapper
    return decorator
