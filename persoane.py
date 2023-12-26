from flask import render_template, request

def persoane_func(app, connection):
     @app.route('/persoane')
     def persoane():
        return render_template('persoane.html')
