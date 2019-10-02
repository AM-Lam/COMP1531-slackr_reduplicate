def test_user_profile(token, u_id):
    assert user_profile(token, u_id) == [{ email, name_first, name_last, handle_str }]
    # ValueError when:
    #  User with u_id is not a valid user