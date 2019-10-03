import pytest
import user_profile

def test_user_profile(token, u_id):
    assert user_profile(token, u_id) == [{email, name_first, name_last, handle_str}]
    assert user_profile(token, "123") == [{'hayden@gmail.com', 'Hayden', 'Smith', 'handle'}]
    assert user_profile(token, "456") == [{'smith@gmail.com', 'Smith', 'Hayden', 'handler'}]

    # ValueError: User with u_id is not a valid user
    with pytest.raises(ValueError):
        user_profile(token, '10')
        user_profile(token, 'notUser')