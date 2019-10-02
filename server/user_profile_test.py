import pytest
import user_profile

def test_user_profile(token, u_id):
    assert user_profile(token, u_id) == [{ email, name_first, name_last, handle_str }]
    # ValueError: User with u_id is not a valid user
    pytest.raises(ValueError, user_profile, 1, 10)