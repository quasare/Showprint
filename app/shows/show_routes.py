from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from .forms import SearchForm
from show_request import shows_search

shows = Blueprint('shows', __name__, template_folder='templates',
                     static_folder='static')

@shows.route('/', methods=['POST', 'GET'])
def show_home():
    form = SearchForm()
    if form.validate_on_submit():
        show = form.search.data
        res = shows_search(show)
        return render_template('search_results.html', res=res)
    return render_template('show_home.html', form=form)

@shows.route('/results/<res>')
def search_results():
    show_list = res
    return     