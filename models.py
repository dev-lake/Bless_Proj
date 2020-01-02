from app import app, db

user_collection = db.Table(
    'collection',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('messages.id'))
)

class Message(db.Model):
    __tablename__ = 'messages'  
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(500))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    users = db.relationship('User', secondary=user_collection, back_populates='messages')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    messages = db.relationship('Message', backref='category')

    def message_amount(self):
        return len(self.messages)

    @staticmethod
    def get_all_category():
        query = Category.query.all()
        category = []
        for q in query:
            c = dict(id=q.id, name=q.name, items=q.message_amount())
            category.append(c)
        return category

    @staticmethod
    def get_category_amount():
        query = Category.query.all()
        return len(query)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    openId = db.Column(db.String(20), unique=True, nullable=False, index=True)
    nickname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10))
    city = db.Column(db.String(20))
    province = db.Column(db.String(20))
    country = db.Column(db.String(20))
    avatarUrl = db.Column(db.String(50))
    unionId = db.Column(db.String(50))
    messages = db.relationship('Message', secondary=user_collection, back_populates='users')

    def favourates(self):
        favourates = []
        for message in self.messages:
            favourates.append(dict(id=message.id, body=message.body))
        return favourates

    def favourates_amount(self):
        return len(self.messages) 

    