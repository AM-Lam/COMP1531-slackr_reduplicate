import pytest
import re
from .database import *
from .auth_login import *
from .auth_register import *
from .access_error import *


def test_login():
    clear_data()

    user_1 = auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
    user_2 = auth_register('user2@domain.com' , 'vscod231343' , 'ussr' , 'b')
    user_3 = auth_register('user3@domain.com.au' , 'vsdco23111' , 'person' , 'c')
    
    token = auth_login('user1@domain.com' ,'passew@321')
    
    assert token['token'] is not None
    assert token['u_id'] is not None

    ###########################################################################

    # valid email
    email = "user@gmail.com"
    assert(check_emailtype(email))

    # email has a dot
    email = 'user.ans@gmail.com'
    assert(check_emailtype(email))

    # email has a dot in domain
    email = 'user@subdomain.domain.com'
    assert(check_emailtype(email))

    # domain as an ip
    email = 'email@123.123.123.123'
    assert(check_emailtype(email))

    # email has digits
    email = '1234567890@domain.com'
    assert(check_emailtype(email))

    # dash in domain
    email = 'email@domain-one.com'
    assert(check_emailtype(email))

    # email has underscores
    email = '_______@domain.com'
    assert(check_emailtype(email))

    # top level domain
    email = 'email@domain.co.jp'
    assert(check_emailtype(email))

    # email has dash
    email = 'firstname-lastname@domain.com'
    assert(check_emailtype(email))

    ###########################################################################

    email = "user@.com"
    # pytest.raises(ValueError, auth_login.check_emailtype, email)   
    # no domain name
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # email is garbage
    email = "#@%^%#$@#$@#.com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # no username
    email = "@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # no html allowed
    email = "Joe Smith <email@domain.com>"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # missing @
    email = "email.domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # multiple @'s
    email = "email@domain@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # leading dot
    email = ".email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # trailing dot
    email = "email.@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # multiple dots
    email = "email..email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # multiple dots
    email = "email..email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # follow up text 
    email = "email@domain.com (Joe Smith)"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # no top level domain
    email = "email@domain"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # leading dash in domain
    email = "email@-domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # invalid ip format
    email = "email@111.222.333.44444"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    # multiple dots in domain
    email = "email@domain..com"
    with pytest.raises(ValueError , match=r"*"):
        check_emailtype(email)

    ###########################################################################

    # here we assume that an existing database has logged the information of user1 and user2 created above
    # what if the email does not exist in the database -->
    pytest.raises(ValueError, validate_email, 'INVALIDeMAIL@domain.com')   

    # user forgot to put the .au domain in the address-->
    pytest.raises(ValueError, validate_email, 'user3@student.unsw.edu')
    
    # did the user forget to put the subdomain (i.e. student.unsw....)? -->
    pytest.raises(ValueError, validate_email, 'user3@unsw.edu.au')
    
    # does my function only accept a particular domain? -->
    pytest.raises(ValueError, validate_email, 'user3@gmail.com.au')
    
    # what if the email and password combo is valid? -->
    assert(validate_email('user1@domain.com')) == True
   
    ###########################################################################

    # what if the password does not have Enough characters? -->
    pytest.raises(ValueError, validate_password, 'user1@domain.com' , 'pas31')

    # what if the password field was just left empty> -->
    pytest.raises(ValueError, validate_password, 'user1@domain.com' , '')

    # what is password has a valid length but is incorrect? -->
    pytest.raises(ValueError, validate_password, 'user1@domain.com' , 'passwordisthis')

    # what if the password exists on the server but is not correctly matched to the provided email -->
    pytest.raises(ValueError, validate_password, 'user3@domain.com' , 'sfdsdfsdfsdfsffsf')

    # what if the email and password combo is valid? -->
    dictio = auth_login('user1@domain.com' ,'passew@321')
    assert dictio['token'] is not None
    assert dictio['u_id'] is not None
