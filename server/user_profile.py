from .access_error import AccessError


def user_profile(token, u_id):
    if u_id_list[token] == u_id:
        if u_id in u_id_dic: 
            return u_id_dic[u_id]
        else:
            raise ValueError(description="We cannot find the details of this user.")
        # details cannot be found based on u_id
    else:
        raise ValueError(description="This username is not existed. Please try again")
        