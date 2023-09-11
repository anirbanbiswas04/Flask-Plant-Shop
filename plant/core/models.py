from plant import db, bcrypt
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(1000), unique=False, nullable=False)
    is_superuser = db.Column(db.Boolean(), unique=False, default=False)

    def __repr__(self):
        return self.username
    
    @property
    def hash_password(self):
        return self.password
    
    @hash_password.setter
    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    