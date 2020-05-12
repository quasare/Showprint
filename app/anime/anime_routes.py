from flask import Blueprint, render_template, jsonify


anime = Blueprint('anime', __name__, template_folder='templates',
                     static_folder='static')

@anime.route('/')
def show_home():
    return render_template('anime_home.html')