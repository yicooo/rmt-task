import json
import secrets
from flask import request, jsonify, make_response
from config import app
from models import Auth, User, Message, BlockList, LogRecords
from functions import hash256default, verify_login

'''
    Endpoint = /createuser

    Input =
        {
            'name': 'string',
            'password: 'string'
        }
'''


@app.route('/createuser', methods=['PUT'])
def create_user():
    try:
        user_data = json.loads(request.data)
        name = user_data['name']
        password = user_data['password']
        # Search if anyone exists with this username
        user = User.objects(name=name).first()
        if user:
            return jsonify({'message': 'Name already exists'})

        else:
            hashed_password = hash256default(password)
            new_user = User(name=name, password=hashed_password)
            new_user.save()
            return jsonify({'message': 'User created successfully', 'name': name})

    except:
        return make_response(jsonify({'error': 'corrupt request'}), 400)


'''
    Endpoint = /login

    Input =
    {
        'name' : 'string',
        'password' : string
    }
'''


@app.route('/login', methods=['POST'])
def login():
    try:
        user_data = json.loads(request.data)
        name = user_data['name']
        user = User.objects(name=name).first()

        if not user:
            return make_response(jsonify({'error': 'Name not found'}), 401)

        elif user.password == hash256default(user_data['password']):
            randomly_generated_token = secrets.token_hex(22)
            auth = Auth.objects(name=name).first()
            if auth:
                auth.update(token=randomly_generated_token)
            else:
                new_auth = Auth(name=name, token=randomly_generated_token)
                new_auth.save()

            log_record = LogRecords(is_success=True, name=name)
            log_record.save()

            return jsonify({
                'message': 'Logged in',
                'name': name,
                'token': randomly_generated_token
            })

        else:

            log_record = LogRecords(is_success=False, name=name)
            log_record.save()

            return make_response(jsonify({'error': 'Wrong password'}), 401)

    except:
        return make_response(jsonify({'error': 'corrupt request'}), 400)


'''
    Endpoint = /blocksender

    Input = 
    {
        'name': 'string',
        'token': 'string',
        'target': 'string'
    }
'''


@app.route('/blocksender', methods=['PUT'])
def block_sender():
    try:
        request_data = json.loads(request.data)
        print(request_data)
        if not verify_login(request_data):
            return make_response(jsonify({
                'error': 'you are not logged in or request is not valid'
            }), 401)

        name = request_data['name']
        target = request_data['target']
        block_rule = BlockList(blocker=name, target=target)
        block_rule.save()
        return jsonify(block_rule.to_dict())

    except:
        return make_response(jsonify({'error': 'corrupt request'}), 400)


'''
    Endpoint = /sendmessage

    Input = 
    {
        'name': 'string',
        'token': 'string',
        'to': 'string',
        'message': 'string'
    }
'''


@app.route('/sendmessage', methods=['PUT'])
def send_message():
    try:
        request_data = json.loads(request.data)

        if not verify_login(request_data):
            return make_response(jsonify({
                'error': 'you are not logged in or request is not valid'
            }), 401)

        sender = request_data['name']
        reciever = request_data['to']
        message = request_data['message']
        # Check block rules
        rule = BlockList.objects(blocker=reciever, target=sender).first()
        if rule:
            print("test3")
            return jsonify({
                'error': 'You are blocked by reciever'
            })

        else:
            message_entry = Message(
                sender=sender, reciever=reciever, message=message)
            message_entry.save()
            return jsonify({
                'message': 'message is sent',
                'from': sender,
                'to': reciever
            })
    except:
        make_response(jsonify({'error': 'corrupt request'}), 400)


'''
    Endpoint = /showmessages

    Input = 
    {
        'name': 'string',
        'token': 'string'
    }
'''


@app.route('/showmessages', methods=['POST'])
def show_messages():
    try:
        request_data = json.loads(request.data)

        if not verify_login(request_data):
            return make_response(jsonify({
                'error': 'you are not logged in or request is not valid'
            }), 401)

        message_set = Message.objects(reciever=request_data['name'])
        message_list = []
        for message in message_set:
            message_list.append(message.to_dict())

        return jsonify(results=message_list)
    except:
        return make_response(jsonify({'error': 'corrupt request'}), 400)


'''
    Endpoint = /showloginhistory

    Input = 
    {
        'name': 'string',
        'token': 'string'
    }
'''


@app.route('/showloginhistory', methods=['POST'])
def show_login_history():
    try:
        request_data = json.loads(request.data)

        if not verify_login(request_data):
            return make_response(jsonify({
                'error': 'you are not logged in or request is not valid'
            }), 401)

        history_set = LogRecords.objects(name=request_data['name'])
        history_list = []
        for entry in history_set:
            history_list.append(entry.to_dict())

        return jsonify(results=history_list)
    except:
        return make_response(jsonify({'error': 'corrupt request'}), 400)


if __name__ == "__main__":
    app.run(debug=True)
