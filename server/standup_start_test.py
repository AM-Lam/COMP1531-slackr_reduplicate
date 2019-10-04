import standup_start
import pytest
token = "hewwo"

def test_standup_start():
    # returns a ValueError if the channel doesn't exist
    pytest.raises(ValueError, standup_start.standup_start, token, not_a_real_channel)

    # returns an AccessError if the user does not have perms
    pytest.raises(AccessError, standup_start.standup_start, token, real_channel)
