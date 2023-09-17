from flask import Flask, render_template, url_for, request, redirect
from helper import * 


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def loginUI():
    error_message_username = None 
    error_message_password = None 
    have_error = False
    execute = None
    username_value = None
    password_value = None
    
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
          
            if username != "yoshito31":
                error_message_username = "Username does not exist"
                have_error = True

            
            elif password != "yoshito31":
                error_message_password = "Password is invalid"
                have_error = True 
        
        if have_error:
            return render_template("login.html", username_error=error_message_username, password_error=error_message_password, username_value=username, password_value=password)
        
        if username == "yoshito31" and password == "yoshito31":
            return render_template("home.html")


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
            if username == "yoshito31":
                error_message_username = "Username already exists"
                have_error = True
            
            if confirm_password != password:
                error_message_password_confirm = "Password does not match"
                have_error = True
            
        
        if have_error:
            return render_template("signup.html", fname_error = error_message_fName, lname_error= error_message_lName, username_error = error_message_username, password_error = error_message_password , confirm_pass_error = error_message_password_confirm)
        

        
    return render_template("signup.html")

        


if __name__ == '__main__':
      app.run(debug=True)