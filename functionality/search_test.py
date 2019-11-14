import pytest
from .search import search
from .auth import auth_register
from .database import clear_data
from .access_error import *

def test_search():
    clear_data()
    
    user = auth_register("valid@email.com", "1234567890", "John", "Doe")

    # find all the matching messages (nothing)
    assert search(user1["token"], "hewwo") == []

    # return nothing if the query string is nothing
    assert search(user["token"], "") == []
