from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

# Configure a secret key for session management
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the LoginManager
login_manager = LoginManager(app)

# Sample User class for demonstration purposes.
# In a real application, you would use your database model for the User.
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# A mock user database for demonstration purposes.
# In a real application, you would query your database for the user based on their credentials.
users = {'user1': {'password': 'password123'},
         'user2': {'password': 'qwerty'}}

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# Dashboard route (requires login)
@app.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome, {current_user.id}! This is your dashboard."

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
