from flask import render_template, request, redirect, session

admin_flag = False


def login_func(app, connection):
    """Contine functionalitatile login-ului"""
    @app.route('/')
    def login():
        session['admin_flag'] = False
        session['username'] = ''
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect('/')

    @app.route('/login', methods=['POST'])
    def login_managing():
        session['admin_flag'] = False
        cursor = connection.cursor()
        cursor.execute('SELECT username, password FROM angajati')

        username = request.form.get('username')
        password = request.form.get('password')

        users = [item for item in cursor]
        cursor.close()
        if (username, password) == ('admin', 'adminpass'):
            session['admin_flag'] = True
            return redirect('/admin')
        elif (username, password) in users:
            session['username'] = username
            return redirect('/imprumuturi')
        else:
            return render_template('login.html', error=1)
