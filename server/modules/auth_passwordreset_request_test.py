import auth_passwordreset_request
import pytest
import auth_register
import auth_login


auth_register.auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')

###########################################################################################################################################
def test_Validate_email():
    # what if the email does not exist in the database -->
    pytest.raises(ValueError, auth_passwordreset_request.validate_email_existence, 'INVALIDeMAIL@domain.com')   

def test_Validate_email1():
    # user forgot to put the .au domain in the address-->
    pytest.raises(ValueError, auth_login.validate_email, 'user3@student.unsw.edu')
    
def test_Validate_email2():
    # did the user forget to put the subdomain (i.e. student.unsw....)? -->
    pytest.raises(ValueError, auth_login.validate_email, 'user3@unsw.edu.au')
    
def test_Validate_email3():
    # does my function only accept a particular domain? -->
    pytest.raises(ValueError, auth_login.validate_email, 'user3@gmail.com.au')
    
def test_Validate_email4():
    # what if the email and password combo is valid? -->
    assert(auth_login.validate_email('user1@domain.com'))

###########################################################################################################################################

def test_send_code():
    ## this should be testing if connection to server was succesful and email was sent successfully! 
    pass
