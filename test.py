from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user data for illustration
users = {'admin': {'password': 'admin_password', 'role': 'admin'}}


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
            return redirect(url_for('admin'))
        else:
            return 'Invalid login credentials'

    return render_template('login.html')


@app.route('/admin')
def admin():
    if 'username' in session:
        # Check user role before granting access to the admin page
        if users[session['username']]['role'] == 'admin':
            return 'Welcome to the admin page'
        else:
            return 'You do not have permission to access this page'
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
