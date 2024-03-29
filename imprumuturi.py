import re

from flask import render_template, session, request, redirect, url_for

from autentification import requires_authentication2

book_list = []
pers = []


def imprumuturi_func(app, connection):
    """Contine functionalitatile tabelului de imprumuturi"""

    @app.route('/imprumuturi', methods=['GET', 'POST'])
    @requires_authentication2
    def imprumuturi():
        if request.method == 'POST':
            global book_list, pers
            print("book_list, pers in imprumuturi")
            print(book_list, pers)
            book_list = []
            pers = []
            persoana = request.form.get('persoana')
            books = request.form.get('books')
            nr_days = request.form.get('nr_days')
            # print(persoana, type(persoana), len(persoana), books, type(books), len(books), nr_days, type(nr_days),
            #       len(nr_days))
            # (1, 'Andrei', 'zacord', 733) <class 'str'>['3', '1'] < class 'str' > 2 < class 'str' >
            if persoana and (len(books) - 2) and nr_days:
                string_list = books.strip("[]").split(", ")
                books = [int(item.strip("'")) for item in string_list]
                persoana = [int(item.strip("'")) if item.isdigit() else item.strip("'") for item in
                            persoana.strip("()").split(", ")]
                nr_days = int(nr_days)
                cursor = connection.cursor()
                for b in books:
                    insert_query = f'''
                                    INSERT INTO imprumuturi
                                    VALUES ({b}, {persoana[0]}, CURRENT_DATE ,
                                        CURRENT_DATE + INTERVAL '{nr_days}' DAY, {persoana[3]})
                                    '''
                    cursor.execute(insert_query)
                connection.commit()
                cursor.close()
            else:
                print('smth baaad ah')

            imprumut = request.form.get('delete_flag')
            if imprumut:
                numbers = [int(match.group()) for match in re.finditer(r'\b\d+\b', imprumut)][:2]
                cursor = connection.cursor()
                cursor.execute(f'''DELETE FROM imprumuturi WHERE id_carte={numbers[0]}
                               AND id_persoana={numbers[1]}''')
                connection.commit()
                cursor.close()

            intarz = request.form.get('delete_flag_int')
            print(intarz)
            if intarz:
                print(intarz, type(intarz))
                numbers = [int(match.group()) for match in re.finditer(r'\b\d+\b', intarz)][:2]
                cursor = connection.cursor()
                cursor.execute(f'''DELETE FROM intarzieri WHERE id_carte={numbers[0]}
                                           AND id_persoana={numbers[1]}''')
                connection.commit()
                cursor.close()

            cursor = connection.cursor()
            # inseram cartile cu intarziere in tabela intarzieri
            cursor.execute('INSERT INTO intarzieri SELECT id_carte, id_persoana, data_returnare FROM imprumuturi '
                           'WHERE data_returnare < SYSDATE')
            # inseram fiecare intarziere (cu un for)

            # delete imp care au intarziere DATE_RETUR < SYSDATE
            cursor.execute('DELETE FROM imprumuturi WHERE data_returnare < SYSDATE')
            connection.commit()
            cursor.execute('SELECT * FROM intarzieri')
            intarzieri = cursor.fetchall()
            cursor.execute('SELECT * FROM imprumuturi')
            imprumuturi = cursor.fetchall()
            cursor.close()
            return redirect(url_for('imprumuturi', imprumuturi=imprumuturi, intarzieri=intarzieri, admin_flag=session['admin_flag']))

        cursor = connection.cursor()
        # inseram cartile cu intarziere in tabela intarzieri
        cursor.execute('INSERT INTO intarzieri SELECT id_carte, id_persoana, data_returnare FROM imprumuturi WHERE '
                       'data_returnare < SYSDATE')
        # inseram fiecare intarziere (cu un for)

        # delete imp care au intarziere DATE_RETUR < SYSDATE
        cursor.execute('DELETE FROM imprumuturi WHERE data_returnare < SYSDATE')
        connection.commit()
        cursor.execute('SELECT * FROM intarzieri')
        intarzieri = cursor.fetchall()
        cursor.execute('SELECT * FROM imprumuturi')
        imprumuturi = cursor.fetchall()
        cursor.close()
        return render_template('imprumuturi.html', imprumuturi=imprumuturi, intarzieri=intarzieri, admin_flag=session['admin_flag'])

    @app.route('/submitform', methods=['GET', 'POST'])
    @requires_authentication2
    def submitform():
        if request.method == 'POST':
            print('/submitform, POST')
        else:
            print('/submitform, GET')
        imp_flag = True
        # exttragem persoana
        global pers
        print('pers: ', pers)
        pers_id = request.form.get('id')
        print('id: ', pers_id)
        if pers_id:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM persoane WHERE id = :item_id', {'item_id': pers_id})
            # global pers
            pers = cursor.fetchall()
            print('pers: ', pers)
            cursor.close()
        # extragem cartile
        global book_list
        book_list.append(request.form.get('carte'))
        book_list = list(filter(lambda x: x is not None, book_list))
        book_list = list(dict.fromkeys(book_list))
        print('book_list: ', book_list)
        return render_template('submitform.html', persoana=pers, book_list=book_list, imp_flag=imp_flag)
