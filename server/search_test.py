import search
token = "hewwo"

def test_search():

    # find all the hewwo messages
    assert search.search(token, "hewwo") == {"hewwo dere"}
