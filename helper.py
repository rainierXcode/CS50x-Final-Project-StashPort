from flask import render_template, redirect, url_for, session
from functools import wraps
import re

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
