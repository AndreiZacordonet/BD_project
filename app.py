from flask import Flask
from routes import configure_routes
from login import admin_flag

from createTables import createTables
import cx_Oracle as oracledb


app = Flask(__name__)
app.secret_key = 'alodabunaziua'

connection = oracledb.connect('bd026', 'bd026', 'bd-dc.cs.tuiasi.ro:1539/orcl')

createTables(connection)

print(admin_flag)
configure_routes(app, connection)

if __name__ == '__main__':
    app.run(debug=True)
    connection.close()
