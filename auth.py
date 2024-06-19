access_token = None

def set_access_token(token):
    global access_token
    access_token = token

def get_access_token():
    return access_token
