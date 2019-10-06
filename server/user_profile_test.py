import pytest
import user_profile

def test_user_profile():
    # assert user_profile(token, u_id) == [{email, name_first, name_last, handle_str}]
    assert user_profile('person1', 123) == {'hayden@gmail.com', 'Hayden', 'Smith', 'handle'}
    assert user_profile('person2', 456) == {'smith@gmail.com', 'Smith', 'Hayden', 'handler'}
    assert user_profile('person3', 789) == {'person@gmail.com', 'one', 'person', '1st'}
    assert user_profile('admin1', 11) == {'admin1@gmail.com', 'one', 'admin', 'admin1'}
    assert user_profile('admin2', 22) == {'admin2@gmail.com', 'two', 'admin', 'admin2'}
    assert user_profile('owner', 159) =={'owner@gmail.com', 'Owner', 'UNSW', 'handler'}

    # ValueError: User with u_id is not a valid user
    with pytest.raises(ValueError):
        #unmatching token and u_id
        user_profile('person1', 465)
        user_profile('person3', 789)
        user_profile('person1', 22)
        user_profile('person2', 22)
        user_profile('admin1', 123)
        user_profile('admin2', 11)

        # typo or wrong token
        user_profile('Person1', 123)
        user_profile('oner', 159)
        user_profile('peraon3', 789)
        user_profile('person', 22)


