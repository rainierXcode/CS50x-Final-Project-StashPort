from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from helper import * 
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash




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
    return render_template("home.html")


@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect("/")

        


if __name__ == '__main__':
      app.run(debug=True)