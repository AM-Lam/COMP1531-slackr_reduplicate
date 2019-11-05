import pytest
from .auth import auth_register
from .database import clear_data
from .access_error import AccessError, ValueError


def test_run_all():
    clear_data()

    # assuming user1 currently does not exist
    token = auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
    assert token['token'] is not None
    assert token['u_id'] is not None
