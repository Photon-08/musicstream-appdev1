from flask import Flask, render_template, request, redirect, session
from flask import current_app as app
from applications.models import User, Admin, Music, album
from .database import db
from werkzeug.utils import secure_filename
import os
from sqlalchemy import text
import seaborn as sns
import matplotlib.pyplot as plt





app.secret_key = 'BAD_SECRET_KEY'



@app.route("/home", methods=["GET","POST"])
def homepage():

    #this will show the logged in/not logged in status in the navbar
    if session["user_name"]:
        app_status=session["user_name"]
    else:
        app_status = "Not Logged In"

    if session["role"] != "ADMIN":
        musics = Music.query.all() #contains all the music details from db
        musics = list(reversed(musics))
        print("-----------")
        for i in musics:
            print(i.path)
        
        albums = album.query.all()

        album_dict_path = {} #{album_name: [path_list]}
        album_dict_songs = {}
        final_album_dict={} #{album_name: {song_name:song_path}}
        for al in albums:
            #
            album_name = al.album_name
            path_list = []
            final_path_list = []
            
            song_list = al.song_name.split(",")
            final_song_list = []
            for song in song_list:
                final_song_list.append(song.strip(" "))

            print(final_song_list)
            print("###########")
            print(song_list)
            print("###########")

            for song in final_song_list:
                print("Song name {}".format(song))
                print(len(song))
                path = Music.query.with_entities(Music.path).filter_by(Name=song).first()
                #print(path)
                path_list.append(path)
                print(type(path))

            print(path_list)
            

                
          
            for i in path_list:
                for j in i:
                    
                    final_path_list.append(j)
            
            album_dict_path[album_name] = final_path_list
            album_dict_songs[album_name] = final_song_list

            print(album_dict_path)
            print(album_dict_songs)

            song_path_dict = dict(map(lambda i,j : (i,j) , final_song_list,final_path_list))
            
            final_album_dict[album_name] = song_path_dict

            print(final_album_dict)
            


        return render_template("index.html",user_name=session['user_name'], role=session['role'], musics=musics, 
                               albums=final_album_dict)

    #if session['role'] == "ADMIN":
    #    return redirect("/admin_dashboard")

@app.route("/", methods=["GET","POST"])
def landing_page():
    
    if request.method == "GET":
        return render_template("auth_page.html")
    
    
    if request.method == "POST":
        print(request.form)
        if request.form.get("register"):
            #print("Reg")
            return redirect("/register")
        
        if request.form.get("login"):
            return redirect("/login")
        
        if request.form.get("admin"):
            return redirect("/admin")

@app.route("/register", methods=["GET","POST"])
def register():
    
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        print("-----------")
        print(request.form)
        if request.form.get("email"):
            user_email = request.form.get("email")

            
            if request.form.get('username'):
                user_name = request.form.get('username')
            

                

                if request.form.get('password'):
                    user_pass = request.form.get('password')
                    user_int = User(user_name=user_name,password=user_pass)

                    db.session.add(user_int)
                    db.session.commit()
                    return redirect("/login")
                    return redirect("/")
                
                else:
                    return render_template("register.html")
            else:
                return render_template("register.html")
        #return "<!doctype html><h6>Registered</h6>"



@app.route("/login",methods=["GET","POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        user_pass = request.form.get('password')
        print("Username: {}".format(username))

        #if username and user_pass:
        user = User.query.filter_by(user_name=username).first()
        if user.user_name == username and user_pass == user.password:
            
            #saving the username and id in session
            session["user_name"] = user.user_name
            session["user_id"] = user.id
            session["role"] = user.role

            return redirect("/home")
        else:
            return render_template('login_error.html')


@app.route("/logout",methods=["GET","POST"])
def logout():

    session.pop("user_id",None)
    session.pop("role",None)
    session.pop("user_name",None)

    return redirect("/")

@app.route("/admin",methods=["GET","POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        user_pass = request.form.get('password')
        print("Username: {}".format(username))

        #if username and user_pass:
        user = Admin.query.filter_by(username=username).first()
        if user.username == username and user_pass == user.password:
            
            #saving the username and id in session
            session["user_name"] = user.username
            session["user_id"] = user.id
            session["role"] = "ADMIN"

            return redirect("/home")
        else:
            return render_template('login_error.html')
        

@app.route("/creator_signup",methods=["GET","POST"])
def creator_regis():
    #if request.method == "GET":


    #fetching the logged in user details
    user_object = User.query.filter_by(user_name=session["user_name"]).first()
    user_object.role = "creator"
    db.session.commit()
    session["role"] = "creator"
    print("User has been Registered as a Creator")
    #print(app.upload_folder)

    return redirect("/creator")

@app.route("/creator",methods=["GET","POST"])
def file_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        flag = False
        file = request.files['file']  
        filename = secure_filename(file.filename)
        print("File Name: {}".format(filename))
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        #will be stored in the db
        path_name = os.path.join(app.config['UPLOAD_FOLDER'], filename).lstrip("/static/")
        song_name = request.form.get("song_name")
        artist_name = request.form.get("artist")
        genre = request.form.get("genre")

        new_song = Music(Name=song_name, Genre=genre, Artist=artist_name, path=path_name)
        db.session.add(new_song)
        db.session.commit()
        flag=True
        if flag:
            uploaded_status="Song Sucefully Uploaded"
        else:
            uploaded_status = "Please upload your song"
        return render_template("creator_page.html", upload_alert=uploaded_status)


    if request.method == "GET":
        return render_template("creator_page.html", user_name=session["user_name"], role=session["role"])
    
@app.route("/create-album",methods=["GET","POST"])
def create_album():
    if request.method == "POST":

        album_name_user = request.form.get("album")
        songs = request.form.get("songs")
        
        artist_name = request.form.get('artist')

        albums = album(album_name=album_name_user, artist=artist_name, song_name=songs)
        db.session.add(albums)
        db.session.commit()

        return redirect("/home")

    if request.method == "GET":
        creator_songs = Music.query.filter_by(Artist=session["user_name"]).all()
        
        for song in creator_songs:
            print(song.Name)
        return render_template("album_creation.html", songs=creator_songs) #
    
@app.route("/admin_dashboard",methods=["GET"])
def admin_dashboard():
    if request.method == "GET":
        if session['role'] == "ADMIN":

            all_songs = Music.query.all()
            artist_list = []
            song_list = []
            genre_list = []

            for song in all_songs:
                song_list.append(song.Name)
            print(song_list)

            for song in all_songs:
                artist_list.append(song.Artist)

            for song in all_songs:
                genre_list.append(song.Genre)

          
            sns.set_theme()
            ax = sns.histplot(artist_list)
            ax = ax.set(xlabel='Artist Names', ylabel='Count', title="Histogram of Artists")
            plt.savefig('static/charts/artist_plot.png')
            plt.clf() 

            sns.histplot(genre_list)
            plt.savefig('static/charts/genre_plot.png')
            plt.clf()
            

                
            sns.set_theme()
            ax = sns.histplot(artist_list)
            ax = ax.set(xlabel='Artist Names', ylabel='Count', title="Histogram of Artists")
            plt.savefig('static/charts/artist_plot.png')
            plt.clf() 

            sns.histplot(genre_list)
            plt.savefig('static/charts/genre_plot.png')
            plt.clf()
                
            
            return render_template("admin_dashboard.html")
        

        
            
            
