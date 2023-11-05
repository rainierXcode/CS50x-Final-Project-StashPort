from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from helper import * 
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
import os
import json

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///stashport.db")

@app.route('/', methods=["GET", "POST"])
def loginUI():
    error_message_username = None 
    error_message_password = None 
    have_error = False
    login_success = True

    if session.get("user_id"):
        return redirect("/home")
    
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
            username_exist = db.execute("SELECT * FROM users WHERE username = ?", username)
            if  not username_exist:
                error_message_username = "Username does not exist"
                have_error = True
                login_success = False

            else:
               stored_password_hash = username_exist[0]["password"]
               if not check_password_hash(stored_password_hash, password):
                error_message_password = "Password is invalid"
                have_error = True 
                login_success = False
        
        if have_error:
            return render_template("login.html", username_error=error_message_username, password_error=error_message_password, username_value=username, password_value=password)
        
        if login_success:
            session["user_id"] = username
            user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
            date = database_date_format(getDate())
            history = "Signed in."
            history_type = "ACCOUNT"
            time = getTime()
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
            return redirect("/home")


    return render_template("login.html")





@app.route('/signup', methods=["GET", "POST"])
def signUI():
    if request.method == "POST":
        error_message_fName = None
        error_message_lName = None
        error_message_username = None
        error_message_password = None
        error_message_password_confirm = None

        fName = request.form.get("fname")
        lName = request.form.get("lname")
        username = request.form.get("username-signup")
        password = request.form.get("password-signup")
        confirm_password = request.form.get("confirm-password-signup")
        have_error = False

        if fName == "":
            error_message_fName = "First name cannot be empty"
            have_error = True

        elif len(fName) < 3:
            error_message_fName = "First name must be at least 4 characters"
            have_error = True

        if lName == "":
            error_message_lName = "Last name cannot be empty"
            have_error = True

        elif len(lName) < 2:
            error_message_lName = "Last name must be at least 2 characters"
            have_error = True

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

        if confirm_password == "":
            error_message_password_confirm =  "Confirm Password cannot be empty"
            have_error = True

        elif len(confirm_password) < 6:
            error_message_password_confirm = "Password must be at least 6 characters"
            have_error = True
        
        
        if not have_error:
            username_exist = db.execute("SELECT username FROM users WHERE username = ?", username)
            if username_exist:
                error_message_username = "Username already exists"
                have_error = True
            
            elif confirm_password != password:
                error_message_password_confirm = "Password does not match"
                have_error = True
            
        
        if have_error:
            return render_template("signup.html", fname_error = error_message_fName, lname_error= error_message_lName, username_error = error_message_username, password_error = error_message_password , confirm_pass_error = error_message_password_confirm,fname_value = fName, lname_value = lName, username_value = username, password_value= password, confirm_password_value = confirm_password)
        
        hash_pass=generate_password_hash(password);
        db.execute("INSERT INTO users(first_name, last_name, username, password, date_created, time_created) VALUES( ?, ?, ?, ?, ?, ?)", fName, lName, username, hash_pass, getDate(), getTime() )
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
        date = database_date_format(getDate())
        history = "Created an account."
        history_type = "ACCOUNT"
        time = getTime()
        db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
        return redirect("/")
        

        
    return render_template("signup.html")

@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    folder_list = db.execute(
    "SELECT f.folder_name, si.src_path, REPLACE(f.folder_name, ' ', '_') AS folder_path , f.folder_id FROM folders AS f JOIN src_img AS si ON f.folder_category_id = si.src_id WHERE f.user_id = ?",
    user_id
)
    if request.method == "POST":
        new_folder_name = request.form.get("folder_name")
        username = session["user_id"]
        img_select = request.form.get("selected_image_add")
        folder_category_id = extractNum(img_select)


        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
        db.execute("INSERT INTO folders(folder_category_id, folder_name, user_id) VALUES(? ,?, ?)",  folder_category_id, new_folder_name, user_id)
        date = database_date_format(getDate())
        history = f'Established a new category named "{new_folder_name}."'
        history_type = "CATEGORIES"
        time = getTime()
        db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
        return redirect("/home")
    
    query = """
    SELECT links.title_name, folders.folder_name, REPLACE(links.title_name, ' ', '_') AS title_path
    FROM links
    JOIN folders ON links.folder_id = folders.folder_id
    JOIN users ON folders.user_id = users.user_id
    WHERE users.user_id = ? ORDER BY links.link_id DESC
    """
    new_post_list = db.execute(query, (user_id))
    full_name = db.execute("SELECT first_name || ' ' || last_name AS full_name FROM users WHERE user_id = ?", user_id)
    current_avatar_path = db.execute("SELECT src_avatar.avatarPath FROM src_avatar JOIN  users ON users.avatarID = src_avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']

    all_avatar_path = all_avatar_path = db.execute("SELECT avatarPath FROM src_avatar")
    current_avatar = db.execute("SELECT avatar.avatarPath FROM src_avatar AS avatar JOIN users ON users.avatarID = avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
    current_avatar_path = db.execute("SELECT src_avatar.avatarPath FROM src_avatar JOIN  users ON users.avatarID = src_avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']

    return render_template("home.html", username = username, folder_list = folder_list, new_post_list = new_post_list, full_name = full_name[0], current_avatar_path = current_avatar_path,  all_avatar_path = all_avatar_path, current_avatar = current_avatar)


@app.route("/home/update-category", methods=["GET", "POST"])
def updateCategory():
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    if request.method == "POST":
        selected_img = request.form.get("selected_image_edit")
        new_name = request.form.get("folder_name_inputinEdit")
        folder_id = int(request.form.get("folder_id"))

        old_name = db.execute("SELECT folder_name FROM folders WHERE folder_id = ?", folder_id)[0]['folder_name']
        date = database_date_format(getDate())
        history = f'Change category {old_name} to {new_name}'
        history_type = "ACCOUNT"
        time = getTime()
        db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)

        category_id = db.execute("SELECT src_id FROM src_img WHERE src_path = ?", selected_img)[0]['src_id']
        db.execute("UPDATE folders SET folder_category_id = ?, folder_name =  ? WHERE user_id = ? AND folder_id = ?", category_id, new_name, user_id, folder_id)
        return redirect("/home")
    return redirect("/home")

@app.route("/logout")
def logout():
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    date = database_date_format(getDate())
    history = "Logged out."
    history_type = "ACCOUNT"
    time = getTime()
    db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
    session["user_id"] = None
    return redirect("/")





        
@app.route("/home/upload", methods=["GET", "POST"])
@login_required
def upload():
    error_message_folder = None
    error_message_title = None
    error_message_link = None
    error_message_description = None
    error_message_tags = None
    folder_value = None
    title_value = None
    link_value = None
    description_value = None
    tags_value = None
    

    all_error = []

    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ?", user_id)
    folders_list = []
    for folder in folders:
        folders_list.append(folder["folder_name"])

    
    latest_category = db.execute("SELECT folder_name FROM folders WHERE user_id = ? ORDER BY folder_id DESC LIMIT 1", user_id)

    if latest_category is not None and len(latest_category) > 0:
        latest_category = latest_category[0]['folder_name']

    count_post = db.execute("SELECT COUNT(links.title_name) AS count FROM links JOIN folders  ON links.folder_id = folders.folder_id WHERE folders.user_id = ?", user_id)[0]['count']
    count_categories = db.execute("SELECT COUNT(folder_name) AS count FROM folders WHERE user_id = ?", user_id)[0]['count']

        
    all_avatar_path = all_avatar_path = db.execute("SELECT avatarPath FROM src_avatar")
    current_avatar = db.execute("SELECT avatar.avatarPath FROM src_avatar AS avatar JOIN users ON users.avatarID = avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
    other_folders = db.execute("SELECT folders.folder_name, src_img.src_id FROM folders JOIN src_img ON folders.folder_category_id = src_img.src_id WHERE folders.user_id = ? ORDER BY folders.folder_id DESC LIMIT 5", user_id)
    current_avatar_path = db.execute("SELECT src_avatar.avatarPath FROM src_avatar JOIN  users ON users.avatarID = src_avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']


    if request.method == "POST":
        folder_choice = request.form.get("folders")
        title = request.form.get("title")
        link = request.form.get("link")
        description  = request.form.get("description")
        tags = request.form.get("tags")

        all_error = uploadReadError(folder_choice, title, link, description, tags, user_id, None)

        if len(all_error) != 0:
            title_value = title
            folder_value = folder_choice
            link_value =link
            description_value = description
            tags_value =tags
            latest_category = folder_value

            return render_template("upload.html", folders = folders_list, all_errors=all_error, folder_value = folder_value, title_value = title_value, link_value = link_value, description_value = description_value, tags_value = tags_value, username = username, latest_category = latest_category, count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path)
        
        else:
            folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_choice, user_id)[0]['folder_id']
            db.execute("INSERT INTO links(title_name, link_url, description, folder_id, date) VALUES (?, ?, ?, ?, ?)",
            title, link, description, folder_id, getLinkTime()) 
            date = database_date_format(getDate())
            history = f'Added a new post titled "{title}" under {folder_choice} category'
            history_type = "POST"
            time = getTime()
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
            link_id = db.execute("SELECT MAX(link_id) AS id FROM links")[0]['id']

            tag_num  = db.execute("SELECT tag_id FROM tags")
            if len(tags) > 0:
                tags_result = json.loads(tags)
                tags_result = removeDuplicateList(tags_result)
                for tag in tags_result:
                    tag_value = tag['value']

                    if len(tag_num )==0:
                        db.execute("INSERT INTO tags(tag_name) VALUES(?)", tag_value)
                        tag_num  = db.execute("SELECT tag_id FROM tags")
                        tag_id = db.execute("SELECT tag_id FROM tags WHERE tag_name = ?", tag_value)[0]['tag_id']
                    else:
                        if tagsExist(tag_value):
                            tag_id = db.execute("SELECT tag_id FROM tags WHERE tag_name = ?", tag_value)[0]['tag_id']
                            
                        
                        else:
                            db.execute("INSERT INTO tags(tag_name) VALUES(?)", tag_value)
                            tag_id = db.execute("SELECT tag_id FROM tags WHERE tag_name = ?", tag_value)[0]['tag_id']
                    db.execute("INSERT INTO PostTag(link_id, tag_id, user_id) VALUES(?, ?, ?)", link_id, tag_id, user_id)
                        
                    
          
            return redirect("/home")
                  
    return render_template("upload.html", folders = folders_list, username = username, latest_category = latest_category, count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path)



@app.route("/home/upload/addfolder", methods=["GET", "POST"])
@login_required
def addFolder():
    if request.method == "POST":
        new_folder_name = request.form.get("folder_name")
        username = session["user_id"]
        img_select = request.form.get("selected_image")
        img_select = os.path.basename(img_select)
        folder_category_id = extractNum(img_select)
        
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
        db.execute("INSERT INTO folders(folder_category_id, folder_name, user_id) VALUES(? ,?, ?)",  folder_category_id, new_folder_name, user_id)
        date = database_date_format(getDate())
        history = f'Established a new category named "{new_folder_name}."'
        history_type = "CATEGORIES"
        time = getTime()
        db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
       
      
        return redirect("/home/upload")
    return redirect("/home/upload")

@app.route("/home/folder/<folder_name>")
@login_required
def folder(folder_name):
        folder_name = str(folder_name)
        folder_name =folder_name.replace("_", " ")
        username = session["user_id"]
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
        folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_name, user_id)
        post_contents = db.execute("SELECT title_name FROM links WHERE folder_id = ? ORDER BY link_id DESC", folder_id[0]["folder_id"])
        title_path_list = getTitlePath(post_contents)
        title_data = list_of_dict_title_data(post_contents, title_path_list)

        count_post = db.execute("SELECT COUNT(links.title_name) AS count FROM links JOIN folders  ON links.folder_id = folders.folder_id WHERE folders.user_id = ?", user_id)[0]['count']
        count_categories = db.execute("SELECT COUNT(folder_name) AS count FROM folders WHERE user_id = ?", user_id)[0]['count']

        
        all_avatar_path = all_avatar_path = db.execute("SELECT avatarPath FROM src_avatar")
        current_avatar = db.execute("SELECT avatar.avatarPath FROM src_avatar AS avatar JOIN users ON users.avatarID = avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
        other_folders = db.execute("SELECT folders.folder_name, src_img.src_id FROM folders JOIN src_img ON folders.folder_category_id = src_img.src_id WHERE folders.user_id = ? ORDER BY folders.folder_id DESC LIMIT 5", user_id)
        current_avatar_path = db.execute("SELECT src_avatar.avatarPath FROM src_avatar JOIN  users ON users.avatarID = src_avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
        folder_name = folder_name.replace(" ", "_")
        return render_template("folder-post.html", username=username,post_contents = title_data, other_folders = other_folders, current_folder = folder_name, count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path)


@app.route("/home/folder/<folder_name>/post/<title>", methods=["GET", "POST"])
@login_required
def viewPost(folder_name, title):
    folder_name = str(folder_name)
    folder_name = folder_name.replace("_", " ")
    path_title = title
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
    folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ?", user_id[0]["user_id"])
    folders_list = []
    for folder in folders:
        folders_list.append(folder["folder_name"])



    title_name = title.replace("_", " ")
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]

    folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_name, user_id)[0]["folder_id"]
    folder_id = int(folder_id)
    title_name = str(title_name)
    post_contents = db.execute("SELECT title_name, link_url, description FROM links  WHERE folder_id = ? AND title_name = ? ", folder_id, title_name)[0]
    other_latest_post = db.execute("SELECT links.title_name FROM links JOIN folders ON links.folder_id = folders.folder_id JOIN users ON folders.user_id = users.user_id WHERE users.user_id = ? AND links.title_name != ? AND folders.folder_name = ? ORDER BY links.link_id DESC LIMIT 15",  user_id, title_name, folder_name)

    title_path_list = getTitlePath(other_latest_post)
    title_data = list_of_dict_title_data(other_latest_post, title_path_list)
    
    date = database_date_format(getDate())
    time = getTime()
    history_type = "POST"

    count_post = db.execute("SELECT COUNT(links.title_name) AS count FROM links JOIN folders  ON links.folder_id = folders.folder_id WHERE folders.user_id = ?", user_id)[0]['count']
    count_categories = db.execute("SELECT COUNT(folder_name) AS count FROM folders WHERE user_id = ?", user_id)[0]['count']

        
    all_avatar_path = all_avatar_path = db.execute("SELECT avatarPath FROM src_avatar")
    current_avatar = db.execute("SELECT avatar.avatarPath FROM src_avatar AS avatar JOIN users ON users.avatarID = avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
    other_folders = db.execute("SELECT folders.folder_name, src_img.src_id FROM folders JOIN src_img ON folders.folder_category_id = src_img.src_id WHERE folders.user_id = ? ORDER BY folders.folder_id DESC LIMIT 5", user_id)
    current_avatar_path = db.execute("SELECT src_avatar.avatarPath FROM src_avatar JOIN  users ON users.avatarID = src_avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
    link_id = db.execute("SELECT links.link_id FROM links JOIN folders ON links.folder_id = folders.folder_id WHERE folders.folder_name = ? AND folders.user_id = ? AND links.title_name = ?", folder_name, user_id, title_name)[0]['link_id']
    all_tags = db.execute("SELECT tags.tag_name, tags.tag_id FROM tags JOIN PostTag ON PostTag.tag_id = tags.tag_id JOIN links ON links.link_id = PostTag.link_id WHERE links.link_id = ?", link_id)

    tag_separation = getTagSeperation(all_tags)

    if request.method == "POST":

        all_error = []
        form_title = request.form.get('title')
        form_folder = request.form.get('folders')
        form_link = request.form.get('link')
        form_description = request.form.get('description')
        form_tags = request.form.get("tags")
        form_title = form_title.replace("_", " ")
        form_folder = form_folder.replace("_", " ")
      

        tag_num  = db.execute("SELECT tag_id FROM tags")


        date = database_date_format(getDate())
        time = getTime()
        history_type = "POST"

        all_error = uploadReadError(form_folder, form_title, form_link, form_description, form_tags, user_id, title_name)    

        if len(all_error) != 0:
                title_path = title_name.replace(" ", "_")         
                folder_path = folder_name.replace(" ", "_")
                title_path = title_name.replace(" ", "_")
                return render_template("post.html", all_errors = all_error, username = username,title_name = title_name, post_contents = post_contents, folder_name = folder_name, folders = folders_list, other_latest_post = title_data, count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path, current_folder = folder_name, all_tags = all_tags, tag_separation = tag_separation, folder_path =folder_path, title_path = title_path)


       
        if form_title != title_name:
            form_title = form_title.replace("_", " ")
            path_title = form_title.replace(" ", "_")
            db.execute("UPDATE links SET title_name = ? WHERE folder_id = ? AND link_id = ?", form_title, folder_id, link_id)
            history = f'Edited the post title "{title_name}" to "{form_title}" under the "{folder_name}" category.'
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)

        
        if post_contents['link_url'] != form_link:
            db.execute("UPDATE links SET link_url = ? WHERE folder_id = ?  AND link_id = ?", form_link, folder_id, link_id)
            history = f'Updated the link with the title "{form_title}" in the "{folder_name}" category.'
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)


        if post_contents['description'] != form_description:
            db.execute("UPDATE links SET description = ? WHERE folder_id = ?  AND link_id = ?", form_description, folder_id, link_id)
            history = f'Updated the description with the title "{form_title}" in the "{folder_name}" category.'
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
        
        if form_folder != folder_name:
            new_folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", form_folder, user_id)[0]["folder_id"]
            db.execute("UPDATE links SET folder_id = ? WHERE folder_id = ? AND title_name = ?",  new_folder_id, folder_id, title_name) 
            history = f'Moved the post titled "{form_title}" to the "{form_folder}" category.'
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)

        
        if len(form_tags) > 0:
            tags_result = json.loads(form_tags)


            for form in tags_result:
                form_value = form['value']

                if not tagsExist(form_value):
                    db.execute("INSERT into tags(tag_name) VALUES(?)", form_value)

            if len(tags_result) == len(all_tags):
                for tag, form in zip(all_tags, tags_result):
                    form_value = form['value']
                    tag_value = tag['tag_name']

                    if form_value != tag_value:
                        tag_id = db.execute("SELECT tag_id FROM tags WHERE tag_name = ?", form_value)[0]['tag_id']
                        PostTagID = db.execute("SELECT PostTag.ID  FROM PostTag JOIN links ON links.link_id = PostTag.link_id  JOIN tags ON tags.tag_id = PostTag.tag_id WHERE PostTag.user_id = ? AND links.title_name = ? AND tags.tag_name = ?", user_id, title_name, tag_value)[0]['ID']
                        db.execute("UPDATE PostTag SET tag_id = ? WHERE ID = ?", tag_id, PostTagID)

            elif  len(tags_result) > len(all_tags):
                for prev, latest in zip(all_tags, tags_result):
                    previous_tag = prev['tag_name']
                    latest_tag = latest['value']
                    if previous_tag != latest_tag:
                        PostTagID = db.execute("SELECT PostTag.ID  FROM PostTag JOIN links ON links.link_id = PostTag.link_id  JOIN tags ON tags.tag_id = PostTag.tag_id WHERE PostTag.user_id = ? AND links.title_name = ? AND tags.tag_name = ?", user_id, title_name, previous_tag)[0]['ID']
                        tag_id = db.execute("SELECT tag_id FROM tags WHERE tag_name = ?", latest_tag)[0]['tag_id']
                        db.execute("UPDATE PostTag SET tag_id = ? WHERE ID = ?", tag_id, PostTagID)
                        

                for i in range(len(all_tags), len(tags_result)):
                    form_value = tags_result[i]['value']
                    tag_id = db.execute("SELECT tag_id FROM tags WHERE tag_name = ?", form_value)[0]['tag_id']
                    db.execute("INSERT INTO PostTag(link_id, tag_id, user_id) VALUES(?, ?, ?)", link_id, tag_id, user_id)

            elif len(all_tags) > len(tags_result):
                tagIdList = []

                for tag in tags_result:
                    tag_value = tag['value']
                    tag_id = db.execute("SELECT tag_id FROM tags WHERE tag_name = ?", tag_value)[0]['tag_id']
                    tagIdList.append(tag_id)

                for prev, latest in zip(all_tags, tags_result):
                    previous_tag = prev['tag_name']
                    latest_tag = latest['value']

                    if previous_tag != latest_tag:
                        PostTagID = db.execute("SELECT PostTag.ID  FROM PostTag JOIN links ON links.link_id = PostTag.link_id  JOIN tags ON tags.tag_id = PostTag.tag_id WHERE PostTag.user_id = ? AND links.title_name = ? AND tags.tag_name = ?", user_id, title_name, previous_tag)[0]['ID']
                        tag_id = db.execute("SELECT tag_id FROM tags WHERE tag_name = ?", latest_tag)[0]['tag_id']
                        db.execute("UPDATE PostTag SET tag_id = ? WHERE ID = ?", tag_id, PostTagID)
                
               
                result = tuple(tagIdList) 
                db.execute("DELETE FROM PostTag WHERE link_id = ? AND tag_id NOT IN (?)", link_id, result)
               

        else:
            db.execute("DELETE FROM PostTag WHERE link_id = (SELECT link_id FROM links WHERE title_name = ?)", title_name)


                        
            
        return redirect(f'/home/folder/{form_folder}/post/{path_title}')

    folder_path = folder_name.replace(" ", "_")
    title_path = title_name.replace(" ", "_")
    return render_template("post.html", username = username,title_name = title_name, post_contents = post_contents, folder_name = folder_name, folders = folders_list, other_latest_post = title_data, count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path, current_folder = folder_name, all_tags = all_tags, tag_separation = tag_separation, folder_path =folder_path, title_path = title_path)



@app.route("/home/folder/<folder_name>/update-avatar", methods=["GET", "POST"])
@app.route("/home/folder/<folder_name>/post/<title>/update-avatar", methods=["GET", "POST"])
@app.route("/home/<upload>/update-avatar", methods=['GET', 'POST'])
@app.route("/history/<history>/update-avatar", methods=['GET', 'POST'])
@app.route("/home/update-avatar", methods=["GET", "POST"])
@login_required
def updateProfileInFolder(folder_name = None, title = None, search_query = None, upload=None , history = None):
    if request.method == "POST":
        avatar_select = request.form.get("selected_avatar")
        username = session["user_id"]
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
        current_avatar_path = db.execute("SELECT src_avatar.avatarPath FROM src_avatar JOIN users ON src_avatar.avatarID = users.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
        date = database_date_format(getDate())
        history_ = f'Avatar Updated'
        history_type = "ACCOUNT"
        time = getTime()
        db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history_, user_id, history_type, time)
        if str(current_avatar_path) != str(avatar_select):
            db.execute("UPDATE users SET avatarID = (SELECT src_avatar.avatarID  FROM src_avatar WHERE src_avatar.avatarPath = ? ) WHERE user_id = ?", avatar_select, user_id)
        if folder_name is not None and title is None:
            return redirect(url_for('folder', folder_name=folder_name))
        elif folder_name is not None and title is not None:
            return redirect(url_for('viewPost', folder_name=folder_name, title=title))
        
        elif upload is not None and upload == "upload":
            return redirect(url_for('upload'))
        
        elif history is not None:
            return redirect(url_for('history', type=history))
        else:
            return redirect("/home")



    

@app.route("/home/folder/<folder_name>/delete-post/<title>")
@login_required
def deletePost(folder_name, title):
    folder_name = str(folder_name)
    folder_name = folder_name.replace("_", " ")
    title_name = str(title)
    title_name = title_name.replace("_", " ")
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_name, user_id)[0]["folder_id"]
    link_id = db.execute("SELECT links.link_id FROM links  JOIN folders  ON folders.folder_id = links.folder_id WHERE links.title_name = ?  AND folders.folder_name = ?  AND folders.user_id = ?", title_name, folder_name, user_id)[0]['link_id'] 
    db.execute("DELETE FROM PostTag WHERE link_id = ?", link_id)
    db.execute("DELETE FROM links WHERE folder_id = ? AND title_name = ?", folder_id, title_name)
    date = database_date_format(getDate())
    history = f'Deleted a post titled "{title}" under the "{folder_name}" category.'
    history_type = "POST"
    time = getTime()
    db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
    return redirect(url_for('folder', folder_name=folder_name))



@app.route("/history/<type>")
@login_required
def history(type):
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    organized_history = {}

    count_post = db.execute("SELECT COUNT(links.title_name) AS count FROM links JOIN folders  ON links.folder_id = folders.folder_id WHERE folders.user_id = ?", user_id)[0]['count']
    count_categories = db.execute("SELECT COUNT(folder_name) AS count FROM folders WHERE user_id = ?", user_id)[0]['count']

    all_avatar_path = all_avatar_path = db.execute("SELECT avatarPath FROM src_avatar")
    current_avatar = db.execute("SELECT avatar.avatarPath FROM src_avatar AS avatar JOIN users ON users.avatarID = avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
    current_avatar_path = db.execute("SELECT src_avatar.avatarPath FROM src_avatar JOIN  users ON users.avatarID = src_avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']

    history_content = ['post', 'categories', 'account']

    if str(type) == "account":
        records = db.execute("SELECT date, time, history FROM user_history WHERE user_id = ? AND history_type = ? ORDER BY date DESC, history_id DESC", user_id, str(type).upper())
        for record in records:
            history = record['history']
            time = record['time']
            date_record = record['date']
            date = history_date_format(date_record)
        
            if date in organized_history:
                organized_history[date].append((history, time))
            else:
                organized_history[date] = [(history, time)]
        history = "account"
        return render_template("history.html",history = history,history_content = history_content, username = username,organized_history = organized_history, count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path)
    
    elif str(type) == "categories":
        records = db.execute("SELECT date, time, history FROM user_history WHERE user_id = ? AND history_type = ? ORDER BY date DESC, history_id DESC", user_id, str(type).upper())
        for record in records:
            history = record['history']
            time = record['time']
            date_record = record['date']
            date = history_date_format(date_record)
        
            if date in organized_history:
                organized_history[date].append((history, time))
            else:
                organized_history[date] = [(history, time)]
        history = "categories"
        return render_template("history.html",history = history,history_content = history_content,username = username, organized_history = organized_history,count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path)
    
    elif str(type) == "post":
        records = db.execute("SELECT date, time, history FROM user_history WHERE user_id = ? AND history_type = ? ORDER BY date DESC, history_id DESC", user_id, str(type).upper())
        for record in records:
            history = record['history']
            time = record['time']
            date_record = record['date']
            date = history_date_format(date_record)
        
            if date in organized_history:
                organized_history[date].append((history, time))
            else:
                organized_history[date] = [(history, time)]
        history = "post"
        return render_template("history.html",history=history, history_content = history_content,username = username,organized_history = organized_history, count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():


    search_query = request.args.get("q")
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]

    sql_query = """
    SELECT links.title_name, folders.folder_name, REPLACE(title_name, ' ', '_') AS title_path
    FROM links
    JOIN folders ON folders.folder_id = links.folder_id
    JOIN users ON folders.user_id = users.user_id
    WHERE (
        title_name LIKE '%' || ? || '%' OR title_name IN (
            SELECT title_name FROM links
            JOIN PostTag ON PostTag.link_id = links.link_id
            JOIN tags ON tags.tag_id = PostTag.tag_id
            WHERE tags.tag_name LIKE '%' || ? || '%'
        )
    ) AND users.user_id = ?
    ORDER BY links.link_id DESC
"""

    search_result = db.execute(sql_query, search_query,search_query, user_id)

    if len(search_query) > 5:
        sql_query = """
        SELECT links.title_name, folders.folder_name, REPLACE(title_name, ' ', '-') AS title_path
        FROM links
        JOIN folders ON folders.folder_id = links.folder_id
        JOIN users ON folders.user_id = users.user_id
        WHERE (title_name LIKE '%' || ? || '%' OR description  LIKE '%' || ? || '%') AND users.user_id = ? ORDER BY links.link_id DESC
        """
        search_result = db.execute(sql_query, search_query, search_query,user_id)

    newest_folders = db.execute("SELECT folders.folder_name, src_img.src_id FROM folders JOIN src_img ON folders.folder_category_id = src_img.src_id WHERE user_id = ? ORDER BY folder_id DESC", user_id)
    
    count_post = db.execute("SELECT COUNT(links.title_name) AS count FROM links JOIN folders  ON links.folder_id = folders.folder_id WHERE folders.user_id = ?", user_id)[0]['count']
    count_categories = db.execute("SELECT COUNT(folder_name) AS count FROM folders WHERE user_id = ?", user_id)[0]['count']

    all_avatar_path = all_avatar_path = db.execute("SELECT avatarPath FROM src_avatar")
    current_avatar = db.execute("SELECT avatar.avatarPath FROM src_avatar AS avatar JOIN users ON users.avatarID = avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
    current_avatar_path = db.execute("SELECT src_avatar.avatarPath FROM src_avatar JOIN  users ON users.avatarID = src_avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']

    if request.method == "POST":
        avatar_select = request.form.get("selected_avatar")
        username = session["user_id"]
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
        db.execute("UPDATE users SET avatarID = (SELECT src_avatar.avatarID  FROM src_avatar WHERE src_avatar.avatarPath = ? ) WHERE user_id = ?", avatar_select, user_id)
        current_avatar_path = db.execute("SELECT src_avatar.avatarPath FROM src_avatar JOIN  users ON users.avatarID = src_avatar.avatarID WHERE users.user_id = ?", user_id)[0]['avatarPath']
        return render_template("search.html",username=username, search_result = search_result,  search_query = search_query ,newest_folders = newest_folders,  count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path)

    return render_template("search.html",username=username, search_result = search_result,  search_query = search_query ,newest_folders = newest_folders,  count_post = count_post, count_categories = count_categories, all_avatar_path = all_avatar_path, current_avatar = current_avatar, current_avatar_path = current_avatar_path)



@app.route("/unavailable/<text>")
def unavailableThis(text):
    return render_template("unavailable.html", text=text)


if __name__ == '__main__':
      app.run(debug=True)