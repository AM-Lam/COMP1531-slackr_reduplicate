Write assumptions that you feel you are making in your interpretation of the specification and of the functions provided.

From message_send to user_profile
-Author: Lai Ming(Ann) Lam

-General assumption apply for every function:
    -assume owner of the channel is also an admin of that channel.
    -assume user can join multiple channels.
    -assume a user can be admin in just one channel or multiple channels.
    -assume admin in one channel don't have the same permission in other channels unless they are also an admin in those channels.
    -assume when the user register, first name of the user is the username since there are no username in register function.
    -permission of anyonewho joins the channel is default as 'member' except the owner unless channel_addowner, admin_userpermission_change is implemented.
    -Admin of the slackr is also an admin of any channel under slackr if such a role exists. Same applied to owner.

-Structure of the database(dictionary/list that I use to store the data):
    - assume all type of the ID(eg. u_id, message_id, react_id) is generated and stored in a database in a form of dictionaries or lists if the related function is successfully exercuted.
    -u_id_dic:{u_id: {email, first name, last name, handle}}
    -message_id_dic: {message_id: {token, channel_id}}
    -permission_id_dic: {token: permission} # permission: 'member', 'admin', 'owner'
    -react_type_list: {}
    -react_id_dic: {react_id: {token, message_id, react type}}
    -pinned_dic: {message_id: }

-message_send:
    -assume the message contains any type of characters like space, upper or lower cases, numbers, or ,./<>;':"()_*&^%$#@!~`-+=. 
    -assume characters which excluded in ASCII table cannot be sent such as emoji.
    -assume message_id is unique among slackr. For example, the same number won't be generated even if the same message is sent in different channels.

-message_remove:
    -assume the creator of that message and admin of that channel has the permission to remove messages.
    -assume if the message no long existed means that the message_id is deleted or cannot be found.
    -assume all the message_id is stored in a dictionary called message_id_dic and token and channel_id is stored in the key.
    -assume channel_list can be used to check whether the user is existing in the channel.

-message_edit:
    -assume the creator of that message is the only can edit the message even admin and owner cannot edit the message.

-message_react and message_unreact(applied for both):
    -assume the creator of that message is the only can react or unreact the message even admin and owner cannot (un)react the message.
    -react_id is represented by a react_type_list to check which reaction to pick. 

-message_pin and message_unpin(applied for both):
    -assume every member in the channel can see what message is (un)pinned.
    -assume only admin of the channel have the permission to pin or unpin the message.
    -assume more than one messages can be (un)pin.

-user_profile:
    -assume handle means that the username of the user.
