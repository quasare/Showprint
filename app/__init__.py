import os
from flask import Flask, render_template, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from .models import db, connect_db
from .shows.show_routes import shows
from .users.users_routes import user
from .auth.auth_routes import auth
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Initialize App Function

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(f'config.{env}')
    
    toolbar = DebugToolbarExtension(app)
    connect_db(app)
    with app.app_context():

        # Import blueprint module
        from .shows.show_routes import shows
        from .users.users_routes import user
        from .auth.auth_routes import auth
        db.create_all()


        # Register blueprint modules
        app.register_blueprint(shows, url_prefix='/shows')
        app.register_blueprint(user, url_prefix='/user')
        app.register_blueprint(auth)

        # Landing page
        @app.route('/')
        def landing():
            if 'username' in session:
                return redirect(url_for('user.user_dashboard'))
            return render_template('landing.html')

        return app

