Write assumptions that you feel you are making in your interpretation of the specification and of the functions provided.

Author: Lai Ming(Ann) Lam
I assume owner of the channel is also an admin.
I assume permission_id, message_id or react_id is generated and stored in a database if the related function is successfully exercuted.
For message_send, I assume that the message can contain any type of characters like space, upper or lower cases, numbers, or ,./<>;':"()_*&^%$#@!~`-+=. 
For message_send, I assume that only characters can be sent.
For message_send, I assume that message_id will only be used once, which means it is unique among slackr. For example, the same number won't be generated even if the message is sent in different channel.
For message_remove, I assume the creator of that message and admin can remove the messages. 
For message_remove/edit, I assume the error is targeted at different situations such as the identity of user and admin causing different error.
For message_remove, I assume that message no long existed means that the message_id is deleted, which means someone execute the remove operation before.
For message_remove, I assume I can use token to detect whether the user is the one create the text.
For message_remove, I assume all the message_id is stored in a dictionary called message_id_dic and token and channel_id is stored in the key.
For message_remove, I assume channel_details can be used to check whether the user is existing in the channel.
For message_remove, I assume permission_id is stored in a dictionary as key is the token and value is permission of the owner of token.
For message_edit/(un)react, I assume the creator of that message is the only can edit the message even admin and owner cannot edit the message.
For message_react/(unreact), I assume I can get the list of channels that the user's joining by getting u_id's dictionary. 
For message_react/(unreact), I assume the channel that the message posted in can be found in message_id's dictionary. 
For message_react/(unreact), I assume the react_id is store in a dictionary with the information of token, message_id and the react type . 
For message_react/(unreact), I assume react_id is represented by a react_id_type to check which reaction to pick. 
For message_react/(unreact), I assume the pinned messages are keeping track in a dictionary. 
For message_pin, I assume every member in the channel can see what message is pinned.
For message_(un)pin, I assume the admin is the only can pin or unpin the message.
For message_(un)pin, I assume more than one messages can be pin.
For user_profile, I assume I can get the details of email, name(first and last) and handle which are valid from u_id.
For user_profile, I assume handle means that the username of the user.

I assume when the user register, first name of the user is the username.
I assume permission_id of anyone is 'member' except the owner or channel_addowner, admin_userpermission_change is implemented.
I assume admin of the slackr is also an admin of any channel under slackr. Same applied to owner.
I assume user can join in multiple channels.