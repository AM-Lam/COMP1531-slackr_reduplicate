def test_user_profile(token, u_id):
    assert user_profile(token, u_id) == []
    # ValueError when:
    #  User with u_id is not a valid user