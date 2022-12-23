from flask import *
import sqlite3

#Start app
app = Flask(__name__)

#Function that takes a username and password and checks if it is a valid user
def check_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    #Get password of username
    cursor.execute(
        'SELECT password FROM login_info WHERE username=?', (username,)
    )
    result = cursor.fetchone()
    if result is not None:
        stored_password = result[0]
        if stored_password == password:
            return 'Login successful'
        else:
            return 'Incorrect password'
    else:
        #No return from sql query
        return 'Username not found'
    #Close connection
    conn.close()


#Function that registers a new user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    #Check if username already exists
    cursor.execute('SELECT * FROM login_info WHERE username=?', (username,))
    result = cursor.fetchone()
    if result is not None:
        #Found a user, user already exists
        return 'Username already exists'

    #Add new user
    cursor.execute(
        'INSERT INTO login_info (username, password) VALUES (?, ?)',
        (username, password)
    )
    #Commit this to the database and then close the connection
    conn.commit()
    conn.close()

    return 'User registered successfully'


#Redirects to login page
@app.route('/')
def index():
    return redirect(url_for("login"))


#Login page
@app.route('/login')
def login_page():
    return render_template('login.html')


#Register page
@app.route('/register')
def register_page():
    return render_template('register.html')


#POST request from login (attempted login)
@app.route('/login', methods=['POST'])
def login():
    #Get username and password from POST request
    username = request.form['username']
    password = request.form['password']

    #Return result of login
    return check_login(username, password)


#POST request from register (attempted registration)
@app.route('/register', methods=['POST'])
def register():
    #Get username and password from POST request
    username = request.form['username']
    password = request.form['password']

    #If they didn't fill in a field
    if not username or not password:
        return 'Username and password are required'

    #Password must be 8 characters, validation
    if len(password) < 8:
        return 'Password must be at least 8 characters long'

    #Return result of registration
    return register_user(username, password)


#Main method, must not be a library
if __name__ == '__main__':
    app.run()