from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__) # Flask Application Initialization- Creates an instance of the Flask application. __name__ tells Flask where to look for resources.

# Connect to SQLite Database
def init_db():        # init_db(): Initializes the SQLite database. It connects to a database file named database.db and creates a users table with columns: id, name, and email. If the table already exists, it won't create a new one (IF NOT EXISTS).
    conn = sqlite3.connect('database.db') # SQLite Connection: Uses sqlite3.connect() to connect to the database and a cursor (conn.cursor()) to execute SQL commands.
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    conn.commit()
    conn.close()

# Home page
@app.route('/')   # Route @app.route('/'): Defines the home page URL (/).
def index():      # 
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users') # Retrieves all the users from the users table with SELECT * FROM users.
    users = c.fetchall() # Fetches the data with c.fetchall(), which returns all rows in the table.
    conn.close()         # Closes the connection to the database.
    return render_template('index.html', users=users) # Passes the retrieved users data to the index.html template to be rendered.

# Add user
@app.route('/add', methods=['POST']) # @app.route('/add', methods=['POST']): Defines a POST route for adding users.

def add_user():
    name = request.form.get('name') # Retrieves the user's name and email from the form submitted in the POST request using request.form.get().
    email = request.form.get('email')
    conn = sqlite3.connect('database.db') # Connects to the SQLite database and inserts the new user into the users table with INSERT INTO users (name, email) VALUES (?, ?) where ? are placeholders for user input.
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Run the application
if __name__ == '__main__': # if __name__ == '__main__':: This ensures that the application runs only when the script is executed directly (not when imported as a module).
    init_db()              # init_db(): Initializes the database when the application starts.
    app.run(debug=True)    # app.run(debug=True): Starts the Flask web server with debugging enabled. This allows the application to automatically reload on code changes and provides helpful error messages
