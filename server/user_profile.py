def user_profile(token, u_id):
    if u_id_list[token] == u_id:
        if u_id in u_id_dic: 
            return u_id_dic[u_id]
        else:
            raise ValueError("We cannot find the details of this user.")
        # details cannot be found based on u_id
    else:
        raise ValueError("This username is not existed. Please try again")
        