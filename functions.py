from models import Auth
import hashlib

def verify_login(data):
    auth = Auth.objects(name=data['name']).first()
    if not auth:
        return False
    else:
        print(data['token'],auth.token)
        if data['token'] == auth.token:
            return True
    return False

def salt(pw):
    return "asdj19" + pw + "ashdu1289"

def hash256default(pw):
    return hashlib.sha256(salt(pw).encode()).hexdigest()