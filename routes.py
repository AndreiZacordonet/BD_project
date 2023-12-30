from login import login_func
from admin import admin_func
from persoane import persoane_func
from carti import carti_func
from imprumuturi import imprumuturi_func


def configure_routes(app, connection):
    """Contine toate rutele aplicatiei"""
    # pagina de login
    login_func(app, connection)

    # pagina de admin
    admin_func(app, connection)

    # pagina de persoane inregistrate
    persoane_func(app, connection)

    # pagina de manageriere a cartilor
    carti_func(app, connection)

    # pagina de imprumuturi
    imprumuturi_func(app, connection)
