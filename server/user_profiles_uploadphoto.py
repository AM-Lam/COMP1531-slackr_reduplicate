import urllib.request

#   user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end,     y_end);
#   return void
#   Exception: ValueError when:
#       - img_url is returns an HTTP status other than 200,
#       - x_start, y_start, x_end, y_end are all within the                   dimensions of the image at the URL.
#   Description: Given a URL of an image on the internet, crops the image within bounds (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end,     y_end):
    # find u_id associated with token (with non-existent database)
    u_id = 12345

    check_imgurl(img_url)
    check_start_coords(x_start, y_start)
    check_end_coords(x_end, y_end)
    change_photo(img_url, x_start, y_start, x_end, y_end)
    return void

def check_imgurl(img_url):
    if urllib.request.urlopen(img_url).getcode() == 200:
        return True
    else:
        raise ValueError("The URL is not working at the moment!")

def check_start_coords(x_start, y_start):
    # we don't know how to get image dimensions yet, so we will assume the max image size is 200x200
    IMG_LIMIT = 200;
    if x_start >= 0 and y_start >= 0 and x_start <= 200 and y_start <= 200:
        return True
    else:
        raise ValueError("Co-ordinates out of bounds.")

def check_end_coords(x_end, y_end):
    # we don't know how to get image dimensions yet, so we will assume the max image size is 200x200
    IMG_LIMIT = 200;
    if x_end >= 0 and y_end >= 0 and x_end <= 200 and y_end <= 200:
        return True
    else:
        raise ValueError("Co-ordinates out of bounds.")

def change_photo(img_url, x_start, y_start, x_end, y_end):
    # change the photo in the database (which doesn't exist)
    pass
