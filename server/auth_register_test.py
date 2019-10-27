import pytest
from .auth_register import *
from .database import *


clear_data()


def test_successfulRegister():
    # assuming user1 currently does not exist
    token = auth_register('user1@gmail.com' ,'passew@321', 'user', 'one')
    assert token['token'] is not None
    assert token['u_id'] is not None

###################################################################################

def test_regEmailtype_good():
    # valid email
    email = "user@gmail.com"
    assert(check_regEmailtype(email))

def test_regEmailtype_good1():
    # email has a dot
    email = 'user.ans@gmail.com'
    assert(check_regEmailtype(email))

def test_regEmailtype_good2():
    # email has a dot in domain
    email = 'user@subdomain.domain.com'
    assert(check_regEmailtype(email))
    
def test_regEmailtype_good4():
    # domain as an ip
    email = 'email@123.123.123.123'
    assert(check_regEmailtype(email))

def test_regEmailtype_good7():
    # email has digits
    email = '1234567890@domain.com'
    assert(check_regEmailtype(email))

def test_regEmailtype_good8():
    # dash in domain
    email = 'email@domain-one.com'
    assert(check_regEmailtype(email))

def test_regEmailtype_good9():
    # email has underscores
    email = '_______@domain.com'
    assert(check_regEmailtype(email))

def test_regEmailtype_good11():
    # top level domain
    email = 'email@domain.co.jp'
    assert(check_regEmailtype(email))

def test_regEmailtype_good12():
    # email has dash
    email = 'firstname-lastname@domain.com'
    assert(check_regEmailtype(email))

###########################################################################################################

def test_regEmailtype_bad1():
    email = "user@.com"
    # pytest.raises(ValueError, auth_login.check_emailtype, email)   
    # no domain name
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad3():
    # email is garbage
    email = "#@%^%#$@#$@#.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad4():
    # no username
    email = "@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad6():
    # missing @
    email = "email.domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad7():
    # multiple @'s
    email = "email@domain@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad8():
    # leading dot
    email = ".email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad9():
    # trailing dot
    email = "email.@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad10():
    # multiple dots
    email = "email..email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad11():
    # multiple dots
    email = "email..email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad12():
    # follow up text 
    email = "email@domain.com (Joe Smith)"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad13():
    # no top level domain
    email = "email@domain"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad14():
    # leading dash in domain
    email = "email@-domain.com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad16():
    # invalid ip format
    email = "email@111.222.333.44444"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

def test_regEmailtype_bad17():
    # multiple dots in domain
    email = "email@domain..com"
    with pytest.raises(ValueError , match=r"*"):
        check_regEmailtype(email)

########################################################################################################################################################################

# for this validate case if the email does not exist the pass!!!
# what if the email does not exist?
def test_regvalidate_email():
    # here we assume that an existing database has logged the information of user1 and user2 created above
    data = get_data()
    assert(validate_regEmail('invalid@gmail.com')) == True 

def test_regvalidate_email1():
    # what if the email does exist?
    data = get_data()
    pytest.raises(ValueError, validate_regEmail, 'user1@gmail.com')
    
###################################################################################################################################################################

def test_check_first():
    assert(check_first("arpit"))

def test_check_first2():
    pytest.raises(ValueError, check_first, 'udnfbhsbdfhbsdhjbfhjsdbfhjsdbfhjsbfhjbshjfbjhfshdbsdbfhjsdbfjhdsbfjhsdbfjhsbfjsbfjhdsbfjhsdbfhj')

########################################################################################################################################################################

def test_check_last():
    assert(check_last("arpit"))

def test_check_last2():
    pytest.raises(ValueError, check_last, 'udnfbhsbdfhbsdhjbfhjsdbfhjsdbfhjsbfhjbshjfbjhfshdbsdbfhjsdbfjhdsbfjhsdbfjhsbfjsbfjhdsbfjhsdbfhj')

#########################################################################################################################################################################

def test_password_strength():
    assert(check_password_strength("sdfadffsfsfeasdadew"))

def test_password_strength1():
    pytest.raises(ValueError, check_password_strength, 'pew')
