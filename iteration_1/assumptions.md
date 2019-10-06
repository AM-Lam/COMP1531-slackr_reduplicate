Write assumptions that you feel you are making in your interpretation of the specification and of the functions provided.

From message_send to user_profile
-Author: Lai Ming(Ann) Lam

-General assumption apply for every function:
    -assuming  slackr is a platform to improve communciation between stakeholders in the university course. Therefore, professors, tutors and students will use slackr to communicate especially when the course will involve teamwork. In this way, we won't have to use our personal account to communciate and can make sure students that are in a team would be able to get a hold with each others.

    -assume all the given token is valid and is a member of at least one channel
    -assume owner of the channel is also an admin of that channel.
    -assume user can join multiple channels.
    -assume a user can be admin in just one channel or multiple channels.
    -assume admin in one channel don't have the same permission in other channels unless they are also an admin in those channels.
    -assume when the user register, first name of the user is the username since there are no username in register function.
    -assume permission of anyonewho joins the channel is default as 'member' except the owner unless channel_addowner, admin_userpermission_change is implemented.
    -assume Admin of the slackr is also an admin of any channel under slackr if such a role exists. Same applied to owner.
    -assume all the id is unique among slackr. For example, the same number won't be generated in the same list even if the same type of function is executed. For example same message is generated in different channels the message_id will be different and will only be used in the original post. There are no same message_id in the message_id_list twice.
    -assume the same id number can appear in different type of id such as '1' can be a channel_id and also a u_id.

-Structure of the database(dictionary/list that I use to store the data):
    - assume all type of the ID(eg. u_id, message_id, react_id) is generated and stored in a database in a form of dictionaries or lists if the related function is successfully exercuted.
    # Record of all successful register user
    -u_id_list:{token: u_id}
    -u_id_dic:{u_id: {email, first name, last name, handle}}
    # message_id_list = {message_id: message}
    -message_id_dic: {message_id: {token, channel_id}}
    -permission_id_list: {1, 2, 3} # permission: 'owner', 'admin', 'member'
    #Based on different channels user have different permission
    -permission_id_dic = {token: {channel_id: permission_id}}
    # keep track of the existing channels in the slackr
    -channel_id_dic: {channel_id: channel name} # eg.{1: channel1, 2: channel2,...}
    # keep track of the valid react that can be used in the slackr
    -react_type_list: {react_id} # eg.{like,love, smile}
    -react_id_dic: {react_id: {token, message_id, react type}}
    -pinned_list: {message_id}

-message_send:
    -assume the message contains any type of characters like space, upper or lower cases, numbers, or ,./<>;':"()_*&^%$#@!~`-+=. 
    -assume characters which excluded in ASCII table cannot be sent such as emoji.

-message_remove:
    -assume the poster of that message and admin of that channel has the permission to remove messages.
    -assume if the message no long existed means that the message_id is deleted or cannot be found.
    -assume all the message_id is stored in a dictionary called message_id_dic and token and channel_id is stored in the key.
    -assume channel_list can be used to check whether the user is existing in the channel.

-message_edit:
    -assume the poster of that message is the only can edit the message even admin and owner cannot edit the message.
    -assume authorised user is the one having a valid account in slackr

-message_react and message_unreact(applied for both):
    -assume the poster of that message is the only can react or unreact the message even admin and owner cannot (un)react the message.
    -react_id is represented by a react_type_list to check which reaction to pick. 

-message_pin and message_unpin(applied for both):
    -assume admin can pin on any message that they see
    -assume every member in the channel can see what message is (un)pinned.
    -assume only admin of the channel have the permission to pin or unpin the message.
    -assume more than one messages can be (un)pin.

-user_profile:
    -assume handle means that the username of the user.
