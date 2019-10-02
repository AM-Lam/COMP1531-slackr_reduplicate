# comment this out until these functions are written
# from channel_list import channel_list
# from channel_details import channel_details

# placeholder functions to use until we get the real ones written
def channel_list(token):
    return [1, 2, 3]


def channel_details(channel_id):
    if channel_id == 1:
        return {
            'name' : "Modernists",
            'owner_members' : [
                {
                    'u_id' : 113,
                    'name_first' : "James",
                    'name_last' : "Joyce"
                }
            ],
            'all_members' : [
                {
                    'u_id' : 111,
                    'name_first' : "Stephen",
                    'name_last' : "Daedalus"
                },
                {
                    'u_id' : 112,
                    'name_first' : "Joseph",
                    'name_last' : "Conrad"
                },
                {
                    'u_id' : 113,
                    'name_first' : "James",
                    'name_last' : "Joyce"
                }
            ]
        }
    elif channel_id == 2:
        return {
            'name' : "Postmodernists",
            'owner_members' : [
                {
                    'u_id' : 110,
                    'name_first' : "Michel",
                    'name_last' : "Foucault"
                }
            ],
            'all_members' : [
                {
                    'u_id' : 110,
                    'name_first' : "Michel",
                    'name_last' : "Foucault"
                },
                {
                    'u_id' : 109,
                    'name_first' : "Giles",
                    'name_last' : "Deleuze"
                }
            ]
        }


def get_uid_from_token(token):
    if token == 1:
        return 111
    elif token == 2:
        return 112


def channel_leave(token, channel_id):
    # somehow get the associated uid
    uid_ = get_uid_from_token(token)

    # check if channel exists, if it does not throw a ValueError
    if channel_id not in channel_list(token):
        raise ValueError

    # otherwise remove the user with this token from the channel
    for index, user in enumerate(channel_details(channel_id)['all_members']):
        if user["u_id"] == uid_:
            del channel_details(channel_id)['all_members'][index]
            break
