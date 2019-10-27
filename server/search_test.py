from .search import search
from .auth_register import auth_register
from .access_error import AccessError
from .database import *
import jwt
import pytest

def test_search():
    secret = get_secret()
    user1 = {
        "token" : jwt.encode({"u_id" : "111"}, secret, algorithm="HS256"),
        "u_id" : "111"
    }

    user2 = {
        "token" : jwt.encode({"u_id" : "112"}, secret, algorithm="HS256"),
        "u_id" : "112"
    }

    user3 = {
        "token" : jwt.encode({"u_id" : "113"}, secret, algorithm="HS256"),
        "u_id" : "113"
    }

    channel1 = channels_create(user1["token"], "Channel 1", True)
    channel2 = channels_create(user1["token"], "Channel 2", True)

    # find all the matching messages (nothing)
    assert search(user1["token"], "hewwo") == []

    # return nothing if the query string is nothing
    assert search(user["token"], "") == []
