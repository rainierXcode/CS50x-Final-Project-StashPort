from flask import render_template, redirect, url_for, session
from functools import wraps
import re
import requests
from datetime import datetime



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
        if response.status_code == 200 or response.status_code == 403:
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


def getDate():
    current_datetime = datetime.now()
    date_format=  current_datetime.strftime("%B %d, %Y")
    return str(date_format)


def getTime():
    current_datetime = datetime.now()
    hour = current_datetime.hour
    minute = current_datetime.minute

    if hour < 12:
        am_pm = "AM"
    else:
        am_pm = "PM"


    if hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12

    hour_str = str(hour) if hour >= 10 else "0" + str(hour) 
    minute_str = str(minute) if minute >= 10 else "0" + str(minute)
    time_format = hour_str + ":" + minute_str + " " + am_pm
    return str(time_format)

def getLinkTime():
    current_datetime = datetime.datetime.now()
    date_format = current_datetime.strftime("%m-%d-%Y")
    return str(date_format)






def history_date_format(date_record):
    date_object = datetime.strptime(date_record, "%m-%d-%Y")
    formatted_date = date_object.strftime("%B %d, %Y")
    return str(formatted_date)

def database_date_format(orig_date):
    date_object = datetime.strptime(orig_date, "%B %d, %Y")
    datebase_date = date_object.strftime("%m-%d-%Y")
    return str(datebase_date)
