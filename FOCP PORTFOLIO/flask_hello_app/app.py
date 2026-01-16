from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dev-secret-key" # Keeps our login sessions secure

# --- Lab 5: Our User Database ---
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "student": {"password": "student123", "role": "user"}
}

# --- Lab 3 & 4: Behind-the-Scenes Logic ---
def add_language(language_list, new_lang):
    if new_lang and new_lang.capitalize() not in language_list:
        language_list.append(new_lang.capitalize())
        return f"{new_lang} has been added to your list!"
    return "That language is either blank or already exists."

def delete_selected_languages(language_list, selected):
    if not selected:
        return "You didn't select anything to delete."
    count = 0
    for lang in selected:
        if lang in language_list:
            language_list.remove(lang)
            count += 1
    return f"Successfully removed {count} language(s)."

def sort_languages(language_list):
    language_list.sort()
    return "List sorted alphabetically!"

# --- The Routes (The Pages) ---

@app.route('/')
def home():
    return render_template("index.html", title="Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['role'] = USERS[username]['role']
            return redirect(url_for('home'))
        message = "Login failed. Check your username or password."
    return render_template("login.html", title="Login", message=message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- This was the missing Greet logic! ---
@app.route('/greet', methods=['GET', 'POST'])
def greet():
    message, string_ops = None, None
    if request.method == 'POST':
        name = request.form.get('name')
        if name and name.strip():
            message = f"Welcome, {name.title()}!"
            string_ops = {
                "Uppercase": name.upper(),
                "Lowercase": name.lower(),
                "Reversed": name[::-1],
                "Length": len(name)
            }
        else:
            message = "Please enter a name so I can work my magic."
    return render_template("greet.html", title="Greet", message=message, string_ops=string_ops)

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    # If the user isn't logged in, kick them back to the login page
    if 'username' not in session:
        return redirect(url_for('login'))

    is_admin = session.get('role') == 'admin'
    
    # Setting up the initial list
    if 'languages' not in globals():
        global languages
        languages = ["Python", "C++", "JavaScript", "Go"]

    message = None
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            message = add_language(languages, request.form.get('language'))
        
        # Only the admin can use these two buttons
        elif action == 'delete_selected' and is_admin:
            selected = request.form.getlist('selected_languages')
            message = delete_selected_languages(languages, selected)
        
        elif action == 'clear' and is_admin:
            languages.clear()
            message = "The list is now empty."
            
        elif action == 'sort':
            message = sort_languages(languages)
        else:
            message = "You don't have permission to do that!"

    return render_template("favorites.html", title="Favorites", 
                           languages=languages, message=message, is_admin=is_admin)

if __name__ == '__main__':
    app.run(debug=True)