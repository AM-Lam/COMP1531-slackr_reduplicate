import pytest
import re
from .database import clear_data
from .auth import auth_login, auth_register
from .access_error import AccessError, Value_Error

def test_login():
    clear_data()

    user_1 = auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user_2 = auth_register('user2@domain.com' , 'vscod231343' , 'ussr' , 'b')
    user_3 = auth_register('user3@domain.com.au' , 'vsdco23111' , 'person' , 'c')

    assert user_1 is not None
    assert user_2 is not None
    assert user_3 is not None
    
    token = auth_login('user1@domain.com' ,'passew@321')
    
    assert token['token'] is not None
    assert token['u_id'] is not None

    ###########################################################################

    # what if the email and password combo is valid? -->
    dictio = auth_login('user1@domain.com' ,'passew@321')
    assert dictio['token'] is not None
    assert dictio['u_id'] is not None
