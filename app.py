from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from helper import * 
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import json
import os

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///stashport.db")

@app.route('/', methods=["GET", "POST"])
def loginUI():
    error_message_username = None 
    error_message_password = None 
    have_error = False
    execute = None
    username_value = None
    password_value = None
    login_success = True

    if session.get("user_id"):
        return redirect("/home")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

       

        if username == "":
            error_message_username = "Username cannot be empty"
            have_error = True

        elif len(username) < 6:
            error_message_username = "Username must be at least 6 characters"
            have_error = True
        
        if password == "":
            error_message_password = "Password cannot be empty"
            have_error = True

        elif len(password) < 6:
            error_message_password = "Password must be at least 6 characters"
            have_error = True
        
    
        if not have_error:
            username_exist = db.execute("SELECT * FROM users WHERE username = ?", username)
            if  not username_exist:
                error_message_username = "Username does not exist"
                have_error = True
                login_success = False

            else:
               stored_password_hash = username_exist[0]["password"]
               if not check_password_hash(stored_password_hash, password):
                error_message_password = "Password is invalid"
                have_error = True 
                login_success = False
        
        if have_error:
            return render_template("login.html", username_error=error_message_username, password_error=error_message_password, username_value=username, password_value=password)
        
        if login_success:
            session["user_id"] = username
            return redirect("/home")


    return render_template("login.html")





@app.route('/signup', methods=["GET", "POST"])
def signUI():
    if request.method == "POST":
        error_message_fName = None
        error_message_lName = None
        error_message_username = None
        error_message_password = None
        error_message_password_confirm = None

        fName = request.form.get("fname")
        lName = request.form.get("lname")
        username = request.form.get("username-signup")
        password = request.form.get("password-signup")
        confirm_password = request.form.get("confirm-password-signup")
        have_error = False

        if fName == "":
            error_message_fName = "First name cannot be empty"
            have_error = True

        elif len(fName) < 3:
            error_message_fName = "First name must be at least 4 characters"
            have_error = True

        if lName == "":
            error_message_lName = "Last name cannot be empty"
            have_error = True

        elif len(lName) < 2:
            error_message_lName = "Last name must be at least 2 characters"
            have_error = True

        if username == "":
            error_message_username = "Username cannot be empty"
            have_error = True
        
        elif len(username) < 6:
            error_message_username = "Username must be at least 6 characters"
            have_error = True
        
        if password == "":
            error_message_password = "Password cannot be empty"
            have_error = True

        elif len(password) < 6:
            error_message_password = "Password must be at least 6 characters"
            have_error = True

        if confirm_password == "":
            error_message_password_confirm =  "Confirm Password cannot be empty"
            have_error = True

        elif len(confirm_password) < 6:
            error_message_password_confirm = "Password must be at least 6 characters"
            have_error = True
        
        
        if not have_error:
            username_exist = db.execute("SELECT username FROM users WHERE username = ?", username)
            if username_exist:
                error_message_username = "Username already exists"
                have_error = True
            
            elif confirm_password != password:
                error_message_password_confirm = "Password does not match"
                have_error = True
            
        
        if have_error:
            return render_template("signup.html", fname_error = error_message_fName, lname_error= error_message_lName, username_error = error_message_username, password_error = error_message_password , confirm_pass_error = error_message_password_confirm,fname_value = fName, lname_value = lName, username_value = username, password_value= password, confirm_password_value = confirm_password)
        
        hash_pass=generate_password_hash(password);
        db.execute("INSERT INTO users(first_name, last_name, username, password) VALUES( ?, ?, ?, ?)", fName, lName, username, hash_pass)
        return redirect("/")
        

        
    return render_template("signup.html")

@app.route("/home")
@login_required
def home():
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
    folder_list = db.execute("SELECT f.folder_name, si.src_path FROM folders AS f JOIN src_img AS si ON f.folder_category_id = si.src_id WHERE f.user_id = ?",  user_id[0]["user_id"])
    return render_template("home.html", username = username, folder_list = folder_list)


@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect("/")





        
@app.route("/home/upload", methods=["GET", "POST"])
@login_required
def upload():
    error_message_folder = None
    error_message_title = None
    error_message_link = None
    error_message_description = None
    error_message_tags = None
    folder_value = None
    title_value = None
    link_value = None
    description_value = None
    tags_value = None

    all_error = []

    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
    folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ?", user_id[0]["user_id"])
    folders_list = []
    for folder in folders:
        folders_list.append(folder["folder_name"])



    if request.method == "POST":
        folder_choice = request.form.get("folders")
        title = request.form.get("title")
        link = request.form.get("link")
        description  = request.form.get("description")
        tags = request.form.get("tags")
    

        if folder_choice == None:
            error_message_folder = "Folder named folder is not available"
            all_error.append(error_message_folder)
            


        if title == "":
            error_message_title = "Title cannot be empty"
            all_error.append(error_message_title)
         

        elif len(title) < 5:
            error_message_title = "Title must be 5 characters above"
            all_error.append(error_message_title)
        
        if link == "":
            error_message_link = "Link cannot be empty"
            all_error.append(error_message_link)


        elif not link_verifier(link):
            error_message_link = "Your Link is Detected Invalid"
            all_error.append(error_message_link)
        

        if description == "":
            error_message_description = "Description cannot be empty"
            all_error.append(error_message_description)


        elif len(description) < 30:
            error_message_description = "Too short, must be 30 characters above"
            all_error.append(error_message_description)


        if tags == tags.endswith(","):
            error_message_tags = "Dont end with comma"
            all_error.append(error_message_tags)



        if len(all_error) != 0:
            title_value = title
            folder_value = folder_choice
            link_value =link
            description_value = description
            tags_value =tags

            return render_template("upload.html", folders = folders_list, all_errors=all_error, folder_value = folder_value, title_value = title_value, link_value = link_value, description_value = description_value, tags_value = tags_value, username = username)
        
        else:
            folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_choice, user_id[0]["user_id"])
            db.execute("INSERT INTO links(title_name, link_url, folder_category, description, folder_id) VALUES (?, ?, ?, ?, ?)",
            title, link, folder_choice, description, folder_id[0]['folder_id'] )
            return redirect("/home")
                  
    return render_template("upload.html", folders = folders_list, username = username)



@app.route("/home/upload/addfolder", methods=["GET", "POST"])
@login_required
def addFolder():
    if request.method == "POST":
        new_folder_name = request.form.get("folder_name")
        username = session["user_id"]
        img_select = request.form.get("selected_image")
        img_select = os.path.basename(img_select)
        folder_category_id = extractNum(img_select)
        
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
        db.execute("INSERT INTO folders(folder_category_id, folder_name, user_id) VALUES(? ,?, ?)",  folder_category_id, new_folder_name, user_id[0]["user_id"])
       
      
        return redirect("/home/upload")
    return redirect("/home/upload")

@app.route("/home/folder/<folder_name>")
@login_required
def folder(folder_name):
        username = session["user_id"]
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
        folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_name, user_id)
        post_contents = db.execute("SELECT title_name FROM links WHERE folder_id = ?", folder_id[0]["folder_id"])
        other_folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ? ORDER BY folder_id DESC LIMIT 5", user_id)
        return render_template("folder-post.html", post_contents = post_contents, other_folders = other_folders, current_folder = folder_name)


@app.route("/home/folder/<folder_name>/delete-post/<title>")
@login_required
def deletePost(folder_name, title):
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_name, user_id)[0]["folder_id"]
    db.execute("DELETE FROM links WHERE folder_id = ? AND title_name = ?", folder_id, title)
    return redirect(url_for('folder', folder_name=folder_name))

if __name__ == '__main__':
      app.run(debug=True)