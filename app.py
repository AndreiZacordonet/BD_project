from flask import Flask
from routes import configure_routes

from createTables import createTables
import cx_Oracle as oracledb


app = Flask(__name__)

connection = oracledb.connect('bd026', 'bd026', 'bd-dc.cs.tuiasi.ro:1539/orcl')
createTables(connection)

configure_routes(app, connection)

if __name__ == '__main__':
    app.run(debug=True)
    connection.close()
