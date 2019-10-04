import re
    
def login(email, password):
    check_emailtype(email)
    validate_email(email)
    validate_password(email, password)      
    uid = 1343254
    token = "something..."
    return {"u_id": uid, "token": token}
    pass
     
        
def check_emailtype(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return True
    else:  
        raise ValueError("this is not a valid email format!")
        return 'false'
    pass

        
def validate_email(email):
    #raise ValueError("error!!")
    # This will check if the email actually exists on the server
    # return TRUE if the email exists
    pass


def validate_password(email, password):
    # This will check if the password to the corresponding email is correct
    pass
         
