from app import app, db

class Message(db.Model):
    __tablename__ = 'messages'  
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(500))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    messages = db.relationship('Message', backref='category')

    def message_amount(self):
        return len(self.messages)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    openId = db.Column(db.String(20),unique=True , nullable=False, index=True)
    nickname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10))
    city = db.Column(db.String(20))
    province = db.Column(db.String(20))
    country = db.Column(db.String(20))
    avatarUrl = db.Column(db.String(50))
    unionId = db.Column(db.String(50))

