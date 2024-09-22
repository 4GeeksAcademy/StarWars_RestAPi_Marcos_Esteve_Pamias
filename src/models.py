from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False) 
    lastname = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.user_name #Cuándo me presentas (repr es repreentación)

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "last_name": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    especies = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)

    def __repr__(self): #Cuándo quiero saber sólo una cosa
        return '<User %r>' % self.username

    def serialize(self): #Cómo quiero presentar los datos de User
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }



class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    orbital_period = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(40), nullable=False)
    population = db.Column(db.String(40), nullable=False, unique=True)
    gravity = db.Column(db.String(40), nullable=False)

    def __repr__(self): #Cuándo quiero saber sólo una cosa
        return '<User %r>' % self.username

    def serialize(self): #Cómo quiero presentar los datos de User
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
 