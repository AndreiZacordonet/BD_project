from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user data for illustration
users = {'admin': {'password': 'admin_password', 'role': 'admin'}}


def is_authenticated():
    return 'username' in session


def requires_authentication(func):
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def home():
    return 'Welcome to the home page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and password == users[username]['password']:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid login credentials'

    return render_template('login.html')


@app.route('/dashboard')
@requires_authentication
def dashboard():
    return 'Welcome to the dashboard'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
