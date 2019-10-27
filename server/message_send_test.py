import pytest
import jwt
from .database import *
from .access_error import *
from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send

def verify_message(message_obj, correct_data):
    if message_obj == correct_data:
        return True
    return False

def test_message_send():
    clear_data()
    
    user1 = auth_register("valid@email.com", "1234567890", "Bob", "Jones")
    user2 = auth_register("valid2@email.com", "0123456789", "John", "Bobs")
    user3 = auth_register("valid3@email.com", "0987654321", "Bob", "Zones")
    
    channel_id = channels_create(user1["token"], "Channel 1", True)

    # try to create a valid message
    message_1 = message_send(user1["token"], channel_id["channel_id"], "Hello")

    # check that the channel exists
    assert message_1 is not None

    # check that the database was correctly updated
    assert verify_message(message_1, {"message_id" : 1}) 
    
    # the user is not a member in the group
    pytest.raises(AccessError, message_send, user3["token"], channel_id["channel_id"], "Hello")

    # reset message_1
    message_1 = None
    # the message is over 1000 characters
    pytest.raises(ValueError, message_send, user1["token"], channel_id["channel_id"],
                 "X" * 1001)


# def test_message_send(token, channel_id, message):
#     #basic cases
#     assert message_send('person1', 1, 'a') == None
#     assert message_send('person1', 1, 'hello') == None
#     assert message_send('admin2', 3, '1233456789') == None
#     #case with 1000 characters
#     assert message_send('person1', 2, 'GKREgW2twKzcZ9wMe3zMsl0yf8OJfYOAB9I9DWd81pIPRmlq7v1p5j1tfifWu8kcoXkG1wu0qLK7xfhHlJUg12YxrvsZazEw4CPF6qfoUsmulUau3XqWwLBLrq3j0gHMGlfW6LqDvdmvx9ppAtN8lDrEIJdeZavF6McKw5O9ldYLKPuwZYfFgHRgcSCNZ9y4A6TSTvF16P1PrE6msit1ESzv9BEPzc9Undl23zq29ZQ9amTuE1lyTG16nftJHD5MgAZpm5bKny9Tsmjj0gNaUIitNjl9d310pu2cM6XU5aLRPfAQmibhmx9PfGpf571jIbVQEVKcp5fC1AtTLxXoVfrRWv3LTWdcf3dZaRQvQeXADCTpgQY0oCo69GmxSzbg4Fl0aXxVOrWI8MlPXijo6JTgvwcy8QGxd8AfZ7QFe3EOtYYUL3MJ3EQLQIaXNeRXTeUQ2MBoHeMRRTxfdHu3dcz9Zb5DDn5N79NaN4rW83jcckHEVQ88S76cSxJdUOarmFT2eHf0kH7NiJAv2E1srrP3fAUJOZvkf3z6ADvzXt0apl2IlsC34NY8MRkWJhIVQOUep8qxejZDLlVIQOoXkhGZK8Fk13wQlFBkqzrZYVEUefWLFPG78OeSk539JY1emF8iNhWV7Z7Jb6Z9KM40GtdvBXGIKqPvT1SG9mKgnXeO115bDzlBeGqJQWS9GSpN5kYrl1EnLYAan9Int0tF0rdCTgQtsUTSfvHfZEJc08K4IZzaqaDWs3ywwvX3f9KakSV2rgQFx5PUXAtm31tEy3Hki00bd42fcvuAIYJFf2NHaz9exbwOqvKQHWFEWVgIRRL5uK8vnAeddJbgH7M9UNGefaYTZAGE2T3PMrTKlryw68g6aVKjDyxOam3yjrQsKvVTkoOFCrKvAzKFughZumB2XHXw8dsflbgpGxxY5kxcsCIpa5WSGmjLL8cTWIbjhUC585zVVRY3FHyR6oQhkCYxhvgaEuvT4CQCiCff') == None
#     #case with special characters
#     assert message_send('person2', 3, 'ajklfn89ru34nfv&*&#@)$)')
#     #case with only space
#     assert message_send('admin1', 1, '    ') == None   

#     # Message is more than 1000 characters
#     with pytest.raises(ValueError):
#         message_send(token, channel_id, 'bfiDw25miCyBvrwSfYWVRTSdunVfTxzWRfkYrvOztvF3BrtCHbXWoIKPbpBhYdQsWf7TTWQ5Z0cKmBBygwVRAyS9Yt6YBtitWYQDVVVembsy7izJMjuVk611l7NmxPWXw8w8pk7EtKHq1464icy6z5qcnG6cSALJUT86hU2tXG3redpcINHEG9BaNTqgngUSGNENIVkD9mzYRFeChjq7CBwZVP7G0yCYxn3M3VSgUIyFbQElRGkKtX7KWvg9FxlFXnld8ScXaTE27i8zT4FqZMf8j45wVYZOJLRpOnX1JaDvfvpMfG5ybCleIQYe9GADEzcP7RxBcs7EaIqSRmpXOZl3kyJDdYubEttcR9rrulQo3dJMzPa3WnaosCByZCEeO3rqHqryXcpwlB8Z5ztYGJ8fiRDMgwloBjjAZyHPU6CTd76zFRXPyywnjzQhmsBVHQ6qjyNQODV9j2mLejkCVjFXgVYbOfQnSQZALo7PDkB4BEQDJWY4GVtG7FfhhGM9YsolHDWzQnGkFjvPfLgI1rXNsacFr2jbb5qv7C8nCnE63BDroyI0UjR0iQqFuNIuJI2pxuibdxZcsifRFjhf3j86Ya03mSBBxoULl8o9mOZx60nYalsQcBGd56qavrrLIqxWB6KOhLoFhSwOyZCc4bU3s4UX8oN0s9BXaeAM7S6dyLbI8qA6OKJFHmpUielq6dlaaSXHOZMmOgG5K6lmpUvaxc9vz0AUmgWTo8ENHv1iHFoqEDgWsjbziBkRaxxCCnyoE6qg00OvNxerVNLQgEYYVj9TBeEPbXlDCQSvx50RAEbE8PxRsf9Fp0ZvdqXcyOr3ZtZ6X20afRnkZx8bcll7UF7LKBJl3BFrRGcpKoT5rUpAEifG3tMNB1jANgrJSbdkh4fwkCRfX1n52VyO9xnXTqijFmr1zMg01SpuSRTcqu901OA4kOQZzh0iQk1baCQDEOrFtDSuSLtXTYXl6nS5upAK0v8AnRxtlsdflhyge')
#         message_send(token, channel_id, 'G52rsuj79i5O9Nmcwny5BTYevH0GVafA18aJqUEHGmEg9peEghkzR8NnoFPPevmr5AV1LgjD46aKiZ2t8rVMNtqOcSOFh4iirvv2FPsU0y5kuYBcSCDFuZvLL51w6ZOY0nsKgfHfBR1tIcn0ihhV3mxGVsB5xqURJ3R8Ou87sCYCAp8rGcWQwxt7yefUCLFCFQa8jWRnJxkU0i8FTmqJLOe98GNEDADqCWbQoBGAemAu0F7CquUTAvVj1JUJeCaw2u1YRXetWxQdgGORpYWfFwRNn2ouv7ogFpXeYTBFd76BnnkJXeie5aBunniPytzA9mL5ovWe01twLKH1BgsiPnQlrOcOhraBDWtk9YlfBfZLi9VuGCzfONLIAearjSCsIoYjpJYnem7zsCUZNhxQrDjDKm4fddnvsN3iSqlddlNFbd9UrkriZFZg9AzQYMxIKOqeuC24lRmoOZT9gSK0SKEh36g1Sx8brIE3EW58tIW0fUrPZZHnxKRArjsZWBTma9uySZwXqJeVkC3tQz0uFOuqP064dDtc9a7huPSk82tRgzj4vAuBiyJEAhES0zBqk0U3N6SaEXBFXEvSOAvfrBhzPr0kmutGwEyMIdSMBGtJamwBmUiTxszGwTNcFbm2G8Q5WfUmLOtDwO6HAu3dMmdSAQkKVM58hsHv5mszaQIAVTNF4d0bblTX2AIdj6NU4wTofJwLY2VhdrOj0rg9jlQFrDSEs3buDesPTFmk0LQ106Q5HP4EIlxLoOAm1fh4AztwbiX7wzyl1jmHoFV9h5jxe6Bk4zVIzoDAPgqPlt76IffJF3cb4FS9kX9FKggmniOK04km80Lil3aCHtVufYbDJWPZ5hAy7V9GJwQd3b4xmL61jjid4o3y0YH7YItI6bGomq1Wset6JrmzRwEu5WdCXh1uWwd9QFZu1CWxUy6nBygFVPSQzgEIpxm4fFiO7GD8GEcLNKlSSTo1Id13wQx2zWu3SqXB2EHcsoXS0')

#     # poster is not a member of the channel
#     assert message_send('person1', 3, 'abs') == None
#     assert message_send('person2', 1, '132456') == None
#     assert message_send('admin1', 3, 'aanjfnajd22*') == None
#     assert message_send('admin2', 1, 'rerarga') == None    
