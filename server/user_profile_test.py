import pytest
import user_profile

def test_user_profile(token, u_id):
    # assert user_profile(token, u_id) == [{email, name_first, name_last, handle_str}]
    assert user_profile('123', '123') == [{'hayden@gmail.com', 'Hayden', 'Smith', 'handle'}]
    assert user_profile('456', '456') == [{'smith@gmail.com', 'Smith', 'Hayden', 'handler'}]

    # ValueError: User with u_id is not a valid user
    with pytest.raises(ValueError):
        user_profile('123', '10')
        user_profile('123', 'notUser')

    with pytest.raises(Error):
        user_profile('123', '456')
        user_profile('123', '789')