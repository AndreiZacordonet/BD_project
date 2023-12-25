import cx_Oracle as oracledb
def createTables(connection):
    cursor = connection.cursor()

    try:
        create_query = '''CREATE TABLE angajati (
                        id NUMBER(3) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        nume VARCHAR(255) NOT NULL,
                        prenume VARCHAR(255) NOT NULL,
                        cnp NUMBER(13) UNIQUE NOT NULL,
                        functie VARCHAR(25) NOT NULL
                    );'''
        cursor.execute(create_query)
    except oracledb.Error:
        pass

    add_admin_query = '''MERGE INTO angajati a
                        USING (SELECT 'admin' as username FROM dual) b
                        ON (a.username = b.username)
                        WHEN NOT MATCHED THEN
                        INSERT (username, password, nume, prenume, cnp, functie)
                        VALUES ('admin', 'adminpass', 'nume', 'prenume', '1234567890123', 'administrator')'''
    cursor.execute(add_admin_query)
    connection.commit()
    cursor.close()
