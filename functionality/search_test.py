<<<<<<< HEAD:server/search_test.py
from .search import search
from .auth_register import auth_register
from .access_error import AccessError
=======
from .message import search
from .auth import auth_register
>>>>>>> master:functionality/search_test.py
from .database import *
import jwt
import pytest

def test_search():
    clear_data()
    
    user = auth_register("valid@email.com", "1234567890", "John", "Doe")

    # find all the matching messages (nothing)
    assert search(user1["token"], "hewwo") == []

    # return nothing if the query string is nothing
    assert search(user["token"], "") == []
