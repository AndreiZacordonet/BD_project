from flask import render_template, session, request

from autentification import requires_authentication2


def carti_func(app, connection):
    """Contine functionalitatile tabelului de carti"""

    @app.route('/carti', methods=['GET', 'POST'])
    @requires_authentication2
    def carti():
        if request.method == 'POST':
            if request.form.get('insert_flag'):
                titlu = request.form.get('titlu')
                autor = request.form.get('autor')
                values = {
                    'titlu': titlu,
                    'autor': autor,
                }
                insert_query = '''
                            INSERT INTO carti (titlu, autor)
                            VALUES (:titlu, :autor)
                        '''
                cursor = connection.cursor()
                cursor.execute(insert_query, values)
                connection.commit()
                cursor.close()
            elif request.form.get('delete_flag'):
                delete_id = request.form.get('delete_flag')
                cursor = connection.cursor()
                cursor.execute('DELETE FROM carti WHERE id=:delete_id', {'delete_id': delete_id})
                connection.commit()
                cursor.close()
            elif request.form.get('imp_flag'):
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM carti')
                carti = cursor.fetchall()
                cursor.execute('SELECT id_carte FROM IMPRUMUTURI WHERE data_returnare > SYSDATE ')
                carti_imp = cursor.fetchall()
                carti_imp = [item[0] for item in carti_imp]
                carti2 = carti.copy()
                for carte in carti:
                    if carte[0] in carti_imp:
                        carti2.remove(carte)
                cursor.close()
                return render_template('carti.html', carti=carti2, imp_flag=True)
            else:
                id = int(request.form.get('id'))
                titlu = request.form.get('titlu')
                autor = request.form.get('autor')
                values = {
                    'id': id,
                    'titlu': titlu,
                    'autor': autor,
                }
                update_query = '''
                                    UPDATE carti
                                    SET titlu=:titlu, autor=:autor
                                    WHERE id=:id
                                '''
                cursor = connection.cursor()
                cursor.execute(update_query, values)
                # modificat commiut and close sa fiedupa if
                connection.commit()
                cursor.close()

        cursor = connection.cursor()
        cursor.execute('SELECT * FROM carti')
        carti = []
        for item in cursor:
            carti.append([x for x in item])
        cursor.close()
        return render_template('carti.html', carti=carti, admin_flag=session['admin_flag'])

    @app.route('/cartiEdit', methods=['POST'])
    @requires_authentication2
    def cartiEdit():
        item_id = int(request.form['id'])
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM carti WHERE id = :item_id', {'item_id': item_id})
        carte = cursor.fetchall()
        cursor.close()
        return render_template('cartiEdit.html', carte=carte[0])

    @app.route('/cartiAdd', methods=['GET'])
    @requires_authentication2
    def cartiAdd():
        return render_template('cartiAdd.html')
