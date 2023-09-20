from flask import Flask, render_template, url_for, request, redirect
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash




app = Flask(__name__)

db = SQL("sqlite:///stashport.db")
username = "rainier01s"

username_exist = db.execute("SELECT * FROM users WHERE username = ?", username)
print(username_exist[0]["password"])