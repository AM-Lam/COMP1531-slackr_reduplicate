Write assumptions that you feel you are making in your interpretation of the specification and of the functions provided.

Author: Lai Ming(Ann) Lam
I assume owner of the channel is also an admin.
I assume permission_id, message_id or react_id is generated and stored in a database if the related function is successfully exercuted.
For message_send, I assume that the message can contain any type of characters like space, upper or lower cases, numbers, or ,./<>;':"()_*&^%$#@!~`-+=. 
For message_remove, I assume the creator of that message and admin can remove the messages. 
For message_remove/edit, I assume the AccessError is targeted at different situations such as the identity of user and admin causing different error.
For message_edit/(un)react, I assume the creator of that message is the only can edit the message.
For message_pin, I assume every member in the channel can see what message is pinned.
For message_(un)pin, I assume the admin is the only can pin or unpin the message.
For message_(un)pin, I assume more than one messages can be pin.
For user_profile, I assume I can get the details of email, name(first and last) and handle which are valid from u_id.
For user_profile, I assume handle means that .
