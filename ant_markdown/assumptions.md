assumptions.md
=======

_Write assumptions that you feel you are making in your interpretation of the specification and of the functions provided._

We are assuming that we have the necessary server space to host the app backend. We are assuming that we have the necessary server funds to host the app backend. We are assuming that we have the necessary server resources to host the app backend.

___

User_profile_setname:
	Assume that inputs given by users are reasonable and will not cause edge cases. We will assume that only alphanumeric characters are used. 

User_profile_setemail:
	Still assuming that inputs are reasonable.

user_profile_sethandle:
	Same assumptions as set name. For example, that inputs do not include exclusively white space, that inputs comply with the Unicode Standard, that inputs do not include formatting characters like zero width spaces. You would want to customise your handle to a larger extent than your name.

user_profiles_setphoto:
	Since this requires both a. A given URL and b. The processing of an image, we are assuming that the given URL actually redirects to a valid image format (png, jpg). This image format will not be a gif, bmp, or other hard to integrate format. We will also assume that given URLs are not potentially malicious to our backend. Though this is more a social issue, we would like to assume given images are appropriate for a University program.

standup_send:
	We will assume that messages sent can be displayed as a message, i.e. Unicode Standard, no formatting characters.

search:
	Assume the Unicode Standard, valid characters only.

admin_userpermission_change:
	We will assume that there is no other way to access the database for a non admin/owner.
