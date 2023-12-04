from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase


db = SQLAlchemy()



class Base(DeclarativeBase):
    pass



from flask_login import UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.String(255), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

    caught = db.relationship('Pokemon', secondary='pokemons_to_users', backref=db.backref('caught', lazy='dynamic'), lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<{self.__class__.__name__} | {self.id}>"
    
    def __str__(self):
        return f"{self.__class__.__name__} | {self.id}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self       

    def catch_pokemon(self, poke):
        self.caught.append(poke)
        db.session.commit()

    def release_pokemon(self, poke):
        self.caught.remove(poke)
        db.session.commit()

    def add_loss(self):
        self.losses += 1
        db.session.commit()

    def add_win(self):
        self.wins += 1
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def login(self):
        login_user(self)

    def logout(self):
        logout_user()

    @property
    def record(self):
        return f"{self.wins} {'win' if self.wins == 1 else 'wins'} - {self.losses} {'loss' if self.losses == 1 else 'losses'}"



class Pokemon(db.Model):
    __tablename__ = 'pokemons'

    id = db.Column(db.String(255), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    game_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(255))
    base_hitpoints = db.Column(db.Integer)
    base_attack = db.Column(db.Integer)
    base_defense = db.Column(db.Integer)
    base_experience = db.Column(db.Integer)
    base_speed = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

    sprites = db.relationship('PokemonSprites', backref=db.backref('pokemon', lazy='dynamic'), lazy='dynamic')

    def __init__(self, game_id, name, base_hp, base_atk, base_def, base_spd, base_exp, height, weight):
        self.game_id = game_id
        self.name = name
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.base_spd = base_spd
        self.base_exp = base_exp
        self.height = height
        self.weight = weight

    def __repr__(self):
        return f"<{self.__class__.__name__} | {self.id}>"
    
    def __str__(self):
        return f"{self.__class__.__name__} | {self.id}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self       


class PokemonSprites(db.Model):
    __tablename__ = 'pokemon_sprites'

    id = db.Column(db.String(255), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    pokemon_id = db.Column(db.String(255), db.ForeignKey('pokemons.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, pokemon_id, name):
        self.pokemon_id = pokemon_id
        self.name = name

    def __repr__(self):
        return f"<{self.__class__.__name__} | {self.id}>"
    
    def __str__(self):
        return f"{self.__class__.__name__} | {self.id}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self       


class PokemonTypes(db.Model):
    __tablename__ = 'pokemon_types'

    id = db.Column(db.String(255), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{self.__class__.__name__} | {self.id}>"
    
    def __str__(self):
        return f"{self.__class__.__name__} | {self.id}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self       


class PokemonAbilities(db.Model):
    __tablename__ = 'pokemon_abilities'

    id = db.Column(db.String(255), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{self.__class__.__name__} | {self.id}>"
    
    def __str__(self):
        return f"{self.__class__.__name__} | {self.id}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self       


class PokemonMoves(db.Model):
    __tablename__ = 'pokemon_moves'

    id = db.Column(db.String(255), primary_key=True, nullable=False, unique=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    name = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<{self.__class__.__name__} | {self.id}>"
    
    def __str__(self):
        return f"{self.__class__.__name__} | {self.id}"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self       



pokemon_to_user = db.Table(
    "pokemons_to_users",
    db.Column("pokemon_id", db.String(255), db.ForeignKey("pokemons.id"), nullable=False, primary_key=True),
    db.Column("user_id", db.String(255), db.ForeignKey("users.id"), nullable=False, primary_key=True),
)



class PokemonToType(db.Model):
    __tablename__ = 'pokemons_to_types'

    pokemon_id = db.Column(db.String, db.ForeignKey('pokemons.id'), nullable=False)
    type_id = db.Column(db.String, db.ForeignKey('pokemon_types.id'), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('pokemon_id', 'type_id'),
    )

    def __init__(self, pokemon_id, type_id):
        self.pokemon_id = pokemon_id
        self.type_id = type_id

    def __repr__(self):
        return f"<{self.__class__.__name__} | Pokemon {self.pokemon_id} <-> Type {self.type_id}>"
    
    def __str__(self):
        return f"<{self.__class__.__name__} | Pokemon {self.pokemon_id} <-> Type {self.type_id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self       



class PokemonToAbility(db.Model):
    __tablename__ = 'pokemons_to_abilities'

    pokemon_id = db.Column(db.String, db.ForeignKey('pokemons.id'), nullable=False)
    ability_id = db.Column(db.String, db.ForeignKey('pokemon_abilities.id'), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('pokemon_id', 'ability_id'),
    )

    def __init__(self, pokemon_id, ability_id):
        self.pokemon_id = pokemon_id
        self.ability_id = ability_id

    def __repr__(self):
        return f"<{self.__class__.__name__} | Pokemon {self.pokemon_id} <-> Ability {self.ability_id}>"
    
    def __str__(self):
        return f"<{self.__class__.__name__} | Pokemon {self.pokemon_id} <-> Ability {self.ability_id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
 


class PokemonToMove(db.Model):
    __tablename__ = 'pokemons_to_moves'

    pokemon_id = db.Column(db.String, db.ForeignKey('pokemons.id'), nullable=False)
    move_id = db.Column(db.String, db.ForeignKey('pokemon_moves.id'), nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('pokemon_id', 'move_id'),
    )

    def __init__(self, pokemon_id, move_id):
        self.pokemon_id = pokemon_id
        self.move_id = move_id

    def __repr__(self):
        return f"<{self.__class__.__name__} | Pokemon {self.pokemon_id} <-> Move {self.move_id}>"
    
    def __str__(self):
        return f"<{self.__class__.__name__} | Pokemon {self.pokemon_id} <-> Move {self.move_id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
 