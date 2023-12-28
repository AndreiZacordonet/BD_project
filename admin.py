from flask import render_template, request, redirect, session
from autentification import requires_authentication, requires_admin_role


def admin_func(app, connection):
    """Contine functionalitatile paginii admin"""
    @app.route('/admin', methods=['GET', 'POST'])
    @requires_authentication
    @requires_admin_role
    def admin():
        if request.method == 'POST':
            if request.form.get('insert_flag'):
                username = request.form.get('username')
                password = request.form.get('password')
                nume = request.form.get('nume')
                prenume = request.form.get('prenume')
                cnp = int(request.form.get('cnp'))
                functie = request.form.get('functie')
                values = {
                    'username': username,
                    'password': password,
                    'nume': nume,
                    'prenume': prenume,
                    'cnp': cnp,
                    'functie': functie
                }
                insert_query = '''
                            INSERT INTO angajati (username, password, nume, prenume, cnp, functie)
                            VALUES (:username, :password, :nume, :prenume, :cnp, :functie)
                        '''
                cursor = connection.cursor()
                cursor.execute(insert_query, values)
                connection.commit()
                cursor.close()
            elif request.form.get('delete_flag'):
                delete_id = request.form.get('delete_flag')
                cursor = connection.cursor()
                cursor.execute('DELETE FROM angajati WHERE id=:delete_id', {'delete_id': delete_id})
                connection.commit()
                cursor.close()
            else:
                id = int(request.form.get('id'))
                username = request.form.get('username')
                password = request.form.get('password')
                nume = request.form.get('nume')
                prenume = request.form.get('prenume')
                cnp = int(request.form.get('cnp'))
                functie = request.form.get('functie')
                values = {
                    'id': id,
                    'username': username,
                    'password': password,
                    'nume': nume,
                    'prenume': prenume,
                    'cnp': cnp,
                    'functie': functie
                }
                update_query = '''
                    UPDATE angajati
                    SET username=:username, password=:password, nume=:nume, prenume=:prenume, cnp=:cnp, functie=:functie
                    WHERE id=:id
                '''
                cursor = connection.cursor()
                cursor.execute(update_query, values)
                # modificat commiut and close sa fiedupa if
                connection.commit()
                cursor.close()

        # selectam informatiile din baza de date cu angajatii
        # si le transmitem catre  pagina
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM angajati')
        angajati = []
        for item in cursor:
            angajati.append([x for x in item])
        cursor.close()
        return render_template('admin.html', angajati=angajati)

    @app.route('/adminAdd', methods=['GET'])
    def adminAdd():
        return render_template('adminAdd.html')

    @app.route('/adminEdit', methods=['POST'])
    def adminEdit():
        item_id = int(request.form['id'])
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM angajati WHERE id = :item_id', {'item_id': item_id})
        angajat = cursor.fetchall()
        cursor.close()
        print(angajat)
        return render_template('adminEdit.html', angajat=angajat[0])
