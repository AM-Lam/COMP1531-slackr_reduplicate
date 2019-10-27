from .auth_passwordreset_request import *
import pytest
from .auth_register import *
from .database import *



auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')

###########################################################################################################################################
def test_Validate_email():
    # what if the email does not exist in the database -->
    pytest.raises(ValueError, validate_email_existence, 'INVALIDeMAIL@domain.com')   
    
def test_Validate_email3():
    # does my function only accept a particular domain? -->
    pytest.raises(ValueError, validate_email_existence, 'user1@domain.com.au')
    
def test_Validate_email4():
    # what if the email and password combo is valid? -->
    assert(validate_email_existence('user1@domain.com')) is not None

###########################################################################################################################################

def test_send_code():
    ## cant test this since send email code has been moved to server.py i.e. flask
    update_data = get_data()
    reset_code = auth_passwordreset_request('user1@domain.com')
    assert(update_data["reset"][reset_code]) == 'user1@domain.com'
    
