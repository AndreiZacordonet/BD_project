from flask import render_template, request, session, redirect, url_for

from autentification import requires_authentication2


def persoane_func(app, connection):
    @app.route('/persoane', methods=['GET', 'POST'])
    @requires_authentication2
    def persoane():
        if request.method == 'POST':
            if request.form.get('insert_flag'):
                nume = request.form.get('nume')
                prenume = request.form.get('prenume')
                cnp = int(request.form.get('cnp'))
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
                cursor.execute(insert_query, values)
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
                cnp = int(request.form.get('cnp'))
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
                cursor.execute(update_query, values)
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
