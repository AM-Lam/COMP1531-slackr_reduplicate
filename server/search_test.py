from .search import search
from .auth_register import auth_register
from .access_error import AccessError
from .database import *
import jwt
import pytest

clear_data()


def test_search():
    user = auth_register("valid@email.com", "1234567890", "John", "Doe")

    # find all the matching messages (nothing)
    assert search(user1["token"], "hewwo") == []

    # return nothing if the query string is nothing
    assert search(user["token"], "") == []
