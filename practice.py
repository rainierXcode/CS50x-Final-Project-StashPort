from flask import Flask, render_template, url_for, request, redirect
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import json




# app = Flask(__name__)

db = SQL("sqlite:///stashport.db")
username = "rainier01s"

user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
# # folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ?", user_id[0]["user_id"])
# # folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", "Programming", user_id[0]["user_id"])
# # print(folder_id)
# # # folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ?", user_id)

# folder_choice = {'folder_name': 'Programing'}


# print(folder_choice["folder_name"])

folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ?", user_id[0]["user_id"])
folders_list = []
for folder in folders:
    folders_list.append(folder["folder_name"])
    

for f in folders_list:
    print(f)
