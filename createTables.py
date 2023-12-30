import cx_Oracle as oracledb


def createTables(connection):
    cursor = connection.cursor()
    # if connection is to the oracle server
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

    try:
        create_query = '''CREATE TABLE carti (
                    id NUMBER(3) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    titlu VARCHAR(50) NOT NULL,
                    autor VARCHAR(30) NOT NULL
                );'''
        cursor.execute(create_query)
    except oracledb.Error:
        pass

    try:
        create_query = '''CREATE TABLE persoane (
                    id NUMBER(3) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nume VARCHAR(30) NOT NULL,
                    prenume VARCHAR(30) NOT NULL,
                    cnp NUMBER(13) UNIQUE NOT NULL
                );'''
        cursor.execute(create_query)
    except oracledb.Error:
        pass

    try:
        create_query = '''CREATE TABLE imprumuturi (
                    id_carte NUMBER(3),
                    id_persoana NUMBER(3),
                    data_imprumutare DATE,
                    data_returnare DATE,
                    cnp NUMBER(13) NOT NULL,
                    
                    CONSTRAINT id_carte_fk FOREIGN KEY (id_carte) REFERENCES carti(id),
                    CONSTRAINT id_persoana_fk FOREIGN KEY (id_persoana) REFERENCES persoane(id)
                );'''
        cursor.execute(create_query)
    except oracledb.Error:
        pass

    # else local db

    add_admin_query = '''MERGE INTO angajati a
                        USING (SELECT 'admin' as username FROM dual) b
                        ON (a.username = b.username)
                        WHEN NOT MATCHED THEN
                        INSERT (username, password, nume, prenume, cnp, functie)
                        VALUES ('admin', 'adminpass', 'nume', 'prenume', '1234567890123', 'administrator')'''
    cursor.execute(add_admin_query)
    connection.commit()
    cursor.close()
