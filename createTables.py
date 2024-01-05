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
                    functie VARCHAR(25) NOT NULL,

                    CONSTRAINT CheckCNPLength CHECK (LENGTH(TO_CHAR(CNP)) = 13)
                );'''
        cursor.execute(create_query)
    except oracledb.Error:
        print('Tabelul angajati exista deja!')
        pass

    try:
        create_query = '''CREATE TABLE carti (
                    id NUMBER(3) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    titlu VARCHAR(50) NOT NULL,
                    autor VARCHAR(30) NOT NULL
                );'''
        cursor.execute(create_query)
    except oracledb.Error:
        print('Tabelul carti exista deja!')
        pass

    try:
        create_query = '''CREATE TABLE persoane (
                            id NUMBER(3) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                            nume VARCHAR(30) NOT NULL,
                            prenume VARCHAR(30) NOT NULL,
                            cnp NUMBER(13) UNIQUE NOT NULL,
                        
                            CONSTRAINT CheckCNPLength CHECK (LENGTH(TO_CHAR(CNP)) = 13)
                        );'''
        cursor.execute(create_query)
    except oracledb.Error:
        print('Tabelul persoane exista deja!')
        pass

    try:
        create_query = '''CREATE TABLE imprumuturi (
                    id_carte NUMBER(3),
                    id_persoana NUMBER(3),
                    data_imprumutare DATE,
                    data_returnare DATE,
                    cnp NUMBER(13) NOT NULL,

                    CONSTRAINT id_carte_fk FOREIGN KEY (id_carte) REFERENCES carti(id),
                    CONSTRAINT id_persoana_fk FOREIGN KEY (id_persoana) REFERENCES persoane(id),
                    PRIMARY KEY (id_carte, id_persoana)
                    );'''
        cursor.execute(create_query)
    except oracledb.Error:
        print('Tabelul imprumuturi exista deja!')
        pass


    try:
        create_query = '''
                        CREATE TABLE intarzieri (
                            id_carte NUMBER(3),
                            id_persoana NUMBER(3),
                            data_returnare DATE,
                        
                            CONSTRAINT id_carte_int FOREIGN KEY (id_carte) REFERENCES carti(id),
                            CONSTRAINT id_persoana_int FOREIGN KEY (id_persoana) REFERENCES persoane(id),
                            PRIMARY KEY (id_carte, id_persoana)
                        ); '''
        cursor.execute(create_query)
    except oracledb.Error:
        print('Tabelul intarzieri exista deja!')
        pass

    # else local db

    add_admin_query = '''MERGE INTO angajati a
                        USING (SELECT 'admin' as username FROM dual) b
                        ON (a.username = b.username)
                        WHEN NOT MATCHED THEN
                        INSERT (username, password, nume, prenume, cnp, functie)
                        VALUES ('admin', 'adminpass', 'nume', 'prenume', '1234567890123', 'administrator')'''
    cursor.execute(add_admin_query)

    insert_query = '''INSERT INTO angajati (username, password, nume, prenume, cnp, functie)
    VALUES ('pinguinus', 'parolafoarteputernica', 'Zacornea', 'Mitică', '1920906227781', 'Bibliotecar Șef');

INSERT INTO angAjati (username, password, nume, prenume, cnp, functie)
    VALUES ('bunica', 'bunica1', 'Barba', 'Florentina', '2920906108129', 'Bibliotecar');

INSERT INTO angAjati (username, password, nume, prenume, cnp, functie)
    VALUES ('Ian', 'GeogIAN123', 'Manole', 'Cosmin', '5021003228150', 'Asistent de Bibliotecă');

INSERT INTO angAjati (username, password, nume, prenume, cnp, functie)
    VALUES ('PC', 'programareacalculatoare', 'Șerban', 'Elena', '8310228359721', 'Consilier pentru Lectură');

INSERT INTO carti (titlu, autor)
    VALUES ('To Kill a Mockingbird', 'Harper Lee');

INSERT INTO carti (titlu, autor)
    VALUES ('1984', 'Francis Scott Fitzgerald');

INSERT INTO carti (titlu, autor)
    VALUES ('The Lord of the Rings', 'John Ronald Reuel Tolkien');

INSERT INTO carti (titlu, autor)
    VALUES ('The Hobbit', 'John Ronald Reuel Tolkien');

INSERT INTO carti (titlu, autor)
    VALUES ('The Silmarillion', 'John Ronald Reuel Tolkien');

INSERT INTO carti (titlu, autor)
    VALUES ('Pride and Prejudice', 'Jane Austen');

INSERT INTO carti (titlu, autor)
    VALUES ('Ion', 'Liviu Rebreanu');

INSERT INTO persoane (nume, prenume, cnp)
    VALUES ('Ghita', 'George', '7990927228910');

INSERT INTO persoane (nume, prenume, cnp)
    VALUES ('Munteanu', 'Maria Genoveva ', '6030228376335');

INSERT INTO persoane (nume, prenume, cnp)
    VALUES ('Tudormeai', 'Alina', '6220228178940');

INSERT INTO persoane (nume, prenume, cnp)
    VALUES ('Munteanu', 'Radu-Ștefan', '7600228175436');

INSERT INTO persoane (nume, prenume, cnp)
    VALUES ('Ciobanu', 'Ana-Maria', '6020927229326');'''

    for insert in insert_query.split('\n\n\n'):
        try:
            cursor.execute(insert)
        except oracledb.Error:
            print('Linie deja inserate')

    connection.commit()
    cursor.close()
