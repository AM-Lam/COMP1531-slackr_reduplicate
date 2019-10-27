import pytest
from .auth_passwordreset_request import *
from .auth_register import *
from .database import *
from .access_error import *


def test_request_test():
    clear_data()
    auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')


    ###########################################################################
    # what if the email does not exist in the database -->
    pytest.raises(ValueError, validate_email_existence, 'INVALIDeMAIL@domain.com')   
    
    # does my function only accept a particular domain? -->
    pytest.raises(ValueError, validate_email_existence, 'user1@domain.com.au')
    
    # what if the email and password combo is valid? -->
    assert(validate_email_existence('user1@domain.com')) is not None

    ###########################################################################

    ## cant test this since send email code has been moved to server.py i.e. flask
    update_data = get_data()
    reset_code = auth_passwordreset_request('user1@domain.com')
    assert(update_data["reset"][reset_code]) == 'user1@domain.com'
    
