from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/login')
@app.route('/')
def loginUI():
    return render_template("login.html")

@app.route('/signup')
def signUI():
    return render_template("signup.html")

if __name__ == '__main__':
    app.run()