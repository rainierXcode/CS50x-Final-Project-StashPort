from flask import render_template, redirect, url_for, session
from functools import wraps
import re
import requests

# Custom decorator to check if the user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('loginUI'))  
        return f(*args, **kwargs)
    return decorated_function

def extractNum(path):
    
    match = re.search(r'\d+', str(path))
    
    if match:
     
        num = int(match.group())
        return num
    else:
        return None


def link_verifier(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False

def getTitlePath(titles):
    titles_path = []
    for title in titles:
        titles_path.append(title['title_name'].replace(" ", "-"))
    return titles_path

def list_of_dict_title_data(post_contents, title_path_list):
    result_list= []
    for title, title_path in zip(post_contents,title_path_list):
        result_dict = {'title_name' : title['title_name'], 'title_path' : title_path}
        result_list.append(result_dict)
    
    return result_list