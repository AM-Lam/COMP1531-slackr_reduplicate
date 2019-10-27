import pytest
from .database import *
from .auth_passwordreset_request import *
from .auth_register import *


def test_dummy_func():
    clear_data()
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
    ## this should be testing if connection to server was succesful and email was sent successfully! 
    ## can't test this since send email code has been moved to server.py i.e. flask
    pass
