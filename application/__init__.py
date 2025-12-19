from flask import Flask
from .extensions import ma, cache, limiter
from .models import db
from .blueprints.mechanics import mechanics_bp
from .blueprints.customers import customers_bp
from .blueprints.ServiceTicket import service_ticket_bp
from .blueprints.Inventory import inventory_bp


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')



    #initialize extentions
    ma.init_app(app)
    db.init_app(app) #adding our db extension to our app
    cache.init_app(app)
    limiter.init_app(app)

    
    #register blueprints
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(service_ticket_bp, url_prefix='/service_tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    return app
