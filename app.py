from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from helper import * 
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
import os

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

@app.route("/home")
@login_required
def home():
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
    folder_list = db.execute("SELECT f.folder_name, si.src_path FROM folders AS f JOIN src_img AS si ON f.folder_category_id = si.src_id WHERE f.user_id = ?",  user_id[0]["user_id"])
    query = """
    SELECT links.title_name, folders.folder_name, REPLACE(links.title_name, ' ', '-') AS title_path
    FROM links
    JOIN folders ON links.folder_id = folders.folder_id
    JOIN users ON folders.user_id = users.user_id
    WHERE users.user_id = ?
    """
    new_post_list = db.execute(query, (user_id[0]["user_id"]))
    full_name = db.execute("SELECT first_name || ' ' || last_name AS full_name FROM users WHERE user_id = ?", user_id[0]["user_id"] )
    return render_template("home.html", username = username, folder_list = folder_list, new_post_list = new_post_list, full_name = full_name[0])


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



    if request.method == "POST":
        folder_choice = request.form.get("folders")
        title = request.form.get("title")
        link = request.form.get("link")
        description  = request.form.get("description")
        tags = request.form.get("tags")
    

        if folder_choice == None:
            error_message_folder = "Folder named folder is not available"
            all_error.append(error_message_folder)
            


        if title == "":
            error_message_title = "Title cannot be empty"
            all_error.append(error_message_title)

        elif link_verifier(title):
            error_message_title = "Title must not be an URL"
            all_error.append(error_message_title)
         

        elif len(title) < 5:
            error_message_title = "Title must be 5 characters above"
            all_error.append(error_message_title)
        
        if link == "":
            error_message_link = "Link cannot be empty"
            all_error.append(error_message_link)


        elif not link_verifier(link):
            error_message_link = "Your Link is Detected Invalid"
            all_error.append(error_message_link)
        

        if description == "":
            error_message_description = "Description cannot be empty"
            all_error.append(error_message_description)


        elif len(description) < 30:
            error_message_description = "Too short, must be 30 characters above"
            all_error.append(error_message_description)


        if tags == tags.endswith(","):
            error_message_tags = "Dont end with comma"
            all_error.append(error_message_tags)



        if len(all_error) != 0:
            title_value = title
            folder_value = folder_choice
            link_value =link
            description_value = description
            tags_value =tags

            return render_template("upload.html", folders = folders_list, all_errors=all_error, folder_value = folder_value, title_value = title_value, link_value = link_value, description_value = description_value, tags_value = tags_value, username = username)
        
        else:
            folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_choice, user_id)
            db.execute("INSERT INTO links(title_name, link_url, folder_category, description, folder_id, date) VALUES (?, ?, ?, ?, ?, ?)",
            title, link, folder_choice, description, folder_id[0]['folder_id'], getLinkTime())
            date = database_date_format(getDate())
            history = f'Added a new post titled "{title}" under {folder_choice} category'
            history_type = "POST"
            time = getTime()
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
            return redirect("/home")
                  
    return render_template("upload.html", folders = folders_list, username = username)



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
        username = session["user_id"]
        user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
        folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_name, user_id)
        post_contents = db.execute("SELECT title_name FROM links WHERE folder_id = ?", folder_id[0]["folder_id"])
        title_path_list = getTitlePath(post_contents)
        title_data = list_of_dict_title_data(post_contents, title_path_list)


        other_folders = db.execute("SELECT folders.folder_name, src_img.src_id FROM folders JOIN src_img ON folders.folder_category_id = src_img.src_id WHERE folders.user_id = ? ORDER BY folders.folder_id DESC LIMIT 5", user_id)
        return render_template("folder-post.html", post_contents = title_data, other_folders = other_folders, current_folder = folder_name)


@app.route("/home/folder/<folder_name>/delete-post/<title>")
@login_required
def deletePost(folder_name, title):
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_name, user_id)[0]["folder_id"]
    db.execute("DELETE FROM links WHERE folder_id = ? AND title_name = ?", folder_id, title)
    date = database_date_format(getDate())
    history = f'Deleted a post titled "{title}" under the "{folder_name}" category.'
    history_type = "POST"
    time = getTime()
    db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
    return redirect(url_for('folder', folder_name=folder_name))


@app.route("/home/folder/<folder_name>/post/<title>", methods=["GET", "POST"])
@login_required
def viewPost(folder_name, title):
    path_title = title
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
    folders = db.execute("SELECT folder_name FROM folders WHERE user_id = ?", user_id[0]["user_id"])
    folders_list = []
    for folder in folders:
        folders_list.append(folder["folder_name"])



    title_name = title.replace("-", " ")
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", folder_name, user_id)[0]["folder_id"]
    folder_id = int(folder_id)
    title_name = str(title_name)
    post_contents = db.execute("SELECT title_name, link_url, description FROM links  WHERE folder_id = ? AND title_name = ? ", folder_id, title_name)[0]
    other_latest_post = db.execute("SELECT links.title_name FROM links JOIN folders ON links.folder_id = folders.folder_id JOIN users ON folders.user_id = users.user_id WHERE users.user_id = ? AND links.title_name != ?",  user_id, title_name)
    
    date = database_date_format(getDate())
    time = getTime()
    history_type = "POST"
   
    if request.method == "POST":

       
        form_title = request.form.get('title')
        form_folder = request.form.get('folders')
        form_link = request.form.get('link')
        form_description = request.form.get('description')

        form_title = form_title.replace(" ", "-")


        date = database_date_format(getDate())
        time = getTime()
        history_type = "POST"

       
        if form_title != title_name:
            form_title = form_title.replace("-", " ")
            path_title = form_title.replace(" ", "-")
            db.execute("UPDATE links SET title_name = ? WHERE folder_id = ?", form_title, folder_id)
            history = f'Edited the post title "{title_name}" to "{form_title}" under the "{folder_name}" category.'
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)

        
        if post_contents['link_url'] != form_link:
            db.execute("UPDATE links SET link_url = ? WHERE folder_id = ?", form_link, folder_id)
            history = f'Updated the link with the title "{form_title}" in the "{folder_name}" category.'
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)


        if post_contents['description'] != form_description:
            db.execute("UPDATE links SET description = ? WHERE folder_id = ?", form_description, folder_id)
            history = f'Updated the description with the title "{form_title}" in the "{folder_name}" category.'
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
        
        if form_folder != folder_name:
            new_folder_id = db.execute("SELECT folder_id FROM folders WHERE folder_name = ? AND user_id = ?", form_folder, user_id)[0]["folder_id"]
            db.execute("UPDATE links SET folder_category = ?, folder_id = ? WHERE folder_id = ? AND title_name = ?", form_folder , new_folder_id, folder_id, title_name)
            history = f'Moved the post titled "{form_title}" to the "{form_folder}" category.'
            db.execute("INSERT INTO user_history(date, history, user_id, history_type, time) VALUES(?, ?, ?, ?, ?)", date, history, user_id, history_type, time)
            
        return redirect(f'/home/folder/{form_folder}/post/{path_title}')

    
    return render_template("post.html", title_name = title_name, post_contents = post_contents, folder_name = folder_name, folders = folders_list, other_latest_post = other_latest_post)



@app.route("/history/<type>")
@login_required
def history(type):
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    organized_history = {}

    if str(type) == "account":
        records = db.execute("SELECT date, time, history FROM user_history WHERE user_id = ? AND history_type = ? ORDER BY date DESC, time DESC, history_id DESC", user_id, str(type).upper())
        for record in records:
            history = record['history']
            time = record['time']
            date_record = record['date']
            date = history_date_format(date_record)
        
            if date in organized_history:
                organized_history[date].append((history, time))
            else:
                organized_history[date] = [(history, time)]
        return render_template("history.html", organized_history = organized_history)
    
    elif str(type) == "categories":
        records = db.execute("SELECT date, time, history FROM user_history WHERE user_id = ? AND history_type = ? ORDER BY date DESC, time DESC, history_id DESC", user_id, str(type).upper())
        for record in records:
            history = record['history']
            time = record['time']
            date_record = record['date']
            date = history_date_format(date_record)
        
            if date in organized_history:
                organized_history[date].append((history, time))
            else:
                organized_history[date] = [(history, time)]
        return render_template("history.html", organized_history = organized_history)
    
    elif str(type) == "post":
        records = db.execute("SELECT date, time, history FROM user_history WHERE user_id = ? AND history_type = ? ORDER BY date DESC, time DESC, history_id DESC", user_id, str(type).upper())
        for record in records:
            history = record['history']
            time = record['time']
            date_record = record['date']
            date = history_date_format(date_record)
        
            if date in organized_history:
                organized_history[date].append((history, time))
            else:
                organized_history[date] = [(history, time)]
        return render_template("history.html", organized_history = organized_history)


@app.route("/search", methods=["GET"])
@login_required
def search():
    search_query = request.args.get("q")
    username = session["user_id"]
    user_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]["user_id"]
    search_result = db.execute(
    "SELECT links.title_name, folder_category , REPLACE(title_name, ' ', '-') AS title_path FROM links "
    "JOIN folders ON folders.folder_id = links.folder_id "
    "JOIN users ON folders.user_id = users.user_id "
    "WHERE title_name LIKE ? OR description LIKE ? AND users.user_id = ?",
    '%' + search_query + '%', '%' + search_query + '%', user_id
)
    newest_folders = db.execute("SELECT folders.folder_name, src_img.src_id FROM folders JOIN src_img ON folders.folder_category_id = src_img.src_id WHERE user_id = ? ORDER BY folder_id DESC", user_id)

    return render_template("search.html", search_result = search_result, newest_folders = newest_folders)

if __name__ == '__main__':
      app.run(debug=True)