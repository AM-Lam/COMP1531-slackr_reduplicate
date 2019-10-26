from .search import search
from .auth_register import auth_register
from .access_error import AccessError

def test_search():
    user = auth_register("valid@email.com", "123456", "John", "Doe")

    # find all the matching messages (nothing)
    assert search(user["token"], "hewwo") == []

    # return nothing if the query string is nothing
    assert search(user["token"], "") == []
