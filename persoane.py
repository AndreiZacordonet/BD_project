import cx_Oracle
from flask import render_template, request, session, redirect, url_for

from autentification import requires_authentication2
from validator_cnp import Validare_CNP


def persoane_func(app, connection):
    @app.route('/persoane', methods=['GET', 'POST'])
    @requires_authentication2
    def persoane():
        if request.method == 'POST':
            if request.form.get('insert_flag'):
                nume = request.form.get('nume')
                prenume = request.form.get('prenume')
                cnp = request.form.get('cnp')

                if not nume.replace(' ', '').replace('-', '').isalpha():
                    return render_template('persoaneAdd.html', error=1)
                if not prenume.replace(' ', '').replace('-', '').isalpha():
                    return render_template('persoaneAdd.html', error=2)
                if not Validare_CNP(cnp):
                    return render_template('persoaneAdd.html', error=3)

                values = {
                    'nume': nume,
                    'prenume': prenume,
                    'cnp': cnp,
                }
                insert_query = '''
                            INSERT INTO persoane (nume, prenume, cnp)
                            VALUES (:nume, :prenume, :cnp)
                        '''
                cursor = connection.cursor()
                try:
                    cursor.execute(insert_query, values)
                except cx_Oracle.Error:
                    return render_template('persoaneAdd.html', error=4)
                connection.commit()
                cursor.close()
            elif request.form.get('delete_flag'):
                delete_id = request.form.get('delete_flag')
                cursor = connection.cursor()
                cursor.execute('DELETE FROM persoane WHERE id=:delete_id', {'delete_id': delete_id})
                connection.commit()
                cursor.close()
            elif request.form.get('imp_flag'):
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM persoane')
                pers = cursor.fetchall()
                cursor.close()
                # return redirect(url_for('persoane', persoane=pers, imp_flag=True, admin_flag=session['admin_flag']))
                return render_template('persoane.html', persoane=pers, imp_flag=True)
            else:
                id = int(request.form.get('id'))
                nume = request.form.get('nume')
                prenume = request.form.get('prenume')
                cnp = request.form.get('cnp')
                persoana = [id, nume, prenume, cnp]

                if not nume.replace(' ', '').replace('-', '').isalpha():
                    return render_template('persoaneEdit.html', persoana=persoana, error=1)
                if not prenume.replace(' ', '').replace('-', '').isalpha():
                    return render_template('persoaneEdit.html', persoana=persoana, error=2)
                if not Validare_CNP(cnp):
                    return render_template('persoaneEdit.html', persoana=persoana, error=3)

                values = {
                    'id': id,
                    'nume': nume,
                    'prenume': prenume,
                    'cnp': cnp
                }
                update_query = '''
                                    UPDATE persoane
                                    SET nume=:nume, prenume=:prenume, cnp=:cnp
                                    WHERE id=:id
                                '''
                cursor = connection.cursor()
                try:
                    cursor.execute(update_query, values)
                except cx_Oracle.Error:
                    return render_template('persoaneEdit.html', persoana=persoana, error=4)
                # modificat commiut and close sa fiedupa if
                connection.commit()
                cursor.close()

            cursor = connection.cursor()
            cursor.execute('SELECT * FROM persoane')
            pers = cursor.fetchall()
            cursor.close()
            return redirect(url_for('persoane', persoane=pers, admin_flag=session['admin_flag']))

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM persoane')
        pers = cursor.fetchall()
        cursor.close()
        return render_template('persoane.html', persoane=pers, admin_flag=session['admin_flag'])

    @app.route('/persoaneEdit', methods=['POST'])
    @requires_authentication2
    def persoaneEdit():
        item_id = int(request.form['id'])
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM persoane WHERE id = :item_id', {'item_id': item_id})
        pers = cursor.fetchall()
        cursor.close()
        return render_template('persoaneEdit.html', persoana=pers[0])

    @app.route('/persoaneAdd', methods=['GET'])
    @requires_authentication2
    def persoaneAdd():
        return render_template('persoaneAdd.html')
