from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin, manager

    # Связь с оборудованием
    equipment = db.relationship('Equipment', backref='assigned_user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}, role: {self.role}>'


class UserRepo:
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_by_id(self, user_id):
        return User.query.get(user_id)

    def add(self, username, password, role='user'):
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def all(self):
        return User.query.all()

    def update(self, user_id, username=None, password=None, role=None):
        user = User.query.get(user_id)
        if not user:
            return None

        if username:
            user.username = username
        if password:
            user.set_password(password)
        if role:
            user.role = role

        db.session.commit()
        return user

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user

    def count_by_role(self):
        from sqlalchemy import func
        return db.session.query(User.role, func.count(User.id)).group_by(User.role).all()