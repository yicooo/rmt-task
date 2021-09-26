from config import db
from datetime import datetime

class User(db.Document):
    name = db.StringField()
    password = db.StringField()
    def to_dict(self):
        return {"name": self.name,
                "password": self.password}

class Message(db.Document):
    sender = db.StringField()
    reciever = db.StringField()
    message = db.StringField()
    def to_dict(self):
        return {"from": self.sender,
                "to": self.reciever,
                "message": self.message}

class BlockList(db.Document):
    blocker = db.StringField()
    target = db.StringField()
    def to_dict(self):
        return {"blocker": self.blocker,
                "target": self.target}

class LogRecords(db.Document):
    date = db.DateTimeField(default=datetime.utcnow)
    is_success = db.BooleanField()
    name = db.StringField()
    def to_dict(self):
        return {"date": datetime.strftime(self.date,format="%m/%d/%Y, %H:%M:%S"),
                "is_success": str(self.is_success),
                "name": self.name}

class Auth(db.Document):
    name = db.StringField()
    token = db.StringField()
    def to_dict(self):
        return {"name": self.name,
                "token": self.token}
