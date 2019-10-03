# token = generateToken('hayden@gmail.com', '123456', 'Hayden', 'Smith')
# channel_id = generateChannel(token, "Channel 1", True)
# message_id = generateMessage(token, channel_id, message)

class AccessError(Exception): 
    pass
    
def auth_register(email, password, firstN, lastN):
    return {"123456": 1, "token": 123456}

def channel_create(token, name, is_public):
    return {"123456": 3, "channel_id": 123456}

def generateToken(email, password, firstN, lastN):
    # Hayden's video on Testing Help https://youtu.be/1WePByrzU5I
    authRegisterDic = auth_register(email, password, firstN, lastN)
    token = authRegisterDic['token']
    return token
    
def generateChannel(token, name, is_public):
    channelCreateDic = channel_create(token, name, is_public)
    channelId = channelCreateDic['channel_id']
    return channelId


