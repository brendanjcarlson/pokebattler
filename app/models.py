from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

catch = db.Table(
    'catch',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.poke_id'), nullable=False))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    wins = db.Column(db.Integer, nullable=True, default=0)
    losses = db.Column(db.Integer, nullable=True, default=0)
    caught = db.relationship('Pokemon', secondary='catch', backref=db.backref('caught', lazy='dynamic'), lazy='dynamic')


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def CREATE(self):
        db.session.add(self)
        db.session.commit()

    def CATCH(self, poke):
        self.caught.append(poke)
        db.session.commit()

    def RELEASE(self, poke):
        self.caught.remove(poke)
        db.session.commit()

    def ADD_LOSS(self):
        self.losses += 1
        db.session.commit()

    def ADD_WIN(self):
        self.wins += 1
        db.session.commit()

    @property
    def record(self):
        return f"{self.wins} {'win' if self.wins == 1 else 'wins'} - {self.losses} {'loss' if self.losses == 1 else 'losses'}"



class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    poke_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    types = db.Column(db.String(32))
    abilities = db.Column(db.String)
    base_hp = db.Column(db.Integer)
    base_atk = db.Column(db.Integer)
    base_def = db.Column(db.Integer)
    base_exp = db.Column(db.Integer)
    base_spd = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    sprite_url = db.Column(db.String)
    is_caught = db.Column(db.Boolean, default=False)
    caught_by = db.Column(db.String, db.ForeignKey('user.username'))


    def __init__(self, poke_id, name, types, abilities, base_hp, base_atk, base_def, base_spd, base_exp, height, weight, sprite_url):
        self.poke_id = poke_id
        self.name = name
        self.types = types
        self.abilities = abilities
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.base_spd = base_spd
        self.base_exp = base_exp
        self.height = height
        self.weight = weight
        self.sprite_url = sprite_url

    def TO_DICT(self):
        return {
            'id': self.poke_id,
            'name': self.name,
            'types': self.types,
            'abilities': self.abilities,
            'base_hp': self.base_hp,
            'base_atk': self.base_atk,
            'base_def': self.base_def,
            'base_spd': self.base_spd,
            'base_exp': self.base_exp,
            'height': self.height,
            'weight': self.weight,
            'sprite_url': self.sprite_url,
            'is_caught': self.is_caught,
            'caught_by': self.caught_by
        }

    def CREATE(self):
        db.session.add(self)
        db.session.commit()

    def UPDATE(self):
        db.session.commit()
