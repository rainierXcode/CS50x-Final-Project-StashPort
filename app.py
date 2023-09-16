from flask import Flask, render_template, url_for, request, redirect
from helper import * 


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def loginUI():
    error_message_username = None 
    error_message_password = None 
    have_error = False
    execute = None
    
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
                error_message_username = "Username doesn't exist"
                have_error = True

            
            elif password != "yoshito31":
                error_message_password = "Password is invalid"
                have_error = True 
        
        if have_error:
            return render_template("login.html", username_error=error_message_username, password_error=error_message_password)
        
        if username == "yoshito31" and password == "yoshito31":
            return render_template("home.html")
    else:
        error_message = None

    return render_template("login.html")





@app.route('/signup')
def signUI():
    return render_template("signup.html")

        


if __name__ == '__main__':
      app.run(debug=True)