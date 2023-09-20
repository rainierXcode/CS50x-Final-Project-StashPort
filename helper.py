from flask import render_template, redirect, url_for, session
from functools import wraps

# Custom decorator to check if the user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            # User is not authenticated, redirect to the login page
            return redirect(url_for('loginUI'))  # Replace 'login' with your login route
        return f(*args, **kwargs)
    return decorated_function