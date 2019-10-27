import pytest
from .auth_register import *
from .database import *
from .access_error import *


def test_run_all():
    clear_data()

    # assuming user1 currently does not exist
    token = auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
    assert token['token'] is not None
    assert token['u_id'] is not None

    ###########################################################################

    # valid email
    email = "user@gmail.com"
    assert(check_regEmailtype(email))

    # email has a dot
    email = 'user.ans@gmail.com'
    assert(check_regEmailtype(email))

    # email has a dot in domain
    email = 'user@subdomain.domain.com'
    assert(check_regEmailtype(email))
        
    # domain as an ip
    email = 'email@123.123.123.123'
    assert(check_regEmailtype(email))

    # email has digits
    email = '1234567890@domain.com'
    assert(check_regEmailtype(email))

    # dash in domain
    email = 'email@domain-one.com'
    assert(check_regEmailtype(email))

    # email has underscores
    email = '_______@domain.com'
    assert(check_regEmailtype(email))

    # top level domain
    email = 'email@domain.co.jp'
    assert(check_regEmailtype(email))

    # email has dash
    email = 'firstname-lastname@domain.com'
    assert(check_regEmailtype(email))

    ########################################################################### 
    
    email = "user@.com"
    # pytest.raises(ValueError, auth_login.check_emailtype, email)   
    # no domain name
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # email is garbage
    email = "#@%^%#$@#$@#.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # no username
    email = "@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # missing @
    email = "email.domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # multiple @'s
    email = "email@domain@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # leading dot
    email = ".email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # trailing dot
    email = "email.@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # multiple dots
    email = "email..email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # multiple dots
    email = "email..email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # follow up text 
    email = "email@domain.com (Joe Smith)"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # no top level domain
    email = "email@domain"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # leading dash in domain
    email = "email@-domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # invalid ip format
    email = "email@111.222.333.44444"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    # multiple dots in domain
    email = "email@domain..com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

    ###########################################################################

    # for this validate case if the email does not exist the pass!!!
    # what if the email does not exist?
    
    # here we assume that an existing database has logged the information of 
    # user1 and user2 created above
    data = get_data()
    assert(validate_regEmail('invalid@gmail.com')) == True 

    # what if the email does exist?
    data = get_data()
    pytest.raises(ValueError, validate_regEmail, 'user1@gmail.com')
        
    ###########################################################################

    assert(check_first("arpit"))

    pytest.raises(ValueError, check_first, 'udnfbhsbdfhbsdhjbfhjsdbfhjsdbfhjsbfhjbshjfbjhfshdbsdbfhjsdbfjhdsbfjhsdbfjhsbfjsbfjhdsbfjhsdbfhj')

    ###########################################################################

    assert(check_last("arpit"))

    pytest.raises(ValueError, check_last, 'udnfbhsbdfhbsdhjbfhjsdbfhjsdbfhjsbfhjbshjfbjhfshdbsdbfhjsdbfjhdsbfjhsdbfjhsbfjsbfjhdsbfjhsdbfhj')

    ###########################################################################

    assert(check_password_strength("sdfadffsfsfeasdadew"))

    pytest.raises(ValueError, check_password_strength, 'pew')
