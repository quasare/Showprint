from flask import Blueprint, render_template, jsonify


shows = Blueprint('shows', __name__, template_folder='templates',
                     static_folder='static')

@shows.route('/')
def show_home():
    return render_te