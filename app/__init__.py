from flask import Flask
from flask_migrate import  Migrate # ORM
from flask_sqlalchemy import SQLAlchemy # ORM
from sqlalchemy import MetaData

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# ORM
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # 블루프린트 : URL
    from .views import main_views, site_views, point_views, data_views, paper_views, analysis_views, user_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(site_views.bp)
    app.register_blueprint(point_views.bp)
    app.register_blueprint(data_views.bp)
    app.register_blueprint(paper_views.bp)
    app.register_blueprint(analysis_views.bp)
    app.register_blueprint(user_views.bp)


    # 필터
    from .filter import format_datetime, format_gdatetime, number_format_simple
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['gdatetime'] = format_gdatetime
    app.jinja_env.filters['number_format'] = number_format_simple
    app.jinja_env.filters['zip'] = zip

    return app