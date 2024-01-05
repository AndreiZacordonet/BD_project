from flask import render_template, request
from autentification import requires_authentication, requires_admin_role, requires_authentication2
import cx_Oracle as oracledb

from validator_cnp import Validare_CNP


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
                cnp = request.form.get('cnp')
                functie = request.form.get('functie')

                if not nume.replace(' ', '').replace('-', '').isalpha():
                    return render_template('adminAdd.html', error=1)
                if not prenume.replace(' ', '').replace('-', '').isalpha():
                    return render_template('adminAdd.html', error=2)
                if not Validare_CNP(cnp):
                    return render_template('adminAdd.html', error=3)

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
                try:
                    cursor.execute(insert_query, values)
                except oracledb.Error:
                    return render_template('adminAdd.html', error=4)
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
                cnp = request.form.get('cnp')
                functie = request.form.get('functie')
                angajat = [id, username, password, nume, prenume, cnp, functie]

                if not nume.replace(' ', '').replace('-', '').isalpha():
                    return render_template('adminEdit.html', angajat=angajat, error=1)
                if not prenume.replace(' ', '').replace('-', '').isalpha():
                    return render_template('adminEdit.html', angajat=angajat, error=2)
                if not Validare_CNP(cnp):
                    return render_template('adminEdit.html', angajat=angajat, error=3)

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
                try:
                    cursor.execute(update_query, values)
                except oracledb.Error:
                    return render_template('adminEdit.html', angajat=angajat, error=4)
                # modificat commiut and close sa fiedupa if
                connection.commit()
                cursor.close()

            # cursor = connection.cursor()
            # cursor.execute('SELECT * FROM angajati')
            # angajati = []
            # for item in cursor:
            #     angajati.append([x for x in item])
            # cursor.close()
            # return redirect('admin.html', angajati=angajati)

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
    @requires_admin_role
    @requires_authentication2
    def adminAdd():
        return render_template('adminAdd.html')

    @app.route('/adminEdit', methods=['POST'])
    @requires_admin_role
    @requires_authentication2
    def adminEdit():
        item_id = int(request.form['id'])
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM angajati WHERE id = :item_id', {'item_id': item_id})
        angajat = cursor.fetchall()
        cursor.close()
        return render_template('adminEdit.html', angajat=angajat[0])
