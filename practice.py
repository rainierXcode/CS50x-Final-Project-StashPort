from flask import Flask, render_template, url_for, request, redirect
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
import requests




# app = Flask(__name__)

# db = SQL("sqlite:///stashport.db")
# username = "rainier01s"

# user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
# folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ?", user_id[0]["user_id"])
# for folder in folders:
#   print(folder["folder_name"])

# # folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ?", user_id)

def link_verifier(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False
    
print(link_verifier("https://www.theodinproject.com/dashboard"))
