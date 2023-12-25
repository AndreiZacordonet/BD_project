from flask import render_template


def carti_func(app):
    """Contine functionalitatile tabelului de carti"""
    @app.route('/carti')
    def carti():
        return render_template('carti.html')
