from flask import render_template, request, redirect


def login_func(app, connection):
    """Contine functionalitatile login-ului"""
    @app.route('/')
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def login_managing():
        cursor = connection.cursor()
        cursor.execute('SELECT username, password FROM angajati')

        username = request.form.get('username')
        password = request.form.get('password')

        users = [item for item in cursor]
        cursor.close()
        if (username, password) == ('admin', 'adminpass'):
            return redirect('/admin')
        elif (username, password) in users:
            return redirect('/persoane')
        else:
            return render_template('login.html', error=1)
