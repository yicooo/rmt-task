from flask import Flask, Response as BaseResponse, json
from flask.testing import FlaskClient
from app import app


def create_user_test(name,password):
    with app.test_client() as tc:
        rv = tc.put('/createuser', json={
            'name': name, 'password': password
        })
        json_data = rv.get_json()
        print(json_data)

def login_return_token(name,password):
    with app.test_client() as tc:
        rv = tc.post('/login', json={
            'name': name, 'password': password
        })
        json_data = rv.get_json()
        print(json_data)
        try:
            return json_data['token']
        except KeyError:
            return ''

def send_message(sender,reciever,token,message):
    with app.test_client() as tc:
        rv = tc.put('/sendmessage', json={
            'name': sender, 
            'to': reciever,
            'token' : token,
            'message' : message
        })
        json_data = rv.get_json()
        print(json_data)

def block_user(name,token,target):
    with app.test_client() as tc:
        rv = tc.put('/blocksender', json={
            'name': name, 
            'target': target,
            'token' : token
        })
        json_data = rv.get_json()
        print(json_data)

def show_messages(name,token):
    with app.test_client() as tc:
        rv = tc.post('/showmessages', json={
            'name': name, 
            'token' : token
        })
        json_data = rv.get_json()
        print(json_data)

def show_history(name,token):
    with app.test_client() as tc:
        rv = tc.post('/showloginhistory', json={
            'name': name, 
            'token' : token
        })
        json_data = rv.get_json()
        print(json_data)


if __name__ == "__main__":
    print('### Creating User 1')
    create_user_test('user1','user1')
    print('### Creating User 2')
    create_user_test('user2','user2')
    print('### Logging in user 1 and retrieving token')
    token = login_return_token('user2','user2')
    print('### Blocking user 1 (still can send messages)')
    block_user('user2',token,'user1')
    print('### Sending message')
    send_message('user2','user1',token,'Hello from user2 to user1')
    print('### Logging in user 2')
    token = login_return_token('user1','user1')
    print('### Showing messsages')
    show_messages('user1',token)
    print('### Intentionally logging in with bad password')
    login_return_token('user1','badword')
    print('### Printing out login history')
    show_history('user1',token)
    print('### Sending message to user 1 but will fail')
    send_message('user1','user2',token,'Hello from user1 to user2')

