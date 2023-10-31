from .database import db 

class User(db.Model):
    #defining the user table
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(120),nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False, default="user")
class Admin(db.Model):
    #defining the admin table
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120),nullable=False)
     
    password = db.Column(db.Text, nullable=False)
    
class Music(db.Model):
    #defining the music table

    __tablename__ = "musics"
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(),  unique=True) #for now removed nullable
    Genre = db.Column(db.String(), nullable=False)
    Artist = db.Column(db.String(),nullable=False)
    path = db.Column(db.String(),nullable=False, unique=True)

class album(db.Model):

    __tablename__ = "creator"
    album_name = db.Column(db.String(),primary_key=True)
    artist = db.Column(db.String())
    song_name = db.Column(db.String())