import pytest
import re
import auth_login
import auth_register

user_1 = auth_register.auth_register('user1@domain.com' , 'passew@321' , 'user' , 'a')
#user_2 = auth_register.register('user2@domain.com' , 'vscod231343' 'ussr' , 'b')
#user_3 = auth_register.register('user3@domain.com.au' , 'vsdco23111' 'person' , 'c')

def test_successfulLogin():
    token = auth_login.auth_login('user1@gmail.com' ,'passew@321')
    assert token['token'] is not None
    assert token['u_id'] is not None

###########################################################################################################

def test_check_emailtype_good():
    # valid email
    email = "user@gmail.com"
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good1():
    # email has a dot
    email = 'user.ans@gmail.com'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good2():
    # email has a dot in domain
    email = 'user@subdomain.domain.com'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good3(): ######################
    # email id has a plus
    email = 'firstname+lastname@domain.com'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good4():
    # domain as an ip
    email = 'email@123.123.123.123'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good5(): #######################
    # domain as an [ip]
    email = 'email@[123.123.123.123]'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good6(): #######################
    # email has quotes
    email = '"email"@domain.com'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good7():
    # email has digits
    email = '1234567890@domain.com'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good8():
    # dash in domain
    email = 'email@domain-one.com'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good9():
    # email has underscores
    email = '_______@domain.com'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good10(): ########################
    # .name in domain
    email = 'email@domain.name'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good11():
    # top level domain
    email = 'email@domain.co.jp'
    assert(auth_login.check_emailtype(email))

def test_check_emailtype_good12():
    # email has dash
    email = 'firstname-lastname@domain.com'
    assert(auth_login.check_emailtype(email))

###########################################################################################################


def test_check_emailtype_bad():
    # email not a string
    email = 1324
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)
    
def test_check_emailtype_bad1():
    email = "user@.com"
    # pytest.raises(ValueError, auth_login.check_emailtype, email)   
    # no domain name
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad3():
    # email is garbage
    email = "#@%^%#$@#$@#.com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad4():
    # no username
    email = "@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad5():
    # no html allowed
    email = "Joe Smith <email@domain.com>"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad6():
    # missing @
    email = "email.domain.com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad7():
    # multiple @'s
    email = "email@domain@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad8():
    # leading dot
    email = ".email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad9():
    # trailing dot
    email = "email.@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad10():
    # multiple dots
    email = "email..email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad11():
    # multiple dots
    email = "email..email@domain.com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad12():
    # follow up text 
    email = "email@domain.com (Joe Smith)"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad13():
    # no top level domain
    email = "email@domain"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad14():
    # leading dash in domain
    email = "email@-domain.com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad15():
    # .web is not a leading top level domain
    email = "email@domain.web"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad16():
    # invalid ip format
    email = "email@111.222.333.44444"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

def test_check_emailtype_bad17():
    # multiple dots in domain
    email = "email@domain..com"
    with pytest.raises(ValueError , match=r"*"):
        auth_login.check_emailtype(email)

###########################################################################################################

def test_validate_email():
    # here we assume that an existing database has logged the information of user1 and user2 created above
    # what if the email does not exist in the database -->
    pytest.raises(ValueError, auth_login.validate_email, 'INVALIDeMAIL@domain.com')   

def test_validate_email1():
    # user forgot to put the .au domain in the address-->
    pytest.raises(ValueError, auth_login.validate_email, 'user3@student.unsw.edu')
    
def test_validate_email2():
    # did the user forget to put the subdomain (i.e. student.unsw....)? -->
    pytest.raises(ValueError, auth_login.validate_email, 'user3@unsw.edu.au')
    
def test_validate_email3():
    # does my function only accept a particular domain? -->
    pytest.raises(ValueError, auth_login.validate_email, 'user3@gmail.com.au')
    
def test_validate_email4():
    # what if the email and password combo is valid? -->
    assert(auth_login.validate_email('user1@domain.com'))
   
############################################################################################################

def test_validate_password():
    # what if the password does not have Enough characters? -->
    pytest.raises(ValueError, auth_login.validate_password, 'user1@domain.com' , 'pas31')

def test_validate_password1():
    # what if the password field was just left empty> -->
    pytest.raises(ValueError, auth_login.validate_password, 'user1@domain.com' , '')

def test_validate_password2():
    # what is password has a valid length but is incorrect? -->
    pytest.raises(ValueError, auth_login.validate_password, 'user1@domain.com' , 'passwordisthis')

def test_validate_password3():
    # what if the password exists on the server but is not correctly matched to the provided email -->
    pytest.raises(ValueError, auth_login.validate_password, 'user1@domain.com' , 'vscod231343')

def test_validate_password4():
    # what if the email and password combo is valid? -->
    dictio = auth_login.auth_login('user1@domain.com' ,'passew@321')
    assert dictio['token'] is not None
    assert dictio['u_id'] is not None
    
    

