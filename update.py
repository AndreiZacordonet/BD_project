import cx_Oracle as oracledb


def insertCarte(connection):
    cursor = connection.cursor()
    try:
        titlu = 'Mustar'
        autor = 'Gica Cosbuci'
        insert_query = f'''
                        INSERT INTO carti (
                        titlu, autor
                        ) 
                        VALUES ('{titlu}', '{autor}')
                        );
                       '''
        cursor.execute(insert_query)
    except oracledb.Error:
        pass
    connection.commit()
    cursor.close()


def deleteCarte(connection):
    cursor = connection.cursor()
    try:
        id = 3
        delete_query = f'''
                        DELETE FROM carti
                        WHERE id = {id};
                       '''
        cursor.execute(delete_query)
    except oracledb.Error:
        pass
    connection.commit()
    cursor.close()


def insertPersoana(connection):
    cursor = connection.cursor()
    try:
        nume = 'Preput'
        prenume = 'Cioaca'
        cnp = 1223456789012
        insert_query = f'''
                            INSERT INTO persoane (
                            nume, prenume, cnp
                            ) 
                            VALUES ('{nume}', '{prenume}', {cnp})
                            );
                           '''
        cursor.execute(insert_query)
    except oracledb.Error:
        pass
    connection.commit()
    cursor.close()


def deletePersoana(connection):
    cursor = connection.cursor()
    try:
        id = 3
        delete_query = f'''
                        DELETE FROM persoane
                        WHERE id = {id};
                       '''
        cursor.execute(delete_query)
    except oracledb.Error:
        pass
    connection.commit()
    cursor.close()


def insertImprumut(connection):
    cursor = connection.cursor()
    try:
        id_carte = 1
        id_persoana = 1
        insert_query = f'''
                        INSERT INTO imprumuturi (
                        id_carte, id_persoana, data_imprumutare, data_returnare, cnp
                        ) 
                        VALUES ({id_carte}, {id_persoana}, CURRENT_DATE, CURRENT_DATE + INTERVAL '14' DAY, 
                        (select p.cnp from persoane p
                        where p.id = {id_persoana})
                        );
                       '''
        cursor.execute(insert_query)
    except oracledb.Error:
        pass
    connection.commit()
    cursor.close()
