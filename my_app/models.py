from datetime import datetime
from my_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    amenities = db.Column(db.ARRAY(db.String), nullable=False)
    master_bedroom = db.Column(db.String(25), nullable=False)
    master_bathroom = db.Column(db.String(25), nullable=False)
    kitchen = db.Column(db.String(25), nullable=False)
    outside_view = db.Column(db.String(25), nullable=False)
    house_pictures = db.Column(db.ARRAY(db.String(25)), nullable=False, default='default_house.jpg')
    address_line_1 = db.Column(db.Text, nullable=False)
    address_line_2 = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=False)
    state_province_region = db.Column(db.String(10), nullable=False)
    zip_postal_code = db.Column(db.String, nullable=False)
    number_of_bedrooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    buy_or_rent = db.Column(db.String(20), nullable=False)
    longitud = db.Column(db.String(25), nullable=False)
    latitud = db.Column(db.String(25), nullable=False)
    floatLongi = db.Column(db.Float, nullable=False)
    floatLati = db.Column(db.Float, nullable=False)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted})"
