from flask import render_template, redirect, url_for, session
from functools import wraps
import re
import requests
from cs50 import SQL
from datetime import datetime
import re

db = SQL("sqlite:///stashport.db")

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
    url_pattern = r'(https?://|www\.)\S+'
    match = re.search(url_pattern, url)
    if match:
        return True
    else:
        return False



def getTitlePath(titles):
    titles_path = []
    for title in titles:
        titles_path.append(title['title_name'].replace(" ", "_"))
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
    current_datetime = datetime.now()
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



def getTagSeperation(tags):
    tag_separation = ""
    for tag in tags:
        tag_value = str(tag['tag_name'])
        tag_separation += tag_value + ","

    if tag_separation:
        tag_separation = tag_separation[:-1]

    return tag_separation;

def formTagComparison(prev, now):
    if len(prev) != len(now):
        return False
    for p, n in zip(prev, now):
        prev_value = str(p['value'])
        now_value = str(n['tag_name'])

        if prev_value != now_value:
            return False
    return True

def userTitleAlreadyUse(title, category):

    exist = db.execute("SELECT title_name FROM links WHERE title_name = ? AND folder_category = ?", title, category)
    if len(exist) > 0:
        return True
    return False


def tagsExist(tag):
    exist = db.execute("SELECT tag_name FROM tags WHERE tag_name = ?", (tag,))

    return len(exist) > 0


def  getTagDict(title_name):
    all_tags = db.execute("SELECT tags.tag_name, tags.tag_id FROM tags JOIN PostTag  ON PostTag.tag_id = tags.tag_id JOIN links  ON links.link_id = PostTag.link_id WHERE links.title_name = ?", title_name)
    list_tag = []

    for tag in all_tags:
        tag_value = tag['tag_name']
        tag_id = tag['tag_id']
        dict_ = {}
        dict_[tag_id] = tag_value
        list_tag.append(dict_)

    return list_tag


def removeDuplicateList(list_):
    temp_list = []

    for l in list_:
        if l not in temp_list:
            temp_list.append(l)
    return temp_list




